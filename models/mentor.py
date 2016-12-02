# mentor.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# This is mentors model which wil handle all mentors mai functions
# Copyrighth 2016 Xindiri, LLC

from flask import Flask, jsonify, request, json

class Mentor():

    # Set table name
    def table_name(self):
        return "mentor"

    # password table_name
    def pwd_table_name(self):
        return "password"

    def account_type(self):
        return 'Mentor'


    # Serialize data from database
    def serialize(self):
        '''
        Serializes data coming from database

        return: serialized  list
        '''
        return {
        'id': self.id,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'category': self.category,
        'email': self.email,
        'country_code': self.country_code,
        'phone': self.phone,
        'profile_image_url': self.profile_image_url,
        'account_status': self.account_status,
        'account_registration_date': self.account_registration_date
        }

    # Find all
    def find_all(self, mysql):
        '''
        Gets all data coming from the database

        return: Json object
        '''

        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * from {} '''.format(self.table_name(self)))
        rows = cursor.fetchall()

        self.id = 356566
        self.first_name = 'Arnaldo'
        self.last_name  = 'Govene'
        self.category ='business'
        self.email = 'arnaldo.govene@outlook.com'
        self.country_code = 258
        self.phone = 846861894
        self.profile_image_url = 'http://localhost/jgjhghg.jpg'
        self.account_status = 'Active'
        self.account_registration_date = '12-01-2016 12:43:33'

        return jsonify(self.serialize(self))


    # Get by id
    def find_by_id(seif, mysql, id):
        '''
        Gets data from the database by id

        return: Json object
        '''

        cursor = mysql.get_db().cursor()
        cursor.execute('''SELECT * from {} WHERE mentor_id = {}'''.format(self.table_name, id))
        row = cursor.fetchone()

        self.id = row[1]
        self.first_name = 'Arnaldo'
        self.last_name  = 'Govene'
        self.category ='business'
        self.email = 'arnaldo.govene@outlook.com'
        self.country_code = 258
        self.phone = 846861894
        self.profile_image_url = 'http://localhost/jgjhghg.jpg'
        self.account_status = 'Active'
        self.account_registration_date = '12-01-2016 12:43:33'

        return jsonify(self.serialize(self))

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

    def exists(self, mysql, email, phone):
        '''
        Checks if account exist

        Parameters:
        mysql: Mysql connection cursor
        email: mentor email
        phone: mentor phone number
        '''

        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM {} WHERE mentor_email = '{}' or mentor_phone = '{}' ".format(self.table_name(self), email, phone))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True



    # Creates a mentor
    def create(self, mysql, first_name, last_name, category, email, country_code, phone, password):
        '''
        Inserts new mentor to the database

        Parameters:
        mysql: Mysql connection cursor
        data : mentor data dictionary
        '''
        cursor = mysql.get_db().cursor()
        sql = '''INSERT INTO {} (mentor_first_name, mentor_last_name,
        mentor_scope_category, mentor_email, mentor_country_code, mentor_phone) VALUES
        ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(self.table_name(self), first_name, last_name, category,
        email, country_code, phone)
        row = cursor.execute(sql)
        mysql.get_db().commit()
        student_id = cursor.lastrowid # Last inserted id
        self.create_password(self, mysql, password, student_id) # Create password
        if row is 1:
            return True
        else:
            return False
