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


