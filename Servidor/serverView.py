import tkinter as tk
from tkinter import ttk
from serverController import ServerController

class ServerView():
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

        self.controller = ServerController()

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
        self.idioma = tk.StringVar(value="es")
        self.setup_dropdown(self.frame_config_principal, "Idioma del chat:", self.idioma, ('es', 'en', 'de'), self.cambiar_idioma)

        # Configuración de STT, LLM y TTS
        self.stt = tk.StringVar(value="local")
        self.llm = tk.StringVar(value="local")
        self.tts = tk.StringVar(value="local")
        self.setup_radio_section(self.frame_config_principal, "STT:", self.stt, self.cambiar_stt)
        self.setup_radio_section(self.frame_config_principal, "LLM:", self.llm, self.cambiar_llm)
        self.setup_radio_section(self.frame_config_principal, "TTS:", self.tts, self.cambiar_tts)

        # Configuración del número de puerto
        
        self.puerto = tk.StringVar(value="5000")
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
        self.whisperSize = tk.StringVar(value="base")
        self.setup_dropdown(self.frame_config_extra, "Tamaño Whisper:", self.whisperSize, ('small', 'base', 'tiny'))

        # Configuración de Modelos LLM
        self.modelos = tk.StringVar(value="Gemma")
        self.setup_dropdown(self.frame_config_extra, "Modelo LLM:", self.modelos, ('Gemma', 'Mistral7B'),  enabled=False)


    def setup_radio_section(self, frame, label_text, variable, command):
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
        label.pack(pady=(10,0))
        entry = tk.Entry(frame, textvariable=variable)
        entry.pack()

    def cambiar_idioma(self, event):
        #print("Idioma seleccionado:", self.idioma.get())
        pass

    def cambiar_stt(self):
        #print("Modo STT seleccionado:", self.stt.get())
        pass

    def cambiar_llm(self):
        #print("Modo LLM seleccionado:", self.llm.get())
        pass
        

    def cambiar_tts(self):
        #print("Modo TTS seleccionado:", self.tts.get())
        pass



    def lanzar_servidor(self):
        """
        Launches the server with the current configuration settings and prints the current state.

        Args:
            None

        Returns:
            None
        """
        """
        print("Estado actual:")
        print("Idioma seleccionado:", self.idioma.get())
        print("Modo STT seleccionado:", self.stt.get())
        print("Modo LLM seleccionado:", self.llm.get())
        print("Modo TTS seleccionado:", self.tts.get())
        print("Tamaño Whisper seleccionado:", self.whisperSize.get())
        print("Modelo LLM seleccionado:", self.modelos.get())
        print("Número de puerto:", self.puerto.get())
       """
        self.master.destroy()
        self.controller.launch_server(self.idioma.get(), self.stt.get(), self.whisperSize.get(),  self.llm.get(),  self.modelos.get(), self.tts.get(),self.puerto.get())
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerView(root)
    root.mainloop()
 