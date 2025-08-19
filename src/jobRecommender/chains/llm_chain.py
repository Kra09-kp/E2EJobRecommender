from jobRecommender.models.llm_model import LLMJobAssistant
from jobRecommender import logger
from langchain_core.runnables import RunnableLambda
from jinja2 import Template


class JobRecommenderChain(LLMJobAssistant):
    """
    A class to handle the job recommendation chain using a language model.
    This class extends the LLMJobAssistant to create a chain that processes
    job recommendations based on a given schema and prompt.
    """

    def __init__(self):
        """
        Initializes the JobRecommenderChain.
        """
        super().__init__()
        
        self.chain = None 

    def invoke(self,prompt):
        """
        Invokes the chain with the given schema and prompt.
        Args:
            prompt (str): The prompt to be processed by the chain.
        Returns:
            The result of the chain invocation.
        """
        if self.chain is None:
            self.chain = self._get_chain()
        logger.info(f"Invoking chain with prompt: {prompt[:75]}...")  # Log the first 75 characters for brevity
        return self.chain.invoke(prompt)

    
    def _get_chain(self,schema=None,structured_output=True):
        """
        Returns the chain of the language model with a structured output.
        Args:
            schema (str): The schema to use for the structured output.
        """
        prompt = RunnableLambda(self._load_prompt)
        model = self._get_model()
        if structured_output and schema is not None:    
            model = model.with_structured_output(schema)
        template = self._get_template()
        self.chain = prompt | template | model
        logger.info("Chain created successfully.")
        return self.chain

    def _load_prompt(self, inputs):
        # print(inputs)
        file_path = inputs['file_path']
        kwargs = {k: v for k, v in inputs.items() if k != "file_path"}

        prompt = self._load_file(file_path)
        prompt = Template(prompt).render(**kwargs)
        # print(prompt)
        logger.info(f"Prompt loaded and rendered: {prompt[:75]}...")  # Log the first 75 characters for brevity
        return {"prompt": prompt}

    