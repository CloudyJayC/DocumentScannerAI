# PDF file handling and text extraction
# Uses pdfplumber to extract text from all pages of a PDF file.
import pdfplumber

def extract_text_from_pdf(file_path):
    """
    Extracts and returns all text from a PDF file as a string.
    Returns an empty string if extraction fails.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
            return text.strip()
    except Exception as e:
        print(f"Error reading PDF file {file_path}: {e}")
        return ""
