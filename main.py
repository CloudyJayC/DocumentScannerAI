
# -----------------------------
# DocumentScannerAI Main Script
# -----------------------------
# This script validates, scans, and analyzes PDF files for keywords, entities, and security issues.

import os
from colorama import Fore, Style, init as colorama_init
from security.validation import is_pdf_file, scan_pdf_for_malicious_content
from file_handlers.pdf_handler import extract_text_from_pdf
from analysis.keyword_analysis import analyze_keywords
from analysis.ai_analysis import ai_analyze_text

from security.error_handling import log_error, log_warning, log_info, handle_exception
from reports.report_generator import generate_text_report

colorama_init(autoreset=True)

def get_pdf_path():
    """Prompt user for PDF file path."""
    print(Fore.CYAN + Style.BRIGHT + "Welcome to DocumentScannerAI!")
    file_path = input(Fore.YELLOW + "Enter the path to your PDF file: ").strip()
    return file_path

def validate_and_scan(file_path):
    """Validate file existence, type, and scan for suspicious PDF elements."""
    try:
        if not os.path.isfile(file_path):
            log_error(f"File not found: {file_path}")
            return False
        if not is_pdf_file(file_path):
            log_warning(f"Invalid PDF: {file_path}")
            return False
        print(Fore.BLUE + "Scanning PDF for suspicious elements...")
        suspicious = scan_pdf_for_malicious_content(file_path)
        if any(count > 0 for count in suspicious.values()):
            log_warning(f"Suspicious elements found in {file_path}: {suspicious}")
            print(Fore.RED + Style.BRIGHT + "Warning: Suspicious PDF Elements Detected:")
            for element, count in suspicious.items():
                if count > 0:
                    print(Fore.RED + f"  {element}: {count}")
            print()
        else:
            log_info(f"File is clean: {file_path}")
            print(Fore.GREEN + "No suspicious elements found. File is clean.\n")
        return True
    except Exception as e:
        handle_exception(e, context="validate_and_scan")
        return False

def extract_and_analyze(file_path, suspicious=None):
    """Extract text from PDF, perform keyword and AI analysis, display and save results."""
    try:
        print(Fore.BLUE + "PDF validated. Extracting text...")
        text = extract_text_from_pdf(file_path)
        if not text:
            log_error(f"No text extracted from: {file_path}")
            print(Fore.RED + "No text could be extracted from the PDF.")
            return
        print(Fore.CYAN + "Text extracted. (First 500 characters):\n")
        print(text[:500])

        # --- Keyword Analysis ---
        analysis_results = analyze_keywords(text)
        print(Fore.MAGENTA + Style.BRIGHT + "\nKeyword Analysis Results:")
        print(f"{Fore.YELLOW}Word count: {analysis_results['word_count']}")
        print(f"{Fore.YELLOW}Unique words: {analysis_results['unique_words']}")
        print(Fore.YELLOW + "Top keywords:")
        for word, freq in analysis_results['keywords']:
            print(f"  {word}: {freq}")
        log_info(f"Keyword analysis complete for: {file_path}")

        # --- AI-powered Entity Analysis ---
        ai_results = ai_analyze_text(text)
        if 'error' in ai_results:
            log_error(f"AI analysis error for {file_path}: {ai_results['error']}")
            print(Fore.RED + f"\nAI Analysis Error: {ai_results['error']}")
        else:
            log_info(f"AI analysis complete for: {file_path}")
            print(Fore.GREEN + Style.BRIGHT + "\nAI-Powered Analysis (spaCy):")
            print(Fore.CYAN + "Summary:")
            print(ai_results['summary'])
            print(Fore.CYAN + "\nNamed Entities:")
            for ent, label in ai_results['entities']:
                print(f"  {ent} ({label})")

        # --- Report Generation ---
        if suspicious is not None:
            report_path = generate_text_report(file_path, suspicious, analysis_results, ai_results)
            print(Fore.GREEN + f"\nReport saved to: {report_path}")
        else:
            print(Fore.YELLOW + "\nReport not generated: suspicious scan data missing.")
    except Exception as e:
        handle_exception(e, context="extract_and_analyze")

def main():
    """Main entry point: orchestrates validation, scanning, analysis, and report generation."""
    file_path = get_pdf_path()
    suspicious = None
    if validate_and_scan(file_path):
        suspicious = scan_pdf_for_malicious_content(file_path)
        extract_and_analyze(file_path, suspicious=suspicious)

if __name__ == "__main__":
    main()
