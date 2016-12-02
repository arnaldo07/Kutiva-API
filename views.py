# views.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is the view level which defines view to be displyed according to the routes
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, request, jsonify, abort
from flask.ext.mysql import MySQL
from models.mentor import Mentor
from models.student import Student
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
        first_name   = request.args.get('first_name')
        last_name    = request.args.get('last_name')
        category     = request.args.get('category')
        email        = request.args.get('email')
        country_code = request.args.get('country_code')
        phone        = request.args.get('phone')
        password     = hashlib.md5(request.args.get('password').encode()).hexdigest() # Hash password

        if first_name is None or last_name is None or category is None or email is None or country_code is None or phone is None or password is None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        elif Mentor.exists(Mentor, mysql, email, phone) is True:
            return jsonify({'Status': 'Error: Mentor already exists'}), 400 # Mentor already exists
        else:
            if Mentor.create(Mentor, mysql, first_name, last_name, category, email, country_code, phone, password) is True:
                return jsonify({'Status': 'Sucess'}), 201 # Success
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
@app.route("/Account/Student/<int:id>", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
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
        first_name   = request.args.get('first_name')
        last_name    = request.args.get('last_name')
        gender       = request.args.get('gender')
        age          = request.args.get('age')
        email        = request.args.get('email')
        country_code = request.args.get('country_code')
        phone        = request.args.get('phone')
        password     = hashlib.md5(request.args.get('password').encode()).hexdigest() # Hash password

        if first_name is None or last_name is None or gender is None or age is None or email is None or country_code is None or phone is None or password is None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        elif Student.exists(Student, mysql, email, phone) is True:
            return jsonify({'Status': 'Error: Student already exists'}), 400 # Mentor already exists
        else:
            if Student.create(Student, mysql, first_name, last_name, gender, age, email, country_code, phone, password) is True:
                return jsonify({'Status': 'Sucess'}), 201 # Success
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
        username   = request.args.get('username')
        password   = hashlib.md5(request.args.get('password').encode()).hexdigest() # Hash password

        if username is None or password is None:
            return jsonify({'Status': 'Error: Missing arguments'}), 400 # Missing arguments
        else:
            id = Student.authenticate(Student, mysql, username, password)
            if id is not None:
                return jsonify({'id': id }), 201 # Success
            else:
                return jsonify({'Status': 'Error: Check you credentials'}), 400 # Missing arguments
    else:
        return jsonify({'Status': 'Error: Bad request'}), 400 # Bad request


if __name__ == "__main__":
    app.run()
