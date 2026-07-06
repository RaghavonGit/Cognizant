from flask import Flask, jsonify, request
import sqlite3, requests as req

app = Flask(__name__)
DB = 'student_service.db'
COURSE_SERVICE = 'http://localhost:5001'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     first_name TEXT, last_name TEXT,
                     email TEXT UNIQUE, enrollment_year INTEGER)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS enrollments
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     student_id INTEGER, course_id INTEGER,
                     UNIQUE(student_id, course_id))''')
    conn.commit()
    conn.close()

@app.route('/api/students/', methods=['GET'])
def get_students():
    conn = get_db()
    students = [dict(r) for r in conn.execute('SELECT * FROM students').fetchall()]
    conn.close()
    return jsonify(students)

@app.route('/api/students/', methods=['POST'])
def create_student():
    data = request.get_json()
    conn = get_db()
    cur = conn.execute('INSERT INTO students (first_name, last_name, email, enrollment_year) VALUES (?,?,?,?)',
                       (data['first_name'], data['last_name'], data['email'], data.get('enrollment_year')))
    conn.commit()
    student_id = cur.lastrowid
    conn.close()
    return jsonify({'id': student_id, **data}), 201

@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    data = request.get_json()
    course_id = data.get('course_id')
    try:
        # Verify course exists by calling Course Service
        resp = req.get(f'{COURSE_SERVICE}/api/courses/{course_id}/', timeout=3)
        if resp.status_code == 404:
            return jsonify({'error': 'Course not found'}), 404
    except req.exceptions.ConnectionError:
        return jsonify({'error': 'Course Service unavailable'}), 503
    conn = get_db()
    conn.execute('INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES (?,?)',
                 (student_id, course_id))
    conn.commit()
    conn.close()
    return jsonify({'student_id': student_id, 'course_id': course_id}), 201

if __name__ == '__main__':
    init_db()
    app.run(port=5002, debug=True)
