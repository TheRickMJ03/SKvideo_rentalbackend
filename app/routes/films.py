from flask import Blueprint, jsonify
from app.database import get_db_connection

films_bp = Blueprint("films", __name__)

@films_bp.route("/films", methods=["GET"])
def get_films():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT film_id, title, release_year FROM film LIMIT 10;")
    films = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(films)
