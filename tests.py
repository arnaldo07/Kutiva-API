from flask import Flask
from flask_testing import TestCase
from flask.ext.mysql import MySQL
from models.mentor import Mentor
from models.course import Course
from models.student import Student
import unittest


class KutivaAPITests(TestCase):
    '''
    This class contains basic configurations for tests

    '''

    def create_app(self):
        '''
        Returns a flask instance and initializes Mysql database
        '''
        self._mysql_ = MySQL()
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config.from_object('testConfig')
        self._mysql_.init_app(app)
        return app


# Mentor Tests
class MentorTests(KutivaAPITests):
    '''
    This class contains basic tests for Course class

    '''

    # Setup
    def setUp(self):
        # self._create = Course.create(Course, self._mysql, course_name = 'testname', course_category = 'testcategory',
        # course_description = 'testdescrition', course_price = '1000', course_duration_time = '2:10:00',
        # image_path = 'testImageTest', mentor_id = 1 ) # create method with sample data for test

        # self._create = Student.create(Student, self._mysql, first_name = 'testName', last_name = 'testSurname', gender ='TestGender',
        # age = 'testAge', email = 'testEmail', country_code = 'testCountryCode', phone = 'testPhone', password = 'testPassword')

        self._create = Mentor.create(Mentor, self._mysql_, first_name = 'TestName', last_name = 'testSurname', category = 'TestCategory',
        email = 'TestEmail', country_code = 'TestCountryCode', phone = 'TestPhone', password = 'TestPassword')


    # Test create
    def test_create(self):
        '''
        Create method includes other dependent methods of the course class
        in this test will cover them too
        '''
        assert self._create is True

# Close tests
class KutivaAPITestsClose(KutivaAPITests):
    '''
    Closes all tests and resets all resources
    '''

    def test_tearDown(self):
        '''
        Tears all all test set data down
        '''
        #cursor = self._mysql_.get_db().cursor()




if __name__ == "__main__":
    unittest.main()
