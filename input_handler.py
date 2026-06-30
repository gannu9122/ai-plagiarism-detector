from PyPDF2 import PdfReader

def extract_text_from_pdf(filepath):
    text = ""

    pdf = PdfReader(filepath)

    for page in pdf.pages:
        text += page.extract_text()

    return text