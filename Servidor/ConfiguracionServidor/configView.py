import tkinter as tk
from tkinter import ttk
from configController import ConfigController

class ConfigView():
    """
    Clase para crear y gestionar la interfaz de configuración del servidor.

    Esta clase maneja la inicialización y el diseño de la interfaz de configuración del servidor
    usando tkinter. Incluye métodos para configurar varios widgets y manejar la entrada del usuario
    para configurar ajustes del servidor tales como idioma, STT, LLM, TTS, tamaño del modelo Whisper y puerto.
    """

    def __init__(self, master):
        """
        Inicializa una instancia de la clase ServerConfig.

        Args:
            master (object): El objeto principal al que pertenece esta instancia.

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
        Configura los widgets principales para la configuración del servidor.

        Args:
            None

        Returns:
            None
        """
        # Frame principal para configuraciones comunes
        self.frame_config_principal = tk.Frame(self.master)
        self.frame_config_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configuración de idioma
        self.idioma = tk.StringVar(value=self.controller.get_language())
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

    def setup_dropdown(self, frame, label_text, variable, options, command=None, enabled=True):
        """
        Configura un widget de lista desplegable dentro de un marco especificado.

        Args:
            frame (tk.Frame): El marco en el que se colocará la lista desplegable.
            label_text (str): El texto a mostrar como etiqueta de la lista desplegable.
            variable (tk.StringVar): La variable a la que se asignará el valor seleccionado.
            options (tuple): Una tupla que contiene las opciones a mostrar en la lista desplegable.
            command (function, optional): Una función que se llamará cuando se seleccione una opción (por defecto es None).
            enabled (bool, optional): Especifica si la lista desplegable está habilitada inicialmente (por defecto es True).

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
        Configura widgets adicionales para la configuración del servidor.

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
        self.setup_dropdown(self.frame_config_extra, "Modelo LLM:", self.modelos, ('Gemma', 'Mistral7B'), enabled=False)

    def setup_radio_section(self, frame, label_text, variable, command=None):
        """
        Configura una sección con botones de opción dentro de un marco especificado.

        Args:
            frame (tk.Frame): El marco en el que se colocará la sección de botones de opción.
            label_text (str): El texto a mostrar como etiqueta de la sección de botones de opción.
            variable (tk.StringVar): La variable a la que se asignará el valor seleccionado.
            command (function): Una función que se llamará cuando se seleccione un botón de opción.

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
        Configura un widget de entrada dentro de un marco especificado.

        Args:
            frame (tk.Frame): El marco en el que se colocará la entrada.
            label_text (str): El texto a mostrar como etiqueta de la entrada.
            variable (tk.StringVar): La variable a la que se asignará el valor de la entrada.

        Returns:
            None
        """
        label = tk.Label(frame, text=label_text, font=("Helvetica", 10, "italic"))
        label.pack(pady=(10, 0))
        entry = tk.Entry(frame, textvariable=variable)
        entry.pack()

    def cambiar_puerto(self, *args):
        """
        Cambia la configuración del puerto del servidor.

        Este método recupera el valor del puerto de la entrada del usuario y lo establece en el controlador.

        Args:
            *args: Argumentos adicionales pasados por el rastreador o controlador de eventos.

        Returns:
            None
        """
        self.controller.set_port(self.puerto.get())

    def cambiar_idioma(self, event):
        """
        Cambia la configuración del idioma.

        Este método recupera el valor del idioma de la entrada del usuario y lo establece en el controlador.

        Args:
            event (Event): El evento que activó el cambio de idioma.

        Returns:
            None
        """
        self.controller.set_language(self.idioma.get())

    def cambiar_stt(self):
        """
        Cambia la configuración del servicio de reconocimiento de voz (STT).

        Este método recupera el valor de STT de la entrada del usuario y lo establece en el controlador.

        Returns:
            None
        """
        self.controller.set_stt(self.stt.get())

    def cambiar_llm(self):
        """
        Cambia la configuración del modelo de lenguaje grande (LLM).

        Este método recupera el valor de LLM de la entrada del usuario y lo establece en el controlador.

        Returns:
            None
        """
        self.controller.set_llm(self.llm.get())

    def cambiar_tts(self):
        """
        Cambia la configuración del servicio de texto a voz (TTS).

        Este método recupera el valor de TTS de la entrada del usuario y lo establece en el controlador.

        Returns:
            None
        """
        self.controller.set_tts(self.tts.get())

    def on_whisper_size_change(self, value):
        """
        Maneja el evento de cambio para la configuración del tamaño del modelo Whisper.

        Este método recupera el valor del tamaño del modelo Whisper de la entrada del usuario y lo establece en el controlador.

        Args:
            value (str): El nuevo tamaño del modelo Whisper seleccionado por el usuario.

        Returns:
            None
        """
        self.controller.set_whisper_size(self.whisperSize.get())

    def on_modelos_change(self, value):
        """
        Maneja el evento de cambio para la configuración de los modelos LLM.

        Este método recupera el valor de los modelos LLM de la entrada del usuario y lo establece en el controlador.

        Args:
            value (str): El nuevo modelo LLM seleccionado por el usuario.

        Returns:
            None
        """
        self.controller.set_llm_models(self.modelos.get())

    def lanzar_servidor(self):
        """
        Lanza el servidor con las configuraciones actuales y imprime el estado actual.

        Args:
            None

        Returns:
            None
        """
        self.master.destroy()
        self.controller.launch_server()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigView(root)
    root.mainloop()
