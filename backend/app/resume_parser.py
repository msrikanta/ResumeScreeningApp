from docx import Document
import PyPDF2


def extract_text_from_resume(file_path: str) -> str:
    """
    Extract text from PDF or DOCX resume file.
    """
    if file_path.lower().endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()

    elif file_path.lower().endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
