using UnityEngine;
using UnityEngine.UI; 
using TMPro;          
using System.Diagnostics;
using System.CodeDom;

using System.Net.Http;
using System.Text;
using System.Net;
using System;

using UnityEngine.SceneManagement;
using System.IO;

public class LoginHandler : MonoBehaviour
{
    public TMP_InputField usernameInputField;  
    public TMP_InputField passwordInputField;  
    public Button loginButton;
    public Button CreateUserButton;
    public TMP_Text textComponent;
    public Button DeleteUserButton;

    private LogInController logInController;

    /**
     * @brief Inicializa la aplicación y configura los oyentes de los botones de la interfaz de usuario.
     * 
     * Este método se llama al iniciar el script. Añade oyentes a los botones de iniciar sesión, crear usuario y eliminar usuario,
     * vinculándolos a sus respectivos métodos de manejo. Luego intenta inicializar el LogInController. Si ocurre un error 
     * durante la inicialización, registra el error y cierra la aplicación.
     */
    void Start()
    {
        // add a listener
        loginButton.onClick.AddListener(Login);
        CreateUserButton.onClick.AddListener(MoveToRegister);
        DeleteUserButton.onClick.AddListener(DeleteUser);
        
        try 
        { 
            logInController = new LogInController();
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("LogIn start:" + ex);
            Application.Quit();
        }
    }

    /**
     * @brief Maneja el proceso de inicio de sesión.
     * 
     * Este método lee el nombre de usuario y la contraseña de los campos de entrada e intenta iniciar sesión usando el LogInController.
     * Si el inicio de sesión es exitoso, registra un mensaje indicando el éxito. Si el inicio de sesión falla, muestra el mensaje de error 
     * en la interfaz de usuario.
     */
    void Login()
    {
        // Lee los valores de los campos de texto y los imprime en la consola
        string username = usernameInputField.text;
        string password = passwordInputField.text;
        string message; 

        message = logInController.LogIn(username, password);
        
        if (message == "OK") {
            UnityEngine.Debug.Log("Enter");
            
        }
        else 
        {
            textComponent.text = message; 
        }
    }

    /**
     * @brief Cambia a la escena de registro de usuario.
     * 
     * Este método llama al método ChangeScene del LogInController para cambiar a la escena de registro de usuario.
     */
    void MoveToRegister()
    {
        logInController.ChangeScene(1); 
    }

    /**
     * @brief Maneja el proceso de eliminación de usuario.
     * 
     * Este método lee el nombre de usuario y la contraseña de los campos de entrada e intenta eliminar al usuario utilizando el LogInController.
     * Registra el resultado y muestra el mensaje en la interfaz de usuario.
     */
    void DeleteUser()
    {
        string username = usernameInputField.text;
        string password = passwordInputField.text;

        string message = logInController.DeleteUser(username, password);
        UnityEngine.Debug.Log(message);
        textComponent.text = message;
    }

}


public class LogInController
{
    string serverUrl = "http://192.168.0.16:5000";


    /**
      * @brief Maneja el proceso de inicio de sesión del usuario.
      * 
      * Este método envía una solicitud de inicio de sesión al servidor con el nombre de usuario y la contraseña proporcionados.
      * Dependiendo de la respuesta del servidor, cambia la escena o devuelve un mensaje de error.
      * 
      * @param username El nombre de usuario del usuario.
      * @param passwd La contraseña del usuario.
      * @return Una cadena que indica el resultado del intento de inicio de sesión.
      */
    public string LogIn(string username, string passwd) 
    {
        string url = $"{this.serverUrl}/logIn";

        string jsonContent = "{\"username\": \"" + username + "\", \"password\": \"" + passwd + "\"}";
        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

        using (var client = new HttpClient())
        {
            try
            {
                // Async post
                var response = client.PostAsync(url, content).Result;

                // HTTP status
                
               if (response.StatusCode == HttpStatusCode.OK) {
                    ChangeScene(2);
                    return "OK";
                }
                if (response.StatusCode == HttpStatusCode.Unauthorized) {
                   return "LogIn have failed";
                }
                if (response.StatusCode == HttpStatusCode.InternalServerError) {
                    return "Something have failed";
                }
                return "Something have failed";
            }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogError   ("Exception occurred: " + ex.Message);
                return "Something have failed";
            }
        }
    }

    /**
      * @brief Maneja el proceso de eliminación de usuario.
      * 
      * Este método envía una solicitud al servidor para eliminar la cuenta de usuario con el nombre de usuario y la contraseña proporcionados.
      * Dependiendo de la respuesta del servidor, devuelve un mensaje que indica el resultado del intento de eliminación.
      * 
      * @param username El nombre de usuario del usuario.
      * @param passwd La contraseña del usuario.
      * @return Una cadena que indica el resultado del intento de eliminación.
      */
    public string DeleteUser(string username, string passwd)
    {
        string url = $"{this.serverUrl}/delete_user";

        string jsonContent = "{\"username\": \"" + username + "\", \"password\": \"" + passwd + "\"}";
        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

        using (var client = new HttpClient())
        {
            try
            {
                // Async post
                var response = client.PostAsync(url, content).Result;

                // HTTP status

                if (response.StatusCode == HttpStatusCode.OK)
                {
                    
                    return "Acount Deleted";
                }
                if (response.StatusCode == HttpStatusCode.Unauthorized)
                {
                    return "Delete Account have failed";
                }
                if (response.StatusCode == HttpStatusCode.InternalServerError)
                {
                    return "Something have failed";
                }
                return "Something have failed";
            }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogError("Exception occurred: " + ex.Message);
                return "Something have failed";
            }
        }
    }

    /**
     * @brief Cambia la escena actual.
     * 
     * Este método cambia la escena actual a la especificada por el índice de la escena dado.
     * 
     * @param i El índice de la escena a la que se va a cambiar.
     */
    public void ChangeScene(int i)
    {
        SceneManager.LoadScene(i);
    }
}
