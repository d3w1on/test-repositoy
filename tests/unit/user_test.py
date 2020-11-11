from models.user import UserModel
from tests.unit.unitBaseTest import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('Test', 'Test123')

        self.assertEqual(user.username, 'Test')
        self.assertEqual(user.password, 'Test123')
