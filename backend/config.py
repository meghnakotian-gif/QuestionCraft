# ============================================================
#  config.py — QuestionCraft Configuration
# ============================================================
#  Reads sensitive settings (DB URL, secret key, etc.) from
#  the .env file so we never hard-code passwords in source code.
# ============================================================

import os
from dotenv import load_dotenv

# Load all variables defined in the .env file into os.environ
load_dotenv()


class Config:
    """Central configuration class for the Flask app."""

    # ----------------------------------------------------------
    # Flask secret key — used to sign session cookies securely.
    # Change this to a long random string in production!
    # ----------------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")

    # ----------------------------------------------------------
    # Supabase PostgreSQL connection string.
    # Format:
    #   postgresql://<user>:<password>@<host>:<port>/<dbname>
    # This value is read from the DATABASE_URL variable in .env
    # ----------------------------------------------------------
    DATABASE_URL = os.getenv("DATABASE_URL")

    # ----------------------------------------------------------
    # Debug mode — set to True during development.
    # Set to False (or remove from .env) before deploying.
    # ----------------------------------------------------------
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
