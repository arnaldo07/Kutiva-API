# mentor.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is students model which wil handle all student  functions
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, jsonify, request, json
from time import gmtime, strftime
from models.mentor import Mentor

class Lesson():

    # Set table name
    def table_name(self):
        return "lesson"



    # Creates a course
    def create(self, mysql, lesson_title, lesson_path, lesson_length, lesson_locked, lesson_section_number, lesson_section_name,
    lesson_course_id):
        '''
        Inserts new lesson to the database

        Parameters:
            mysql: Mysql connection cursor
            lesson_title : type(string) is the lesson name
            lesson_path: type(string) is the uploaded lesson path
            lesson_length:type(time) lesson duration time
            lesson_locked: type(boolean) TRUE if lesson is locked for preview else FALSE
            lesson_section_number: section hierarchal number
            lesson_section_name: the name of the section
            lesson_course_id: type(int) the lesson course id

        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (lesson_title, lesson_location_path, lesson_length_time, lesson_locked, lesson_section_number,
        lesson_section_name, lesson_course_id) VALUES
        ('{}', '{}', '{}', '{}', '{}', '{}', {} )'''.format(self.table_name(self), lesson_title, lesson_path, lesson_length, lesson_locked,
        lesson_section_number, lesson_section_name, lesson_course_id )
        row = cursor.execute(sql)
        mysql.get_db().commit()
        if row is 1:
            return cursor.lastrowid # last inserted id
        else:
            return None
