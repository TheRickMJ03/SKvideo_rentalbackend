# app/routes/rent.py
from flask import Blueprint, request, jsonify
from app.database import get_db_connection
from datetime import datetime

rent_bp = Blueprint("rent", __name__)

@rent_bp.route("/rent", methods=["POST"])
def rent_film():
    data = request.get_json()
    film_id = data.get("film_id")
    customer_id = data.get("customer_id")

    if not film_id or not customer_id:
        return jsonify({"error": "Missing film_id or customer_id"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Get an available inventory item for this film
        cursor.execute("""
            SELECT inventory_id FROM inventory
            WHERE film_id = %s
            LIMIT 1
        """, (film_id,))
        inventory_item = cursor.fetchone()

        if not inventory_item:
            return jsonify({"error": "No inventory available for this film"}), 404

        inventory_id = inventory_item['inventory_id']

        # 2. Create the rental record
        rental_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id)
            VALUES (%s, %s, %s, NULL, 1)
        """, (rental_date, inventory_id, customer_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Film rented successfully!"}), 201

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"error": str(e)}), 500
