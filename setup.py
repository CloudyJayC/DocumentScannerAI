"""
Setup configuration for DocumentScannerAI
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DocumentScannerAI",
    version="1.1.0",
    author="Jason Cameron",
    description="AI-powered PDF scanner and resume analyzer with local LLM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CloudyJayC/DocumentScannerAI",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyQt6==6.6.1",
        "pdfplumber==0.10.3",
        "requests==2.31.0",
        "fpdf2==2.7.9",
    ],
    entry_points={
        "console_scripts": [
            "document-scanner=gui_main:main",
        ],
    },
)
