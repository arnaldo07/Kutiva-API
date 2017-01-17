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

    # finds lessons by course id
    def find_by_course(self, mysql, course_id ):
        '''
        Selects lessons by course_id ordered by section number
        Parameters:
            mysql: Mysql connection cursor
            course_id: the lessons course id
        '''
        cursor = mysql.get_db().cursor()
        sql = '''SELECT * FROM {} WHERE lesson_course_id = {} order by lesson_section_number , lesson_id asc'''.format(self.table_name(self),
        course_id);
        cursor.execute(sql)
        row = cursor.fetchall()
        if row is None:
            return None
        else:
            result = []
            for i in row:
                data = {
                    'id':                        i[0],
                    'lesson_title':              i[1],
                    'lesson_path':               i[2],
                    'lesson_length':             str(i[3]),
                    'lesson_locked':             i[4], # defines wether is locked for previews
                    'lesson_section_number':     i[5],
                    'lesson_section_name':       i[6],
                    'lesson_course_id':          i[7],
                    }
                result.append(data)
            return result

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
