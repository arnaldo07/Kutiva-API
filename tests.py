from flask import Flask
from flask_testing import TestCase
from flaskext.mysql import MySQL
from models.mentor import Mentor
from models.course import Course
from models.student import Student
import unittest
import os
import tempfile

class KutivaAPITests(TestCase):
    '''
    This class contains basic configurations for tests
    To perfom tests here, first need to setup a test database
    '''

    def create_app(self):
        '''
        Returns a flask instance and initializes Mysql test database
        '''
        self._mysql_ = MySQL()
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config.from_object('testConfig') # test database configurations
        self._mysql_.init_app(app)
        return app


# Mentor Tests
class MentorTests(KutivaAPITests):
    '''
    This class contains basic tests for Mentor classs
    '''


    def setUp(self):
        pass

    # Create() test
    def test_create(self):
        '''
        Create method includes other dependent methods of the course class
        in this test will cover them too
        '''
        assert Mentor.create(Mentor, self._mysql_, first_name = 'TestName', last_name='TestSurname', category='TestCategory',
        email='Test@mail.com', country_code='258', phone='841234567', password='TestPassword') is True

    # create_email_verification() test
    def test_create_email_verification(self):
        assert Mentor.create_email_verification(Mentor, self._mysql_, account_id = 1) is True

    # exists() test
    def test_email_exists(self):
        # Test@mail account is already created in the top
        # So, it must assert it is true
        assert Mentor.email_exists(Mentor, self._mysql_, email = 'Test@mail.com') is True

    # create_password() test
    def test_create_password(self):
        assert Mentor.create_password(Mentor, self._mysql_, hashed_password = '6ws546sd4ds64', mentor_id = 1) is True

    # authenticate() test
    def test_authenticate(self):
        assert Mentor.authenticate(Mentor, self._mysql_, username = 'Test@mail.com', password = 'TestPassword') is not None # 1 = mentor account id

    # find_by_category()
    def test_find_by_category(self):
        assert Mentor.find_by_category(Mentor, self._mysql_, category = "TestCategory") is not None

    # find_by_id() test
    def test_find_by_id(self):
        assert Mentor.find_by_id(Mentor, self._mysql_, id = 1) is not None

    # find_all() test
    def test_find_all(self):
        assert Mentor.find_all(Mentor, self._mysql_) is not None


class StudentTests(KutivaAPITests):
    """This class contains basic tests for Student class"""

    def setUp(self):
        self._token = Student.create_email_verification(Student, self._mysql_, account_id = 1) # Setup that

    # Create() test
    def test_create(self):
        '''
        Create method includes other dependent methods of the course class
        in this test will cover them too
        '''
        assert Student.create(Student, self._mysql_, first_name = "TestName", last_name = "TestSurname", email ="Test@mail.com",
        password = "TestPassword") is not None

    # find_all() test
    def test_find_all(self):
        assert Student.find_all(Student, self._mysql_) is not None

    # find_by_id() test
    def test_find_by_id(self):
        assert Student.find_by_id(Student, self._mysql_, id = 1) is not None

    # authenticate() test
    def test_authenticate(self):
        assert Student.authenticate(Student, self._mysql_, username = 'Test@mail.com', password = 'TestPassword') is not None # 1 = mentor account id

     # create_email_verification() test
    def test_create_email_verification(self):
        assert self._token is not None

    # desactivate_email_verification()
    def test_desactivate_email_verification(self):
        assert Student.desactivate_email_verification(Student, self._mysql_, token = self._token, account_id = 1) is True

    # email_verification_in_date()
    def test_email_verification_in_date(self):
        assert Student.email_verification_in_date(Student, self._mysql_, token = self._token, id=1) is True

# Close tests
class KutivaAPITestsClose(KutivaAPITests):
    '''
    Closes all tests and resets all resources
    '''

    def test_tearDown(self):
        '''
        Truncates all test database tables data
        '''
        cursor = self._mysql_.get_db().cursor()
        sql = '''SELECT CONCAT('truncate table ', table_name, ';') FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA ='kutivatest'
        AND TABLE_TYPE = 'BASE TABLE' '''
        cursor.execute(sql)
        row = cursor.fetchall()
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for i in row:
            for x in i:
                cursor.execute(str(x))
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')




if __name__ == "__main__":
    unittest.main()
