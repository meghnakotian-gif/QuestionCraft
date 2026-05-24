# ============================================================
#  app.py — QuestionCraft Flask Application Entry Point
# ============================================================
#  This is the main file that starts the Flask web server.
#  Run this file to launch the backend:  python app.py
# ============================================================

from flask import Flask, jsonify
from config import Config          # Our custom config (reads .env file)
from db import get_connection      # Helper function to connect to Supabase DB

# ----------------------------------------------------------
# Create the Flask application instance
# ----------------------------------------------------------
app = Flask(__name__)

# Load configuration values (SECRET_KEY, DATABASE_URL, DEBUG, etc.)
app.config.from_object(Config)


# ----------------------------------------------------------
# Route: Home  →  GET /
# ----------------------------------------------------------
# A simple sanity-check route to confirm the server is running.
@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Welcome to QuestionCraft API 🎓",
        "version": "1.0.0"
    })


# ----------------------------------------------------------
# Route: DB Test  →  GET /test-db
# ----------------------------------------------------------
# Tries to open a database connection and run a lightweight
# query.  Returns success or an error message — great for
# verifying that your Supabase credentials are correct.
@app.route("/test-db")
def test_db():
    try:
        conn = get_connection()       # Attempt to connect
        cursor = conn.cursor()

        # A simple query that always returns the DB server time
        cursor.execute("SELECT NOW();")
        db_time = cursor.fetchone()[0]

        cursor.close()
        conn.close()                  # Always close connections when done

        return jsonify({
            "status": "success",
            "message": "Database connected successfully! ✅",
            "db_server_time": str(db_time)
        })

    except Exception as e:
        # Return the error message so you can debug easily
        return jsonify({
            "status": "error",
            "message": "Database connection failed ❌",
            "error": str(e)
        }), 500


# ----------------------------------------------------------
# Run the app
# ----------------------------------------------------------
# debug=True reloads the server automatically when you save
# a file — very helpful during development.
if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", True))
