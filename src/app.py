import os

import psycopg
from dotenv import load_dotenv
from flask import Flask, jsonify
from psycopg.rows import dict_row


load_dotenv()

app = Flask(__name__)


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        row_factory=dict_row,
        connect_timeout=5
    )


@app.get("/health")
def health_check():
    return jsonify(
        {
            "service": "clinical-trials-data-quality-api",
            "status": "healthy"
        }
    )


@app.get("/api/quality-overview")
def quality_overview():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vw_quality_overview;")
                overview = cursor.fetchone()

        if overview is None:
            return jsonify({"error": "No quality overview data found"}), 404

        return jsonify(overview)

    except psycopg.Error:
        app.logger.exception("Database query failed")
        return jsonify({"error": "Unable to retrieve quality overview"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)