from abc import ABC, abstractmethod
import PyPDF2
import docx

class DocumentProcessor(ABC):
    def __init__(self, file):
        self.file = file

    @abstractmethod
    def process(self):
        pass


class PDFProcessor(DocumentProcessor):
    def process(self) -> dict:
        reader = PyPDF2.PdfReader(self.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        return {"text": text, "file_type": "pdf"}


class DOCXProcessor(DocumentProcessor):
    def process(self) -> dict:
        doc = docx.Document(self.file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return {"text": text, "file_type": "pdf"}


class TXTProcessor(DocumentProcessor):
    def process(self) -> dict:
        text = self.file.read().decode('utf-8')
        return {"text": text, "file_type": "pdf"}


class DocumentProcessorFactory:
    @staticmethod
    def get_processor(uploaded_file):
        if uploaded_file.content_type == "application/pdf":
            return PDFProcessor(uploaded_file)
        elif uploaded_file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return DOCXProcessor(uploaded_file)
        elif uploaded_file.content_type == "text/plain":
            return TXTProcessor(uploaded_file)
        else:
            raise ValueError(f"Unsupported file type: {uploaded_file.content_type}")