using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using System.IO;
using System;

using System.Net.Http;
using System.Threading.Tasks;
using System.Net.Http.Headers;
using System.Threading;
using UnityEngine.Networking;



public class Cliente : MonoBehaviour
{
    public AudioSource audioSource;
    private bool isRecording = false;                                                   
    private string filePath = "AudioRecorded.wav";                    
    static private HttpClient httpClient = new HttpClient();                        //Mantiene el estado entre llamadas                   
    static public string SERVER_URL = "http://192.168.0.16:5000";
    private ServerRequests sr = new ServerRequestsController(SERVER_URL, httpClient);
    public Animator dashiAnimator;



    void Start()
    {   
        //Registra al usuario en el servidor

        audioSource = GetComponent<AudioSource>();
        StartCoroutine(RegisterUserCoroutine());
        UnityEngine.Debug.Log("AudioSource component initialized.");
        
    }


    void Update()
    {   
        // Maneja las pulsaciones de teclado y el estado de la grabacion 
        if (Input.GetKeyDown(KeyCode.Space))
        {
            if (!isRecording)
            {
                isRecording = true;
                StartRecording(audioSource);
            }
            else
            {
                isRecording=false;
                dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Strafe");
                StopRecordingAndSave(audioSource);
                StartCoroutine(UploadWavCoroutine(filePath));

            }
        }
    }

    void OnApplicationQuit()
    {
        StartCoroutine(LogoutCoroutine());
        UnityEngine.Debug.Log("Game is closing, leaving.");
    }

    public void StartRecording(AudioSource audioSource)
    {
        //Comprueba que haya un microfono
        //Inicia la grabacion de un audio de 40 segundos 
        if (Microphone.devices.Length <= 0)
        {
            UnityEngine.Debug.LogWarning("No microphone devices found!");
            return;
        }

        audioSource.clip = Microphone.Start(null, true, 40, 44100);
        audioSource.loop = false;
        UnityEngine.Debug.Log("Recording started. Press Space to stop.");
    }

    void StopRecordingAndSave(AudioSource audioSource)
    {
        //Para la grabacion y llama a la funcion que se encarga de guardarla
        if (!Microphone.IsRecording(null))
        {
            UnityEngine.Debug.Log("Recording was not active.");
            return;
        }

        if (audioSource.clip.length > 0)
        {
            Microphone.End(null);
            UnityEngine.Debug.Log("Recording stopped.");
            SaveWavFile(audioSource);
            UnityEngine.Debug.Log("Audio data captured and file save initiated.");
        }
        else
        {
            UnityEngine.Debug.Log("No audio data was captured.");
        }
    }


    void SaveWavFile(AudioSource audioSource)
    {
        //Guarda la grabacion en un audio de 40 segundos
        if (audioSource.clip == null) return;

        var samples = new float[audioSource.clip.samples * audioSource.clip.channels];
        audioSource.clip.GetData(samples, 0);
        byte[] wavFile = WavUtility.FromAudioClip(audioSource.clip, samples);

        if (wavFile.Length > 0)
        {
            File.WriteAllBytes(filePath, wavFile);
            UnityEngine.Debug.Log($"Audio file saved successfully at {filePath}");
        }
        else
        {
            UnityEngine.Debug.Log("Failed to convert audio data to WAV format.");
        }
    }



    private IEnumerator RegisterUserCoroutine()
    {
        // Registra usuario en el servidor
        Task<string> registerTask = sr.RegisterUser();
        
        // Comprueba si la tarea a terminado
        while (!registerTask.IsCompleted)
        {
            yield return null; 
        }
        try
        {
            string data = registerTask.Result; // Obtener el resultado de la tarea
            UnityEngine.Debug.Log(data);
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Failed to register user: " + ex.Message);
        }
    }

    //Se encarga de esperar el audio de vuelta del servidor e iniciar el proceso de reproduccion cuando contesta
    IEnumerator UploadWavCoroutine(string filename)
    {
        //Sube audio al servidor 
        Task<AudioReturn> task = Task.Run(() => sr.UploadWav(filename));
        while (!task.IsCompleted)
        {
            yield return null;
        }

        if (task.IsFaulted)
        {
            UnityEngine.Debug.LogError("Error uploading file: " + task.Exception.ToString());
        }
        else
        {
            //Guarda lo que devuelve el servidor en una clase creada para ello
            AudioReturn audioReturn = task.Result;
            string path = Directory.GetCurrentDirectory(); 
            string filepath = Path.Combine(path, "Assets", "Resources", "outputClient.wav");
            StartCoroutine(LoadAndPlay(filepath));
            UnityEngine.Debug.Log("Upload successful!");
        }
    }

    //Accede a la propia carpeta como si fuera un servidor 
    //No se puede usar resource.Load porque unity tarda unos segundos en detectar el audio en la carpeta resources 
    //Y toma el audio anterior ademas de aumentar el delay bastante tiempo
    IEnumerator LoadAndPlay(string filePath)
    {
        using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip("file://" + filePath, AudioType.WAV))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                audioSource.clip = clip;
                dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Talk");
                audioSource.Play();
                StartCoroutine(WaitForAudioToEnd());

            }
            
            else
            {
                UnityEngine.Debug.LogError(www.error);
            }
        }
    }

    //Espera al final de la reproduccion del audio y cambia el animator controler para dejar en espera
    //al profesor
    IEnumerator WaitForAudioToEnd()
    {
        while (audioSource.isPlaying)
        {
            yield return null; // Espera un frame
        }

        dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Idle");
    }

    //Se encarga de esperar la respuesta del servidor
    public IEnumerator LogoutCoroutine()
    {
        //Sube audio al servidor 
        Task<string> task = Task.Run(() => sr.Logout());
        while (!task.IsCompleted)
        {
            yield return null;
        }

        if (task.IsFaulted)
        {
            UnityEngine.Debug.LogError("Error uploading file: " + task.Exception.ToString());
        }
        else
        {
            //Guarda lo que devuelve el servidor en una clase creada para ello
            string str = task.Result;
            
            UnityEngine.Debug.Log("LogOut successful!");
        }
    }

}


public static class WavUtility
{

    public static byte[] FromAudioClip(AudioClip clip, float[] samples)
    {
        //This method FromAudioClip converts an array of float audio samples into a byte array. It scales the float samples to 16-bit integers and then converts them to bytes,
        var sampleCount = clip.samples * clip.channels;
        var frequency = clip.frequency;
        var byteDepth = 2;

        byte[] bytes = new byte[sampleCount * byteDepth];

        int rescaleFactor = 32767; // to convert float to Int16

        for (int i = 0; i < samples.Length; i++)
        {
            short value = (short)(samples[i] * rescaleFactor);
            byte[] byteArr = BitConverter.GetBytes(value);
            byteArr.CopyTo(bytes, i * byteDepth);
        }

        return ConvertAndWrite(bytes, sampleCount, clip.channels, frequency, byteDepth);
    }

    static byte[] ConvertAndWrite(byte[] dataSource, int sampleCount, int channels, int frequency, int byteDepth)
    {
        //Convierte el codigo a wav y lo escribe en la ruta especificada
        MemoryStream memoryStream = new MemoryStream();
        BinaryWriter writer = new BinaryWriter(memoryStream);

        WriteHeader(writer, sampleCount, channels, frequency, byteDepth);

        writer.Write(dataSource);

        return memoryStream.ToArray();
    }

    static void WriteHeader(BinaryWriter writer, int sampleCount, int channels, int frequency, int byteDepth)
    {
        writer.Write(new char[4] { 'R', 'I', 'F', 'F' });

        int chunkSize = 36 + (sampleCount * byteDepth * channels);
        writer.Write(chunkSize);

        writer.Write(new char[4] { 'W', 'A', 'V', 'E' });
        writer.Write(new char[4] { 'f', 'm', 't', ' ' });
        writer.Write(16);
        writer.Write((short)1);
        writer.Write((short)channels);
        writer.Write(frequency);
        writer.Write(frequency * channels * byteDepth);
        writer.Write((short)(channels * byteDepth));
        writer.Write((short)(8 * byteDepth));
        writer.Write(new char[4] { 'd', 'a', 't', 'a' });
        writer.Write(sampleCount * byteDepth * channels);
    }
}


public class ServerRequestsController
{
    //Esta clase se encarga directamente del trato con el servidor 
    private string serverUrl;
    private HttpClient session;

    // Constructor de la clase MyService
    public ServerRequests(string serverUrl, HttpClient session)
    {
        this.serverUrl = serverUrl;
        this.session = session ?? throw new ArgumentNullException(nameof(session), "HttpClient session cannot be null");
    }

    public async Task<string> RegisterUser()
    {
        //Intenta registrar el usuario en el servidor 3 veces, si no lo consigue lanza un error
        int counter = 0;
        while (counter < 3)
        {
            try
            {
                HttpResponseMessage response = await session.GetAsync(serverUrl);
                string responseBody = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine("Register Success:");
                    Console.WriteLine(responseBody);
                    return responseBody;
                }
                else
                {
                    HandleError(response);
                    counter++;
                }
            }
            catch (HttpRequestException)
            {
                Console.WriteLine("Unable to connect.");
                Console.WriteLine($"Retrying to establish connection: {counter}/2");
                counter++;
            }
        }

        throw new Exception("Cannot connect to server");
    }


    public async Task<AudioReturn> UploadWav(string filename)
    {
        //Crea la URL a la que va a hacer las peticiones y las variables necesarias 
        string url = $"{this.serverUrl}/upload_wav";
        string audioname = "outputClient";
        string audiopath = "Assets/Resources/outputClient.wav";
        AudioReturn audioReturn = new AudioReturn();    //Objeto de la clase que se va a devolver 
            
 
        using (var content = new MultipartFormDataContent())
        {
            //Lee el archivo de audio
            byte[] fileBytes = File.ReadAllBytes(filename);
            var fileContent = new ByteArrayContent(fileBytes);
            //A�ade el contenido al envio
            fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse("audio/wav");
            content.Add(fileContent, "wav_file", Path.GetFileName(filename));
            //Realiza la peticion
            HttpResponseMessage response = await this.session.PostAsync(url, content);

            if (response.IsSuccessStatusCode)
            {
                //Crea el Json
                string jsonResponse = await response.Content.ReadAsStringAsync();
                var json_data = JsonUtility.FromJson<ServerResponseAudio>(jsonResponse);
                //Decodifica y guarda el audio
                byte[] audio_data = Convert.FromBase64String(json_data.audio);
                File.WriteAllBytes(audiopath, audio_data);
                UnityEngine.Debug.Log($"File saved: {audioname}");
                //prepara los datos que va a devolver
                audioReturn.isEnd = json_data.flag;
                audioReturn.outName = audioname; 
                return audioReturn;
            }
            else
            {
                HandleError(response);
                return null;
            }
            }

    }

    public async Task<string> Logout()
    {
        string url = $"{this.serverUrl}/logout";

        // Logouts request
        HttpResponseMessage response = await session.GetAsync(url);

        // Check return code
        if (response.StatusCode != System.Net.HttpStatusCode.OK)
        {
            throw new Exception("Unable to logout");
        }
        return ("ok");
        
    }

    private void HandleError(HttpResponseMessage response)
    {
        switch (response.StatusCode)
        {
            case System.Net.HttpStatusCode.Unauthorized:
                UnityEngine.Debug.LogError("User should be registered");
                break;
            case System.Net.HttpStatusCode.NotFound:
                UnityEngine.Debug.LogError("No audio WAV received or selected");
                break;
            case System.Net.HttpStatusCode.InternalServerError:
                UnityEngine.Debug.LogError("Internal server error");
                break;
            default:
                UnityEngine.Debug.LogError($"Unhandled status code: {response.StatusCode}");
                break;
        }
    }
}

//Clases para almacenar datos
public class ServerResponseAudio
{
    public string audio;
    public bool flag;
}

public class AudioReturn
{
    public string outName;
    public bool isEnd;
}
