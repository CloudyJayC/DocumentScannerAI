"""
pdf_handler.py — PDF Text Extraction and Cleaning

Provides robust text extraction from PDF files with intelligent cleaning
optimized for resume documents. Handles hyphenated line breaks, removes
junk lines, identifies section headers, and formats output for analysis.

Uses pdfplumber for reliable text extraction with custom tolerances.
"""

import re
import pdfplumber


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
    try:
        raw_pages = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Use custom tolerances for reliable text extraction
                # x_tolerance: allows slight horizontal spacing variations
                # y_tolerance: allows slight vertical spacing variations
                page_text = page.extract_text(x_tolerance=2, y_tolerance=3)
                if page_text:
                    raw_pages.append(page_text)

        if not raw_pages:
            return ""  # Likely an image-only PDF

        raw_text = "\n".join(raw_pages)
        return _clean_text(raw_text)

    except Exception as e:
        raise RuntimeError(f"Failed to read PDF: {e}") from e


def _clean_text(text: str) -> str:
    """Apply intelligent cleaning rules to raw PDF text.
    
    Performs multiple passes to clean and normalize the text:
    1. Remove non-printable characters and unicode garbage
    2. Fix hyphenated line breaks (word-\\nbreak → wordbreak)
    3. Collapse multiple spaces/tabs per line
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

    # PASS 2: Fix hyphenated line breaks from PDF column layout
    # Example: "Computer-\nScience" becomes "ComputerScience"
    text = re.sub(r'-\n(\S)', r'\1', text)

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

    # PASS 5: Add blank line before detected section headers
    # This makes the document structure clearer for both reading and AI analysis
    # Extended keywords for different resume styles and structures
    common_headers = {
        # Education
        "education", "academic", "qualifications", "degree", "credentials",
        # Experience/Work
        "experience", "employment", "work experience", "career history", "professional experience",
        "positions held", "work history", "job history", "professional background",
        # Skills
        "skills", "technical skills", "core competencies", "competencies", "expertise",
        "proficiencies", "abilities", "capabilities", "areas of expertise",
        # Summary
        "summary", "professional summary", "executive summary", "profile", "objective",
        "career objective", "professional objective", "about", "about me",
        # Certifications/Training
        "certifications", "certification", "certified", "licenses", "license", "training",
        "professional development", "courses", "accreditations",
        # Projects
        "projects", "portfolio", "key projects", "notable projects",
        # Additional
        "awards", "honors", "recognition", "achievements", "accomplishments",
        "languages", "language", "volunteer", "volunteering", "volunteer work",
        "publications", "references", "contact", "contact information", "details",
        "interests", "additional", "activities", "involvement", "leadership",
        "technical expertise", "knowledge", "tools", "technologies", "technical proficiencies",
    }
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
                lower_clean in common_headers or
                lower in common_headers
            )
        )
        # Add spacing before header to separate sections
        if is_header and i > 0 and spaced and spaced[-1] != "":
            spaced.append("")  # Insert blank line before section
        spaced.append(line)

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

    return "\n".join(final).strip()
