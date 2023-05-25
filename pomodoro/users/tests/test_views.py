from django.urls import reverse
from rest_framework.test import APITestCase

from .factories import UserFactory

# userFactory 수정필요하다.
# 조사해서 사용하기
# pdf에는 없다.
# 패스워드 어떻게 만들고 팩토리 어떻게 사용하는지 확인하기
# facker도.
# Userfacotory.build()와 CheeseFacotry의 차이점은 뭐지?


class TestUserApiLogin(APITestCase):
    def setUp(self):
        self.user = UserFactory(username="test123", password="test123")
        self.url = reverse("users:login")

        self.data = {"username": self.user.username, "password": "test123"}

    def test_valid_login(self):
        response = self.client.post(self.url, data=self.data, format="json")

        self.assertEqual(response.status_code, 200)

    # def test_invaild_login(self):
    #     pass


# class TestuserApiLogout(APITestCase):
#     def setUp(self):
#         self.user = UserFactory()
