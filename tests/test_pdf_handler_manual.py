
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from file_handlers.pdf_handler import extract_text_from_pdf

def test_extract_text_from_pdf():
    # Path to a sample PDF file (update this path as needed)
    sample_pdf = os.path.join(os.path.dirname(__file__), '../sample_resumes/sample.pdf')
    if not os.path.exists(sample_pdf):
        print(f"Sample PDF not found: {sample_pdf}")
        return
    text = extract_text_from_pdf(sample_pdf)
    print("Extracted text:\n", text)

if __name__ == "__main__":
    test_extract_text_from_pdf()
