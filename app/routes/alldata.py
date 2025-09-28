from flask import Blueprint, jsonify, request
from app.database import get_db_connection

alldatabp = Blueprint("alldata", __name__)

@alldatabp.route("/films", methods=["GET"])
def get_all_films():
    search = request.args.get("search", "").strip()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    base_query = """
        SELECT
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            GROUP_CONCAT(DISTINCT c.name ORDER BY c.name SEPARATOR ', ') AS genre,
            GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) ORDER BY a.last_name, a.first_name SEPARATOR ', ') AS actors,
            COUNT(DISTINCT r.rental_id) AS rental_count
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        LEFT JOIN inventory i ON f.film_id = i.film_id
        LEFT JOIN rental r ON i.inventory_id = r.inventory_id
        LEFT JOIN film_actor fa ON f.film_id = fa.film_id
        LEFT JOIN actor a ON fa.actor_id = a.actor_id
    """

    where_clauses = []
    params = []

    if search:
        like_pattern = f"%{search}%"

        if search.isdigit():
            where_clauses.append("""
                (
                    f.film_id = %s OR
                    f.title LIKE %s OR
                    c.name LIKE %s OR
                    a.first_name LIKE %s OR
                    a.last_name LIKE %s
                )
            """)
            params.extend([int(search), like_pattern, like_pattern, like_pattern, like_pattern])
        else:
            where_clauses.append("""
                (
                    f.title LIKE %s OR
                    c.name LIKE %s OR
                    a.first_name LIKE %s OR
                    a.last_name LIKE %s
                )
            """)
            params.extend([like_pattern]*4)

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    group_order_sql = """
        GROUP BY f.film_id, f.title, f.description, f.release_year
        ORDER BY f.title ASC
    """

    query = base_query + where_sql + group_order_sql

    cursor.execute(query, tuple(params))
    films = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(films)
