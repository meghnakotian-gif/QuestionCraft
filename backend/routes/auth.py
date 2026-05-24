# ============================================================
#  routes/auth.py — Authentication Routes (Starter Template)
# ============================================================
#  Add login / register / logout endpoints here.
#  This file uses a Flask "Blueprint" — a way to group related
#  routes so app.py stays clean and organised.
#
#  To activate this blueprint, add these two lines to app.py:
#      from routes.auth import auth_bp
#      app.register_blueprint(auth_bp, url_prefix="/auth")
# ============================================================

from flask import Blueprint, jsonify, request

# Create a Blueprint named "auth"
auth_bp = Blueprint("auth", __name__)


# ----------------------------------------------------------
# Route: POST /auth/register
# ----------------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Placeholder for user registration.
    Replace this with actual DB insert logic later.
    """
    data = request.get_json()          # Parse incoming JSON body
    return jsonify({
        "status": "success",
        "message": "Register endpoint reached (not implemented yet)",
        "received": data
    })


# ----------------------------------------------------------
# Route: POST /auth/login
# ----------------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Placeholder for user login.
    Replace this with actual DB lookup + password check later.
    """
    data = request.get_json()
    return jsonify({
        "status": "success",
        "message": "Login endpoint reached (not implemented yet)",
        "received": data
    })
