from models.store import StoreModel
from tests.base_test import BaseTest
from models.item import ItemModel
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel.find_by_name('test')
                resp = client.post('/store/test', data={'name': 'test'})

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(resp.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel.find_by_name('test')
                client.post('/store/test', data={'name': 'test'})
                request = client.post('/store/test', data={'name': 'test'})

                self.assertEqual(request.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'test' already exists."},
                                     json.loads(request.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():

                client.post('/store/test', data={'name': 'test'})

                request = client.delete('/store/test', data={'name': 'test'})

                self.assertDictEqual({'message': 'Store deleted'}, json.loads(request.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel.find_by_name('test')
                client.post('/store/test', data={'name': 'test'})
                request = client.get('/store/test', data={'name': 'test'})
                expected = {'name': 'test', 'items': []}

                self.assertEqual(request.status_code, 200)
                self.assertDictEqual(expected, json.loads(request.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                request = client.get('/store/test', data={'name': 'test'})
                expected = {'message': 'Store not found'}

                self.assertEqual(request.status_code, 404)
                self.assertDictEqual(expected, json.loads(request.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel.find_by_name('test')
                ItemModel('test_item', 19.99, 1)
                client.post('/store/test', data={'name': 'test'})
                client.post('/item/test_item', data={'name': 'test_item',
                                                     'price': 19.99,
                                                     'store_id': 1})

                request2 = client.get('/store/test', data={'name': 'test'})

                expected = {'name': 'test', 'items': [{'name': 'test_item',
                                                       'price': 19.99}]}

                self.assertEqual(request2.status_code, 200)
                self.assertDictEqual(expected, json.loads(request2.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store_1').save_to_db()
                StoreModel('store_2').save_to_db()
                resp = client.get('/stores')
                expected = {'stores': [{'name': 'store_1', 'items': []},
                                       {'name': 'store_2', 'items': []}]}

                self.assertDictEqual(expected, json.loads(resp.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store_1').save_to_db()
                StoreModel('store_2').save_to_db()
                ItemModel('item_1', 19.99, 1).save_to_db()
                ItemModel('item_2', 19.99, 2).save_to_db()
                resp = client.get('/stores')
                expected = {'stores': [{'name': 'store_1', 'items': [{'name': 'item_1', 'price': 19.99}]},
                                       {'name': 'store_2', 'items': [{'name': 'item_2', 'price': 19.99}]}]}

                self.assertDictEqual(expected, json.loads(resp.data))
