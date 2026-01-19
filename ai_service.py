import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver

class AIService:
    # load .env file
    load_dotenv()

    def __init__(self, message_id):
        self.__message_id = message_id
        self.__llm = init_chat_model(
            model = 'gemini-2.5-flash-lite',
            model_provider= 'google_genai'
        )

    def __list_directory(self, path: str = '.'):
        """ List all files and folders in directory """
        items = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            items.append({
                'name': name,
                'path': os.path.abspath(full_path),
                'type': 'directory' if os.path.isdir(full_path) else 'file',
            })

        return items

    def __read_file(self, file_path: str) -> str:
        """ Read file contents"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def __write_file(self, content: str, file_path: str) -> str:
        """ Write contents to file """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            return f'{content} written to {file_path}'

    def ask_ai(self, user_input:str):
        """ Get API response """

        system_prompt = """
        You are an helpful AI coding agent helps users create, read and edit files using natural language .

        Your Work Flow:
        1. If user mentions a file path or file name:
            - call __list_directory function to get the all folders and files.
        
        2. IF the file exists:
            - IF user ask for view the content:
                - call __read_file function to read the file content.
            
           IF user ask for add more data, modify or update the content of the file:
                - first call __read_file function to read the file content.
                - understand the data on the file.
                - then call __write_file function to add or update the file with the sample data.
        
        3. IF the file doesn't exist:
            - call __write_file function to add or update the contents of the file.
            
        4. IF user doesn't provide a specific file name: 
            - create a meaningful file name.
            
        5. If the user says "add more data" or "update it" without a file name:
            - use the most recently created or modified file as the target.
            
        6. Do not add duplicate content.
      
        Output Rules:
            - Briefly explain what has done. 
            - Always return the plain text as response. 
            - Never return python list, dictionaries or arrays.
        """

        with SqliteSaver.from_conn_string('checkpoint.db') as checkpointer:

            agent = create_agent(
                model = self.__llm,
                tools=[self.__list_directory, self.__read_file, self.__write_file],
                system_prompt=system_prompt,
                checkpointer=checkpointer,
            )

            # user_input = 'create me a persons.csv file with some person names and salaries inside'
            response = agent.invoke({'messages': [{'role': 'user', 'content': user_input}]},
                                    {'configurable': {'thread_id': self.__message_id}})

            content = response['messages'][-1].content
            return content
