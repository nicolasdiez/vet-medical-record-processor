import asyncio

import fitz  # type: ignore[import-untyped]

from app.domain.ports.outbound.interfaces import FileTextExtractorPort


class PDFFileTextExtractorAdapter(FileTextExtractorPort):
    """PyMuPDF implementation of the FileTextExtractorPort.

    Extracts plain text from PDF files using the fitz library. This adapter
    offloads the synchronous PyMuPDF operations to a thread pool to avoid 
    blocking the async event loop.
    """
    
    async def extract_text(self, file_content: bytes, filename: str) -> str:
        """Extracts plain text from a PDF file using PyMuPDF (fitz).

        Args:
            file_content (bytes): The raw binary content of the uploaded PDF file.
            filename (str): The name of the file being processed.

        Returns:
            str: The fully extracted plain text from all pages.

        Raises:
            ValueError: If the file signature doesn't match a valid PDF.
            RuntimeError: If PyMuPDF fails to parse the document structure.
        """
        if not filename.lower().endswith(".pdf"):
            raise ValueError(f"Unsupported file type. Expected PDF, got: {filename}")

        # Delegate the heavy synchronous task to a worker thread
        extracted_text = await asyncio.to_thread(self._extract_sync, file_content)
        return extracted_text

    def _extract_sync(self, file_content: bytes) -> str:
        """Synchronous worker method that performs the PyMuPDF operations.

        Opens the PDF directly from memory bytes and iterates through pages 
        to extract the text payload.

        Args:
            file_content (bytes): The raw binary content of the PDF.

        Returns:
            str: The combined plain text extracted from all pages.

        Raises:
            RuntimeError: If PyMuPDF fails to parse the PDF byte stream.
        """
        try:
            # Open the document directly from memory bytes (no disk I/O)
            doc = fitz.open(stream=file_content, filetype="pdf")
            full_text = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                # Extract text from each page
                full_text.append(page.get_text("text"))
                
            return "\n".join(full_text)
            
        except Exception as e:
            # In a real production environment, we would use a proper logger here
            raise RuntimeError(f"Failed to parse PDF content: {str(e)}")