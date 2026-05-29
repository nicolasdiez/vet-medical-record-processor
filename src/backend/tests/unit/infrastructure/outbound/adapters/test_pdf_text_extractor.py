import os

import pytest

from app.infrastructure.outbound.pdf_text_extractor import (
    PDFFileTextExtractorAdapter,
)

# Resolve the absolute path to the fixtures directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../../fixtures"))

@pytest.fixture
def extractor() -> PDFFileTextExtractorAdapter:
    """
    Fixture to instantiate the adapter before each test.
    """
    return PDFFileTextExtractorAdapter()

@pytest.mark.asyncio
async def test_extract_text_from_real_pdf(extractor: PDFFileTextExtractorAdapter):
    """
    Tests that the adapter can successfully read and extract text 
    from a real clinical PDF file.
    """
    pdf_path = os.path.join(FIXTURES_DIR, "clinical_history_1.pdf")
    
    # Ensure the file exists before testing
    assert os.path.exists(pdf_path), f"Please place a test PDF at {pdf_path}"
    
    with open(pdf_path, "rb") as f:
        file_content = f.read()
        
    filename = "clinical_history_1.pdf"
    
    # Execute the method under test
    extracted_text = await extractor.extract_text(file_content, filename)
    
    # Assertions
    assert isinstance(extracted_text, str)
    assert len(extracted_text) > 0

@pytest.mark.asyncio
async def test_extract_text_rejects_non_pdf_extension(extractor: PDFFileTextExtractorAdapter):
    """
    Tests the fail-fast validation for unsupported file extensions.
    """
    file_content = b"fake image bytes"
    filename = "image.png"
    
    with pytest.raises(ValueError) as exc_info:
        await extractor.extract_text(file_content, filename)
        
    assert "Unsupported file type" in str(exc_info.value)
    assert "Expected PDF" in str(exc_info.value)

@pytest.mark.asyncio
async def test_extract_text_handles_corrupted_pdf(extractor: PDFFileTextExtractorAdapter):
    """
    Tests that the adapter raises a RuntimeError when PyMuPDF fails to parse 
    invalid or corrupted binary data mimicking a PDF.
    """
    corrupted_content = b"%PDF-1.4\n%Fake corrupted content"
    filename = "corrupted.pdf"
    
    with pytest.raises(RuntimeError) as exc_info:
        await extractor.extract_text(corrupted_content, filename)
        
    assert "Failed to parse PDF content" in str(exc_info.value)