import os
from dotenv import load_dotenv
from supabase import create_client

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# =========================
# CHECK ENVIRONMENT
# =========================

print("URL found:", bool(url))
print("KEY found:", bool(key))

# =========================
# CREATE SUPABASE CLIENT
# =========================

supabase = create_client(url, key)

print("Supabase client created successfully!")

# =========================
# INSERT TEST CUSTOMER
# =========================

response = supabase.table("customers").insert({
    "id": 1,
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "company": "Rahul Traders",
    "phone": "9876543210"
}).execute()

print("Customer inserted successfully!")
print(response.data)