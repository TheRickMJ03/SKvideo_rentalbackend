from flask import Blueprint, jsonify
from app.database import get_db_connection

films_bp = Blueprint("films", __name__)

@films_bp.route("/api/top-films", methods=["GET"])  # 🔄 updated route
def get_top_rented_films():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT f.film_id, f.title, f.release_year,f.description, f.rating, COUNT(r.rental_id) as rental_count
        FROM film f
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        GROUP BY f.film_id
        ORDER BY rental_count DESC
        LIMIT 5;
    """

    cursor.execute(query)
    films = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(films)
