# app.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is the view level which defines view to be displyed according to the routes
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, request, jsonify, json
from flaskext.mysql import MySQL
from models.mentor import Mentor
from models.student import Student
from models.course import Course
from models.lesson import Lesson
from utils import Utils
import hashlib
import os, shutil
from werkzeug.utils import secure_filename

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
        result = Mentor.find_all(Mentor, mysql)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 'Error: No results was found'}), 404 # No results were found

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
            return jsonify({'status': 111,'report': 'Error: Missing arguments'}), 400 # Missing arguments
        elif Mentor.email_exists(Mentor, mysql, email) is True:
            return jsonify({'status': 'Error: Mentor already exists'}), 400 # Mentor already exists
        else:
            result = Mentor.create(Mentor, mysql, first_name, last_name, category, email, country_code, phone, password)
            if result is not None:
                return jsonify({'status': 'Sucess', 'id': result}), 201 # Success
            else:
                return jsonify({'status': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem

# Mentors CRDU by id
@app.route("/Account/Mentors/<int:id>", methods = ['GET', 'UPDATE', 'DELETE'])
def find_mentors_by_id (id):
    if request.method   == 'GET':
        result = Mentor.find_by_id(Mentor, mysql, id)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 'Error: No results was found'}), 404 # No results were found

    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"

# Mentor by category
@app.route("/Account/Mentors/<string:category>", methods = ['GET'])
def find_mentors_by_category (category):
    if request.method   == 'GET':
        result = Mentor.find_by_category(Mentor, mysql, category)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 'Error: No results was found'}), 404 # No results were found


    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"

# Mentor login
@app.route("/Account/Mentors/Login/", methods = ['POST'])
def login_mentors():
    if request.method == 'POST':
        username   = request.json.get('username')
        password   = hashlib.md5(request.json.get('password').encode()).hexdigest() # Hash password

        if username is None or password is None:
            return jsonify({'status': 111,'report': 'Error: Missing arguments'}), 400 # Missing arguments
        else:
            id = Mentor.authenticate(Mentor, mysql, username, password)
            if id is not None:
                return jsonify({'id': id }), 201 # Success
            else:
                return jsonify({'status': 'Error: Check you credentials'}), 400 # Missing arguments
    else:
        return jsonify({'status': 'Error: Bad request'}), 400 # Bad request


# All students CRDU
@app.route("/Account/Students/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_students ():
    if request.method   == 'GET':
        result = Student.find_all(Student, mysql)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 'Error: No results was found'}), 404 # No results were found

    # POST student data
    elif request.method == 'POST':
        first_name   = request.json.get('first_name')
        last_name    = request.json.get('last_name')
        email        = request.json.get('email')
        password     = hashlib.md5(request.json.get('password').encode()).hexdigest() # Hash password

        if first_name is None or last_name is None or email is None or password is None:
            return jsonify({'status': 111,'report': 'Error: Missing arguments'}), 400 # Missing arguments
        elif Student.email_exists(Student, mysql, email ) is True:
            return jsonify({'status': 222, 'report': 'Error: Student already exists'}), 400 # Mentor already exists
        else:
            token, id = Student.create(Student, mysql, first_name, last_name, email, password)
            if  token is not None:
                return jsonify({'status': 100, 'report': 'Success', 'student_id': id, 'token': token }), 201 # Success
            else:
                return jsonify({'status': 333 ,'report': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem

    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"


# Create student account email verification
@app.route("/Account/Students/CreateActivation/", methods = ['POST'])
def student_create_email_activation():
    if request.method == 'POST':
        id = request.json.get('id')
        token = Student.create_email_verification(Student, mysql, id)
        if token is None:
            return jsonify({'status': 333 ,'report': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem
        else:
            return jsonify({'status': 100, 'report': 'Success', 'student_id': id, 'token': token }), 201 # Success


# Student account email activation
@app.route("/Account/Students/Activate/", methods = ['POST'])
def student_account_activation():
    if request.method == 'POST':
        id    = request.json.get('id')
        token = request.json.get('token')
        if id is None or token is None:
            return jsonify({'status': 111,'report': 'Missing arguments'}), 400 # Missing arguments
        else:
            in_date = Student.email_verification_in_date(Student, mysql, token, id) # Hold true if verification expired
            if in_date is False:
                return jsonify({'status': 105,'report': 'Verification expired'}), 400 # Wrong answer
            elif Student.account_activate(Student, mysql, id) is True:
                Student.desactivate_email_verification(Student, mysql, token, id)
                return jsonify({'status': 100,'report': 'Success'}), 200 # Sucess
            else:
                return jsonify({'status': 444,'report': 'Access denied'}), 400 # Wrong answer

# CRDU Student by id
@app.route("/Account/Students/<int:id>", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_student_by_id (id):
    if request.method   == 'GET':
        result = Student.find_by_id(Student, mysql, id)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 444, 'reoprt': 'Error: No results was found'}), 404 # No results were found

    elif request.method == 'POST':
        return"POST by "+str(id)
    elif request.method == 'UPDATE':
        return "UPDATESby "+str(id)
    elif request.method == 'DELETE':
        return "DELETES by "+str(id)

# Students login
@app.route("/Account/Students/Login/", methods = ['POST'])
def login_students():
    if request.method == 'POST':
        username   = request.json.get('username')
        password   = hashlib.md5(request.json.get('password').encode()).hexdigest() # Hash password
        is_active = Student.is_active(Student, mysql, username)
        if username is None or password is None:
            return jsonify({'status': 111, 'report':'Missing arguments'}), 400 # Missing arguments
        else:
            id = Student.authenticate(Student, mysql, username, password)
            if id is not None:
                if is_active is True:
                    return json.dumps({'status': 100, 'report':'Success', 'id': id }), 201 # Success
                else:
                    return jsonify({'status': 445, 'report': 'Access denied: account not active'}), 400 # Acces denied
            else:
                return jsonify({'status': 444, 'report': 'Access denied: Check you credentials'}), 400 # credentials
    else:
        return jsonify({'status': 'Error: Bad request'}), 404 # Bad request


# Courses
@app.route("/Courses/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_courses ():
    if request.method   == 'GET':
        result = Course.find_all(Course, mysql)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 444, 'reoprt': 'Error: No results was found'}), 404 # No results were found

    # POST course data
    elif request.method == 'POST':

        course_name          = request.json.get('course_name')
        course_category      = request.json.get('course_category')
        course_description   = request.json.get('course_description')
        course_price         = request.json.get('course_price')
        course_duration_time = request.json.get('course_duration_time')
        course_audience_level= request.json.get('course_audience_level')
        course_tags          = request.json.get('course_tags')
        mentor_id            = request.json.get('mentor_id')
        cover_image_path     = request.json.get('cover_image')

        if course_name is None or course_category is None or course_description is None or course_price is None or course_duration_time is None or course_audience_level is None or course_tags is None or cover_image_path is None or mentor_id is None:
            return jsonify({'status': 111,'report': 'Error: Missing arguments'}), 400 # Missing arguments
        else:
            result = Course.create(Course, mysql, course_name, course_category, course_description, course_price, course_duration_time,
            course_audience_level, course_tags, cover_image_path, mentor_id)
            if result is not None:
                return jsonify({'status': 100, 'report':'Sucess', 'id': result}), 201 # Success
            else:
                return jsonify({'status': 333 ,'report': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem

    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"

# Courses by id
@app.route("/courses/<int:id>", methods = ['GET', 'UPDATE', 'DELETE'])
def find_course_by_id (id):
    if request.method   == 'GET':
        result = Course.find_by_id(Course, mysql, id)
        if result is not None:
            return jsonify({'status': 100, 'report': 'Success', 'course': result}), 200 # Success
        else:
            return jsonify({'status': 444, 'report': 'Error: No results was found'}), 404 # No results were found

    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"

# Courses by category
@app.route("/Courses/<string:category>", methods = ['GET'])
def find_course_by_category (category):
    if request.method   == 'GET':
        result = Course.find_by_category(Course, mysql, category)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 444, 'reoprt': 'Error: No results was found'}), 404 # No results were found
    else:
        return jsonify({'status': 445, 'report': 'Error: Bad request'}), 400 # Bad request

# Courses by search
@app.route("/Courses/Search/<string:search>", methods = ['GET'])
def search_course (search):
    if request.method   == 'GET':
        result = Course.search(Course, mysql, search)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'status': 444, 'reoprt': 'Error: No results was found'}), 404 # No results were found
    else:
        return jsonify({'status': 445, 'report': 'Error: Bad request'}), 400 # Bad request


# Lesson
@app.route("/Course/Lessons/Create", methods = ['POST'])
def create_lesson():
    if request.method == 'POST':
        lesson_title  = request.json.get('lesson_title')
        lesson_path   = request.json.get('lesson_path')
        lesson_length = '5:03'
        lesson_locked = request.json.get('lesson_locked')
        lesson_section_number  = 1
        lesson_section_name  = request.json.get('lesson_section_name')
        lesson_course_id = request.json.get('course_id')
        lesson_mentor_id = request.json.get('mentor_id')

        if lesson_title is None or lesson_path is None or lesson_length is None or lesson_locked is None or lesson_section_number is None or lesson_section_name is None or lesson_course_id is None or lesson_mentor_id is None:
            return jsonify({'status': 111,'report': 'Error: Missing arguments'}), 400 # Missing arguments
        else:
            # check if course exists
            exists = Course.find_by_ids(Course, mysql, lesson_mentor_id, lesson_course_id)
            if exists is not None:
                result = Lesson.create(Lesson, mysql, lesson_title, lesson_path, lesson_length, lesson_locked, lesson_section_number,
                lesson_section_name, lesson_course_id) # create lesson
                if result is not None:
                    return jsonify({'status': 100, 'report': 'Success', 'lesson_id': result, 'course_id': lesson_course_id }), 201 # Success
                else:
                    return jsonify({'status': 333 ,'report': 'Error: Ups, Something went wrong, we don´t know what'}), 400 # Any database problem
            else:
                return jsonify({'status': 445, 'report': 'Error: Bad request'}), 400 # Bad request

# Display lessons by course id
@app.route('/lessons/<int:course_id>', methods=['GET'])
def lesson_by_course(course_id):
    if request.method == 'GET':
        result = Lesson.find_by_course(Lesson, mysql, course_id );
        if result is not None:
            return jsonify({'status': 100, 'report': 'Success', 'lessons': result}), 200 # Success
        else:
            return jsonify({'status': 445, 'report': 'Error: No results was found'}), 404 # No results were found
    else:
        return jsonify({'status': 445, 'report': 'Error: Bad request'}), 400 # Bad request




if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8000, debug = True)
