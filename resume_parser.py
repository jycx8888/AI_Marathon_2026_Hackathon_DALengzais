import pdfplumber
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF resume."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def load_resumes_from_folder(folder: str) -> list:
    """Load all PDF resumes from a folder."""
    candidates = []
    for i, filename in enumerate(os.listdir(folder)):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            text = extract_text_from_pdf(path)
            candidates.append({
                "id": i + 1,
                "name": filename.replace(".pdf", ""),
                "resume_text": text[:2000]  # trim to avoid token overflow
            })
    return candidates