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
        result = Mentor.find_all(Mentor, mysql)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found

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

# Mentors CRDU by id
@app.route("/Account/Mentors/<int:id>", methods = ['GET', 'UPDATE', 'DELETE'])
def find_mentors_by_id (id):
    if request.method   == 'GET':
        result = Mentor.find_by_id(Mentor, mysql, id)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found

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
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found


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


# All students CRDU
@app.route("/Account/Students/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_students ():
    if request.method   == 'GET':
        result = Student.find_all(Student, mysql)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found

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
        expired = Student.email_verification_in_date(Student, mysql, token, id) # Hold true if verification expired
        result = Student.account_activate(Student, mysql, id, token)
        if id is None or token is None:
            return jsonify({'status': 111,'report': 'Missing arguments'}), 400 # Missing arguments
        elif expired is True:
            return jsonify({'status': 105,'report': 'Verification expired'}), 400 # Wrong answer
        elif result is True:
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
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found

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
            return jsonify({'Status': 111, 'report':'Missing arguments'}), 400 # Missing arguments
        elif is_active is False:
            return jsonify({'status': 445, 'report': 'Access denied: account not active'}), 400 # Missing arguments
        else:
            id = Student.authenticate(Student, mysql, username, password)
            if id is not None:
                return json.dumps({'status': 100, 'report':'Success', 'id': id }), 201 # Success
            else:
                return jsonify({'status': 444, 'report': 'Access denied: Check you credentials'}), 400 # Missing arguments
    else:
        return jsonify({'Status': 'Error: Bad request'}), 404 # Bad request


# Courses
@app.route("/Courses/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_courses ():
    if request.method   == 'GET':
        result = Course.find_all(Course, mysql)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found


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

# Courses by id
@app.route("/Courses/<int:id>", methods = ['GET', 'UPDATE', 'DELETE'])
def find_course_by_id (id):
    if request.method   == 'GET':
        result = Course.find_by_id(Course, mysql, id)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found

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
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found
    else:
        return jsonify({'Status': 'Error: Bad request'}), 400 # Bad request

# Courses by search
@app.route("/Courses/Search/<string:search>", methods = ['GET'])
def search_course (search):
    if request.method   == 'GET':
        result = Course.search(Course, mysql, search)
        if result is not None:
            return result # Json encoded response
        else:
            return jsonify({'Status': 'Error: No results was found'}), 404 # No results were found
    else:
        return jsonify({'Status': 'Error: Bad request'}), 400 # Bad request



if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=8000, debug = True)
