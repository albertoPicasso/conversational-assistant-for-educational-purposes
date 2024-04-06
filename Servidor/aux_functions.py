import os

class Aux_functions:

    
    ## Add new messages to session['mensajes'] whit format [role,message]
    def addMessageToChat(self, message, role, state):
        """
        Args:
        - message (str): The message to be added to the conversation.
        - role (str): The role of the participant sending the message (e.g., 'user', 'assistant', etc.).
        - chat (list): The conversation history to which the message will be added.
        - state (session): The state of this client on server
        Returns: modified state
        """
        message_entry = [role, message]
        state['mensajes'].append(message_entry)
        return state


    def printAllChat(self, state): 
        """
        Args:
        - state (session): Contains the conversation history to be printed.

        Returns:
        None
        """
        lista_mensajes = state['mensajes']
        print('Lista de mensajes ')
        for mensaje in lista_mensajes:
            print(mensaje)

    
    def createUserDirectory(self, name):
        """
        Creates a new directory/folder with the specified name.

        Args:
        - name (str): The name of the directory to be created.

        Returns:
        None
        """
        #Path to new directory / folder
        path_to_directory = os.path.join(os.getcwd(), name)

        #Create directory
        os.mkdir(path_to_directory)
        print(f"The directory'{name}' has been created successfully")
