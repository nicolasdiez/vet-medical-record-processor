import fitz  # PyMuPDF
import asyncio
from app.domain.ports.outbound.interfaces import FileTextExtractorPort

class PDFFileTextExtractorAdapter(FileTextExtractorPort):
    """
    Adapter that uses PyMuPDF to extract raw text from PDF binary content.
    """
    
    async def extract_text(self, file_content: bytes, filename: str) -> str:
        """
        Extracts text from a PDF file. 
        Uses asyncio.to_thread to prevent the CPU-bound PDF parsing 
        from blocking the FastAPI asynchronous event loop.
        """
        if not filename.lower().endswith(".pdf"):
            raise ValueError(f"Unsupported file type. Expected PDF, got: {filename}")

        # Delegate the heavy synchronous task to a worker thread
        extracted_text = await asyncio.to_thread(self._extract_sync, file_content)
        return extracted_text

    def _extract_sync(self, file_content: bytes) -> str:
        """
        Synchronous method that actually performs the PyMuPDF operations.
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