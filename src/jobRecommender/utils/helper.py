import fitz  # PyMuPDF for PDF processing
import os
from jobRecommender import logger

import bleach
import json
import ast
import pandas as pd


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        

    Returns:
        str: The extracted text from the PDF.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")
    

    doc = fitz.open(stream = pdf_path.read(),
                        filetype="pdf")
    
    text = ""
    for page in doc:
        text += page.get_text() # type: ignore

    return text

def load_env_variables(key_name: str):
    """
    Loads environment variables from a .env file.

    This function reads the .env file and sets the environment variables accordingly.
    Args:
        key_name (str): The prefix for the environment variable names to be loaded. for eg: GROQ OR APIFY
    """
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file

    # Extract variables
    API_KEY = os.getenv(f"{key_name}_API_KEY")
    logger.info(f"Loaded {key_name} API key from environment variables.")
    return API_KEY




def make_data_clean(data: str):
    """
    Wrapper: detect JSON vs Python literal string,
    convert to DataFrame → clean dict list.
    """
    try:
        # Try JSON first (most common case from APIs)
        data_list = json.loads(data)
        logger.info("Parsed using JSON")
    except json.JSONDecodeError:
        # Fall back to Python literal
        data_list = ast.literal_eval(data)
        logger.info("Parsed using ast.literal_eval")

    df = pd.DataFrame(data_list)

    # Keep only useful columns (if exist)
    keep_cols = ['link', 'title', 'companyLogo', 'location', 'postedAt',
                 'descriptionHtml', 'applicantsCount']
    df = df[[col for col in keep_cols if col in df.columns]]

    return df.to_dict(orient="records")



def sanitize_html(html_text: str) -> str:
    # Allowed tags (tum apne hisaab se add/remove kar sakte ho)
    allowed_tags = [
        "p", "b", "i", "u", "em", "strong", "br", "ul", "ol", "li",
        "a", "span", "div"
    ]
    allowed_attrs = {
        "a": ["href", "title", "target"],
        "span": ["style"],
        "div": ["style"]
    }
    
    return bleach.clean(html_text, tags=allowed_tags, attributes=allowed_attrs, strip=True)
