import unittest
import json

# fix import errors
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import app

app = app.create_app()
app.config.from_object('config.TestingConfig')



class DiaryTests(unittest.TestCase):
    """Tests functionality of the API"""


    def setUp(self):
        """Initialize important variables and makes them easily availabe through the self keyword"""
        self.app = app.test_client()
        self.diary = json.dumps({"diary_no" : "007"})
        self.entry = json.dumps({"entry_no" : "20"})
        self.todo = json.dumps({"todo_item" : "Going to cinema with my friends"})
        self.existing_diary = self.app.post('/api/v1/diaries', data=self.diary, content_type='application/json')
        self.existing_entry = self.app.post('/api/v1/entries', data=self.entry, content_type='application/json')
        

    def test_get_all_diaries(self):
        """Tests successfully getting all diaries through the diaries endpoint"""
        response = self.app.get('/api/v1/diaries')
        self.assertEqual(response.status_code, 200)

    def test_successful_diary_creation(self):
            """Tests successfully creating a new diary through the diaries endpoint"""
            data = json.dumps({"diary_no" : "010", "to-do" : "hhhhhhhhh"})
            response = self.app.post('/api/v1/diaries', data=data, content_type='application/json')
            result = json.loads(response.data)
            self.assertEqual(result.get("diary_no"), 10)
            self.assertEqual(result.get("to-do"), "hhhhhhhhh")
            self.assertEqual(response.status_code, 201)
        
    def test_diary_creation_existing_number(self):
        """Tests unsuccessfully creating a new diary because of existing diary_number"""
        data = json.dumps({"diary_no." : "210"})
        response = self.app.post('/api/v1/diaries', data=data, content_type='application/json') # pylint: disable=W0612
      

    def test_create_diary_empty_number(self):
        """Tests unsuccessfully creating a new diary because of empty number"""
        data = json.dumps({"diary_no" : ""})
        response = self.app.post('/api/v1/diaries', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"diary_no": "kindly provide a diary number"})



    def test_create_diary_invalid_number(self):
        """Tests unsuccessfully creating a new diary because of invalid number"""
        data = json.dumps({"diary_number" : "four hundred"})
        response = self.app.post('/api/v1/diaries', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {"diary_no": "kindly provide a diary number"})

    def test_get_one_diary(self):
        """Tests successfully getting a diary through the diaries endpoint"""
        response = self.app.get('/api/v1/diaries/2')
        self.assertEqual(response.status_code, 200)

    def test_getting_non_existing_diary(self):
        """Test getting a diary_number while providing non-existing id"""
        response = self.app.get('/api/v1/diaries/57')
        self.assertEqual(response.status_code, 404)

    # def test_successful_diary_update(self):
    #     """Test a successful diary update"""
    #     data = json.dumps({"diary_no": "006", "to-do": "hhhhh", "todo": "hhhhhh"})
    #     response = self.app.put('/api/v1/diaries/1', data=data, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    def test_updating_non_existing_diary(self):
        """Test updating non_existing diary"""
        data = json.dumps({"diary_number": "600"})
        response = self.app.put('/api/v1/Diaries/600', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successful_diary_deletion(self):
        """Test a successful diary deletion"""
        response = self.app.delete('/api/v1/diaries/2')
        self.assertEqual(response.status_code, 200)


#     # Entry tests
    def test_get_all_entries(self):
        """Tests successfully getting all entries through the entry endpoint"""
        response = self.app.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)

    # def test_successful_entry_creation(self):
    #     """Tests successfully creating a new entry through the entry endpoint"""
    #     data = json.dumps({"entry_pass": 40, "entry_option": "jjjjj"})
    #     response = self.app.post('/api/v1/entries', data=data, content_type='application/json')
    #     result = json.loads(response.data)
    #     self.assertEqual(result.get("entry_option"), "jjjjj")
    #     self.assertEqual(result.get("entry_pass"), 40) 
    #     self.assertEqual(response.status_code, 201)

    def test_entry_creation_existing_number(self):
        """Tests unsuccessfully creating an entry because of existing diary number"""
        data = json.dumps({"diary_number" :"020", "entry": "to watch a game"})
        response = self.app.post('/api/v1/entries', data=data, content_type='application/json') # pylint: disable=W0612
        response2 = self.app.post('/api/v1/entries', data=data, content_type='application/json')
        result = json.loads(response2.data)
        self.assertEqual(result.get("message"), {'entry_option': 'kindly provide an entry option'})

    def test_create_empty_entry(self):
        """Tests unsuccessfully creating a new entry because of empty diary number"""
        data = json.dumps({ "entry" : "........."})
        response = self.app.post('/api/v1/entries', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {'entry_option': 'kindly provide an entry option'})


    def test_create_menu_invalid_entry(self):
        """Tests unsuccessfully creating a new entry"""
        data = json.dumps({"diary_number": "one hundred"})
        response = self.app.post('/api/v1/entries', data=data, content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result.get("message"), {'entry_option': 'kindly provide an entry option'})

    # def test_get_one_entry(self):
    #     """Tests successfully getting an entry through the entries endpoint"""
    #     response = self.app.get('/api/v1/entries/1')
    #     self.assertEqual(response.status_code, 200)

    def test_getting_non_existing_entry(self):
        """Test getting an entry option while providing non-existing id"""
        response = self.app.get('/api/v1/entries/57')
        self.assertEqual(response.status_code, 404)

    # def test_successful_update(self):
    #     """Test a successful entry option update"""
    #     data = json.dumps({"entry_option" : "020", "entry_pass" : "50"})
    #     response = self.app.put('/api/v1/entries/57', data=data, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    def test_updating_non_existing_entry(self):
        """Test getting an entry option while providing non-existing id"""
        response = self.app.put('/api/v1/entry/57')
        self.assertEqual(response.status_code, 404)


    # def test_good_deletion(self):
    #     """Test a successful entry deletion"""
    #     response = self.app.delete('/api/v1/entries/1')
    #     self.assertEqual(response.status_code, 200)
        
    def test_deleting_non_existing_entry(self):
        """Test getting an entry option while providing non-existing id"""
        response = self.app.delete('/api/v1/entries/57')
        self.assertEqual(response.status_code, 404)


  
if __name__ == '__main__':
    unittest.main()
