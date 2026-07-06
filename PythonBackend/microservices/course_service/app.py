from flask import Flask, jsonify, request
import sqlite3, os

app = Flask(__name__)
DB = 'course_service.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS courses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     code TEXT UNIQUE NOT NULL,
                     credits INTEGER,
                     department TEXT)''')
    conn.commit()
    conn.close()

@app.route('/api/courses/', methods=['GET'])
def get_courses():
    conn = get_db()
    courses = [dict(r) for r in conn.execute('SELECT * FROM courses').fetchall()]
    conn.close()
    return jsonify(courses)

@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.get_json()
    conn = get_db()
    cur = conn.execute('INSERT INTO courses (name, code, credits, department) VALUES (?,?,?,?)',
                       (data['name'], data['code'], data['credits'], data.get('department', '')))
    conn.commit()
    course_id = cur.lastrowid
    conn.close()
    return jsonify({'id': course_id, **data}), 201

@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    conn = get_db()
    course = conn.execute('SELECT * FROM courses WHERE id=?', (course_id,)).fetchone()
    conn.close()
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(dict(course))

if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)
