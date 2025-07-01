import sqlite3
import pandas as pd

def load_data(db_file='invoice_data.db'):
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM invoices"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def generate_monthly_summary(df):
    df['Month'] = pd.to_datetime(df['date'], dayfirst=True).dt.strftime('%B %Y')
    summary = df.groupby('Month')['amount'].sum().reset_index()
    print("\n📅 Monthly Summary:")
    print(summary)
    summary.to_excel("monthly_report.xlsx", index=False)
    print("✅ monthly_report.xlsx generated.")

def generate_vendor_summary(df):
    summary = df.groupby('vendor')['amount'].sum().reset_index()
    print("\n🏢 Vendor Summary:")
    print(summary)
    summary.to_excel("vendor_report.xlsx", index=False)
    print("✅ vendor_report.xlsx generated.")

# Run reports
if __name__ == "__main__":
    df = load_data()
    if df.empty:
        print("⚠️ No invoice data found in the database.")
    else:
        generate_monthly_summary(df)
        generate_vendor_summary(df)
