from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test',
                                                            'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = {'Authorization': f'JWT {auth_token}'}

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')

                self.assertEqual(401, resp.status_code)

    def test_item_not_fount(self):
        with self.app() as client:
            with self.app_context():

                resp = client.get('item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item_with_auth(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                pass

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                pass

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                pass

    def test_update_item(self):
        with self.app() as client:
            with self.app_context():
                pass

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                pass
