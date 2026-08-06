import PyPDF2
from io import BytesIO

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a given PDF byte array.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n"
        return extracted_text.strip()
    except Exception as e:
        return ""
