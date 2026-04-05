from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"courses": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

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

# 🔒 получение видео через сервер (защита)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
if __name__ == "__main__":
    app.run()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
