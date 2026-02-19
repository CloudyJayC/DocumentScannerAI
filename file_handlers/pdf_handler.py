# file_handlers/pdf_handler.py
# PDF text extraction with cleaning optimised for resume documents.

import re
import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and returns cleaned text from a PDF file.
    Raises RuntimeError if the file cannot be read.
    Returns an empty string only if the PDF is genuinely empty/image-only.
    """
    try:
        raw_pages = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text(x_tolerance=2, y_tolerance=3)
                if page_text:
                    raw_pages.append(page_text)

        if not raw_pages:
            return ""

        raw_text = "\n".join(raw_pages)
        return _clean_text(raw_text)

    except Exception as e:
        raise RuntimeError(f"Failed to read PDF: {e}") from e


def _clean_text(text: str) -> str:
    """
    Cleans raw PDF text into readable format suitable for display and AI analysis.
    """
    # Remove non-printable characters
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    # Re-join hyphenated line breaks (e.g. "experi-\nence" -> "experience")
    text = re.sub(r'-\n(\S)', r'\1', text)

    # Collapse tabs and multiple spaces per line
    lines = text.split("\n")
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]

    # Remove junk lines (symbols only, single chars, bare page numbers)
    cleaned = []
    for line in lines:
        if not line:
            cleaned.append("")
            continue
        if re.fullmatch(r'[\W\d\s]+', line):
            continue
        if len(line) <= 2:
            continue
        cleaned.append(line)

    # Add blank line above detected section headers
    common_headers = {
        "education", "experience", "skills", "summary", "objective",
        "certifications", "projects", "awards", "languages", "interests",
        "references", "profile", "work experience", "professional experience",
        "technical skills", "achievements", "publications", "volunteering",
        "contact", "about", "career objective", "professional summary",
    }
    spaced = []
    for i, line in enumerate(cleaned):
        lower = line.lower().strip()
        is_header = (
            len(line) < 50
            and not line.endswith(('.', ',', ';', ':'))
            and (line.isupper() or line.istitle() or lower in common_headers)
        )
        if is_header and i > 0 and spaced and spaced[-1] != "":
            spaced.append("")
        spaced.append(line)

    # Collapse more than 1 consecutive blank line
    final = []
    blank_count = 0
    for line in spaced:
        if line == "":
            blank_count += 1
            if blank_count <= 1:
                final.append(line)
        else:
            blank_count = 0
            final.append(line)

    return "\n".join(final).strip()
