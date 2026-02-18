import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from file_handlers.pdf_handler import extract_text_from_pdf
from analysis.keyword_analysis import analyze_keywords

class TestPDFHandler(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        sample_pdf = os.path.join(os.path.dirname(__file__), '../sample_resumes/sample.pdf')
        self.assertTrue(os.path.exists(sample_pdf), f"Sample PDF not found: {sample_pdf}")
        text = extract_text_from_pdf(sample_pdf)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 20, "Extracted text is too short.")

class TestKeywordAnalysis(unittest.TestCase):
    def test_analyze_keywords(self):
        text = "Python is great. Python and AI are the future. AI, Python, and data."
        result = analyze_keywords(text)
        self.assertIn('keywords', result)
        self.assertIn('word_count', result)
        self.assertIn('unique_words', result)
        self.assertGreater(result['word_count'], 0)
        self.assertGreater(result['unique_words'], 0)
        self.assertTrue(any(word == 'python' for word, _ in result['keywords']))

if __name__ == "__main__":
    unittest.main()
