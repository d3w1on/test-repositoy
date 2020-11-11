from models.store import StoreModel
from tests.unit.unitBaseTest import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.name, 'test')
