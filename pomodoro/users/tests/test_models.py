from django.test import TestCase

from .factories import UserFactory


class TestUserModel(TestCase):
    def setUp(self):
        self.user = UserFactory(password="test1234")

    def test_user_str_representation(self):
        self.assertEqual(self.user.__str__(), self.user.username)
        self.assertEqual(str(self.user), self.user.username)

    def test_user_authentication(self):
        self.assertTrue(self.user.check_password("test1234"))
