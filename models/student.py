# mentor.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is students model which wil handle all student  functions
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, jsonify, request, json

class Student():

    # Set table name
    def table_name(self):
        return "student"

    # password table_name
    def pwd_table_name(self):
        return "password"

    # Sets account type
    def account_type(self):
        return "Student"


    def authenticate(self, mysql, username, password):
        '''
        authenticates student account

        Parameters:
            mysql: Mysql connection cursor
            username: student account email
            password: student account password
        '''
        cursor = mysql.get_db().cursor()
        sql = '''SELECT student_id FROM {} JOIN {} WHERE (student_id = password_owner_account_id and password_owner_account_type = '{}')
         and ( student_email = '{}' and password_encrypted = '{}' )'''.format(self.table_name(self), self.pwd_table_name(self), self.account_type(self), username, password)
        cursor.execute(sql)
        row = cursor.fetchone()

        if row is None:
            return None
        else:
            return row[0]


    def exists(self, mysql, email, phone):
        '''
        Checks if account exist

        Parameters:
        mysql: Mysql connection cursor
        email: student email
        phone: student phone number
        '''

        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM {} WHERE student_email = '{}' or student_phone = '{}' ".format(self.table_name(self), email, phone))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True


    def create_password(self, mysql, hashed_password, student_id):
        '''
        Inserts new password to the database

        Parameters:
        mysql: Mysql connection cursor
        hashed_password: student accoumt hashed password
        student_id: student primary key
        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (password_encrypted, password_owner_account_type, password_owner_account_id ) VALUES
        ('{}', '{}', '{}')'''.format(self.pwd_table_name(self), hashed_password, self.account_type(self), student_id)
        row = cursor.execute(sql)
        mysql.get_db().commit()
        if row is 1:
            return True
        else:
            return False


    # Creates a student
    def create(self, mysql, first_name, last_name, gender, age, email, country_code, phone, password):
        '''
        Inserts new student to the database

        Parameters:
        mysql: Mysql connection cursor
        data : mentor data dictionary
        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (student_first_name, student_last_name,
        student_gender, student_age, student_email, student_country_code, student_phone) VALUES
        ('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(self.table_name(self), first_name, last_name, gender,
        age, email, country_code, phone)
        row = cursor.execute(sql)
        mysql.get_db().commit()
        student_id = cursor.lastrowid # las inserted id
        self.create_password(self, mysql, password, student_id) # Create password
        if row is 1:
            return True
        else:
            return False
