import fitz
from fitz import Page

def extract_pdf_text(pdf_path:str):
    doc = fitz.open(pdf_path)
    text = []

    for page in doc:
        page_text = page.get_text("text",sort=True)
        text.append(page_text)

    doc.close()
    return "\n".join(text)

def extract_pdf_pages(pdf_path:str):
    doc = fitz.open(pdf_path)
    pages = []

    for page_no,page in enumerate(doc,start=1):
        page:Page
        page_text = page.get_text("text",sort=True)
        pages.append({
            "page_no":page_no,
            "text":page_text
        })

    doc.close()
    return pages