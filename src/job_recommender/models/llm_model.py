from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


class LLMJobAssistant:
    def __init__(self, model_name="llama3-8b-8192", temperature=0.5, max_tokens=512):
        """
        Initializes the LLMJobAssistant with specified parameters.

        Args:
            model_name (str): The name of the language model to use.
            temperature (float, optional): Controls the randomness of the model's output. 
                Lower values make the output more deterministic. Defaults to 0.5.
            max_tokens (int, optional): The maximum number of tokens to generate in the response. 
                Defaults to 512.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _get_model(self):
        """
        Returns the configured language model.

        This function initializes and returns a ChatGroq model with the specified parameters.

        Returns:
            ChatGroq: The configured language model.
        """
        if self.model_name is None:
            raise ValueError("Model name must be specified.")
        return ChatGroq(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    @staticmethod
    def _get_template():
        """
        Returns the chat template used for generating prompts.

        This function defines a chat template that includes a user message placeholder.

        Returns:
            ChatPromptTemplate: The chat prompt template.
        """
        return ChatPromptTemplate([
            ('user', '{prompt}'),
        ])
    
    @staticmethod
    def _load_file(file_path):
        """
        Loads the prompt from a file or another source.

        This function reads the prompt from a file named "prompt.txt" and returns it.

        Returns:
            str: The loaded prompt content.
        """
        content = ''
        with open(file_path, 'r') as file:
            content = file.read()
        return content