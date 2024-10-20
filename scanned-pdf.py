from pdf2image import convert_from_path
import pytesseract
import os

def ocr_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

scanned_dir = 'Jan to Mar/scanned'
output_dir = 'results/scanned'
os.makedirs(output_dir, exist_ok=True)

for pdf_file in os.listdir(scanned_dir):
    if pdf_file.lower().endswith('.pdf'):
        pdf_path = os.path.join(scanned_dir, pdf_file)
        text = ocr_pdf(pdf_path)
        output_file = os.path.join(output_dir, pdf_file.replace('.pdf', '.txt'))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
