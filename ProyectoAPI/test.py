import json
import unittest

from app import db
from app import create_app

from config import config

class TestAPI(unittest.TestCase):
    def setUp(self):
        enviroment = config['test']
        self.app = create_app(enviroment)
        self.client = self.app.test_client()

        self.content_type = 'application/json'
        self.path = 'http://127.0.0.1:5000/api/v1/tasks'
        self.path_first_task = self.path + '/1'
        self.path_fake_task = self.path + '/100'
        self.path_data_to_update = { 'title': 'Nuevo título' }
    
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_one_equals_one(self):
        self.assertEqual(1, 1)

    def test_get_all_tasks(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)

    def get_task_id(self, response):
        data = json.loads(response.data.decode('utf-8'))
        return data['data']['id']

    def test_get_first_task(self):
        response = self.client.get(path=self.path_first_task,
                                    content_type=self.content_type)

        self.assertEqual(response.status_code, 200)

        task_id = self.get_task_id(response)
        
        self.assertEqual(task_id, 1)

    def test_not_found(self):
        response = self.client.get(path=self.path_fake_task,
                                    content_type=self.content_type)
        
        self.assertEqual(response.status_code, 404)

#PruebaGei hecha por rauka
    def test_len(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))
        len_data = data['data']
#Cambiar el 2, segun el numero de task creadas, para este caso siempre se generara 2 tasks
        self.assertEqual(len(len_data), 2)

    def test_create(self):
        data = {
            'title':'title', 'description':'description', 'deadline':'2020-12-12 12:00:00'
        } 
        response = self.client.post(self.path, data=json.dumps(data), content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))
        id_data = data['data']['id']
        self.assertEqual(id_data, 3)

    def test_update(self):

        response = self.client.put(path=self.path_first_task, data=json.dumps(self.path_data_to_update), content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))
        update_data_title = data['data']['title']

        self.assertEqual(update_data_title, self.path_data_to_update['title'])

#Test hecho por rauka para actualizar una tarea que no exista.
    def test_update_not_found(self):
        response = self.client.put(path=self.path_fake_task, data=json.dumps(self.path_data_to_update), content_type=self.content_type)
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data.decode('utf-8'))
        update_fake_data = data['data']

        self.assertEqual(update_fake_data, data['data'])

    def test_delete_task(self):
        response = self.client.delete(path=self.path_first_task, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(path=self.path_first_task, content_type=self.content_type)
        self.assertEqual(response.status_code, 404)
            
if __name__ == '__main__':
    unittest.main()