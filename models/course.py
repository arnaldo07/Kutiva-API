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

    # Create course_image table
    def insert_course_image(self, mysql, image_path, course_id):
        '''
        Inserts course images location to database

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
            return True
        else:
            return False

    # Create course_mentor menay_to_many table
    def insert_course_mentor(self, mysql, course_id, mentor_id):
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
            return True
        else:
            return False

    # Creates a course
    def create(self, mysql, course_name, course_category, course_description, course_price, course_duration_time,
    course_audience_level, course_tags, image_path, mentor_id):
        '''
        Inserts new course to the database

        Parameters:
            mysql: Mysql connection cursor
            course_name : the course name
            course_category: the course category or scope
            course_description: the course content description
            course_price: the course price amount
            course_duration_time: the course duration time
            course_audience_level: defines the level of audience the course was done
            course_tags: the keywords related to the course for SEO purposes
            image_path: image location path
        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (course_name, course_category, course_description, course_price, course_audience_level, course_tags,
        course_duration_time) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(self.table_name(self), course_name, course_category,
        course_description, course_price, course_audience_level, course_tags, course_duration_time )
        row = cursor.execute(sql)
        mysql.get_db().commit()
        course_id = cursor.lastrowid # last inserted id
        self.insert_course_image(self, mysql, image_path, course_id) # Stores image to database
        self.insert_course_mentor(self, mysql, course_id, mentor_id) # Create course mentor menay_to_many table
        if row is 1:
            return course_id
        else:
            return None


    # Update
    def update(self, mysql, course_name, course_id):
        '''
        Updates courses database

        Parameters:
            mysql: Mysql connection cursor

        '''
        cursor = mysql.get_db().cursor()
        sql = '''UPDATE {} SET course_name = {} WHERE course_id = '{}' '''.format(self.course_mentor_table_name(self),
        course_name, course_id )
        row = cursor.execute(sql)
        mysql.get_db().commit()

        if row is 1:
            return True
        else:
            return False

    # Find all
    def find_all(self, mysql):
        '''
        Find all courses
        Parameters:
            mysql: Mysql connection cursor

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
                    'course_audience_level':    i[5],
                    'course_tags':              i[6],
                    'course_duration':          str(i[7]),
                    'course_stars':             i[8],
                    'course_status':            i[9],
                    'course_published':         i[10],
                    'course_image_id':          i[14],
                    'course_image_href':        i[15],
                    'course_image_active':      i[16],
                    'course_image_datetime':    i[17],
                    'mentor_id':                i[19],
                    'mentor_first_name':        i[20],
                    'mentor_last_name':         i[21],
                    'mentor_scope_category':    i[22],
                    'mentor_email':             i[23],
                    'mentor_country_code':      i[24],
                    'mentor_phone':             i[25],
                    'mentor_image':             i[26],
                    'mentor_status':            i[27],
                    'mentor_account_datetime':  i[28]
                    }
                result.append(data)

            return jsonify(result)

    # Find course by id
    def find_by_id(self, mysql, course_id):
        '''
        Find a course by id

        Parameters:
            mysql: Mysql connection cursor
            course_id: id of the course

        '''
        cursor = mysql.get_db().cursor()
        sql = '''SELECT * FROM {} JOIN {} JOIN {} JOIN {} WHERE (course_image_course_id = course_id and course_id = cm_course_id
        and cm_mentor_id = mentor_id ) and course_id = {} '''.format(self.table_name(self), self.course_mentor_table_name(self),
        self.course_image_table_name(self), Mentor.table_name(self), course_id)
        cursor.execute(sql)
        row = cursor.fetchone()

        if row is None:
            return None
        else:
            data = {
                'course_id':                row[0],
                'course_name':              row[1],
                'course_category':          row[2],
                'course_description':       row[3],
                'course_price':             row[4],
                'course_audience_level':    row[5],
                'course_tags':              row[6],
                'course_duration':          str(row[7]),
                'course_stars':             row[8],
                'course_status':            row[9],
                'course_published':         row[10],
                'course_image_id':          row[14],
                'course_image_href':        row[15],
                'course_image_active':      row[16],
                'course_image_datetime':    row[17],
                'mentor_id':                row[19],
                'mentor_first_name':        row[20],
                'mentor_last_name':         row[21],
                'mentor_scope_category':    row[22],
                'mentor_email':             row[23],
                'mentor_country_code':      row[24],
                'mentor_phone':             row[25],
                'mentor_image':             row[26],
                'mentor_status':            row[27],
                'mentor_account_datetime':  row[28]
                }
            return jsonify(data)


    # Find course by id
    def find_by_ids(self, mysql, mentor_id, course_id):
        '''
        Find a course by ids

        Parameters:
            mysql: Mysql connection cursor
            mentor_id: id of the mentor
            course_id: id of the course

        '''
        cursor = mysql.get_db().cursor()
        sql = '''SELECT * FROM {} JOIN {} JOIN {} JOIN {} WHERE (course_image_course_id = course_id and course_id = cm_course_id
        and cm_mentor_id = mentor_id ) and course_id = {} and cm_mentor_id = {} '''.format(self.table_name(self), self.course_mentor_table_name(self),
        self.course_image_table_name(self), Mentor.table_name(self), course_id, mentor_id)
        cursor.execute(sql)
        row = cursor.fetchone()

        if row is None:
            return None
        else:
            data = {
                'course_id':                row[0],
                'course_name':              row[1],
                'course_category':          row[2],
                'course_description':       row[3],
                'course_price':             row[4],
                'course_audience_level':    row[5],
                'course_tags':              row[6],
                'course_duration':          str(row[7]),
                'course_stars':             row[8],
                'course_status':            row[9],
                'course_published':         row[10],
                'course_image_id':          row[14],
                'course_image_href':        row[15],
                'course_image_active':      row[16],
                'course_image_datetime':    row[17],
                'mentor_id':                row[19],
                'mentor_first_name':        row[20],
                'mentor_last_name':         row[21],
                'mentor_scope_category':    row[22],
                'mentor_email':             row[23],
                'mentor_country_code':      row[24],
                'mentor_phone':             row[25],
                'mentor_image':             row[26],
                'mentor_status':            row[27],
                'mentor_account_datetime':  row[28]
                }
            return jsonify(data)


    # Find course by id
    def find_by_category(self, mysql, course_category):
        '''
        Find a course by category

        Parameters:
            mysql: Mysql connection cursor
            course_category: category of the course

        '''
        cursor = mysql.get_db().cursor()
        sql = '''SELECT * FROM {} JOIN {} JOIN {} JOIN {} WHERE (course_image_course_id = course_id and course_id = cm_course_id
        and cm_mentor_id = mentor_id ) and course_category = "{}" '''.format(self.table_name(self), self.course_mentor_table_name(self),
        self.course_image_table_name(self), Mentor.table_name(self), course_category)
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
                    'course_audience_level':    i[5],
                    'course_tags':              i[6],
                    'course_duration':          str(i[7]),
                    'course_stars':             i[8],
                    'course_status':            i[9],
                    'course_published':         i[10],
                    'course_image_id':          i[14],
                    'course_image_href':        i[15],
                    'course_image_active':      i[16],
                    'course_image_datetime':    i[17],
                    'mentor_id':                i[19],
                    'mentor_first_name':        i[20],
                    'mentor_last_name':         i[21],
                    'mentor_scope_category':    i[22],
                    'mentor_email':             i[23],
                    'mentor_country_code':      i[24],
                    'mentor_phone':             i[25],
                    'mentor_image':             i[26],
                    'mentor_status':            i[27],
                    'mentor_account_datetime':  i[28]
                    }
                result.append(data)

            return jsonify(result)

    # Search course
    def search(self, mysql, search):
        '''
        Search

        Parameters:
            mysql: Mysql connection cursor
            search: search content

        '''
        cursor = mysql.get_db().cursor()
        sql = '''SELECT * FROM {} JOIN {} JOIN {} JOIN {} WHERE (course_image_course_id = course_id and course_id = cm_course_id
        and cm_mentor_id = mentor_id ) and ( course_name LIKE "%{}%" OR course_category LIKE "%{}%" OR course_description LIKE "%{}%"
        OR mentor_first_name LIKE "%{}%" OR mentor_last_name LIKE "%{}%" ) '''.format(self.table_name(self),
        self.course_mentor_table_name(self), self.course_image_table_name(self), Mentor.table_name(self), search, search, search,
        search, search)
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
                    'course_audience_level':    i[5],
                    'course_tags':              i[6],
                    'course_duration':          str(i[7]),
                    'course_stars':             i[8],
                    'course_status':            i[9],
                    'course_published':         i[10],
                    'course_image_id':          i[14],
                    'course_image_href':        i[15],
                    'course_image_active':      i[16],
                    'course_image_datetime':    i[17],
                    'mentor_id':                i[19],
                    'mentor_first_name':        i[20],
                    'mentor_last_name':         i[21],
                    'mentor_scope_category':    i[22],
                    'mentor_email':             i[23],
                    'mentor_country_code':      i[24],
                    'mentor_phone':             i[25],
                    'mentor_image':             i[26],
                    'mentor_status':            i[27],
                    'mentor_account_datetime':  i[28]
                    }
                result.append(data)

            return jsonify(result)
