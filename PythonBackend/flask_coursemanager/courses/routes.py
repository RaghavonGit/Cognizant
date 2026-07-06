from flask import Blueprint, request, jsonify
from extensions import db
from courses.models import Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code

@courses_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return make_response_json([c.to_dict() for c in courses])

@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON body provided'}), 400
    required = ['name', 'code', 'credits', 'department_id']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    course = Course(name=data['name'], code=data['code'], credits=data['credits'], department_id=data['department_id'])
    db.session.add(course)
    db.session.commit()
    return make_response_json(course.to_dict(), 201)

@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict())

@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON body provided'}), 400
    course.name = data.get('name', course.name)
    course.code = data.get('code', course.code)
    course.credits = data.get('credits', course.credits)
    db.session.commit()
    return make_response_json(course.to_dict())

@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Course deleted'}), 200

@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_enrolled_students(course_id):
    course = Course.query.get_or_404(course_id)
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    students = [e.student.to_dict() for e in enrollments]
    return make_response_json(students)
