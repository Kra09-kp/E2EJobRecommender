import os
from langchain.schema.runnable import RunnableParallel
from langchain_core.runnables import RunnableLambda
from src.jobRecommender.chains.llm_chain import JobRecommenderChain
from src.jobRecommender.schema.output_schema import *
from src.jobRecommender import logger


class AskLLM(JobRecommenderChain):
    def __init__(self,):
        """
        Initialize the AskLLM class with the LLM chain.
        This class is responsible for handling the parallel chains for suggestions, keywords, skill gaps, project ideas, and improvement areas.
        """
        self.llm_chain = JobRecommenderChain()
        self.setup_chains()


    def get_suggestion(self,resume_text):
        """
        Get suggestions based on the resume text.
        """
        # resume_text = input_data.resume_text
        folder_path = "prompts/"

        self.final_chain()
        logger.info("Running chain for suggestions.")
        return self.suggestions_chain.invoke({
            "folder_path": folder_path,
            "resume": resume_text
        })

    def get_keywords(self,input_data):
        """
        Get keywords from the resume text.
        """
        resume_text = input_data.resume_text
        folder_path = "prompts/"
        file_path = "keyword_prompt.txt"
        self.keywords_chain = self.llm_chain._get_chain(Keywords)
        logger.info("Running chain for keywords.")
        return self.keywords_chain.invoke({
            "file_path": self.create_path(folder_path, file_path),
            "resume_text": resume_text
        })  # type: ignore

    def final_chain(self):
        """
        Final chain that runs all the parallel chains and returns the results.
        """

        skill_gap_chain = RunnableLambda(
            lambda x: self.find_skill_gap_chain.invoke({
                "file_path": self.create_path(self._safe_dict_access(x, 'folder_path'), "finding_skill_gap_prompt.txt"),
                "resume_text": self._safe_dict_access(x,"resume")
            }).content # type: ignore
        )

        projects_idea_chain = RunnableLambda(
            lambda x: self.project_idea_chain.invoke({
                "file_path": self.create_path(self._safe_dict_access(x, 'folder_path'), "project_ideas_prompt.txt"),
                "resume_text": self._safe_dict_access(x,"resume")
            }).content # type: ignore
        )

        improvements_areas_chain = RunnableLambda(
            lambda x: self.improvement_areas_chain.invoke({
                "file_path": self.create_path(self._safe_dict_access(x, 'folder_path'), "wycd_prompt.txt"),
                "resume_text": self._safe_dict_access(x,"resume")
            }).content # type: ignore
        )
        self.suggestions_chain = RunnableParallel({
            "find_skill_gap": skill_gap_chain,
            "project_ideas": projects_idea_chain,
            "improvement_areas": improvements_areas_chain
        })

        

    def setup_chains(self):
        self.find_skill_gap_chain = self.llm_chain._get_chain()
        self.project_idea_chain = self.llm_chain._get_chain()
        self.improvement_areas_chain = self.llm_chain._get_chain()  
        self.keywords_chain = self.llm_chain._get_chain()
       
    def create_path(self, folder_path, file_name):
        """   
            Creates a path for the file in the given folder.
        """
        return os.path.join(folder_path, file_name)

    def _safe_dict_access(self, x, key):
        if not isinstance(x, dict):
            logger.error(f"Input to chain must be a dict, got {type(x)}")
            raise TypeError(f"Input to chain must be a dict, got {type(x)}")
        return x[key]
