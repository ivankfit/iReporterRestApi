from app import app
import unittest
import json
from app.views.users import is_valid


class TestsUsers(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def test_create_user(self):
        
        #checks if a user can be created
        
        expecteduser_obj = {
            "firstname": "ivan kfit",
             "lastname": "ivan kfit",
            "othernames": "ivan kfit",
            "username": "kfit",
            "phone_number": "0705749598",
            "email": "tweheyoivan@gmail.com",
            "is_admin":True

        }
        response = self.client.post(
            "api/v1/users",
            data=json.dumps(expecteduser_obj),
            content_type="application/json")
        results = json.loads(response.data.decode())

        self.assertEqual(
            results['success'], True)
        self.assertEqual(response.status_code, 201)

    def test_cannot_create_a_user_without_email(self):
        """
        checks if cannot create a user who has no email
        """
        expecteduser_obj = {
            "firstname": "ivan kfit",
             "lastname": "ivan kfit",
              "othernames": "ivan kfit",
            "username": "kfit",
            "phone_number": "0705749598",
            "is_admin":True

        }
        response=self.client.post('/api/v1/users',data=json.dumps(expecteduser_obj),
            content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(data['msg'], 'Email is missing')
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 400)

    def test_cannot_create_a_user_without_username(self):
        expecteduser_obj = {
            "firstname": "ivann kfit",
            "lastname": "ivan kfitt",
            "othernames": "ivann k",
            "phone_number": "0705749598",
            "email": "email000000@test.com",
            "is_admin":True

        }
        response=self.client.post('/api/v1/users', data=json.dumps(expecteduser_obj),
            content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(data['msg'], 'User must have a username')
        self.assertEqual(response.status_code, 400)
    
    def test_cannot_create_a_user_without_firstname(self):
        expecteduser_obj = {
            "username": "ivan2",
            "lastname": "van",
            "othernames": "ivann k",
            "phone_number": "0705749598",
            "email": "email000000@test.com",
            "is_admin":True

        }
        response=self.client.post('/api/v1/users', data=json.dumps(expecteduser_obj),
            content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(data['msg'], 'firstname must be provided')
        self.assertEqual(response.status_code, 400)

    def test_cannot_create_a_user_without_lastname(self):
        expecteduser_obj = {
            "username": "ivan2",
            "firstname": "Tivan",
            "othernames": "ivannk",
            "phone_number": "0705749598",
            "email": "email000000@test.com",
            "is_admin":True

        }
        response=self.client.post('/api/v1/users', data=json.dumps(expecteduser_obj),
            content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(data['msg'], 'lastname must be provided')
        self.assertEqual(response.status_code, 400)    

    def test_user_cannot_have_someones_user_name(self):
        users = []
        expecteduser_obj = {
            "firstname": "ivann kfit",
            "lastname": "ivan kfitt",
            "othernames": "ivann k",
            "username": "kfit",
            "phone_number": "0705749598",
            "email": "email000000@test.com",
            "is_admin":True

        }
        users.append(expecteduser_obj)
        user_obj = {
            "firstname": "ivan kfit",
             "lastname": "ivan kfit",
            "username": "kfit",
            "othernames":"hhhhhhhh",
            "email":"kfitivn@gmail.com",
            "phone_number": "0705749598",
            "is_admin":True

        }
        response = self.client.post(
            "api/v1/users",
            data=json.dumps(user_obj),
            content_type="application/json")
        data2 = json.loads(response.data.decode())
        self.assertEqual(data2['success'], False)
        self.assertEqual(response.status_code, 409)

    def test_user_cannot_have_someone_else_email_address(self):
        usersList = []
        expecteduser_obj = {
            "firstname": "ivan kfit1",
            "lastname": "ivan kfit2",
            "othernames": "ivan kfit",
            "username": "kfit1",
            "phone_number": "0705749598",
            "email": "email@test.com",
            "is_admin":False

        }
        self.client.post(
            "api/v1/users",
            data=json.dumps(expecteduser_obj),
            content_type="application/json")
        
        user_obj2 = {
           "firstname": "ivan kfit9",
            "lastname": "ivan kfit9",
            "username": "kfit9",
            "email":"email@test.com",
            "phone_number": "0705749598",
            "is_admin":True,
            "othernames":"my other"

        }
        response = self.client.post(
            "api/v1/users",
            data=json.dumps(user_obj2),
            content_type="application/json")
        results = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 409)

    def test_user_cannot_have_an_invalid_email(self):
        """
        tests if user supplies a valid email
        """
        user_obj = {
            "firstname": "ivannn kfit",
             "lastname": "ivanmm kfit",
            "username": "kfit",
            "email":"kfitivan123",
            "phone_number": "0705749598",
            "othernames":"my other",
            "is_admin":True

        }
        response = self.client.post(
            "api/v1/users",
            data=json.dumps(user_obj),
            content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 401)

    def test_get_a_no_users_message(self):
        '''
        tests if a user gets a readable no users message when users are not there
        :return:
        '''
        response = self.client.get('api/v1/users', content_type='application/json')
        data = json.loads(response.data.decode())
        count = data['count']
        if count == 0:
            self.assertEqual(data['msg'], 'No users yet')
        self.assertEqual(response.status, '200 OK')

if __name__ == "__main__":
    unittest.main()