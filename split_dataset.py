import os
import shutil
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
from tqdm import tqdm


def is_text_based(pdf_path):
    """
    Checks if a PDF is text-based by attempting to extract text.
    If text is found, it's considered text-based; otherwise, it may be scanned.
    """
    try:
        text = extract_text(pdf_path, maxpages=1)
        if text and text.strip():
            return True
        else:
            return False
    except:
        return False


def has_images(pdf_path):
    """
    Checks if a PDF contains images, which may indicate a scanned or mixed PDF.
    """
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        return True
        return False
    except:
        return False


def detect_pdf_type(pdf_path):
    """
    Determines the type of PDF: 'text', 'scanned', or 'mixed'.
    """
    text_based = is_text_based(pdf_path)
    image_based = has_images(pdf_path)

    if text_based and not image_based:
        return 'text_based'
    elif not text_based and image_based:
        return 'scanned'
    elif text_based and image_based:
        return 'mixed'
    else:
        return 'unknown'


def split_dataset(dataset_path):
    """
    Splits PDFs into subfolders based on their detected type.
    """
    # Create directories for each type
    types = ['text_based', 'scanned', 'mixed', 'unknown']
    for pdf_type in types:
        os.makedirs(os.path.join(dataset_path, pdf_type), exist_ok=True)

    # List all PDF files in the dataset directory
    pdf_files = [f for f in os.listdir(dataset_path) if f.lower().endswith('.pdf')]

    for pdf_file in tqdm(pdf_files, desc='Processing PDFs'):
        pdf_path = os.path.join(dataset_path, pdf_file)
        pdf_type = detect_pdf_type(pdf_path)

        # Move the file to the corresponding directory
        destination = os.path.join(dataset_path, pdf_type, pdf_file)
        shutil.move(pdf_path, destination)

    print('Dataset splitting completed.')


if __name__ == '__main__':
    dataset_folder = 'Jan to Mar'  # Replace with your folder path
    split_dataset(dataset_folder)
