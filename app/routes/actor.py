from flask import Blueprint, jsonify
from app.database import get_db_connection

actor_bp = Blueprint("actor", __name__)

# Route 1: Get top 5 actors
@actor_bp.route("/api/top-actors", methods=["GET"])
def get_top_actors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
       SELECT 
            a.actor_id,
            CONCAT(a.first_name, ' ', a.last_name) AS actor_name,
            COUNT(DISTINCT f.film_id) AS film_count
        FROM actor a
        JOIN film_actor fa ON a.actor_id = fa.actor_id
        JOIN film f ON fa.film_id = f.film_id
        JOIN inventory i ON f.film_id = i.film_id  
        GROUP BY a.actor_id
        ORDER BY film_count DESC
        LIMIT 5;
    """
    cursor.execute(query)
    actors = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(actors)


# Route 2: Get top 5 rented films for a specific actor
@actor_bp.route("/api/actors/<int:actor_id>/top-films", methods=["GET"])
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
