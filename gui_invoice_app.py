import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
import re
import pandas as pd
import os
from db_handler import create_connection, create_table, insert_invoice

def extract_invoice_details(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        invoice_number = re.search(r'Invoice Number:\s*(INV\d+)', text)
        invoice_date = re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})', text)
        vendor = re.search(r'Vendor:\s*(.+)', text)
        amount = re.search(r'Amount:\s*([\d,]+\.\d{2}|\d+)', text)

        return {
            "invoice_number": invoice_number.group(1) if invoice_number else "Not found",
            "date": invoice_date.group(1) if invoice_date else "Not found",
            "vendor": vendor.group(1).strip() if vendor else "Not found",
            "amount": float(amount.group(1).replace(',', '')) if amount else "Not found"
        }
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {str(e)}")
        return None

def save_to_database_and_excel(invoice):
    conn = create_connection()
    create_table(conn)
    result = insert_invoice(conn, invoice)

    # Save to Excel
    excel_file = 'invoice_log.xlsx'
    new_row = {
        'Invoice Number': invoice['invoice_number'],
        'Date': invoice['date'],
        'Vendor': invoice['vendor'],
        'Amount': invoice['amount']
    }

    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        if invoice['invoice_number'] in df['Invoice Number'].values:
            return "⚠️ Already exists in Excel and DB"
        df_new = pd.DataFrame([new_row])
        df = pd.concat([df, df_new], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_excel(excel_file, index=False)

    return "✅ Invoice saved!" if result == 1 else "⚠️ Already exists in database"

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    invoice = extract_invoice_details(file_path)
    if not invoice:
        return

    # Show on GUI
    invoice_number_var.set(invoice["invoice_number"])
    date_var.set(invoice["date"])
    vendor_var.set(invoice["vendor"])
    amount_var.set(invoice["amount"])

    # Save to DB + Excel
    status = save_to_database_and_excel(invoice)
    status_var.set(status)

# GUI Layout
root = tk.Tk()
root.title("Invoice Extractor")
root.geometry("400x300")

tk.Button(root, text="📄 Upload Invoice PDF", command=browse_file).pack(pady=10)

invoice_number_var = tk.StringVar()
date_var = tk.StringVar()
vendor_var = tk.StringVar()
amount_var = tk.StringVar()
status_var = tk.StringVar()

tk.Label(root, text="Invoice Number").pack()
tk.Entry(root, textvariable=invoice_number_var).pack()

tk.Label(root, text="Date").pack()
tk.Entry(root, textvariable=date_var).pack()

tk.Label(root, text="Vendor").pack()
tk.Entry(root, textvariable=vendor_var).pack()

tk.Label(root, text="Amount").pack()
tk.Entry(root, textvariable=amount_var).pack()

tk.Label(root, textvariable=status_var, fg="blue").pack(pady=10)

root.mainloop()
