from pypdf import PdfReader
import docx


class FileParserService:

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    @staticmethod
    def parse_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    @staticmethod
    def parse_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
