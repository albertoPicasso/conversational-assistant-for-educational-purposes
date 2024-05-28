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
     * @brief Inicializa la aplicaci�n y configura los oyentes de los botones de la interfaz de usuario.
     * 
     * Este m�todo se llama al iniciar el script. A�ade oyentes a los botones de iniciar sesi�n, crear usuario y eliminar usuario,
     * vincul�ndolos a sus respectivos m�todos de manejo. Luego intenta inicializar el LogInController. Si ocurre un error 
     * durante la inicializaci�n, registra el error y cierra la aplicaci�n.
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
     * @brief Maneja el proceso de inicio de sesi�n.
     * 
     * Este m�todo lee el nombre de usuario y la contrase�a de los campos de entrada e intenta iniciar sesi�n usando el LogInController.
     * Si el inicio de sesi�n es exitoso, registra un mensaje indicando el �xito. Si el inicio de sesi�n falla, muestra el mensaje de error 
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
     * Este m�todo llama al m�todo ChangeScene del LogInController para cambiar a la escena de registro de usuario.
     */
    void MoveToRegister()
    {
        logInController.ChangeScene(1); 
    }

    /**
     * @brief Maneja el proceso de eliminaci�n de usuario.
     * 
     * Este m�todo lee el nombre de usuario y la contrase�a de los campos de entrada e intenta eliminar al usuario utilizando el LogInController.
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
      * @brief Maneja el proceso de inicio de sesi�n del usuario.
      * 
      * Este m�todo env�a una solicitud de inicio de sesi�n al servidor con el nombre de usuario y la contrase�a proporcionados.
      * Dependiendo de la respuesta del servidor, cambia la escena o devuelve un mensaje de error.
      * 
      * @param username El nombre de usuario del usuario.
      * @param passwd La contrase�a del usuario.
      * @return Una cadena que indica el resultado del intento de inicio de sesi�n.
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
      * @brief Maneja el proceso de eliminaci�n de usuario.
      * 
      * Este m�todo env�a una solicitud al servidor para eliminar la cuenta de usuario con el nombre de usuario y la contrase�a proporcionados.
      * Dependiendo de la respuesta del servidor, devuelve un mensaje que indica el resultado del intento de eliminaci�n.
      * 
      * @param username El nombre de usuario del usuario.
      * @param passwd La contrase�a del usuario.
      * @return Una cadena que indica el resultado del intento de eliminaci�n.
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
     * Este m�todo cambia la escena actual a la especificada por el �ndice de la escena dado.
     * 
     * @param i El �ndice de la escena a la que se va a cambiar.
     */
    public void ChangeScene(int i)
    {
        SceneManager.LoadScene(i);
    }
}
