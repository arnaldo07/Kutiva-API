# mentor.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is students model which wil handle all student  functions
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, jsonify, request, json
from time import gmtime, strftime
from models.mentor import Mentor
import hashlib

class Course():

    # Set table name
    def table_name(self):
        return "course"

    # Set course_mentor table name
    def course_mentor_table_name(self):
        return "course_mentor"

    # Set course_image table name
    def course_image_table_name(self):
        return "course_image"


    def find_all(self, mysql):
        '''
        Find all courses

        '''
        cursor = mysql.get_db().cursor()
        sql = '''SELECT * FROM {} JOIN {} JOIN {} JOIN {} WHERE (course_image_course_id = course_id and course_id = cm_course_id
        and cm_mentor_id = mentor_id ) '''.format(self.table_name(self), self.course_mentor_table_name(self),
        self.course_image_table_name(self), Mentor.table_name(self))
        cursor.execute(sql)
        row = cursor.fetchall()

        if row is None:
            return None
        else:
            result = []
            for i in row:
                data = {
                    'course_id':                i[0],
                    'course_name':              i[1],
                    'course_category':          i[2],
                    'course_description':       i[3],
                    'course_price':             i[4],
                    'course_duration':          str(i[5]),
                    'course_stars':             i[6],
                    'course_status':            i[7],
                    'course_published':         i[8],
                    'course_image_id':          i[12],
                    'course_image_href':        i[13],
                    'course_image_active':      i[14],
                    'course_image_datetime':    i[15],
                    'mentor_id':                i[17],
                    'mentor_first_name':        i[18],
                    'mentor_last_name':         i[19],
                    'mentor_scope_category':    i[20],
                    'mentor_email':             i[21],
                    'mentor_country_code':      i[22],
                    'mentor_phone':             i[23],
                    'mentor_image':             i[24],
                    'mentor_status':            i[25],
                    'mentor_account_datetime':  i[26]
                    }
                result.append(data)

            return jsonify(result)

    # Create course_image table
    def course_image_table(self, mysql, image_path, course_id):
        '''
        Inserts course images location to datbase

        Parameters:
            mysql: Mysql connection cursor
            image_path : the image location path
            course_id: course identification

        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (course_image_path, course_image_course_id) VALUES ('{}', '{}')'''.format(self.course_image_table_name(self),
        image_path, course_id)
        row = cursor.execute(sql)
        mysql.get_db().commit()

        if row is 1:
            return course_id
        else:
            return None

    # Create course_mentor menay_to_many table
    def course_mentor_table(self, mysql, course_id, mentor_id):
        '''
        Inserts course_mentor which is many_to_many table of mentors
        and courses

        Parameters:
            mysql: Mysql connection cursor
            course_id : the course identification
            mentor_id: mentor identification

        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (cm_course_id, cm_mentor_id) VALUES ('{}', '{}')'''.format(self.course_mentor_table_name(self),
        course_id, mentor_id)
        row = cursor.execute(sql)
        mysql.get_db().commit()

        if row is 1:
            return course_id
        else:
            return None

    # Creates a course
    def create(self, mysql, course_name, course_category, course_description, course_price, course_duration_time, image_path, mentor_id):
        '''
        Inserts new course to the database

        Parameters:
            mysql: Mysql connection cursor
            course_name : the course name
            course_category: the course category or scope
            course_description: the course content description
            course_price: the course price amount
            course_duration_time: the course duration time
            image_path: image location path
        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (course_name, course_category, course_description, course_price, course_duration_time) VALUES
        ('{}', '{}', '{}', '{}', '{}')'''.format(self.table_name(self), course_name, course_category, course_description, course_price,
        course_duration_time)
        row = cursor.execute(sql)
        mysql.get_db().commit()
        course_id = cursor.lastrowid # last inserted id
        self.course_image_table(self, mysql, image_path, course_id) # Stores image to database
        self.course_mentor_table(self, mysql, course_id, mentor_id) # Create course mentor menay_to_many table
        if row is 1:
            return course_id
        else:
            return None
