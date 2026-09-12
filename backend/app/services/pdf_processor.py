from pathlib import Path

from pypdf import PdfReader

from app.services.topic_analysis import analyze_exam_text


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Read a PDF and return extracted text for downstream question parsing."""
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n\n".join(pages)


def analyze_pdf_file(pdf_path: str | Path) -> dict:
    """Extract questions from a PDF and build topic summary metadata."""
    text = extract_text_from_pdf(pdf_path)
    payload = analyze_exam_text(text)
    payload["source_file"] = str(pdf_path)
    if not payload["questions"]:
        payload["message"] = "No text could be extracted from the uploaded PDF."
    return payload
