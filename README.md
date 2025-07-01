# 🧾 Automated Invoice Processing System

This project is a Python-based tool that automates the extraction of invoice details from PDF files and logs them into Excel and SQLite. It features a GUI built with Tkinter and supports duplicate prevention, vendor-wise and monthly reporting.

---

## 📌 Features

- 📄 Extracts **Invoice Number, Date, Vendor, Amount** from PDF invoices
- 💾 Stores entries into:
  - `invoice_log.xlsx` (Excel)
  - `invoice_data.db` (SQLite)
- 🧠 Prevents duplicate entries
- 🖼️ Easy-to-use **GUI** (Tkinter)
- 📊 Report generator:
  - Monthly totals
  - Vendor-wise summary

---

## 🛠️ Tech Stack

- `Python`
- `pdfplumber` (PDF reading)
- `re` (Regex extraction)
- `pandas`, `openpyxl` (Excel handling)
- `sqlite3` (Database)
- `tkinter` (GUI)

---

## 📁 Folder Structure

AutomatedInvoiceSystem/
├── gui_invoice_app.py # GUI for uploading invoices
├── db_handler.py # Handles database operations
├── extract_invoice_number.py # CLI-based invoice extraction (optional)
├── generate_reports.py # Generates summary Excel reports
├── invoice_log.xlsx # Excel log of all invoices
├── invoice_data.db # SQLite DB storing invoices
└── invoices/
└── sample_invoice.pdf # Sample test invoice

yaml
Copy
Edit

---

## 🖥️ How to Run

Install requirements:

```bash
pip install pdfplumber pandas openpyxl
Run the GUI:

bash
Copy
Edit
python gui_invoice_app.py
Run reports:

bash
Copy
Edit
python generate_reports.py
📦 Sample Output
✅ Successfully extracted:

yaml
Copy
Edit
Invoice Number: INV12345
Date: 01/07/2024
Vendor: ACME Corporation
Amount: 2150.00
Generated files:

invoice_log.xlsx

invoice_data.db

monthly_report.xlsx

vendor_report.xlsx

📚 Future Enhancements
Email inbox integration

OCR support for scanned invoices

Multi-vendor dashboard

🙋 Author
Rasalakushwanth – [Automated Invoice Processing System – 2025 Submission]

yaml
Copy
Edit

---

✅ Let me know when you're ready for:

### 📊 Step 9.2: PowerPoint Slides (PPT)

I’ll create your entire final presentation — title, intro, screenshots, flowchart, demo, and conclusion — in clean, college format.

Just reply:

**"Next: PPT"** and I’ll generate it for you!
