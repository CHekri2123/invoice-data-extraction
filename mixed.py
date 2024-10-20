from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
import os
import re

def clean_text(text):
    # Remove non-ASCII characters
    text = text.encode('ascii', errors='ignore').decode()
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_text_mixed_pdf(pdf_path):
    # Extract text directly
    text = extract_text(pdf_path)
    text_length = len(text.strip())
    print(f"Extracted {text_length} characters from {pdf_path} using direct extraction.")

    # Decide whether to apply OCR
    if text_length < 100:  # Define a threshold, e.g., MIN_TEXT_LENGTH = 100
        print(f"Text is insufficient. Applying OCR to {pdf_path}.")
        images = convert_from_path(pdf_path)
        ocr_text = ''
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
        # Use only OCR text
        combined_text = ocr_text
    else:
        print(f"Text is sufficient. Skipping OCR for {pdf_path}.")
        combined_text = text

    # Clean and chunk the text
    print(f"Cleaning text of {pdf_path}")
    cleaned_text = clean_text(combined_text)
    print(f"Chunking text of {pdf_path}")
    chunked_text = chunk_text(cleaned_text)
    return '\n'.join(chunked_text)


def chunk_text(text, max_tokens=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1  # +1 for space
        if current_length >= max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


mixed_dir = 'Jan to Mar/mixed'
output_dir = 'results/mixed-data'
os.makedirs(output_dir, exist_ok=True)

for pdf_file in os.listdir(mixed_dir):
    if pdf_file.lower().endswith('.pdf'):
        pdf_path = os.path.join(mixed_dir, pdf_file)
        print(f"Processing {pdf_path}")
        text = extract_text_mixed_pdf(pdf_path)

        output_file = os.path.join(output_dir, pdf_file.replace('.pdf', '.txt'))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
