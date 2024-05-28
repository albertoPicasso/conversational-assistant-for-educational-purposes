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

public class RegisterScript : MonoBehaviour
{
    public TMP_InputField nameInputField;
    public TMP_InputField usernameInputField;
    public TMP_InputField passwordInputField;
    public Button registerButton;
    public TMP_Text textComponent;

    public RegisterController regController;

    /**
    * @brief Inicializa la aplicación y configura el oyente del botón de registro.
    */
    void Start()
    {
        registerButton.onClick.AddListener(Register);

        try
        {
            regController = new RegisterController();
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogError("Register user:" + ex);
            Application.Quit();
        }
    }

    /**
     * @brief Maneja el proceso de registro del usuario.
     * 
     * Este método lee el nombre, nombre de usuario y contraseña de los campos de entrada e intenta registrar al usuario utilizando
     * el RegisterController. Si el registro es exitoso, registra un mensaje y cambia la escena. Si el registro falla,
     * muestra el mensaje de error en la interfaz de usuario.
     */
    void Register()
    {
        string name = nameInputField.text; 
        string username = usernameInputField.text;
        string password = passwordInputField.text;
        string message;

        message = regController.RegisterUser(name, username, password);
       
        if (message == "OK")
        {
            UnityEngine.Debug.Log("Registered");
            SceneManager.LoadScene(0);
        }
        else
        {
            textComponent.text = message;
        }
    }
}

public class RegisterController
{
    string serverUrl = "http://192.168.0.16:5000";



    /**
     * @brief Registra un nuevo usuario en el servidor.
     * 
     * Este método envía una solicitud de registro al servidor con el nombre, nombre de usuario y contraseña proporcionados.
     * Dependiendo de la respuesta del servidor, devuelve un mensaje que indica el resultado del intento de registro.
     * 
     * @param name El nombre del usuario.
     * @param username El nombre de usuario del usuario.
     * @param passwd La contraseña del usuario.
     * @return Una cadena que indica el resultado del intento de registro.
     */
    public string RegisterUser(string name, string username, string passwd)
    {

        string url = $"{this.serverUrl}/register_new_user";

        string jsonContent = "{\"name\": \"" + name + "\",\"username\": \"" + username + "\", \"password\": \"" + passwd + "\"}";
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
                    return "OK";
                }
                if (response.StatusCode == HttpStatusCode.Conflict)
                {
                    return "Username is not aviable";
                }
                else 
                {
                    return "Something have failed";
                }
            }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogError("Exception occurred: " + ex.Message);
                return "Something have failed ";
            }
        }

    }




}
