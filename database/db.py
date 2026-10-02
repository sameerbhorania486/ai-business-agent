import os

from dotenv import load_dotenv
from supabase import create_client, Client


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# =========================
# VALIDATE ENVIRONMENT
# =========================

if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is missing from .env")


# =========================
# SUPABASE CONNECTION
# =========================

def get_connection() -> Client:
    """
    Create and return a Supabase client.
    """

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )
