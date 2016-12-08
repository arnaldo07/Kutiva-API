# mentor.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is students model which wil handle all student  functions
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, jsonify, request, json
from time import gmtime, strftime
import hashlib

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

    # Email_verification table_name
    def mail_verify_table_name(self):
        return "email_verfication"

    # Find all
    def find_all(self, mysql):
        '''
        Gets all data from the database

        Parameters:
            mysql: Mysql connection cursor
        '''

        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * FROM {} '''.format(self.table_name(self)))
        row = cursor.fetchall()

        if row is None:
            return None
        else:
            result = []
            for i in row:
                data = {
                    'id':                        i[0],
                    'first_name':                i[1],
                    'last_name':                 i[2],
                    'gender':                    i[3],
                    'birthdate':                 i[4],
                    'email':                     i[5],
                    'country_code':              i[6],
                    'phone':                     i[7],
                    'profile_image_url':         i[8],
                    'account_status':            i[9],
                    'account_registration_date': i[10]
                    }

                result.append(data)

            return jsonify(result)

    # Get by id
    def find_by_id(self, mysql, id):
        '''
        Gets data from the database by id

        Parameters:
            mysql: Mysql connection cursor
            id: student id
        '''

        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * FROM {} WHERE student_id = {}'''.format(self.table_name(self), id))
        row = cursor.fetchone()

        if row is None:
            return None
        else:
            data = {
                'id':                        row[0],
                'first_name':                row[1],
                'last_name':                 row[2],
                'gender':                    row[3],
                'birthdate':                 row[4],
                'email':                     row[5],
                'country_code':              row[6],
                'phone':                     row[7],
                'profile_image_url':         row[8],
                'account_status':            row[9],
                'account_registration_date': row[10]
                }

            return jsonify(data)


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

    # Create email verification
    def create_email_verification(self, mysql, account_id):
            '''
            Inserts new email_verificaion to the database

            Parameters:
                mysql: Mysql connection cursor
                account_id : verification account id
            '''
            active = True # Set email token active to true
            cur_datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime()) # Generate current datetime
            tokenize = "{}{}".format(account_id, cur_datetime) # To be turned to token
            token = hashlib.md5(tokenize.encode()).hexdigest() # Hash token
            cursor = mysql.get_db().cursor()

            sql = '''INSERT INTO {} (email_verification_token, email_verification_active,
            email_verification_account_type, email_verification_account_id ) VALUES
            ('{}', '{}', '{}', '{}')'''.format(self.mail_verify_table_name(self), token, active, self.account_type(self),account_id )
            row = cursor.execute(sql)
            mysql.get_db().commit()

            if row is None:
                return False
            else:
                return True


    # Update email verification
    def update_email_verification(self, mysql, account_id):
            '''
            Updates email_verificaion to the database

            Parameters:
                mysql: Mysql connection cursor
                account_id : verification account id
            '''
            active = True # Set email token active to true
            cur_datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime()) # Generate current datetime
            tokenize = "{}{}".format(account_id, cur_datetime) # To be turned to token
            token = hashlib.md5(tokenize.encode()).hexdigest() # Hash token
            cursor = mysql.get_db().cursor()

            sql = '''UPDATE {} SET email_verification_token = '{}' AND email_verification_active = '{}' AND
            email_verification_datetime = CURRENT_TIMESTAMP WHERE email_verification_account_type = '{}'
            AND email_verification_account_id '''.format(self.mail_verify_table_name(self), token, active,
            self.account_type(self), account_id )
            row = cursor.execute(sql)
            mysql.get_db().commit()

            if row is None:
                return False
            else:
                return True


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
        student_gender, student_birthdate, student_email, student_country_code, student_phone) VALUES
        ('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(self.table_name(self), first_name, last_name, gender,
        age, email, country_code, phone)
        row = cursor.execute(sql)
        mysql.get_db().commit()
        student_id = cursor.lastrowid # last inserted id
        self.create_password(self, mysql, password, student_id) # Create password
        self.create_email_verification(self, mysql, student_id) # Create email verification token
        if row is 1:
            return student_id
        else:
            return None
