import fitz  # PyMuPDF for PDF processing
import os

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

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

def load_env_variables():
    """
    Loads environment variables from a .env file.

    This function reads the .env file and sets the environment variables accordingly.
    """
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file

    # Extract variables
    GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    APIFY_API_KEY = os.getenv("APIFY_API_KEY")
    