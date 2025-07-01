import sqlite3

def create_connection(db_file='invoice_data.db'):
    """Create or open a database connection."""
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    """Create the invoices table if it does not exist."""
    sql_create_invoices_table = """
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_number TEXT PRIMARY KEY,
        date TEXT,
        vendor TEXT,
        amount REAL
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql_create_invoices_table)
    conn.commit()

def insert_invoice(conn, invoice):
    """
    Insert invoice data into the invoices table.
    If invoice_number already exists, it will skip the insertion.

    invoice: dict with keys - invoice_number, date, vendor, amount
    """
    sql_insert = """
    INSERT OR IGNORE INTO invoices (invoice_number, date, vendor, amount)
    VALUES (?, ?, ?, ?);
    """
    cursor = conn.cursor()
    cursor.execute(sql_insert, (
        invoice['invoice_number'],
        invoice['date'],
        invoice['vendor'],
        invoice['amount']
    ))
    conn.commit()
    return cursor.rowcount  # Returns 1 if inserted, 0 if skipped (duplicate)
