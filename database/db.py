import sqlite3

DB_NAME = "/tmp/business.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    create_tables(connection)
    return connection


def create_tables(connection):
    cursor = connection.cursor()

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            company TEXT,
            phone TEXT
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    # Inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            product_id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()


def insert_sample_data():
    connection = get_connection()
    cursor = connection.cursor()

    customers = [
        (1, "Rahul Sharma", "rahul@example.com", "Sharma Enterprises", "9876543210"),
        (2, "Amit Patel", "amit@example.com", "Patel Traders", "9876543211"),
        (3, "Neha Shah", "neha@example.com", "Shah Industries", "9876543212"),
    ]

    orders = [
        (101, 1, "Laptop", 2, 120000, "Delivered"),
        (102, 1, "Wireless Mouse", 5, 5000, "Shipped"),
        (103, 2, "Keyboard", 3, 4500, "Processing"),
    ]

    inventory = [
        (1, "Laptop", 25, 60000),
        (2, "Wireless Mouse", 100, 1000),
        (3, "Keyboard", 50, 1500),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        (id, name, email, company, phone)
        VALUES (?, ?, ?, ?, ?)
    """, customers)

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, product, quantity, total_amount, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, orders)

    cursor.executemany("""
        INSERT OR IGNORE INTO inventory
        (product_id, product, quantity, price)
        VALUES (?, ?, ?, ?)
    """, inventory)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    connection = sqlite3.connect(DB_NAME)
    create_tables(connection)
    connection.close()

    insert_sample_data()

    print("Database and sample data created successfully.")
