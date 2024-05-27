import tkinter as tk
from tkinter import ttk
from configController import ConfigController

class ServerView():
    """
    Class for creating and managing the server configuration interface.

    This class handles the initialization and layout of the server configuration interface
    using tkinter. It includes methods for setting up various widgets and handling user input
    to configure server settings such as language, STT, LLM, TTS, Whisper model size, and port.
    """

    def __init__(self, master):
        """
        Initializes an instance of the ServerConfig class.

        Args:
            - master (object): The master object to which this instance belongs.

        Returns:
            None
        """

        self.master = master
        self.master.title("Server Config")
        self.master.geometry("600x300")

        self.controller = ConfigController()

        self.setup_main_widgets()
        self.setup_extra_widgets()

    def setup_main_widgets(self):
        """
        Sets up the main widgets for the server configuration.

        Args:
            None

        Returns:
            None
        """

        # Frame principal para configuraciones comunes
        self.frame_config_principal = tk.Frame(self.master)
        self.frame_config_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuración de idioma
        self.idioma = tk.StringVar(value= self.controller.get_language())
        self.setup_dropdown(self.frame_config_principal, "Idioma del chat:", self.idioma, ('es', 'en', 'de'), self.cambiar_idioma)

        # Configuración de STT, LLM y TTS
        self.stt = tk.StringVar(value=self.controller.get_stt())
        self.llm = tk.StringVar(value=self.controller.get_llm())
        self.tts = tk.StringVar(value=self.controller.get_tts())
        self.setup_radio_section(self.frame_config_principal, "STT:", self.stt, self.cambiar_stt)
        self.setup_radio_section(self.frame_config_principal, "LLM:", self.llm, self.cambiar_llm)
        self.setup_radio_section(self.frame_config_principal, "TTS:", self.tts, self.cambiar_tts)

        # Configuración del número de puerto
        
        self.puerto = tk.StringVar(value=self.controller.get_port())
        self.puerto.trace_add("write", self.cambiar_puerto)
        self.setup_entry(self.frame_config_principal, "Número de puerto:", self.puerto)

        # Botón de lanzamiento
        boton_play = tk.Button(self.master, text="Play", command=self.lanzar_servidor, bg="green", font=("Helvetica", 10, "bold"))
        boton_play.pack(side=tk.BOTTOM, pady=10)

    
    def setup_dropdown(self, frame, label_text, variable, options, command=None, enabled = True):
        """
        Sets up a dropdown widget within a specified frame.

        Args:
            - frame (tk.Frame): The frame in which the dropdown will be placed.
            - label_text (str): The text to display as a label for the dropdown.
            - variable (tk.StringVar): The variable to which the selected value will be assigned.
            - options (tuple): A tuple containing the options to be displayed in the dropdown.
            - command (function, optional): A function to be called when an option is selected (default is None).
            - enabled (bool, optional): Specifies whether the dropdown is initially enabled (default is True).

        Returns:
            None
        """

        label = tk.Label(frame, text=label_text, font=("Helvetica", 10, "italic"))
        label.pack(pady=(10,0))  # Espaciado vertical para la etiqueta
        
        dropdown = ttk.Combobox(frame, textvariable=variable, state="readonly" if enabled else "disabled", values=options)
        dropdown.current(0)  # Establece el valor inicial seleccionado
        dropdown.pack(pady=(0,20))  # Espaciado vertical después del dropdown
        
        if command:
            dropdown.bind("<<ComboboxSelected>>", command)  # Enlaza un comando que se ejecuta al seleccionar

    def setup_extra_widgets(self):
        """
        Sets up additional widgets for the server configuration.

        Args:
            None

        Returns:
            None
        """
        # Frame para configuraciones adicionales
        self.frame_config_extra = tk.Frame(self.master, padx=20, pady=20)
        self.frame_config_extra.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Configuración de Tamaño Whisper
        self.whisperSize = tk.StringVar(value=self.controller.get_whisper_size())
        self.setup_dropdown(
            self.frame_config_extra, 
            "Tamaño Whisper:", 
            self.whisperSize, 
            ('small', 'base', 'tiny'), 
            self.on_whisper_size_change
        )

        # Configuración de Modelos LLM
        self.modelos = tk.StringVar(value="Gemma")
        self.setup_dropdown(self.frame_config_extra, "Modelo LLM:", self.modelos, ('Gemma', 'Mistral7B'),  enabled=False)


    def setup_radio_section(self, frame, label_text, variable, command = None):
        """
        Sets up a section with radio buttons within a specified frame.

        Args:
            - frame (tk.Frame): The frame in which the radio section will be placed.
            - label_text (str): The text to display as a label for the radio section.
            - variable (tk.StringVar): The variable to which the selected value will be assigned.
            - command (function): A function to be called when a radio button is selected.

        Returns:
            None
        """

        label = tk.Label(frame, text=label_text, font=("Helvetica", 10, "italic"))
        label.pack(pady=(0,5))
        frame_botones = tk.Frame(frame)
        frame_botones.pack()
        tk.Radiobutton(frame_botones, text="Local", variable=variable, value="local", command=command).pack(side=tk.LEFT, expand=True)
        tk.Radiobutton(frame_botones, text="Remoto", variable=variable, value="remoto", command=command).pack(side=tk.LEFT, expand=True)



    def setup_entry(self, frame, label_text, variable):
        """
        Sets up an entry widget within a specified frame.

        Args:
            - frame (tk.Frame): The frame in which the entry will be placed.
            - label_text (str): The text to display as a label for the entry.
            - variable (tk.StringVar): The variable to which the entry's value will be assigned.

        Returns:
            None
        """
        label = tk.Label(frame, text=label_text, font=("Helvetica", 10, "italic"))
        label.pack(pady=(10, 0))
        entry = tk.Entry(frame, textvariable=variable)
        entry.pack()


    def cambiar_puerto(self, *args):
        """
        Change the server port setting.

        This method retrieves the port value from the user input and sets it in the controller.

        Args:
            *args: Additional arguments passed by the trace or event handler.
        """
        self.controller.set_port(self.puerto.get())

    def cambiar_idioma(self, event):
        """
        Change the language setting.

        This method retrieves the language value from the user input and sets it in the controller.

        Args:
            event (Event): The event that triggered the language change.
        """
        self.controller.set_language(self.idioma.get())

    def cambiar_stt(self):
        """
        Change the speech-to-text (STT) setting.

        This method retrieves the STT value from the user input and sets it in the controller.
        """
        self.controller.set_stt(self.stt.get())

    def cambiar_llm(self):
        """
        Change the large language model (LLM) setting.

        This method retrieves the LLM value from the user input and sets it in the controller.
        """
        self.controller.set_llm(self.llm.get())

    def cambiar_tts(self):
        """
        Change the text-to-speech (TTS) setting.

        This method retrieves the TTS value from the user input and sets it in the controller.
        """
        self.controller.set_tts(self.tts.get())

    def on_whisper_size_change(self, value):
        """
        Handle the change event for the Whisper model size setting.

        This method retrieves the Whisper model size value from the user input and sets it in the controller.

        Args:
            value (str): The new Whisper model size selected by the user.
        """
        self.controller.set_whisper_size(self.whisperSize.get())

    def on_modelos_change(self, value):
        """
        Handle the change event for the LLM models setting.

        This method retrieves the LLM models value from the user input and sets it in the controller.

        Args:
            value (str): The new LLM model selected by the user.
        """
        self.controller.set_llm_models(self.modelos.get())



    def lanzar_servidor(self):
        """
        Launches the server with the current configuration settings and prints the current state.

        Args:
            None

        Returns:
            None
        """

        self.master.destroy()
        self.controller.launch_server()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerView(root)
    root.mainloop()
