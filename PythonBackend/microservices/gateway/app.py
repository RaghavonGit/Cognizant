from flask import Flask, request, jsonify, Response
import requests as req

app = Flask(__name__)

COURSE_SERVICE = 'http://localhost:5001'
STUDENT_SERVICE = 'http://localhost:5002'

def proxy(service_url, path):
    url = f"{service_url}{path}"
    try:
        resp = req.request(
            method=request.method,
            url=url,
            json=request.get_json(silent=True),
            params=request.args,
            timeout=5
        )
        return Response(resp.content, status=resp.status_code, content_type='application/json')
    except req.exceptions.ConnectionError:
        return jsonify({'error': f'Service unavailable'}), 503

@app.route('/api/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def courses_proxy(path):
    return proxy(COURSE_SERVICE, f'/api/courses/{path}')

@app.route('/api/courses/', methods=['GET', 'POST'])
def courses_list_proxy():
    return proxy(COURSE_SERVICE, '/api/courses/')

@app.route('/api/students/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def students_proxy(path):
    return proxy(STUDENT_SERVICE, f'/api/students/{path}')

@app.route('/api/students/', methods=['GET', 'POST'])
def students_list_proxy():
    return proxy(STUDENT_SERVICE, '/api/students/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
