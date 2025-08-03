from job_recommender.models.llm_model import LLMJobAssistant
from langchain_core.runnables import RunnableLambda


class JobRecommenderChain(LLMJobAssistant):
    """
    A class to handle the job recommendation chain using a language model.
    """

    def __init__(self):
        self.chain = None
    
    def invoke(self,schema,prompt):
        self.chain = self._get_chain(schema)
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

    