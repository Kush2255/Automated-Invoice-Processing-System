from db_utils import create_connection, create_table, insert_invoice

def main():
    # Step 1: Connect to DB and create table
    conn = create_connection('invoice_data.db')
    create_table(conn)

    # Example invoice details extracted from your PDF processing
    invoice_number = "INV12345"
    date = "01/07/2024"
    vendor = "ACME Corporation"
    amount = 2150.00

    # Step 2: Prepare the invoice data dictionary
    invoice_data = {
        'invoice_number': invoice_number,
        'date': date,
        'vendor': vendor,
        'amount': amount
    }

    # Step 3: Insert invoice into database
    inserted = insert_invoice(conn, invoice_data)
    if inserted:
        print(f"Inserted invoice {invoice_number}")
    else:
        print(f"Skipped duplicate invoice {invoice_number}")

    # Step 4: Close the connection
    conn.close()

if __name__ == "__main__":
    main()
