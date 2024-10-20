import streamlit as st
import os
from PyPDF2 import PdfReader
from pyzerox import zerox  # For GPT extraction
import asyncio
import pytesseract
from pdf2image import convert_from_path
from dotenv import load_dotenv
import re

# Load environment variables (like API key)
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_AI")

# Helper function to detect if PDF is scanned or not
def is_scanned_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return len(text.strip()) == 0
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return True

# Extract text from images using OCR and extract selected fields
def extract_text_with_ocr(file_path, selected_fields=None):
    try:
        images = convert_from_path(file_path)
        extracted_text = "".join(pytesseract.image_to_string(img) for img in images)
        
        # If specific fields are selected, extract only those fields
        if selected_fields:
            return {field: extract_field_value(field, extracted_text) for field in selected_fields}

        # Return the full text if no specific fields are selected
        return {"full_text": extracted_text}
    except Exception as e:
        st.error(f"OCR extraction error: {e}")
        return {}

# Simple regex-based field extraction logic
def extract_field_value(field, text):
    patterns = {
        "Invoice Number": r"(?i)(?:Invoice\s*#?:?\s*)([A-Za-z0-9\-]+)",
        "Invoice Date": r"(?i)Invoice\s*Date:?\s*([\d]{1,2}\s\w{3}\s\d{4})",
        "Email": r"[\w\.-]+@[\w\.-]+",
        "Total Amount": r"(?i)Total\s*Amount\s*[:\-]?\s*\₹?([\d.,]+)"
    }
    match = re.search(patterns.get(field, ""), text)
    return match.group(1) if match else "Not Found"

# Calculate trust score based on valid fields extracted
def calculate_trust_score(extracted_data):
    total_fields = len(extracted_data)
    valid_fields = sum(1 for value in extracted_data.values() if value != "Not Found")
    return (valid_fields / total_fields) * 100

# GPT extraction using Zerox
async def gpt_extraction(file_path):
    try:
        result = await zerox(
            file_path=file_path,
            model="gpt-4o-mini",
            output_dir="./output_test",
            cleanup=True,
            maintain_format=True,
        )
        if result is None:
            raise ValueError("API response is None.")
        return result
    except Exception as e:
        st.error(f"GPT extraction error: {e}")
        return None

# Streamlit UI setup
st.set_page_config(layout="wide", page_title="Invoice Data Extraction", page_icon="📄")
st.title("Invoice Data Extraction System")

# PDF upload section
uploaded_file = st.file_uploader("Upload an Invoice PDF", type=["pdf"])

if uploaded_file:
    temp_path = f"./temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    is_scanned = is_scanned_pdf(temp_path)

    # Radio button to toggle between extraction methods
    extraction_method = st.radio(
        "Select Extraction Method", 
        ["GPT-based Extraction", "OCR-based Extraction"], 
        index=0 if not is_scanned else 1,
    )

    if extraction_method == "GPT-based Extraction":
        if st.button("Extract with GPT"):
            result = asyncio.run(gpt_extraction(temp_path))
            if result:
                if not result.pages:
                    st.error("No pages found in the GPT response.")
                else:
                    content = result.pages[0].content
                    extracted_data = extract_data_from_invoice(content)
                    trust_score = calculate_trust_score(extracted_data)

                    # Display Markdown content and extracted data
                    st.markdown(content)
                    st.json({"Extracted Data": extracted_data, "Trust Score": trust_score})

                    if trust_score < 99:
                        st.warning(f"Trust Score below 99%! Score: {trust_score:.2f}%")

    elif extraction_method == "OCR-based Extraction":
        selected_fields = st.multiselect(
            "Select fields to extract",
            ["Invoice Number", "Invoice Date", "Email", "Total Amount"]
        )

        if st.button("Extract with OCR"):
            ocr_result = extract_text_with_ocr(temp_path, selected_fields)
            trust_score = calculate_trust_score(ocr_result)

            # Display OCR results
            st.json({"Extracted Data": ocr_result, "Trust Score": trust_score})

            if trust_score < 99:
                st.warning(f"Trust Score below 99%! Score: {trust_score:.2f}%")

    # Clean up uploaded file
    os.remove(temp_path)

else:
    st.info("Please upload an invoice PDF to proceed.")
