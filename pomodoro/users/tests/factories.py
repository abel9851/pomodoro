from typing import Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from faker import Faker as Fake

Fake.seed(0)

fake = Fake()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

    username = Faker("name", locale="ko_KR")
    email = Faker("email")
    first_name = Faker("first_name", locale="ko_KR")
    last_name = Faker("last_name", locale="ko_KR")

    @post_generation
    def password(obj, create: bool, extracted: Sequence, **kwargs):
        if not create:
            return
        password = extracted if extracted else fake.password(length=20, special_chars=True, upper_case=True, lower_case=True)
        obj.set_password(password)
        obj.save()
