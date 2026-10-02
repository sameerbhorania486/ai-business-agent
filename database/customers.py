from langchain_core.tools import tool

from database.db import get_connection


# =========================
# SEARCH CUSTOMER
# =========================

@tool
def search_customer(name: str, business_id: int) -> str:
    """
    Search for a customer by name
    within the authenticated business.
    """

    supabase = get_connection()

    search_name = name.strip()

    response = (
        supabase
        .table("customers")
        .select(
            "id, name, email, company, phone"
        )
        .eq("business_id", business_id)
        .ilike(
            "name",
            f"%{search_name}%"
        )
        .execute()
    )

    results = response.data

    if not results:
        return "Customer not found."

    customers = []

    for customer in results:
        customers.append({
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "company": customer["company"],
            "phone": customer["phone"],
        })

    return str(customers)


# =========================
# GET ALL CUSTOMERS
# =========================

@tool
def get_all_customers(business_id: int) -> str:
    """
    Get all customers belonging to the authenticated business.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("customers")
        .select(
            "id, name, email, company, phone"
        )
        .eq("business_id", business_id)
        .order("id")
        .execute()
    )

    customers = response.data

    if not customers:
        return "No customers found."

    result = []

    for customer in customers:
        result.append({
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "company": customer["company"],
            "phone": customer["phone"],
        })

    return str({
        "status": "success",
        "customers": result
    })


# =========================
# ADD CUSTOMER
# =========================

@tool
def add_customer(
    name: str,
    email: str = "",
    company: str = "",
    phone: str = "",
    business_id: int = 0
) -> str:
    """
    Add a new customer to the authenticated business.
    """

    supabase = get_connection()

    customer_name = name.strip()

    if not customer_name:
        return "Customer name is required."

    # -------------------------
    # Generate customer ID
    # -------------------------

    existing_response = (
        supabase
        .table("customers")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )

    existing_customers = existing_response.data

    if existing_customers:
        new_customer_id = (
            existing_customers[0]["id"] + 1
        )
    else:
        new_customer_id = 1

    # -------------------------
    # Insert customer
    # -------------------------

    response = (
        supabase
        .table("customers")
        .insert({
            "id": new_customer_id,
            "name": customer_name,
            "email": email.strip(),
            "company": company.strip(),
            "phone": phone.strip(),
            "business_id": business_id
        })
        .execute()
    )

    if not response.data:
        return "Failed to add customer."

    customer = response.data[0]

    return str({
        "status": "success",
        "message": "Customer added successfully.",
        "customer": {
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "company": customer["company"],
            "phone": customer["phone"]
        }
    })


# =========================
# UPDATE CUSTOMER
# =========================

@tool
def update_customer(
    customer_id: int,
    email: str | None = None,
    company: str | None = None,
    phone: str | None = None,
    business_id: int = 0
) -> str:
    """
    Update an existing customer's details
    within the authenticated business.
    """

    supabase = get_connection()

    # -------------------------
    # Check customer exists
    # -------------------------

    existing_response = (
        supabase
        .table("customers")
        .select(
            "id, name, email, company, phone"
        )
        .eq("id", customer_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    existing_customers = existing_response.data

    if not existing_customers:
        return "Customer not found."

    # -------------------------
    # Prepare updates
    # -------------------------

    updates = {}

    if email is not None:
        updates["email"] = email.strip()

    if company is not None:
        updates["company"] = company.strip()

    if phone is not None:
        updates["phone"] = phone.strip()

    if not updates:
        return "No customer information was provided to update."

    # -------------------------
    # Update customer
    # -------------------------

    response = (
        supabase
        .table("customers")
        .update(updates)
        .eq("id", customer_id)
        .eq("business_id", business_id)
        .execute()
    )

    if not response.data:
        return "Failed to update customer."

    customer = response.data[0]

    return str({
        "status": "success",
        "message": "Customer updated successfully.",
        "customer": {
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "company": customer["company"],
            "phone": customer["phone"]
        }
    })


# =========================
# DELETE CUSTOMER
# =========================

@tool
def delete_customer(
    customer_id: int,
    business_id: int = 0
) -> str:
    """
    Delete an existing customer
    within the authenticated business.
    """

    supabase = get_connection()

    # -------------------------
    # Check customer belongs
    # to this business
    # -------------------------

    existing_response = (
        supabase
        .table("customers")
        .select(
            "id, name, email, company, phone"
        )
        .eq("id", customer_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    existing_customers = existing_response.data

    if not existing_customers:
        return "Customer not found."

    customer = existing_customers[0]

    # -------------------------
    # Delete customer
    # -------------------------

    response = (
        supabase
        .table("customers")
        .delete()
        .eq("id", customer_id)
        .eq("business_id", business_id)
        .execute()
    )

    if not response.data:
        return "Failed to delete customer."

    return str({
        "status": "success",
        "message": "Customer deleted successfully.",
        "customer": {
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "company": customer["company"],
            "phone": customer["phone"]
        }
    })