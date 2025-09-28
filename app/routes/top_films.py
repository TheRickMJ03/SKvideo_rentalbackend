
from flask import Blueprint, jsonify
from app.database import get_db_connection

top_filmsbp = Blueprint("top_films", __name__)
@top_filmsbp.route("/api/actors/<int:actor_id>/top-films", methods=["GET"])
def get_top_films(actor_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            f.film_id,
            f.title,
            COUNT(r.rental_id) AS rental_count
        FROM film f
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN inventory i ON f.film_id = i.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        WHERE fa.actor_id = %s
        GROUP BY f.film_id
        ORDER BY rental_count DESC
        LIMIT 5;
    """
    cursor.execute(query, (actor_id,))
    films = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(films)
