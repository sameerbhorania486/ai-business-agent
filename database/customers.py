from langchain_core.tools import tool

from database.db import get_connection


@tool
def search_customer(name: str) -> str:
    """
    Search for a customer by name from the SQLite database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, company, phone
        FROM customers
        WHERE name LIKE ?
    """, (f"%{name.strip()}%",))

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "Customer not found."

    customers = []

    for customer in results:
        customers.append({
            "id": customer[0],
            "name": customer[1],
            "email": customer[2],
            "company": customer[3],
            "phone": customer[4],
        })

    return str(customers)