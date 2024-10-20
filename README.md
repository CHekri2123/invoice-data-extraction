

## Installation

### Prerequisites
Make sure you have the following installed on your system:

- **Python 3.8+**
- **Tesseract OCR**

#### Install Tesseract:

- **Ubuntu/Debian**:  
   Open your terminal and run the following commands:
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   ```

- **macOS**:  
   Use Homebrew to install Tesseract:
   ```bash
   brew install tesseract
   ```

- **Windows**:  
   Download and install Tesseract from the official [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).  
   Follow the installation instructions provided on their page.

---

## Project Structure
```
/InvoiceExtraction
│
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (e.g., OpenAI API key)
├── /output_test        # Output folder for extracted files
└── README.md           # Documentation
```

---

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/invoice-extraction-system.git
   cd invoice-extraction-system
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file:
   ```
   OPEN_AI=<your-openai-api-key>
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

5. Upload an invoice PDF and choose the extraction method (GPT or OCR).  

---

## Trust Score Calculation

The **Trust Score** reflects the reliability of the extracted data.

**Formula**:
```
Trust Score = (Valid Fields / Total Fields) × 100
```

This ensures each missing or incorrect field decreases the trust score, giving the user a clear assessment of the data's reliability.

---

## Error Handling

1. **PDF Type Detection**:
   - The system checks if the uploaded PDF is scanned or regular and suggests the appropriate extraction method.

2. **API Error Handling**:
   - If GPT extraction fails, a clear error message is shown without crashing the system.

3. **Fallback to OCR**:
   - If GPT extraction fails, the user can switch to OCR-based extraction to ensure continuous workflow.

---

## Performance Optimization

- **Asynchronous Processing**:  
  Both GPT and OCR-based extractions run asynchronously using `asyncio`, ensuring quick processing of multiple invoices.
  
- **Temporary File Handling**:  
  Uploaded PDFs are saved temporarily and removed after processing to minimize disk usage.

---

## Future Improvements

- **Batch Processing**:  
  Add the ability to process multiple invoices simultaneously.

- **Auto-Detection of Fields**:  
  Use machine learning to predict field names instead of manual selection.

- **Database Integration**:  
  Store extracted data in a database for further analysis and auditing.

---

## License

This project is licensed under the MIT License.

---

```