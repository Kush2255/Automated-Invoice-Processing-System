import sqlite3

def create_connection(db_file='invoice_data.db'):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    sql = '''
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_number TEXT PRIMARY KEY,
        date TEXT,
        vendor TEXT,
        amount REAL
    );
    '''
    conn.execute(sql)
    conn.commit()

def insert_invoice(conn, invoice):
    sql = '''
    INSERT OR IGNORE INTO invoices (invoice_number, date, vendor, amount)
    VALUES (?, ?, ?, ?);
    '''
    cur = conn.cursor()
    cur.execute(sql, (
        invoice['invoice_number'],
        invoice['date'],
        invoice['vendor'],
        invoice['amount']
    ))
    conn.commit()
    return cur.rowcount  # 1 if inserted, 0 if duplicate
