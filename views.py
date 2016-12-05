# views.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is the view level which defines view to be displyed according to the routes
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, request, jsonify, json
from flask.ext.mysql import MySQL
from models.mentor import Mentor
from models.student import Student
from models.course import Course
from utils import Utils
import hashlib

mysql = MySQL()
app = Flask(__name__)
app.config.from_object('config')
mysql.init_app(app)


# Display index page
@app.route('/')
def index():
    return ''


# All mentors CRDU
@app.route("/Account/Mentors/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_mentors ():
    if request.method   == 'GET':
        return Mentor.find_all(Mentor, mysql)

    # POST Mentors data
    elif request.method == 'POST':
        first_name   = request.json.get('first_name')
        last_name    = request.json.get('last_name')
        category     = request.json.get('category')
        email        = request.json.get('email')
        country_code = request.json.get('country_code')
        phone        = request.json.get('phone')
        password     = hashlib.md5(request.json.get('password').encode()).hexdigest() # Hash password

        if first_name is None or last_name is None or category is None or email is None or country_code is None or phone is None or password is None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        elif Mentor.exists(Mentor, mysql, email, phone) is True:
            return jsonify({'Status': 'Error: Mentor already exists'}), 400 # Mentor already exists
        else:
            result = Mentor.create(Mentor, mysql, first_name, last_name, category, email, country_code, phone, password)
            if result is not None:
                return jsonify({'Status': 'Sucess', 'id': result}), 201 # Success
            else:
                return jsonify({'Status': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem

    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"


# Mentor login
@app.route("/Account/Mentors/Login/", methods = ['POST'])
def login_mentors():
    if request.method == 'POST':
        username   = request.args.get('username')
        password   = hashlib.md5(request.args.get('password').encode()).hexdigest() # Hash password

        if username is None or password is None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        else:
            id = Mentor.authenticate(Mentor, mysql, username, password)
            if id is not None:
                return jsonify({'id': id }), 201 # Success
            else:
                return jsonify({'Status': 'Error: Check you credentials'}), 400 # Missing arguments
    else:
        return jsonify({'Status': 'Error: Bad request'}), 400 # Bad request


# CRDU mentor by id
@app.route("/Account/Students/<int:id>", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_student_by_id (id):
    if request.method   == 'GET':
        return Mentor.find_by_id(Mentor, mysql, id)
    elif request.method == 'POST':
        return"POST by "+str(id)
    elif request.method == 'UPDATE':
        return "UPDATESby "+str(id)
    elif request.method == 'DELETE':
        return "DELETES by "+str(id)


# All students CRDU
@app.route("/Account/Students/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_students ():
    if request.method   == 'GET':
        return ''

    # POST student data
    elif request.method == 'POST':
        first_name   = request.json.get('first_name')
        last_name    = request.json.get('last_name')
        gender       = request.json.get('gender')
        birthdate    = request.json.get('birthdate')
        email        = request.json.get('email')
        country_code = request.json.get('country_code')
        phone        = request.json.get('phone')
        password     = hashlib.md5(request.json.get('password').encode()).hexdigest() # Hash password

        if first_name is None or last_name is None or gender is None or birthdate is None or email is None or country_code is None or phone is None or password is None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        elif Student.exists(Student, mysql, email, phone) is True:
            return jsonify({'Status': 'Error: Student already exists'}), 400 # Mentor already exists
        else:
            result = Student.create(Student, mysql, first_name, last_name, gender, birthdate, email, country_code, phone, password)
            if  result is not None:
                return jsonify({'Status': 'Sucess', 'id': result}), 201 # Success
            else:
                return jsonify({'Status': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem


    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"


# Mentor login
@app.route("/Account/Students/Login/", methods = ['POST'])
def login_students():
    if request.method == 'POST':
        username   = request.json.get('username')
        password   = hashlib.md5(request.json.get('password').encode()).hexdigest() # Hash password

        if username is None or password is None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        else:
            id = Student.authenticate(Student, mysql, username, password)
            if id is not None:
                return json.dumps({'id': id }), 201 # Success
            else:
                return jsonify({'Status': 'Error: Check you credentials'}), 400 # Missing arguments
    else:
        return jsonify({'Status': 'Error: Bad request'}), 400 # Bad request


# Courses
@app.route("/Courses/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_courses ():
    if request.method   == 'GET':
        return Course.find_all(Course, mysql)

    # POST course data
    elif request.method == 'POST':
        course_name          = request.json.get('course_name')
        course_category      = request.json.get('course_category')
        course_description   = request.json.get('course_description')
        course_duration_time = request.json.get('course_duration_time')

        if course_name is not None or course_category is not None or course_description is not None or course_duration_time is not None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        else:
            mentor_id = session['mentor_id']
            result = Course.create(Course, mysql, course_name, course_category, course_description, course_price, course_duration_time, mentor_id)
            if result is not None:
                return jsonify({'Status': 'Sucess', 'id': result}), 201 # Success
            else:
                return jsonify({'Status': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem

    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"


if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8000, debug = True)
