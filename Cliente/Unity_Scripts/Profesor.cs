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



//=============================================================================
// ╔══════════════════════════════════════════════════════╗                     
// ║                       VISTA                          ║                     
// ╚══════════════════════════════════════════════════════╝                     
//=============================================================================
public class Profesor : MonoBehaviour
{
    public AudioSource audioSource;
    public Animator dashiAnimator;

    private string outFileName; 
    private Controller controller;

    // Start is called before the first frame update

    /**
     * @brief Inicializa la aplicación y configura los componentes necesarios.
     * 
     * Este método se llama al iniciar el script. Inicializa el controlador, recupera la ruta del archivo de salida
     * y comienza una coroutine para registrar la sesión del usuario en el servidor. Luego intenta limpiar datos antiguos,
     * recuperar el componente AudioSource y configurar los ajustes de la pantalla. Si ocurre un error durante la inicialización,
     * registra el error y cierra la aplicación.
     */
    void Start()
    {
        controller = new Controller();
        outFileName = controller.GetoutFilePath();
        // Registers the user on the server.
        StartCoroutine(controller.RegisterUserSessionCoroutine());
 
        try
        {

            controller.CleanData(); 
            // Retrieves the AudioSource component attached to the GameObject.
            audioSource = GetComponent<AudioSource>();

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

    // Update is called once per frame
    /**
     * @brief Actualiza el estado de la aplicación en cada frame.
     * 
     * Este método se llama una vez por frame y verifica la entrada del usuario. Si se presiona la tecla espacio, alterna el estado de grabación
     * llamando al método Spacepressed en el controlador. Si la grabación se detiene, cambia el controlador del animador a un movimiento de "Strafe",
     * inicia una coroutine para subir el archivo WAV y otra coroutine para verificar la existencia del archivo de audio y reproducirlo cuando esté disponible.
     */
    void Update()
    {
        bool wait = false;
        if (Input.GetKeyDown(KeyCode.Space))
        {
            wait = controller.Spacepressed(audioSource);
            
            if (wait) 
            {
                dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Strafe");
                StartCoroutine(controller.UploadWavCoroutine());
                StartCoroutine(CheckAndPlayAudio(outFileName)); 
            }
        }
        
    }

    /**
     * @brief Coroutine para verificar la existencia de un archivo de audio y reproducirlo cuando esté disponible.
     * 
     * Esta coroutine verifica continuamente si un archivo de audio especificado existe en una ruta dada. Si el archivo no existe,
     * espera 1 segundo antes de verificar nuevamente. Una vez que se encuentra el archivo, inicia otra coroutine para cargar y reproducir el audio.
     * 
     * @param fileName El nombre del archivo que se va a verificar y reproducir.
     * @return Un IEnumerator que se puede usar para gestionar la ejecución de la coroutine.
     */
    IEnumerator CheckAndPlayAudio(string fileName)
    {
        string path = Directory.GetCurrentDirectory();
        string filePath = Path.Combine(path, fileName);

        // Verificar si el archivo existe antes de intentar cargarlo
        while (!File.Exists(filePath))
        {
            yield return new WaitForSeconds(1); // Espera 1 segundo antes de verificar de nuevo
        }

        StartCoroutine(LoadAndPlayCoroutine(fileName));
    }

    /**
     * @brief Coroutine para cargar y reproducir un clip de audio desde un archivo especificado.
     * 
     * Esta coroutine carga un clip de audio desde la ruta de archivo especificada usando UnityWebRequestMultimedia. Crea una
     * instancia de UnityWebRequest para obtener el clip de audio de forma asíncrona, cediendo el control hasta que la solicitud se complete.
     * Al completarse con éxito, recupera el clip de audio descargado y lo asigna al componente AudioSource. La coroutine también
     * cambia el controlador del animador a un movimiento de "Talk", reproduce el clip de audio e inicia otra coroutine para esperar
     * a que termine de reproducirse. Si la solicitud falla, registra un mensaje de error.
     * 
     * La clave aquí es indicar que queremos cargar un archivo de audio local usando el protocolo de archivo. Si se usa http o https 
     * en lugar de file, se cargará un recurso remoto. Este método es la forma más rápida de cargar recursos creados dinámicamente 
     * porque otros métodos, como Resources.Load, pueden causar problemas de sincronización debido a los retrasos en la detección 
     * de nuevos recursos por parte de Unity.
     * 
     * @param fileName El nombre del archivo que se va a cargar y reproducir.
     * @return Un IEnumerator que se puede usar para gestionar la ejecución de la coroutine.
     */
    IEnumerator LoadAndPlayCoroutine(string fileName)
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
        string path = Directory.GetCurrentDirectory();
        string filePath = Path.Combine(path, fileName);

        using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip("file://" + filePath, AudioType.WAV))
        {
            yield return www.SendWebRequest();
            try
            {
                if (www.result == UnityWebRequest.Result.Success)
                {
                    AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                    audioSource.clip = clip;
                    //Change teachers animator
                    dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Talk");
                    audioSource.Play();
                    StartCoroutine(WaitForAudioToEndCoroutine(filePath));

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

    /**
     * @brief Coroutine que espera a que termine la reproducción del audio y luego realiza operaciones de limpieza.
     * 
     * Esta coroutine espera hasta que el AudioSource deje de reproducir. Una vez que la reproducción de audio se completa, 
     * establece el controlador del animador en un estado inactivo, elimina el archivo especificado si existe, y registra 
     * un mensaje indicando el fin de la reproducción.
     * 
     * @param pathToFile La ruta al archivo que debe eliminarse después de que termine la reproducción del audio.
     * @return Un IEnumerator que se puede usar para gestionar la ejecución de la coroutine.
     */
    IEnumerator WaitForAudioToEndCoroutine(string pathToFile)
    {

        while (audioSource.isPlaying)
        {
            yield return null;
        }
        dashiAnimator.runtimeAnimatorController = Resources.Load<RuntimeAnimatorController>("BasicMotions@Idle");
        if (File.Exists(pathToFile))
        {
            // Borra el archivo
            File.Delete(pathToFile);
            Console.WriteLine("Archivo borrado con éxito.");
        }
        UnityEngine.Debug.Log("Fin repro");
    }



    /**
     * @brief Maneja las operaciones cuando la aplicación está a punto de cerrarse.
     * 
     * Esta función se llama automáticamente cuando la aplicación está a punto de cerrarse. Inicia una coroutine asíncrona
     * para realizar las operaciones de cierre de sesión llamando al método LogoutCoroutine del controlador. Además, registra 
     * un mensaje indicando que el juego se está cerrando.
     */
    void OnApplicationQuit()
    {
        // This function is called when the application is about to quit.
        // It initiates an asynchronous coroutine to perform logout operations.
        // Additionally, it logs a message indicating that the game is closing.
        StartCoroutine(controller.LogoutCoroutine());
        UnityEngine.Debug.Log("Game is closing, leaving.");        
    }
}


//=============================================================================
// ╔══════════════════════════════════════════════════════╗                     
// ║                   CONTROLADORES                      ║                     
// ╚══════════════════════════════════════════════════════╝                     
//=============================================================================
public class Controller 
{
    Model model = new Model();
    ServerRequestsController src = new ServerRequestsController();

    public string GetoutFilePath()
    {
        return model.GetoutFilePath(); 
    }

    //Clean data
    /**
     * @brief Limpia los datos llamando al método CleanData del modelo.
     * 
     * Este método delega la tarea de limpiar los datos al método CleanData del modelo.
     * Es una función simple que asegura que la lógica de limpieza de datos esté encapsulada dentro del modelo.
     */
    public void CleanData()
    {
        model.CleanData(); 
    }

    //LogOut
    /**
     * @brief Coroutine para manejar el registro de una sesión de usuario.
     * 
     * Esta coroutine inicia una tarea asíncrona para registrar una sesión de usuario con el servidor. Comienza la tarea de registro
     * y espera a que se complete. Al completarse, verifica si la tarea encontró algún fallo. Si ocurrió un error durante el proceso de registro,
     * registra un mensaje de error y lanza una excepción. En caso de cualquier excepción, registra el error y termina la aplicación.
     * 
     * @return Un IEnumerator que se puede usar para gestionar la ejecución de la coroutine.
     */
    public IEnumerator RegisterUserSessionCoroutine()
    {

        Task<string> registerTask = src.RegisterUserSession();
        while (!registerTask.IsCompleted)
        {
            yield return null;
        }

        try
        {
            if (registerTask.IsFaulted)
            {
                UnityEngine.Debug.LogError("Error registering user session: " + registerTask.Exception.ToString());
                throw new Exception("Registering user session:" + registerTask.Exception.ToString());
            }
            
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Starting:" + ex);
            Application.Quit();
        }
    }

    //Record Audio
    /**
     * @brief Maneja el estado de grabación cuando se presiona la tecla espacio.
     * 
     * Este método verifica si la grabación está actualmente en progreso. Si no está grabando, comienza la grabación de audio.
     * Si ya está grabando, detiene la grabación de audio. El método devuelve un valor booleano que indica el nuevo 
     * estado de la grabación.
     * 
     * @param audioSource El componente AudioSource utilizado para grabar o detener la grabación.
     * @return True si la grabación se detuvo, false si la grabación comenzó.
     */
    public bool Spacepressed(AudioSource audioSource) 
    {
        if (!(model.GetIsRecording()))
        {
            model.AudioRecord(audioSource);
            return false; 
        }
        else
        { 
            model.StopAudioRecord(audioSource);
            return true; 

        }
    }


    /**
     * @brief Coroutine para manejar la subida de un archivo WAV.
     * 
     * Esta coroutine inicia una tarea asíncrona para subir un archivo WAV al servidor. Recupera las rutas de los archivos,
     * comienza la tarea de subida y espera a que se complete. Al completarse, verifica si la tarea encontró algún fallo.
     * Si ocurrió un error durante el proceso de subida, registra un mensaje de error y lanza una excepción. Si la 
     * subida es exitosa, procesa la respuesta del servidor, guarda los datos de audio y registra un mensaje de éxito. En caso 
     * de cualquier excepción, registra el error y termina la aplicación.
     * 
     * @return Un IEnumerator que se puede usar para gestionar la ejecución de la coroutine.
     */
    public IEnumerator UploadWavCoroutine()
    {
        string filename = model.GetfilePath();
        string outFilename = model.GetoutFilePath();
        AudioReturn audioReturn = new AudioReturn(); 

        Task<AudioReturn> task = Task.Run(() => src.UploadWav(filename));
        while (!task.IsCompleted)
        {
            yield return null;
        }

        try
        {
            if (task.IsFaulted)
            {
                UnityEngine.Debug.LogError("Error uploading file: " + task.Exception.ToString());
                throw new Exception("Uploading file:" + task.Exception.ToString());

            }
            else
            {
                audioReturn = task.Result;
                byte[] audio_data = audioReturn.audio_data; 
                model.SaveServerResponse(audio_data, outFilename); 
                //Save the audio in assets/Resources, now it isn´t necessaty because not using 
                //Resources.Load due to huge delay and problems synchronizing
                string path = Directory.GetCurrentDirectory();
                string filepath = Path.Combine(path, "outputClient.wav");
                UnityEngine.Debug.Log("Upload successful!");
            }
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Starting:" + ex);
            Application.Quit();
        }


    }

    //Logout 
    /**
     * @brief Coroutine para manejar el proceso de cierre de sesión del usuario.
     * 
     * Esta coroutine inicia una tarea de cierre de sesión y espera a que se complete. Cede continuamente hasta que 
     * la tarea se complete. Al completarse, verifica si la tarea encontró algún fallo. Si ocurrió un error 
     * durante el proceso de cierre de sesión, registra una advertencia y lanza una excepción. Si el cierre de sesión 
     * es exitoso, registra un mensaje de éxito. En caso de cualquier excepción, registra el error y termina la aplicación.
     * 
     * @return Un IEnumerator que se puede usar para gestionar la ejecución de la coroutine.
     */
    public IEnumerator LogoutCoroutine()
    {
        Task<string> task = Task.Run(() => src.Logout());
        while (!task.IsCompleted)
        {
            yield return null;
        }

        try
        {
            if (task.IsFaulted)
            {
                UnityEngine.Debug.LogWarning("Error Leaving: " + task.Exception.ToString());
                throw new Exception("Error Leaving: " + task.Exception.ToString());

            }
            else
            {
                string str = task.Result;
                UnityEngine.Debug.Log("Logout successful!");
            }
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Starting:" + ex);
            Application.Quit();
        }

    }
}



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


    /**
     * @brief Registra una sesión de usuario en el servidor de forma asíncrona.
     * 
     * Este método intenta registrar a un usuario en el servidor enviando una solicitud HTTP GET a la URL del servidor.
     * Si la conexión es exitosa y el código de estado de la respuesta indica éxito, lee el cuerpo de la respuesta
     * y lo devuelve como una cadena, indicando un registro exitoso. Si el código de estado de la respuesta indica un error,
     * maneja el error y reintenta hasta tres veces. Si el intento de conexión falla debido a una HttpRequestException,
     * registra un mensaje y reintenta hasta tres veces. Si todos los intentos de reintento fallan, lanza una excepción que indica
     * que no se puede conectar al servidor.
     * 
     * @return Una tarea que representa la operación asíncrona. El resultado de la tarea contiene el cuerpo de la respuesta como una cadena
     * si el registro es exitoso.
     * @throws Exception si todos los intentos de reintento fallan y no se puede establecer la conexión con el servidor.
     */
    public async Task<string> RegisterUserSession()
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


    /**
      * @brief Sube un archivo WAV al servidor de forma asíncrona y procesa la respuesta.
      * 
      * Este método sube un archivo WAV especificado por el parámetro filename a un servidor. Construye la
      * URL de subida, lee el archivo de audio y envía una solicitud POST con el archivo como datos de formulario multiparte.
      * Si la subida es exitosa, procesa la respuesta del servidor, decodifica los datos de audio, guarda el
      * archivo de audio localmente y prepara los datos para ser devueltos. Si la subida falla, maneja el
      * error y devuelve null.
      * 
      * @param filename El nombre del archivo WAV que se va a subir.
      * @return Una tarea que representa la operación asíncrona. El resultado de la tarea contiene un 
      * objeto AudioReturn con los datos de la respuesta del servidor o null si la subida falla.
      */
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
                // Prepares the data to be returned.
                audioReturn.isEnd = json_data.flag;
                audioReturn.audio_data = audio_data;
                return audioReturn;
            }
            else
            {
                HandleError(response);
                return null;
            }
        }
    }

    /**
       * @brief Maneja errores basados en el código de estado de la respuesta HTTP.
       * 
       * Este método verifica el código de estado de una respuesta HTTP y registra un mensaje de error apropiado.
       * También lanza una excepción con un mensaje de error específico dependiendo del código de estado.
       * Los códigos de estado manejados incluyen Unauthorized (401), Not Found (404) y Internal Server Error (500).
       * Para otros códigos de estado, se registra un mensaje de error genérico y se lanza una excepción.
       * 
       * @param response El mensaje de respuesta HTTP que contiene el código de estado a manejar.
       * @throws Exception con un mensaje correspondiente al código de estado de error.
       */
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


    /**
     * @brief Cierra la sesión del usuario en el servidor de forma asíncrona.
     * 
     * Este método envía una solicitud GET asíncrona al servidor para cerrar la sesión del usuario actual.
     * Construye la URL para la solicitud de cierre de sesión utilizando la URL base del servidor. Si la solicitud de cierre de sesión
     * es exitosa (devuelve el código de estado HTTP OK), el método devuelve la cadena "ok".
     * Si la solicitud de cierre de sesión falla por cualquier razón (por ejemplo, problemas de red, errores del servidor),
     * se lanza una excepción detallando la falla.
     *
     * @return Task<string> Una tarea que representa la operación asíncrona. El resultado de la tarea
     * es "ok" si el cierre de sesión es exitoso; de lo contrario, se lanza una excepción.
     * @exception Exception Lanzada si la solicitud de cierre de sesión devuelve un código de estado distinto de OK.
     */
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




//=============================================================================
// ╔══════════════════════════════════════════════════════╗                     
// ║                     MODELO                           ║                     
// ╚══════════════════════════════════════════════════════╝                     
//=============================================================================

public class Model
   
{ 
    private bool isRecording  = false;
    private const int AUDIOSECS = 40;
    private string filePath = "AudioRecorded.wav";
    private string outFilePath = "outputClient.wav";

    /**
     * @brief Obtiene el estado de grabación.
     * 
     * Este método devuelve un valor booleano que indica si la grabación está en progreso.
     * 
     * @return True si la grabación está en progreso, false de lo contrario.
     */
    public bool GetIsRecording()
    {
        return isRecording;
    }

    /**
     * @brief Obtiene la ruta del archivo.
     * 
     * Este método devuelve una cadena que contiene la ruta del archivo.
     * 
     * @return La ruta del archivo como una cadena.
     */
    public string GetfilePath()
    {
        return filePath;
    }

    /**
     * @brief Obtiene la ruta de salida del archivo.
     * 
     * Este método devuelve una cadena que contiene la ruta de salida del archivo.
     * 
     * @return La ruta de salida del archivo como una cadena.
     */
    public string GetoutFilePath()
    {
        return outFilePath;
    }


    /**
     * @brief Limpia los datos eliminando un archivo especificado si existe.
     * 
     * Este método verifica si existe un archivo en la ruta de salida especificada. Si el archivo existe, lo elimina.
     * Esto es útil para asegurar que los archivos antiguos o temporales se eliminen antes de que se procesen o creen nuevos datos.
     */
    public void CleanData()
    {
        //string filePath = "outputClient.wav";

        // Check if the file exists before trying to delete it
        if (File.Exists(outFilePath))
        { 
            File.Delete(outFilePath);
            
        }

    }


    /**
     * @brief Comienza a grabar audio usando el componente AudioSource proporcionado.
     * 
     * Este método inicia una grabación de audio usando el AudioSource especificado. Verifica si un dispositivo de micrófono
     * está disponible. Si no está disponible, registra una advertencia y sale de la función. Si hay un micrófono disponible,
     * comienza a grabar un clip de audio con una duración y una tasa de muestreo predefinidas. La grabación no se repetirá.
     *
     * @param audioSource El componente AudioSource utilizado para grabar el audio.
     */
    public void AudioRecord(AudioSource audioSource) {

        isRecording = true;
        if (Microphone.devices.Length <= 0)
        {
            UnityEngine.Debug.LogWarning("No microphone devices found!");
            return;
        }

        audioSource.clip = Microphone.Start(null, true, AUDIOSECS, 44100);
        audioSource.loop = false;
        UnityEngine.Debug.Log("Recording started. Press Space to stop.");
    }


    /**
     * @brief Detiene la grabación de audio y desencadena la guardado del audio grabado.
     * 
     * Este método finaliza la sesión de grabación de audio usando el AudioSource dado. Verifica si la grabación está
     * actualmente activa con Microphone.IsRecording(). Si la grabación no está activa, se registra una advertencia. Si la grabación
     * está activa y el clip de audio ha capturado datos (longitud > 0), detiene la grabación y llama a un método para guardar
     * el audio. Si no se capturan datos de audio (longitud del clip de audio es 0), se registra un mensaje de error.
     *
     * @param audioSource El componente AudioSource del cual se detiene la grabación de audio.
     */
    public void StopAudioRecord(AudioSource audioSource)
    {
        

        if (!Microphone.IsRecording(null))
        {
            UnityEngine.Debug.LogWarning("Recording was not active.");
        }

        else if (audioSource.clip.length > 0)
        {
            Microphone.End(null);
            UnityEngine.Debug.Log("Stop record");
            SaveWavFile(audioSource);
        }

        
        isRecording=false;
    }


    /**
     * @brief Guarda el clip de audio grabado como un archivo WAV.
     * 
     * Este método verifica si el clip de audio del AudioSource proporcionado es nulo. Si es así,
     * se registra un error y se lanza una excepción. De lo contrario, recupera los datos de audio,
     * los convierte en un arreglo de bytes WAV usando WavUtility.FromAudioClip() e intenta guardar
     * estos datos en el disco. Si el archivo WAV tiene una longitud no nula, se guarda y se registra un mensaje
     * de éxito. Si el archivo WAV está vacío o la conversión falla, se registra un error y se lanza
     * una excepción.
     *
     * @param audioSource El componente AudioSource que contiene el clip de audio que se va a guardar.
     * @exception Exception Lanzada si no se capturan datos de audio o si la conversión al formato WAV falla.
     */
    void SaveWavFile(AudioSource audioSource)
    {
         
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


    /**
     * @brief Guarda la respuesta del servidor como un archivo de audio.
     * 
     * Este método guarda un arreglo de bytes de datos de audio en una ruta de archivo especificada. Escribe los
     * datos de audio en el disco usando File.WriteAllBytes y registra la ruta del archivo guardado. Esta
     * función se utiliza típicamente para almacenar archivos de audio recibidos de respuestas del servidor.
     *
     * @param audio_data El arreglo de bytes que contiene los datos de audio que se van a guardar.
     * @param audiopath La ruta del archivo donde se deben guardar los datos de audio.
     */
    public void SaveServerResponse(byte[] audio_data, string audiopath) 
    {
         
        File.WriteAllBytes(audiopath, audio_data);
        UnityEngine.Debug.Log($"File saved: {audiopath}");
    }


}

public static class WavUtility
{
    /**
     * @brief Convierte las muestras en flotante de un AudioClip en un arreglo de bytes y las procesa en formato WAV.
     * 
     * Este método toma un AudioClip y sus muestras en flotante, convierte las muestras en flotante a enteros de 16 bits,
     * y luego a bytes. Maneja la conversión escalando los valores en flotante y empaquetándolos en un arreglo de bytes.
     * Finalmente, llama a otro método para convertir estos datos en bytes a un archivo en formato WAV usando los encabezados
     * y metadatos apropiados.
     *
     * @param clip El AudioClip del cual se toma la información base como el conteo de muestras, canales y frecuencia.
     * @param samples El arreglo de flotantes de muestras de audio del AudioClip.
     * @return byte[] Un arreglo de bytes formateado como un archivo WAV con los encabezados y datos apropiados.
     */
    public static byte[] FromAudioClip(AudioClip clip, float[] samples)
    {    
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

    /**
     * @brief Convierte datos de audio en un formato de archivo WAV y lo devuelve como un arreglo de bytes.
     * 
     * Este método crea un archivo WAV escribiendo los encabezados y metadatos necesarios en un flujo de memoria,
     * seguido por los propios datos de audio. Utiliza un BinaryWriter para escribir datos en el MemoryStream,
     * asegurando que los datos de audio estén formateados según las especificaciones del archivo WAV.
     *
     * @param dataSource El arreglo de bytes que contiene los datos de audio en bruto que se escribirán en el archivo WAV.
     * @param sampleCount El número total de muestras en los datos de audio.
     * @param channels El número de canales de audio (por ejemplo, 1 para mono, 2 para estéreo).
     * @param frequency La tasa de muestreo de los datos de audio (en Hz).
     * @param byteDepth La profundidad de cada muestra en bytes (por ejemplo, 2 para audio de 16 bits).
     * @return byte[] Un arreglo de bytes que representa el archivo WAV completo con encabezados y datos de audio.
     */
    static byte[] ConvertAndWrite(byte[] dataSource, int sampleCount, int channels, int frequency, int byteDepth)
    {
        MemoryStream memoryStream = new MemoryStream();
        BinaryWriter writer = new BinaryWriter(memoryStream);

        WriteHeader(writer, sampleCount, channels, frequency, byteDepth);

        writer.Write(dataSource);

        return memoryStream.ToArray();
    }


    /**
     * @brief Escribe el encabezado del archivo WAV en un flujo binario.
     * 
     * Este método escribe los encabezados necesarios para un archivo WAV, incluyendo el chunk RIFF, el chunk de formato,
     * y el comienzo del chunk de datos. Especifica el tamaño de cada chunk basado en las características de los datos de audio
     * como el número de muestras, el número de canales, la frecuencia y la profundidad de bytes. Esta configuración
     * asegura que el archivo WAV resultante cumpla con el formato estándar WAV.
     *
     * @param writer El BinaryWriter utilizado para escribir los encabezados en el flujo binario.
     * @param sampleCount El número total de muestras en los datos de audio.
     * @param channels El número de canales de audio (por ejemplo, 1 para mono, 2 para estéreo).
     * @param frequency La tasa de muestreo de los datos de audio (en Hz).
     * @param byteDepth La profundidad de cada muestra en bytes (por ejemplo, 2 para audio de 16 bits).
     */
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

// Wrapper clases 
public class ServerResponseAudio
{
    public string audio;
    public bool flag;
}

public class AudioReturn
{
    public byte[] audio_data;
    public bool isEnd;
}
