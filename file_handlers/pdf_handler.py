# file_handlers/pdf_handler.py
# PDF text extraction with cleaning for resume documents.

import re
import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and returns cleaned text from a PDF file.
    Applies resume-specific cleaning to produce readable output.
    Returns an empty string if extraction fails.
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
        print(f"Error reading PDF file {file_path}: {e}")
        return ""


def _clean_text(text: str) -> str:
    """
    Cleans raw PDF text into a readable format suitable for display and AI analysis.

    Steps:
      1. Normalize unicode and remove non-printable characters
      2. Fix words broken across lines by a hyphen (re-join them)
      3. Collapse runs of whitespace/tabs on a single line into one space
      4. Remove lines that are pure junk (single characters, only symbols, page numbers)
      5. Detect likely section headers and ensure they stand out with a blank line above
      6. Collapse more than two consecutive blank lines into one
      7. Strip leading/trailing whitespace
    """

    # 1. Remove non-printable / non-ASCII junk characters, keep standard punctuation
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    # 2. Re-join hyphenated line breaks (e.g. "experi-\nence" → "experience")
    text = re.sub(r'-\n(\S)', r'\1', text)

    # 3. Collapse horizontal whitespace (tabs, multiple spaces) on each line
    lines = text.split("\n")
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]

    # 4. Remove junk lines
    cleaned_lines = []
    for line in lines:
        # Skip empty lines at this stage (we'll re-add controlled spacing later)
        if not line:
            cleaned_lines.append("")
            continue
        # Skip lines that are only symbols/numbers with no real words
        if re.fullmatch(r'[\W\d\s]+', line):
            continue
        # Skip very short lines that are likely artifacts (single chars, page numbers)
        if len(line) <= 2:
            continue
        cleaned_lines.append(line)

    # 5. Detect section headers and add a blank line above them for readability.
    # A header is a short line (under 50 chars) that is either ALL CAPS or Title Case
    # and doesn't end with a sentence-ending punctuation mark.
    common_headers = {
        "education", "experience", "skills", "summary", "objective",
        "certifications", "projects", "awards", "languages", "interests",
        "references", "profile", "work experience", "professional experience",
        "technical skills", "achievements", "publications", "volunteering",
        "contact", "about", "career objective", "professional summary",
    }

    spaced_lines = []
    for i, line in enumerate(cleaned_lines):
        lower = line.lower().strip()
        is_header = (
            len(line) < 50
            and not line.endswith(('.', ',', ';', ':'))
            and (
                line.isupper()
                or line.istitle()
                or lower in common_headers
            )
        )
        # Add a blank line before headers (but not before the very first line)
        if is_header and i > 0 and spaced_lines and spaced_lines[-1] != "":
            spaced_lines.append("")
        spaced_lines.append(line)

    # 6. Collapse more than 2 consecutive blank lines into 1
    final_lines = []
    blank_count = 0
    for line in spaced_lines:
        if line == "":
            blank_count += 1
            if blank_count <= 1:
                final_lines.append(line)
        else:
            blank_count = 0
            final_lines.append(line)

    return "\n".join(final_lines).strip()