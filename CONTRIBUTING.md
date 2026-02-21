# Contributing to DocumentScannerAI

First off, thanks for taking the time to contribute! 🎉

This document provides guidelines and instructions for contributing to the DocumentScannerAI project.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating a bug report, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details:**
  - Python version
  - OS and version
  - Ollama version
  - PyQt6 version

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python style guide (PEP 8)
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## Development Setup

### 1. Fork & Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/your-username/DocumentScannerAI.git
cd DocumentScannerAI
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-dark-mode` for new features
- `bugfix/fix-pdf-parsing` for bug fixes
- `docs/update-readme` for documentation

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest pytest-cov black flake8
```

### 4. Make Your Changes

- Write clean, readable code
- Add comments for complex logic
- Follow existing code style
- Update docstrings

### 5. Test Your Changes

```bash
# Run existing tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_full_pipeline.py -v

# Check code style
flake8 *.py analysis/ file_handlers/ tests/

# Format code with Black
black *.py analysis/ file_handlers/ tests/
```

### 6. Update Documentation

- Update [README.md](README.md) if adding features
- Update docstrings in your code
- Add comments for non-obvious logic

### 7. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"
```

**Commit message guidelines:**
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### 8. Push & Create Pull Request

```bash
git push origin feature/your-feature-name
```

Open a pull request on GitHub with:
- Clear title describing the changes
- Description of what changed and why
- Link to related issues (if any)
- Screenshots/videos for UI changes

## Style Guide

### Python Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```python
# Good
def analyze_resume(pdf_path: str) -> dict:
    """Analyze a resume PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary with analysis results
    """
    result = extract_and_analyze(pdf_path)
    return result

# Bad
def analyze_resume(path):
    result=extract_and_analyze(path)
    return result
```

### Documentation

- Use clear docstrings for all functions and classes
- Include type hints
- Add comments for complex logic
- Keep README updated

### Naming Conventions

```python
# Classes: PascalCase
class PDFAnalyzer:
    pass

# Functions/variables: snake_case
def extract_text_from_pdf():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 10_000_000
```

## Testing Guidelines

### Writing Tests

- Create test files in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Keep tests independent

```python
def test_pdf_validation_passes_for_valid_file(self):
    """Test that valid PDFs pass validation."""
    result = validate_pdf('sample_resumes/sample.pdf')
    self.assertTrue(result)

def test_pdf_validation_fails_for_invalid_file(self):
    """Test that invalid PDFs fail validation."""
    result = validate_pdf('fake.pdf')
    self.assertFalse(result)
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.

# Run specific test
python -m pytest tests/test_full_pipeline.py::test_pipeline
```

## File Structure

When adding new features, maintain the existing structure:

```
├── analysis/          # AI/LLM related modules
├── file_handlers/     # File I/O and processing
├── tests/             # Test files
│   ├── test_*.py      # Test files matching modules
├── config.py          # Configuration
└── gui_main.py        # GUI entry point
```

## Documentation

### README Updates

If your contribution affects user-facing functionality, update the README:

1. Features section (if adding new features)
2. Configuration section (if adding config options)
3. Usage section (if changing how users interact)

### Docstrings

All public functions should have docstrings:

```python
def validate_pdf(file_path: str) -> bool:
    """Validate that a file is a genuine PDF.
    
    Performs dual-layer validation:
    1. Extension check (.pdf only)
    2. Magic number verification (%PDF- header)
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if file is a valid PDF, False otherwise
        
    Raises:
        FileNotFoundError: If file does not exist
    """
    pass
```

## Submitting a Pull Request

1. **Title**: Clear, concise description of changes
2. **Description**: Explain what changed and why
3. **Type**: Mark as bug fix, new feature, or enhancement
4. **Related Issues**: Link to #issue-number
5. **Checklist**:
   - [ ] Code follows style guidelines
   - [ ] All tests pass
   - [ ] New tests added for new functionality
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)

## Questions?

Feel free to:
- Open an issue for discussion
- Start a discussion on GitHub
- Contact the maintainers

## Recognition

Contributors are recognized in:
- README.md as community contributors
- GitHub's contributors page
- Release notes for significant contributions

---

Thank you for contributing to DocumentScannerAI! 🎉
