from flask import Flask, request, jsonify
from flask import Flask
from models.mentor import Mentor
from config import *

app = Flask(__name__)

# Display index page
@app.route('/')
def index():
    return ''

# All mentors CRDU
@app.route("/Account/Mentors/", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_all_mentors ():
    if request.method   == 'GET':
        return 'GET'
    elif request.method == 'POST':
        return"POST"
    elif request.method == 'UPDATE':
        return "UPDATES"
    elif request.method == 'DELETE':
        return "DELETES"

# CRDU mentor by id
@app.route("/Account/Mentors/<int:id>", methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def find_mentor_by_id (id):
    if request.method   == 'GET':
        return "GET by "+str(id)
    elif request.method == 'POST':
        return"POST by "+str(id)
    elif request.method == 'UPDATE':
        return "UPDATESby "+str(id)
    elif request.method == 'DELETE':
        return "DELETES by "+str(id)



if __name__ == "__main__":
    app.debug = 'TRUE'
    app.run()
