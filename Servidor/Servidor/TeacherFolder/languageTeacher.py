from .teacherInterface import TeacherInterface

## Implementación de LlmInterface usando la API de OpenAI

class LanguageTeacher(TeacherInterface):
    def __init__(self, lang):
        """
        Inicializa el objeto LanguageTeacher con el idioma especificado.

        Args:
            lang (str): El idioma en el que se realizará la evaluación.
        """
        self.lang = lang

    def checkEndChat(self, message: str) -> bool:
        """
        Verifica si el mensaje indica el fin del chat basado en ciertos niveles.

        Args:
            message (str): El mensaje a verificar para determinar si indica el fin del chat.

        Returns:
            bool: True si el mensaje contiene alguno de los niveles predefinidos, False en caso contrario.
        """
        levels = ["A1", "A2", "B1", "B2", "C1", "C2", "[END]"]
        for level in levels:
            if level in message:
                return True
        return False

    def evaluation(self, message_list, last_message, LLM):
        """
        Evalúa un chat basado en los niveles de competencia lingüística del MCER y genera una respuesta utilizando un modelo de lenguaje.

        Este método procesa una lista de mensajes, añadiendo un mensaje generado por el sistema para guiar una evaluación
        de la conversación según criterios específicos: coherencia, variedad de vocabulario y precisión gramatical.
        La respuesta se ajusta en función de la configuración del idioma y luego se procesa mediante el modelo de lenguaje (LLM).

        Args:
            message_list (List[List[str]]): La lista de mensajes previos en el chat.
            last_message (str): El mensaje más reciente.
            LLM (Any): El modelo de aprendizaje de lenguaje utilizado para procesar el chat.

        Returns:
            str: La respuesta generada por el modelo de lenguaje tras evaluar la conversación.
        """
        chat = []
        # Crear el mensaje del sistema
        keyString = (
            "Evaluate the following transcribed conversation from a speaking test according to the "
            "Common European Framework of Reference (CEFR) language proficiency levels. Focus on the following aspects, "
            "which are assessable from a written transcript: "
            "1. Coherence: Assess how logically ideas are connected and if the conversation flows logically from one point to another. "
            "2. Range of Vocabulary: Evaluate the variety and appropriateness of the vocabulary used. "
            #"3. Grammatical Accuracy: Determine the correctness of the grammar used throughout the conversation. "
            "Please provide an assessment considering these aspects and indicate the approximate CEFR level (A1, A2, B1, B2, C1, C2) "
            "And how to improve it. "
            "Don't forget to indicate the approximate CEFR level."
            "Keep in mind that this is a transcription so there may be minor errors in gender and number, as well as with similar sounding words. "
            "be short please"
        )

        if self.lang == "es":
            language = " Please answer in Spanish."
        elif self.lang == "en":
            language = " Please answer in English."
        elif self.lang == "de":
            language = " Please answer in German."

        systemMessage = keyString + language

        # Crear la nueva lista de mensajes
        chat.append(["system", systemMessage])

        # Añadir todos los nuevos mensajes excepto el mensaje del sistema
        for message_to_append in message_list[1:]:
            chat.append(message_to_append)

        # Pedir al LLM (local si el servidor está en modo LLM local o remoto si el servidor está en modo LLM remoto)
        # Utiliza la misma clase que el servidor, por lo que tiene una configuración y comportamiento idénticos
        
        last_message = LLM.request_to_llm(chat, 0.3)

        return last_message
