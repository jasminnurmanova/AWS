from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Database configuration - REPLACE THESE WITH YOUR ACTUAL CREDENTIALS
DB_HOST = "db-jasmin.c32geugqgvkj.ap-southeast-1.rds.amazonaws.com"
DB_NAME = "db_jasmin"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_PORT = "5432"

# Table name
TABLE_NAME = "tbl_jasmin_marvel_characters_dataset"

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/api/characters', methods=['GET'])
def get_characters():
    """Get all characters from the database"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"SELECT * FROM {TABLE_NAME}")
            characters = cur.fetchall()

            # Convert to list of dictionaries
            result = []
            for character in characters:
                result.append(dict(character))

        conn.close()
        return jsonify(result)

    except Exception as e:
        print(f"Error getting characters: {e}")
        return jsonify({"error": "Failed to retrieve characters"}), 500

@app.route('/api/characters', methods=['POST'])
def add_character():
    """Add a new character to the database"""
    try:
        character_data = request.json

        # Validate required fields
        required_fields = ['Character', 'Real Name', 'affiliation', 'powers', 'Role', 'Power Level']
        for field in required_fields:
            if field not in character_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        with conn.cursor() as cur:
            # Construct query dynamically
            columns = ', '.join([f'"{key}"' for key in character_data.keys()])
            placeholders = ', '.join(['%s'] * len(character_data))

            query = f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})'
            cur.execute(query, list(character_data.values()))

        conn.commit()
        conn.close()

        return jsonify({"message": "Character added successfully"})

    except Exception as e:
        print(f"Error adding character: {e}")
        return jsonify({"error": "Failed to add character"}), 500

@app.route('/api/characters', methods=['DELETE'])
def delete_characters():
    """Delete selected characters from the database"""
    try:
        data = request.json
        characters_to_delete = data.get('characters', [])

        if not characters_to_delete:
            return jsonify({"error": "No characters specified for deletion"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        with conn.cursor() as cur:
            # Use parameterized query with placeholders
            placeholders = ', '.join(['%s'] * len(characters_to_delete))
            query = f'DELETE FROM {TABLE_NAME} WHERE "Character" IN ({placeholders})'
            cur.execute(query, characters_to_delete)

        conn.commit()
        conn.close()

        return jsonify({"message": "Characters deleted successfully"})

    except Exception as e:
        print(f"Error deleting characters: {e}")
        return jsonify({"error": "Failed to delete characters"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    # Run the app on all available interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)