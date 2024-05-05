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

/*
???   ??? ????? ?????? ???    ???
???   ??? ????? ?????? ???    ???
???   ??? ????? ????   ??? ?? ???
???? ???? ????? ????   ??????????
 ???????  ????? ?????? ??????????
  ?????   ????? ??????  ???????? 
*/

public class ClientView : MonoBehaviour
{
    public AudioSource audioSource;
    public Animator dashiAnimator;

    private bool isRecording = false;
    private bool isReady = true; 
    private string filePath = "AudioRecorded.wav"; 
    

    private ServerRequestsController sr = new ServerRequestsController();
    
    private const int AUDIOSECS = 40; 
    private string coRouotineErrorHandler = null; 


    void Start()
    {
        // Registers the user on the server.
        try { 
            // Retrieves the AudioSource component attached to the GameObject.
            audioSource = GetComponent<AudioSource>();

            // Initiates the asynchronous coroutine to register the user.
            StartCoroutine(RegisterUserCoroutine());

            // Logs a message indicating successful initialization of the AudioSource component.
            UnityEngine.Debug.Log("AudioSource component initialized.");

            //Screen Management 
             Screen.fullScreen = false;
        Screen.fullScreenMode = FullScreenMode.Windowed;
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Starting:" + ex);
            Application.Quit(); 
        }
    }



    void Update()
    {
        // This function is called every frame and handles keyboard input for recording audio. 
        // When the space key is pressed, it toggles between starting and stopping audio recording. 
        // If recording is initiated, it sets the recording state to true and starts recording using the AudioSource component. 
        // If recording is already in progress and the space key is pressed again, it sets the recording state to false, 
        // changes the animator controller to Strafe motion, stops recording, saves the recorded audio, and initiates the coroutine 
        // to upload the audio file to a server.
        try
        {
            //An error occour in some coroutine
            if (coRouotineErrorHandler != null)
            {
                throw new Exception(coRouotineErrorHandler);

            }
            if (Input.GetKeyDown(KeyCode.Space))
            {
                if (!isRecording && isReady )
                {
                    isReady = false;
                    isRecording = true;
                    StartRecording(audioSource);
                    UnityEngine.Debug.Log("A");

                }
                else
                {
                    if (isRecording && !isReady) { 
                        isRecording = false;
                        dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Strafe");
                        StopRecordingAndSave();
                        StartCoroutine(UploadWavCoroutine(filePath));
                        UnityEngine.Debug.Log("B");
                    }
                    UnityEngine.Debug.Log("C");
                }
            }

        }
        catch (Exception ex) 
        {
            UnityEngine.Debug.LogError("RESTARTING CONECTION: An error have occured" + ex);
            RestartConnection();
        }
    }

    void RestartConnection() 
    {
        //Try to get a new session whit server
        try
        {
            //Stop all coroutinies before this 
            StartCoroutine(LogoutCoroutine());
            ServerRequestsController sr = new ServerRequestsController();
            StartCoroutine(RegisterUserCoroutine());
        }
        catch (Exception ex) 
        {
            UnityEngine.Debug.Log("Cannot restart conection : " + ex);
            Application.Quit();
        }
    }

    void OnApplicationQuit()
    {
        // This function is called when the application is about to quit.
        // It initiates an asynchronous coroutine to perform logout operations.
        // Additionally, it logs a message indicating that the game is closing.
        StartCoroutine(LogoutCoroutine());
        UnityEngine.Debug.Log("Game is closing, leaving.");
    }

    public void StartRecording(AudioSource audioSource)
    {
        // This method starts audio recording using the provided AudioSource component.
        // It first checks if a microphone device is available. If not, it logs a warning message and returns.
        // If a microphone is available, it starts recording an audio clip with a duration of AUDIOSECS  seconds at a sample rate of 44100 Hz.
        // The recording is set to not loop, and a message is logged to indicate that recording has started.
        if (Microphone.devices.Length <= 0)
        {
            UnityEngine.Debug.LogWarning("No microphone devices found!");
            return;
        }

        audioSource.clip = Microphone.Start(null, true, AUDIOSECS, 44100);
        audioSource.loop = false;
        UnityEngine.Debug.Log("Recording started. Press Space to stop.");
    }

    void StopRecordingAndSave()
    {
        // This method stops the audio recording and calls a function responsible for saving the recorded audio.
        // It first checks if recording is currently active using Microphone.IsRecording().
        // If recording is not active, it logs a message indicating that recording was not active and returns.
        // If recording is active and the recorded audio clip contains data, it stops the recording using Microphone.End().
        // If no audio data was captured (audio clip length is 0), it logs a error message indicating so.
        
        
        if (!Microphone.IsRecording(null))
        {
            UnityEngine.Debug.LogWarning("Recording was not active.");
        }

        else if (audioSource.clip.length > 0)
        {
            Microphone.End(null);
            SaveWavFile();
        }
        
    }


    void SaveWavFile()
    {
        // This method is responsible for saving the recorded audio clip as a WAV file.
        // It first checks if the audio clip is null. If it is, the method returns without performing any further actions.
        // It then retrieves the audio data from the audio clip using AudioClip.GetData() and stores it in an array of floats.
        // The audio data is then converted into a byte array representing a WAV file using the WavUtility.FromAudioClip() method.
        // If the resulting WAV file has a non-zero length, it is written to disk at the specified file path using File.WriteAllBytes().
        // A message is logged indicating the successful saving of the audio file.
        // If the conversion process fails or the resulting WAV file has zero length, a failure message is logged.

        if (audioSource.clip == null) 
        {
            UnityEngine.Debug.LogError("No audio data was captured.");
            throw new Exception("No audio data was captured.");

        }

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
            throw new Exception("Failed to convert audio data to WAV format.");

        }
    }

    // Coroutines in Unity are special methods defined with the IEnumerator return type.
    // They allow for asynchronous behavior by pausing and resuming execution over multiple frames.
    // When a coroutine is started using StartCoroutine(), Unity executes the coroutine method until it encounters a yield statement.
    // At that point, control returns to the caller, allowing other code to run.
    // When the condition specified by the yield statement is met (e.g., WaitForSeconds), Unity resumes executing the coroutine from where it left off.
    // This allows coroutines to perform tasks over time, such as animations, timers, or network operations, without blocking the main thread.
  
    private IEnumerator RegisterUserCoroutine()
    {
        
            Task<string> registerTask = sr.RegisterUser();
            while (!registerTask.IsCompleted)
            {
                yield return null;
            }

        try
        {
            if (registerTask.IsFaulted)
            {
                UnityEngine.Debug.LogError("Error registering user: " + registerTask.Exception.ToString());
                throw new Exception("Registering user:" + registerTask.Exception.ToString());
            }
            string data = registerTask.Result;
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Starting:" + ex);
            Application.Quit(); 
        }
      
    }

   
    IEnumerator UploadWavCoroutine(string filename)
    {
       
            Task<AudioReturn> task = Task.Run(() => sr.UploadWav(filename));
            while (!task.IsCompleted)
            {
                yield return null;
            }

        try { 
            if (task.IsFaulted)
            {
                UnityEngine.Debug.LogError("Error uploading file: " + task.Exception.ToString());
                throw new Exception("Uploading file:" + task.Exception.ToString());

            }
            else
            {
                AudioReturn audioReturn = task.Result;
                //Save the audio in assets/Resources, now it isn�t necessaty because not using 
                //Resources.Load due to huge delay and problems synchronizing
                string path = Directory.GetCurrentDirectory();
                string filepath = Path.Combine(path, "outputClient.wav");
                StartCoroutine(LoadAndPlayCoroutine(filepath));
                UnityEngine.Debug.Log("Upload successful!");
            }
    }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Starting:" + ex);
            Application.Quit(); 
        }

     
    }


    IEnumerator LoadAndPlayCoroutine(string filePath)
    {
        // This coroutine loads an audio clip from the specified file path using UnityWebRequestMultimedia.
        // It first creates a UnityWebRequest instance to fetch the audio clip asynchronously.
        // It then yields control until the request completes by using www.SendWebRequest().
        // When the request is successful, it retrieves the downloaded audio clip using DownloadHandlerAudioClip.GetContent(www).
        // It assigns the downloaded audio clip to the AudioSource component, changes the animator controller to Talk motion,
        // plays the audio clip, and starts another coroutine to wait for the audio to finish playing.
        // If the request fails, it logs an error message.

        //The key here is indicate that we want to load a local audio using file if instead of file we use http or https
        //we will load a remote resource

        //That is the fastest way I found to load resouces created dinamically, others methods as Resources.Load causes problems 
        //Unity takes a few seconds to detect the new resource but the code detect this inmediatly so some synchrionizings problems happened

            using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip("file://" + filePath, AudioType.WAV))
            {
                yield return www.SendWebRequest();
            try { 
                if (www.result == UnityWebRequest.Result.Success)
                {
                    AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                    audioSource.clip = clip;
                    //Change teachers animator
                    dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Talk");
                    audioSource.Play();
                    StartCoroutine(WaitForAudioToEndCoroutine());

                }

                else
                {
                    UnityEngine.Debug.LogError(www.error);
                    throw new Exception("Loading response audio" + www.error);
                }
             }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogError("Starting:" + ex);
                Application.Quit();
            }
    }

    }


    IEnumerator WaitForAudioToEndCoroutine()
    {

            while (audioSource.isPlaying)
            {
                yield return null;
            }
            isReady = true; 
            dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Idle");
            UnityEngine.Debug.Log("IsReady" + isReady + "IsRecording" + isRecording);
    }

    
    public IEnumerator LogoutCoroutine()
    {
       
            Task<string> task = Task.Run(() => sr.Logout());
            while (!task.IsCompleted)
            {
                yield return null;
            }
        try { 

            if (task.IsFaulted)
            {
                UnityEngine.Debug.LogWarning("Error Leaving: " + task.Exception.ToString());
                throw new Exception("Error Leaving: " + task.Exception.ToString());

            }
            else
            {
                string str = task.Result;
                UnityEngine.Debug.Log("Log out successful!");
            }
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Starting:" + ex);
            Application.Quit(); 
        }

    }


}

//Clases para el manejo del audio

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
        //Convert to Wav using the apropiate header and metadata and write it
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



/*
 ???????  ???????  ????   ??? ?????????? ???????  ???????? ???       ???      ???????? ??????? 
???????? ????????? ?????  ??? ?????????? ???? ??? ???????? ????      ???      ???????? ???  ???
???      ???   ??? ?????? ???    ???     ???? ??? ???   ?? ????      ???      ????     ???  ???
???      ???   ??? ??????????    ???     ???????? ???   ?? ????      ???      ??????   ????????
???????? ????????? ??? ??????    ???     ???  ??? ???????? ????????? ???????? ??????? ???  ???
 ???????  ???????  ???  ?????    ???     ???  ??? ???????? ????????? ???????? ???????? ???  ???
*/

public class ServerRequestsController
{
    //Handle the request to server
    private string serverUrl;
    private HttpClient session; //save state between diferent requests 

    //Constructor
    public ServerRequestsController()
    {
        this.serverUrl = "http://192.168.0.16:5000";
        this.session = new HttpClient();
    }

    public async Task<string> RegisterUser()
    {
        // This asynchronous method is responsible for registering a user on the server.
        // It attempts to connect to the server using an HTTP GET request.
        // If the connection is successful and the response status code indicates success,
        // it reads the response body and returns it as a string, indicating successful registration.
        // If the response status code indicates an error, it handles the error and retries up to three times.
        // If the connection attempt fails due to an HttpRequestException, it logs a message and retries up to three times.
        // If all retry attempts fail, it throws an exception indicating that it cannot connect to the server.

        int counter = 0;
        while (counter < 3)
        {
            try
            {
                HttpResponseMessage response = await session.GetAsync(serverUrl);
                string responseBody = await response.Content.ReadAsStringAsync();

                if (response.IsSuccessStatusCode)
                {
                    return responseBody;
                }
                else
                {
                    UnityEngine.Debug.LogWarning($"Logging in:  Unhandled status code: {response.StatusCode}");
                    counter++;
                }
            }
            catch (HttpRequestException)
            {
                UnityEngine.Debug.LogWarning("Unable to connect.");
                UnityEngine.Debug.LogWarning($"Retrying to establish connection: {counter}/2");
                counter++;
            }
        }

        throw new Exception("Loggin in: couldnt connect whit server");
    }
    
    public async Task<AudioReturn> UploadWav(string filename)
    {
        // This asynchronous method is responsible for uploading a WAV file to the server.
        // It creates the URL for the upload request and sets up necessary variables.
        // It reads the audio file specified by the filename parameter and prepares the file content for upload.
        // Then, it sends a POST request to the server with the WAV file as multipart form data.
        // If the upload is successful, it processes the server response, decodes the audio data,
        // saves the audio file locally, and prepares the data to be returned.
        // If the upload fails, it handles the error and returns null.

        // Constructs the URL for the upload request and initializes necessary variables.
        string url = $"{this.serverUrl}/upload_wav";
        string audioname = "outputClient";
        string audiopath = "outputClient.wav";
        AudioReturn audioReturn = new AudioReturn();    // Object of the class to be returned

        using (var content = new MultipartFormDataContent())
        {
            // Reads the audio file.
            byte[] fileBytes = File.ReadAllBytes(filename);
            var fileContent = new ByteArrayContent(fileBytes);
            // Adds the audio file content to the request.
            fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse("audio/wav");
            content.Add(fileContent, "wav_file", Path.GetFileName(filename));
            // Sends the request.
            HttpResponseMessage response = await this.session.PostAsync(url, content);

            if (response.IsSuccessStatusCode)
            {
                // Processes the server response.
                string jsonResponse = await response.Content.ReadAsStringAsync();
                var json_data = JsonUtility.FromJson<ServerResponseAudio>(jsonResponse);
                // Decodes and saves the audio.
                byte[] audio_data = Convert.FromBase64String(json_data.audio);
                File.WriteAllBytes(audiopath, audio_data);
                UnityEngine.Debug.Log($"File saved: {audioname}");
                // Prepares the data to be returned.
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

    private void HandleError(HttpResponseMessage response)
    {
        string error;  
        switch (response.StatusCode)
        {
            case System.Net.HttpStatusCode.Unauthorized:
                error = "Uploading wav: User should be registered";
                UnityEngine.Debug.LogError(error);
                throw new Exception(error);
                
            case System.Net.HttpStatusCode.NotFound:
                error = "Uploading wav: No audio WAV received or selected";
                UnityEngine.Debug.LogError("Uploading wav: No audio WAV received or selected");
                throw new Exception(error);
                
            case System.Net.HttpStatusCode.InternalServerError:
                error = "Uploading wav: Internal server error";
                UnityEngine.Debug.LogError("Uploading wav: Internal server error");
                throw new Exception(error);
                
            default:
                error = $"Uploading wav: status code: {response.StatusCode}";
                UnityEngine.Debug.LogError($"Uploading wav: status code: {response.StatusCode}");
                throw new Exception(error);
                
        }
    }

    public async Task<string> Logout()
    {
        // This asynchronous method is responsible for logging out the user from the server.
        // It constructs the URL for the logout request and sends a GET request to the server.
        // If the logout request is successful (returns status code OK), it returns "ok".
        // If the logout request fails for any reason, it throws an exception indicating the failure.

        string url = $"{this.serverUrl}/logout";

        // Logouts request
        HttpResponseMessage response = await session.GetAsync(url);

        // Check return code
        if (response.StatusCode != System.Net.HttpStatusCode.OK)
        {
            throw new Exception($"Leaving: Unhandled status code: {response.StatusCode}");
        }
        return ("ok");
        
    }


}







// Wrapper clases 
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
