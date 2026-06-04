import fitz

def extract_pdf_text(pdf_path:str):
    doc = fitz.open(pdf_path)
    text = []

    for page in doc:
        page_text = page.get_text()
        text.append(page_text)

    doc.close()
    return "\n".join(text)