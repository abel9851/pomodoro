from django.test import TestCase
from rest_framework import exceptions
from users.serializers import UserLoginTokenObtainPairSerializer
from users.tests.factories import UserFactory


class TestUserLoginTokenObjtainPairSerializer(TestCase):
    """Test UserLoginTokenObtainPairSerializer"""

    def setUp(self):
        self.serializer = UserLoginTokenObtainPairSerializer
        self.user = UserFactory(username="test", password="test12332")
        self.request_data = {"username": "test", "password": "test12332"}

    def test_valid_serializer(self):
        serializer = self.serializer(data=self.request_data)
        serializer.is_valid()
        data = serializer.validated_data

        self.assertIn("refresh", data)
        self.assertIn("access", data)

    def test_invalid_serializer(self):
        invalid_data = self.request_data.copy()
        invalid_data["password"] = "dsmlasd"
        serializer = self.serializer(data=invalid_data)

        with self.assertRaisesMessage(exceptions.AuthenticationFailed, "Incorrect authentication credentials."):
            serializer.is_valid()
            print(serializer.errors)
