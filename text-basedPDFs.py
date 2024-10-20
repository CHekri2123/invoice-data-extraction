from pdfminer.high_level import extract_text
import os

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

text_based_dir = 'Jan to Mar/text_based'
output_dir = 'results/text-based'
os.makedirs(output_dir, exist_ok=True)

for pdf_file in os.listdir(text_based_dir):
    if pdf_file.lower().endswith('.pdf'):
        pdf_path = os.path.join(text_based_dir, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        output_file = os.path.join(output_dir, pdf_file.replace('.pdf', '.txt'))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
