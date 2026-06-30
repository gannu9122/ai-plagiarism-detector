from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(filename, results):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Plagiarism Report", styles['Title']))

    for r in results:
        text = f"""
        File1: {r['file1']}  
        File2: {r['file2']}  
        Similarity: {r['similarity']}%
        """
        content.append(Paragraph(text, styles['Normal']))

    doc.build(content)