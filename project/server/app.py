from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------- ПУТИ ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "../web")
DATA_FILE = os.path.join(BASE_DIR, "data.json")
DB_FILE = os.path.join(BASE_DIR, "../database/db.sqlite3")

OWNER_ID = 123456789  # ⚠️ ВСТАВЬ СВОЙ TELEGRAM ID

# ---------- БАЗА ----------
def get_db():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- ДАННЫЕ ----------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"courses": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- FRONTEND ----------
@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(WEB_DIR, path)

# ---------- AUTH ----------
@app.route("/auth", methods=["POST"])
def auth():
    body = request.json

    user_id = body["id"]
    username = body.get("username", "")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()

    if not user:
        cur.execute(
            "INSERT INTO users (id, username, is_admin) VALUES (?, ?, 0)",
            (user_id, username)
        )
        conn.commit()

    cur.execute("SELECT id, username, is_admin FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()

    conn.close()

    return jsonify({
        "id": user[0],
        "username": user[1],
        "is_admin": user[2]
    })

# ---------- АДМИН ----------
@app.route("/add_admin", methods=["POST"])
def add_admin():
    body = request.json

    if body["owner_id"] != OWNER_ID:
        return jsonify({"error": "not allowed"})

    new_admin_id = body["user_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE users SET is_admin=1 WHERE id=?", (new_admin_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

# ---------- API ----------
@app.route("/courses")
def get_courses():
    return jsonify(load_data()["courses"])

@app.route("/add_course", methods=["POST"])
def add_course():
    data = load_data()
    body = request.json

    new_course = {
        "id": len(data["courses"]) + 1,
        "title": body.get("title"),
        "lessons": []
    }

    data["courses"].append(new_course)
    save_data(data)

    return jsonify({"status": "ok"})

@app.route("/add_lesson", methods=["POST"])
def add_lesson():
    data = load_data()
    body = request.json

    for c in data["courses"]:
        if c["id"] == int(body["course_id"]):
            c["lessons"].append({
                "title": body.get("title", "Без названия"),
                "video": body["video"]
            })

    save_data(data)
    return jsonify({"status": "ok"})

@app.route("/delete_lesson", methods=["POST"])
def delete_lesson():
    data = load_data()
    body = request.json

    for c in data["courses"]:
        if c["id"] == int(body["course_id"]):
            if len(c["lessons"]) > int(body["index"]):
                c["lessons"].pop(int(body["index"]))

    save_data(data)
    return jsonify({"status": "deleted"})

@app.route("/get_video")
def get_video():
    course_id = int(request.args.get("course_id"))
    index = int(request.args.get("index"))

    data = load_data()

    for c in data["courses"]:
        if c["id"] == course_id:
            video = c["lessons"][index]["video"]
            return jsonify({"video": video})

    return jsonify({"error": "not found"})

# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
