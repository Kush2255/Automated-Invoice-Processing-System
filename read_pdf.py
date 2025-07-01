import pdfplumber
import re
import pandas as pd
import os

# Function to extract text
def extract_text_from_pdf(file_path):
    full_text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text

# Function to extract invoice details
def extract_invoice_details(text):
    invoice_number = re.search(r"Invoice\s*Number[:\s]*([A-Z0-9-]+)", text, re.IGNORECASE)
    date = re.search(r"Date[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})", text)
    vendor = re.search(r"Vendor[:\s]*(.+)", text)
    
    # 🔧 FIXED regex for Amount (more flexible)
    amount = re.search(r"Amount[:\s]*([0-9,]+\.\d{2})", text, re.IGNORECASE)

    return {
        "Invoice Number": invoice_number.group(1) if invoice_number else "Not found",
        "Date": date.group(1) if date else "Not found",
        "Vendor": vendor.group(1) if vendor else "Not found",
        "Amount": amount.group(1) if amount else "Not found"
    }

# Function to save to Excel
def save_to_excel(data, file_path="output/invoice_log.xlsx"):
    # If file exists, append to it
    if os.path.exists(file_path):
        df_existing = pd.read_excel(file_path)
        df_new = pd.DataFrame([data])
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = pd.DataFrame([data])
    
    # Save to Excel
    df_combined.to_excel(file_path, index=False)
    print(f"\n✅ Invoice saved to: {file_path}")

# Main
if __name__ == "__main__":
    path = "invoices/sample_invoice.pdf"
    text = extract_text_from_pdf(path)
    
    print("------ Extracted Invoice Details ------")
    details = extract_invoice_details(text)
    for key, value in details.items():
        print(f"{key}: {value}")
    
    save_to_excel(details)
