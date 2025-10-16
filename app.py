from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- DATABASE SETUP ---
def get_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            level_air REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- API UNTUK ESP32 ---
@app.route("/api/post_data", methods=["POST"])
def post_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "msg": "no json"}), 400

    temperature = data.get("temperature")
    humidity = data.get("humidity")
    level_air = data.get("level_air")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    conn.execute(
        "INSERT INTO sensor_data (timestamp, temperature, humidity, level_air) VALUES (?, ?, ?, ?)",
        (timestamp, temperature, humidity, level_air)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 200


# --- API UNTUK DASHBOARD ---
@app.route("/api/get_data", methods=["GET"])
def get_data():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM sensor_data ORDER BY id DESC LIMIT 20"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


# --- DASHBOARD WEB ---
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
