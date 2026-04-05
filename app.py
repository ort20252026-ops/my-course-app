from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Конфигурация
ADMIN_ID = "ort20252026-ops"
DATA_FILE = "courses_data.json"

# Инициализация данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"courses": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Проверка админа
def is_admin(user_id):
    return user_id == ADMIN_ID

# API Endpoints
@app.route('/courses', methods=['GET'])
def get_courses():
    data = load_data()
    return jsonify({"courses": data["courses"]})

@app.route('/add_course', methods=['POST'])
def add_course():
    try:
        user_id = request.json.get('user_id')
        if not is_admin(user_id):
            return jsonify({"error": "Access denied"}), 403
        
        data = load_data()
        course = {
            "id": len(data["courses"]) + 1,
            "title": request.json.get('title'),
            "lessons": []
        }
        data["courses"].append(course)
        save_data(data)
        return jsonify(course), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/add_lesson', methods=['POST'])
def add_lesson():
    try:
        user_id = request.json.get('user_id')
        if not is_admin(user_id):
            return jsonify({"error": "Access denied"}), 403
        
        data = load_data()
        course_id = int(request.json.get('course_id'))
        
        for course in data["courses"]:
            if course["id"] == course_id:
                lesson = {
                    "id": len(course["lessons"]) + 1,
                    "title": request.json.get('title'),
                    "video": request.json.get('video')
                }
                course["lessons"].append(lesson)
                save_data(data)
                return jsonify(lesson), 201
        
        return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/delete_lesson', methods=['POST'])
def delete_lesson():
    try:
        user_id = request.json.get('user_id')
        if not is_admin(user_id):
            return jsonify({"error": "Access denied"}), 403
        
        data = load_data()
        course_id = int(request.json.get('course_id'))
        lesson_id = int(request.json.get('lesson_id'))
        
        for course in data["courses"]:
            if course["id"] == course_id:
                course["lessons"] = [l for l in course["lessons"] if l["id"] != lesson_id]
                save_data(data)
                return jsonify({"success": True}), 200
        
        return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/delete_course', methods=['POST'])
def delete_course():
    try:
        user_id = request.json.get('user_id')
        if not is_admin(user_id):
            return jsonify({"error": "Access denied"}), 403
        
        data = load_data()
        course_id = int(request.json.get('course_id'))
        data["courses"] = [c for c in data["courses"] if c["id"] != course_id]
        save_data(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000}