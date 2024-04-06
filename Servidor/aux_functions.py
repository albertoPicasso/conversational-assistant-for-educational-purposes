import os

class Aux_functions:

    
    ## Add new messages to session['mensajes'] whit format [role,message]
    def addMessageToChat(self, message:str, role:str , state):
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
        message_list = state['mensajes']
        print('Lista de mensajes ')
        for message in message_list:
            print(message)

    
    def createUserDirectory(self, name:str):
        """
        Creates a new directory/folder with the specified name.

        Args:
        - name (str): The name of the directory to be created.

        Returns:
        None
        """
        #Path to new directory / folder
        path_to_directory = os.path.join(os.getcwd(), name)
        os.mkdir(path_to_directory)
        

    def checkEndChat (self, message:str) -> bool: 
        """
        Checks if the message indicates the end of the chat based on certain levels.

        Args:
        - message (str): The message to be checked for indicating the end of the chat.

        Returns:
        - bool: True if the message contains any of the predefined levels, False otherwise.
        """
        levels = ["A1","A2","B1","B2","C1","C2"]

        for level in levels: 
            if level in message:
                return True
        
        return False 
