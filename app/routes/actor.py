from flask import Blueprint, jsonify
from app.database import get_db_connection

actor_bp = Blueprint("actor", __name__)

@actor_bp.route("/actor", methods=["GET"])
def get_actor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT actor_id, first_name, last_name FROM actor LIMIT 10;")
    actor = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(actor)