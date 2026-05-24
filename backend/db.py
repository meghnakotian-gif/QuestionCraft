# ============================================================
#  db.py — Database Connection Helper
# ============================================================
#  This module provides a single reusable function that opens
#  a new PostgreSQL connection using the DATABASE_URL from .env
#
#  Usage (in any route file):
#      from db import get_connection
#      conn = get_connection()
# ============================================================

import psycopg2
import os
from dotenv import load_dotenv

# Make sure .env is loaded even if this file is imported directly
load_dotenv()


def get_connection():
    """
    Opens and returns a new PostgreSQL database connection.

    Reads the connection string from the DATABASE_URL environment
    variable (set in your .env file).

    Returns:
        psycopg2 connection object

    Raises:
        Exception: if the connection could not be established
                   (e.g. wrong credentials, network issue)
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is not set. "
            "Please add it to your .env file."
        )

    # psycopg2 accepts the full Supabase connection string directly
    connection = psycopg2.connect(database_url)
    return connection
