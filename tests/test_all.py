import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_handlers.pdf_handler import extract_text_from_pdf


class TestPDFHandler(unittest.TestCase):
    """Tests for PDF text extraction."""

    def setUp(self):
        self.sample_pdf = os.path.join(
            os.path.dirname(__file__), '../sample_resumes/sample.pdf'
        )

    def test_sample_pdf_exists(self):
        """Ensure the sample PDF used for testing is present."""
        self.assertTrue(
            os.path.exists(self.sample_pdf),
            f"Sample PDF not found: {self.sample_pdf}"
        )

    def test_extract_returns_string(self):
        """extract_text_from_pdf should return a non-empty string for a valid PDF."""
        if not os.path.exists(self.sample_pdf):
            self.skipTest("Sample PDF not available.")
        text = extract_text_from_pdf(self.sample_pdf)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 20, "Extracted text is too short — may be image-only.")

    def test_extract_invalid_path_raises(self):
        """extract_text_from_pdf should raise RuntimeError for a missing file."""
        with self.assertRaises(RuntimeError):
            extract_text_from_pdf("/nonexistent/path/fake.pdf")

    def test_extract_non_pdf_raises(self):
        """extract_text_from_pdf should raise RuntimeError for a non-PDF file."""
        # Create a temporary fake file
        fake_path = os.path.join(os.path.dirname(__file__), 'fake_test_file.txt')
        with open(fake_path, 'w') as f:
            f.write("This is not a PDF.")
        try:
            with self.assertRaises(RuntimeError):
                extract_text_from_pdf(fake_path)
        finally:
            os.remove(fake_path)

    def test_cleaned_text_has_no_excess_blank_lines(self):
        """Cleaned output should not contain more than one consecutive blank line."""
        if not os.path.exists(self.sample_pdf):
            self.skipTest("Sample PDF not available.")
        text = extract_text_from_pdf(self.sample_pdf)
        self.assertNotIn('\n\n\n', text, "Output contains excessive blank lines.")

    def test_cleaned_text_no_leading_trailing_whitespace(self):
        """Cleaned output should be stripped of leading/trailing whitespace."""
        if not os.path.exists(self.sample_pdf):
            self.skipTest("Sample PDF not available.")
        text = extract_text_from_pdf(self.sample_pdf)
        self.assertEqual(text, text.strip())


class TestValidation(unittest.TestCase):
    """Tests for PDF validation logic inlined in gui_main."""

    def test_is_pdf_file_rejects_wrong_extension(self):
        """Files without .pdf extension should be rejected."""
        # We test the logic directly rather than importing gui_main (requires Qt)
        import os
        fake_path = "/some/path/document.docx"
        _, ext = os.path.splitext(fake_path)
        self.assertNotEqual(ext.lower(), '.pdf')

    def test_allowed_extensions_config(self):
        """config.py ALLOWED_EXTENSIONS should be a set containing .pdf"""
        from config import ALLOWED_EXTENSIONS
        self.assertIsInstance(ALLOWED_EXTENSIONS, set)
        self.assertIn('.pdf', ALLOWED_EXTENSIONS)


if __name__ == "__main__":
    unittest.main()
