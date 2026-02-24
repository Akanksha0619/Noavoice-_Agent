from pypdf import PdfReader
import docx


class FileParserService:
    """
    Service to extract text from uploaded files (PDF, DOCX, TXT)
    Used in Global Knowledge Base upload
    """

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        text = ""
        reader = PdfReader(file_path)

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return text.strip()

    @staticmethod
    def parse_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text])
        return text.strip()

    @staticmethod
    def parse_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()