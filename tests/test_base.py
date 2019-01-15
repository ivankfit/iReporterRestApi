from app import app
import unittest
import json
import datetime


class TestsStart(unittest.TestCase):

    def setUp(self):
         self.app = app.test_client()
        
    def test_if_can_get_users(self):
        response = self.app.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
    def test_if_can_get_welcome(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


    def test_if_can_get_redflags(self):
        response = self.app.get('/api/v1/red-flags')
        self.assertEqual(response.status_code, 200)

    def test_if_comment_is_not_submited(self):
        expectedreq ={

        "type":"Red_flag",
        "location":"Mbarara",
        "status":"draft",
        "image":"image"

        }
        result = self.app.post('/api/v1/red-flags', content_type = 'multipart/form-data', 
            data=json.dumps(expectedreq))
        data=json.loads(result.data.decode())
        self.assertEqual(result.status_code,400)
        self.assertEqual(data['msg'],'comment missing! please supply in the comment')

    # def test_if_location_is_not_captured(self):
    #     expectedreq ={

    #     "type":"Red_flag",
    #     "comment":"asked for bribe",
    #     "status":"draft",
    #     "image":"image"

    #     }
    #     result = self.app.post('/api/v1/red-flags', content_type = 'multipart/form-data', 
    #         data=json.dumps(expectedreq))
    #     data=json.loads(result.data.decode())
    #     self.assertEqual(result.status_code,400)
    #     self.assertEqual(data['msge'],'location is missing')
   
    def test_redflag_not_json(self):
        expectedreq ={
	
        "comment":"he ran away",
        "type":"Red_flag",
        "location":"Mbarara",
        "status":"draft",
        "image":"image"

        }
        result = self.app.post(
            '/api/v1/red-flags',
            content_type = 'text/html',
            data=json.dumps(expectedreq)
        )

        data=json.loads(result.data.decode())
        self.assertEqual(data['msg'],'request header type should be form-data')

    def test_create_user_request_not_json(self):
        """ Test redflag content to be posted not in json format """
        expectedreq = {
             'incident_type': 'government intervention/broken bridge',
            'comment_description': 'river rwizi bridge had broken down',
            'status': 'ressolved',
            'current_location': 'kashanyarazi, mbarara',
            'created': 'Nov 29 2018 : 11:04AM'
        }
        result = self.app.post(
            '/api/v1/users',
            content_type = 'text/html',
            data=json.dumps(expectedreq)
        )
        data=json.loads(result.data.decode())
        self.assertEqual(result.status_code,401)
        self.assertEqual(data['failed'],'content-type must be application/json')
       

    def test_if_user_cant_delete_innexistent_flag(self):
        res=self.app.delete('/api/v1/red-flags/1')
        data=json.loads(res.data.decode())
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['msg'],'item not found')

    def test_if_user_cannot_update_inexistent_specific_redflag(self):
        res=self.app.put('/api/v1/red-flags/2')
        data=json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['msg'], 'item not found')
    def test_if_user_cant_get_an_innexistent_flag(self):
        res=self.app.get('/api/v1/red-flags/2')
        data=json.loads(res.data.decode())
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['msg'],'item not found')
    def test_if_user_cannot_edit_innexistent_comment(self):
        res=self.app.patch('/api/v1/red-flags/1/comment')
        data=json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['msge'], 'item not found')

    def test_if_user_cannot_edit_innexistent_location(self):
        response=self.app.patch('/api/v1/red-flags/668/location')
        data=response.data.decode()
       


    def test_can_create_a_red_flag(self):
        """ Tests if a user can create a redflag """
        expectedreq = {
             'type':'intervention',
             'comment': 'river rwizi bridge had broken down',
             'location': 'kashanyarazi, mbarara',
            
        }
        result = self.app.post(
            '/api/v1/red-flags',
            content_type = 'multipart/form-data',
            data=json.dumps(expectedreq)
        )
        data=json.loads(result.data.decode())
        self.assertIn('msg',data)
       

if __name__ == "__main__":
    unittest.main()