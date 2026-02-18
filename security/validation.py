

# Validation and security checks for PDF files
import os
from config import ALLOWED_EXTENSIONS
from security.utils.pdfid_stub import scan_pdf


def is_pdf_file(file_path):
	"""
	Checks if the file is a PDF by extension and by file signature (magic number).
	Returns True if valid PDF, False otherwise.
	"""
	_, ext = os.path.splitext(file_path)
	if ext.lower() not in ALLOWED_EXTENSIONS:
		return False
	try:
		with open(file_path, 'rb') as f:
			header = f.read(5)
			if header == b'%PDF-':
				return True
	except Exception as e:
		print(f"Validation error: {e}")
	return False


def scan_pdf_for_malicious_content(file_path):
	"""
	Scan the PDF for suspicious elements using pdfid (stub).
	Returns a dict of suspicious element counts (e.g., JavaScript, embedded files).
	"""
	return scan_pdf(file_path)
