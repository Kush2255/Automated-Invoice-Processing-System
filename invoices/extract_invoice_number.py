import pdfplumber
import re
from db_handler import create_connection, create_table, insert_invoice
import pandas as pd
import os

with pdfplumber.open("sample_invoice.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text()

# Invoice Number
match = re.search(r'Invoice Number:\s*(INV\d+)', text)
if match:
    invoice_number = match.group(1)
    print("✅ Invoice Number:", invoice_number)
else:
    invoice_number = "Not found"
    print("❌ Invoice number not found.")

# Invoice Date
date_match = re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})', text)
if date_match:
    invoice_date = date_match.group(1)
    print("✅ Date:", invoice_date)
else:
    invoice_date = "Not found"
    print("❌ Date not found.")

# Vendor Name
vendor_match = re.search(r'Vendor:\s*(.+)', text)
if vendor_match:
    vendor = vendor_match.group(1).strip()
    print("✅ Vendor:", vendor)
else:
    vendor = "Not found"
    print("❌ Vendor not found.")

# Amount
amount_match = re.search(r'Amount:\s*([\d,]+\.\d{2}|\d+)', text)
if amount_match:
    amount = float(amount_match.group(1).replace(',', ''))
    print("✅ Amount:", amount)
else:
    amount = "Not found"
    print("❌ Amount not found.")

# ✅ Step 5: Store into SQLite
invoice_data = {
    'invoice_number': invoice_number,
    'date': invoice_date,
    'vendor': vendor,
    'amount': amount
}

conn = create_connection()
create_table(conn)
result = insert_invoice(conn, invoice_data)

if result == 1:
    print("✅ Invoice saved to database.")
else:
    print("⚠️ Duplicate invoice — already exists.")

# ✅ Step 6: Export to Excel (append or create)
excel_file = 'invoice_log.xlsx'

new_row = {
    'Invoice Number': invoice_number,
    'Date': invoice_date,
    'Vendor': vendor,
    'Amount': amount
}

if os.path.exists(excel_file):
    df_existing = pd.read_excel(excel_file)

    # Avoid duplicates
    if invoice_number in df_existing['Invoice Number'].values:
        print("⚠️ Invoice already exists in Excel. Skipping write.")
    else:
        df_new = pd.DataFrame([new_row])
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(excel_file, index=False)
        print("✅ Invoice added to Excel.")
else:
    df = pd.DataFrame([new_row])
    df.to_excel(excel_file, index=False)
    print("✅ Excel file created and invoice logged.")
