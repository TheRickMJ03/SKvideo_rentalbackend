from flask import Blueprint, jsonify
from app.database import get_db_connection

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/customer", methods=["GET"])
def get_customer():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT customer_id, store_id, first_name,last_name FROM customer LIMIT 10;")
    customer = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(customer)