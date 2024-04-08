import tkinter as tk
from tkinter import ttk
import subprocess
import os

def cambiar_idioma(event):
    idioma_seleccionado = idioma.get()
    print("Idioma seleccionado:", idioma_seleccionado)

def cambiar_stt():
    global stt_mode
    stt_mode = stt.get()
    print("Modo STT seleccionado:", stt_mode)
    # Habilitar o deshabilitar el desplegable extra basado en la selección de STT
    if stt_mode == "local":
        desplegable_extra.config(state="readonly")
    else:
        desplegable_extra.config(state="disabled")

def cambiar_llm():
    global llm_mode
    llm_mode = llm.get()
    print("Modo LLM seleccionado:", llm_mode)
    # Habilitar o deshabilitar el segundo desplegable basado en la selección de LLM
    if llm_mode == "local":
        desplegable_modelos.config(state="readonly")
    else:
        desplegable_modelos.config(state="disabled")

def cambiar_tts():
    global tts_mode
    tts_mode = tts.get()
    print("Modo TTS seleccionado:", tts_mode)

def imprimir_estado():
    print("Estado actual:")
    print("Idioma seleccionado:", idioma.get())
    print("Modo STT seleccionado:", stt.get())
    print("Modo LLM seleccionado:", llm.get())
    print("Modo TTS seleccionado:", tts.get())
    print("Tamaño Whisper seleccionado:", whisperSize.get())
    print("Modelo LLM seleccionado:", modelos.get())
    print("NUmero de puerto:", puerto.get())
    lanzar_servidor()
    
def lanzar_servidor():    
    ventana.destroy()
    comando = "python3.10 servidor.py"+" " + idioma.get() +" "+ stt.get()+" "+ whisperSize.get()+" "+ llm.get()+" "+ modelos.get()+" "+  tts.get()+" "+ puerto.get()
    os.system(comando)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Server config")
ventana.geometry("600x300")

# Crear el frame principal para contener todo excepto el desplegable extra
frame_config_principal = tk.Frame(ventana)
frame_config_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear una variable de control para el menú desplegable del idioma
idioma = tk.StringVar()

# Etiqueta y menú desplegable para el idioma
etiqueta_idioma = tk.Label(frame_config_principal, text="Idioma del chat:",font=("Helvetica", 10, "italic"))
etiqueta_idioma.pack(pady=(10,0))
desplegable = ttk.Combobox(frame_config_principal, textvariable=idioma, state="readonly", values=('es', 'en', 'de'))
desplegable.current(0)
desplegable.pack(pady=(0,20))
desplegable.bind("<<ComboboxSelected>>", cambiar_idioma)

# Función para configurar los botones y etiquetas
def configurar_seccion(frame, etiqueta_texto, var_control, cmd):
    etiqueta = tk.Label(frame, text=etiqueta_texto,font=("Helvetica", 10, "italic"))
    etiqueta.pack(pady=(0,5))
    frame_botones = tk.Frame(frame)
    frame_botones.pack()
    radio_local = tk.Radiobutton(frame_botones, text="Local", variable=var_control, value="local", command=cmd)
    radio_remoto = tk.Radiobutton(frame_botones, text="Remoto", variable=var_control, value="remoto", command=cmd)
    radio_local.pack(side=tk.LEFT, expand=True)
    radio_remoto.pack(side=tk.LEFT, expand=True)

# Variables globales para almacenar los modos
stt_mode, llm_mode, tts_mode = "local", "local", "local"

# Configuración de STT
stt = tk.StringVar(value="local")
configurar_seccion(frame_config_principal, "STT:", stt, cambiar_stt)

# Configuración de LLM
llm = tk.StringVar(value="local")
configurar_seccion(frame_config_principal, "LLM:", llm, cambiar_llm)

# Configuración de TTS
tts = tk.StringVar(value="local")
configurar_seccion(frame_config_principal, "TTS:", tts, cambiar_tts)

# Crear el frame y menú desplegable para "Configuración de Modelos" a la derecha
frame_config_modelos = tk.Frame(ventana, padx=20, pady=70)
frame_config_modelos.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))

whisperSize = tk.StringVar()
etiqueta_extra = tk.Label(frame_config_modelos, text="Tamaño Whisper:", font=("Helvetica", 10, "italic"))
etiqueta_extra.pack(pady=(10,0))
desplegable_extra = ttk.Combobox(frame_config_modelos, textvariable=whisperSize, state="readonly", values=('small', 'base', 'tiny'))
desplegable_extra.current(0)
desplegable_extra.pack()

# Crear un segundo desplegable para modelos de LLM solo cuando LLM esté en local
modelos = tk.StringVar()
etiqueta_modelos = tk.Label(frame_config_modelos, text="Modelo LLM:", font=("Helvetica", 10, "italic"))
etiqueta_modelos.pack(pady=(10,0))
desplegable_modelos = ttk.Combobox(frame_config_modelos, textvariable=modelos, state="readonly", values=('Gemma', 'Mistral7B' ))
desplegable_modelos.current(0)
desplegable_modelos.pack()

#Puerto
puerto = tk.StringVar()
puerto.set("5000")
etiqueta_puerto = tk.Label(frame_config_principal, text="Número de puerto:", font=("Helvetica", 10, "italic"))
etiqueta_puerto.pack(pady=(10,0))
cuadro_puerto = tk.Entry(frame_config_principal, textvariable=puerto)
cuadro_puerto.pack()

# Botón de "Play" para imprimir el estado actual
boton_play = tk.Button(ventana, text="Play", command=imprimir_estado, bg="green", font=("Helvetica", 10, "bold"))
boton_play.pack(side=tk.BOTTOM, pady=10)



# Iniciar el bucle principal de la aplicación
ventana.mainloop()

