from src.job_recommender.models.llm_model import LLMJobAssistant
from langchain_core.runnables import RunnableLambda


class JobRecommenderChain(LLMJobAssistant):
    """
    A class to handle the job recommendation chain using a language model.
    This class extends the LLMJobAssistant to create a chain that processes
    job recommendations based on a given schema and prompt.
    """

    def __init__(self,schema):
        self.schema = schema
        super().__init__()
        self.chain = self._get_chain(self.schema) 

    def invoke(self,prompt):
        """
        Invokes the chain with the given schema and prompt.
        Args:
            prompt (str): The prompt to be processed by the chain.
        Returns:
            The result of the chain invocation.
        """
        
        return self.chain.invoke(prompt)

    
    def _get_chain(self,schema):
        """
        Returns the chain of the language model with a structured output.
        Args:
            schema (str): The schema to use for the structured output.
        """
        prompt = RunnableLambda(self._load_prompt)
        model = self._get_model()
        structured_model = model.with_structured_output(schema)
        template = self._get_template()
        self.chain = prompt | template | structured_model
        return self.chain

    def _load_prompt(self, inputs):
        file_path = inputs['file_path']
        kwargs = {k: v for k, v in inputs.items() if k != "file_path"}

        prompt = self._load_file(file_path)
        prompt = prompt.format(**kwargs)
        return {"prompt": prompt}

    