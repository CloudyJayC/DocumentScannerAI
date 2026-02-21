"""
test_all.py — Unit Tests for DocumentScannerAI

Tests for PDF extraction, text cleaning, and validation logic.
"""

import os
import sys
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_handlers.pdf_handler import extract_text_from_pdf


class TestPDFHandler(unittest.TestCase):
    """Tests for PDF text extraction and cleaning functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_pdf = os.path.join(
            os.path.dirname(__file__), '../sample_resumes/sample.pdf'
        )

    def test_sample_pdf_exists(self):
        """Verify the sample PDF is available for testing."""
        self.assertTrue(
            os.path.exists(self.sample_pdf),
            f"Sample PDF not found: {self.sample_pdf}"
        )

    def test_extract_returns_string(self):
        """Verify extract_text_from_pdf returns a non-empty string for valid PDFs."""
        if not os.path.exists(self.sample_pdf):
            self.skipTest("Sample PDF not available.")
        
        text = extract_text_from_pdf(self.sample_pdf)
        self.assertIsInstance(text, str, "Result should be a string")
        self.assertGreater(
            len(text), 20,
            "Extracted text is too short — PDF may be image-only"
        )

    def test_extract_invalid_path_raises_error(self):
        """Verify RuntimeError is raised for non-existent PDF file."""
        with self.assertRaises(RuntimeError):
            extract_text_from_pdf("/nonexistent/path/fake.pdf")

    def test_extract_non_pdf_raises_error(self):
        """Verify RuntimeError is raised for non-PDF files."""
        # Create a temporary fake file for testing
        fake_path = os.path.join(os.path.dirname(__file__), 'fake_test_file.txt')
        with open(fake_path, 'w') as f:
            f.write("This is not a PDF file.")
        
        try:
            with self.assertRaises(RuntimeError):
                extract_text_from_pdf(fake_path)
        finally:
            # Clean up
            if os.path.exists(fake_path):
                os.remove(fake_path)

    def test_cleaned_text_no_excess_blank_lines(self):
        """Verify cleaned text doesn't have more than one consecutive blank line."""
        if not os.path.exists(self.sample_pdf):
            self.skipTest("Sample PDF not available.")
        
        text = extract_text_from_pdf(self.sample_pdf)
        # Check for triple newlines (two consecutive blank lines)
        self.assertNotIn(
            '\n\n\n', text,
            "Output should not contain excessive blank lines"
        )

    def test_cleaned_text_stripped(self):
        """Verify cleaned output is stripped of leading/trailing whitespace."""
        if not os.path.exists(self.sample_pdf):
            self.skipTest("Sample PDF not available.")
        
        text = extract_text_from_pdf(self.sample_pdf)
        self.assertEqual(
            text, text.strip(),
            "Output should be stripped of leading/trailing whitespace"
        )

    def test_text_cleaning_removes_non_printable(self):
        """Verify that non-printable characters are handled during cleaning."""
        if not os.path.exists(self.sample_pdf):
            self.skipTest("Sample PDF not available.")
        
        text = extract_text_from_pdf(self.sample_pdf)
        # Text should only contain printable ASCII characters and newlines
        for char in text:
            self.assertTrue(
                char == '\n' or (32 <= ord(char) < 127),
                f"Non-printable character found: {repr(char)}"
            )


class TestPDFValidation(unittest.TestCase):
    """Tests for PDF file validation logic."""

    def test_allowed_extensions_configuration(self):
        """Verify config contains correct allowed file extensions."""
        from config import ALLOWED_EXTENSIONS
        self.assertIsInstance(ALLOWED_EXTENSIONS, set)
        self.assertIn('.pdf', ALLOWED_EXTENSIONS)
        self.assertEqual(ALLOWED_EXTENSIONS, {'.pdf'})

    def test_pdf_extension_check(self):
        """Verify PDFs are identified by .pdf extension."""
        import os
        
        # Test various extensions
        pdf_path = "/path/to/document.pdf"
        _, ext = os.path.splitext(pdf_path)
        self.assertEqual(ext.lower(), '.pdf')
        
        non_pdf_path = "/path/to/document.txt"
        _, ext = os.path.splitext(non_pdf_path)
        self.assertNotEqual(ext.lower(), '.pdf')


class TestAIAnalysisInterface(unittest.TestCase):
    """Tests for AI analysis module interface (without Ollama)."""

    def test_analyse_resume_rejects_empty_text(self):
        """Verify analyse_resume raises ValueError for empty input."""
        from analysis.ai_analysis import analyse_resume
        
        with self.assertRaises(ValueError):
            analyse_resume("")
        
        with self.assertRaises(ValueError):
            analyse_resume("   \n\n  ")

    def test_analyse_resume_accepts_valid_text(self):
        """Verify analyse_resume accepts non-empty text (would fail at Ollama stage)."""
        from analysis.ai_analysis import analyse_resume
        
        # This should not raise ValueError, but may raise RuntimeError (Ollama not running)
        try:
            analyse_resume("Sample resume text with education and experience")
        except RuntimeError as e:
            # Expected if Ollama is not running
            self.assertIn("Ollama", str(e))
        except ValueError:
            self.fail("ValueError should not be raised for non-empty text")


if __name__ == "__main__":
    unittest.main()
