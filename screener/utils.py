import PyPDF2
import io


def extract_text_from_pdf(file) -> str:
    """Extract text from uploaded PDF file object."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        return ""
