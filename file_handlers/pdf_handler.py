"""
pdf_handler.py — PDF Text Extraction and Cleaning

Extracts and cleans text from PDF files, optimized for resumes.
Handles hyphenated line breaks, removes junk lines, detects section headers,
and normalizes whitespace. Uses pdfplumber with custom tolerances.
"""

import re
import pdfplumber

from config import PDF_X_TOLERANCE, PDF_Y_TOLERANCE, RESUME_SECTION_HEADERS
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """Extract and clean text from a PDF file.
    
    Uses pdfplumber for reliable text extraction with custom tolerances,
    then applies resume-specific cleaning: fixing line breaks, removing junk,
    detecting section headers, and formatting for readability.
    
    Args:
        file_path: Path to the PDF file to extract text from
    
    Returns:
        Cleaned, formatted text string. Empty string if PDF is image-only.
    
    Raises:
        RuntimeError: If file cannot be read or pdfplumber fails
    """
    logger.info(f"Extracting text from PDF: {file_path}")
    
    try:
        raw_pages = []
        with pdfplumber.open(file_path) as pdf:
            logger.debug(f"PDF has {len(pdf.pages)} pages")
            for i, page in enumerate(pdf.pages):
                # Use custom tolerances for reliable text extraction
                # x_tolerance: allows slight horizontal spacing variations
                # y_tolerance: allows slight vertical spacing variations
                page_text = page.extract_text(
                    x_tolerance=PDF_X_TOLERANCE, 
                    y_tolerance=PDF_Y_TOLERANCE
                )
                if page_text:
                    raw_pages.append(page_text)
                    logger.debug(f"Extracted {len(page_text)} chars from page {i+1}")

        if not raw_pages:
            logger.warning(f"No text extracted from PDF (likely image-only): {file_path}")
            return ""  # Likely an image-only PDF

        raw_text = "\n".join(raw_pages)
        logger.info(f"Extracted {len(raw_text)} chars from {len(raw_pages)} pages")
        
        cleaned_text = _clean_text(raw_text)
        logger.info(f"Cleaned text: {len(cleaned_text)} chars")
        return cleaned_text

    except Exception as e:
        logger.error(f"Failed to extract text from PDF {file_path}: {e}", exc_info=True)
        raise RuntimeError(f"Failed to read PDF: {e}") from e


def _clean_text(text: str) -> str:
    """Apply intelligent cleaning rules to raw PDF text.
    
    Performs multiple passes to clean and normalize the text:
    logger.debug("Starting text cleaning process")
    
    # PASS 1: Remove non-printable characters and unicode trash
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
    logger.debug("Pass 1 complete: removed non-printable characters"
    4. Remove junk lines (symbols, page numbers, single chars)
    5. Add spacing before section headers for structure
    6. Remove excessive blank lines (max one consecutive)
    
    Args:
        text: Raw text extracted from PDF
    
    Returns:
        Cleaned, well-formatted text suitable for display and analysis
    """
    # PASS 1: Remove non-printable characters and unicode trash
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)

    logger.debug("Pass 2 complete: fixed hyphenated line breaks")

    # PASS 3: Normalize spacing — collapse tabs and multiple spaces
    lines = text.split("\n")
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]
    logger.debug(f"Pass 3 complete: normalized spacing on {len(lines)} lines")
    # PASS 3: Normalize spacing — collapse tabs and multiple spaces
    lines = text.split("\n")
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]

    # PASS 4: Filter out junk lines that don't contain real content
    # Remove: pure symbols, page numbers, single characters, empty lines
    cleaned = []
    for line in lines:
        if not line:
            cleaned.append("")  # Preserve intentional blank lines
            continue
        # Skip lines that are only symbols/numbers/whitespace
        if re.fullmatch(r'[\W\d\s]+', line):
            continue
        # Skip very short junk (single letters only, but allow 2-letter things like skills)
        if len(line) == 1:
            continue
        cleaned.append(line)
    
    logger.debug(f"Pass 4 complete: filtered {len(lines) - len(cleaned)} junk lines")

    # PASS 5: Add blank line before detected section headers
    # This makes the document structure clearer for both reading and AI analysis
    # Keywords from config.py
    spaced = []
    for i, line in enumerate(cleaned):
        lower = line.lower().strip()
        # Remove trailing punctuation for comparison
        lower_clean = lower.rstrip(':-•–—').rstrip()
        
        # Detect headers: short lines, all caps, title case, or in our keyword list
        is_header = (
            len(line) < 60  # Reasonable header length
            and not line.endswith(('.', ',', ';'))  # Not a sentence ending
            and (
                line.isupper() or 
                line.istitle() or 
                lower_clean in RESUME_SECTION_HEADERS or
                lower in RESUME_SECTION_HEADERS
            )
        )
        # Add spacing before header to separate sections
        if is_header and i > 0 and spaced and spaced[-1] != "":
            spaced.append("")  # Insert blank line before section
        spaced.append(line)
    
    logger.debug(f"Pass 5 complete: added section spacing")

    # PASS 6: Collapse excessive blank lines (limit to 1 consecutive)
    # This prevents empty space from bloating the output
    final = []
    blank_count = 0
    for line in spaced:
        if line == "":
            blank_count += 1
            if blank_count <= 1:  # Allow max one blank line
                final.append(line)
        else:
            blank_count = 0
            final.append(line)

    result = "\n".join(final).strip()
    logger.debug(f"Pass 6 complete: collapsed blank lines, final length {len(result)} chars")
    return result