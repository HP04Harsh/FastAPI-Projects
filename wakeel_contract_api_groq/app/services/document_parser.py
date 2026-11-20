import os
from PyPDF2 import PdfReader


def extract_text(file_path: str) -> tuple[str, int, int]:
    """
    Extracts text, page count, and word count from PDF or TXT.
    Returns: (text_content, page_count, word_count)
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text_content = f.read()
        page_count = 1

    elif ext == ".pdf":
        reader = PdfReader(file_path)
        page_count = len(reader.pages)
        pages_text = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                pages_text.append(extracted)
        text_content = "\n".join(pages_text)

    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    word_count = len(text_content.split())
    return text_content, page_count, word_count