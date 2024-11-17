import factory
import factory.fuzzy
from config.settings import AUTH_USER_MODEL
from tasks.models import Task
from projects.models import Project
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AUTH_USER_MODEL

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "pwpwpw01")


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project
        django_get_or_create = ("name",)

    name = factory.sequence(lambda n: f"project_{n}")
    user = factory.SubFactory(UserFactory)
    description = factory.LazyFunction(fake.text)
    color = factory.Faker("hex_color")
    is_active = factory.Faker("boolean")


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.sequence(lambda n: f"task_{n}")
    memo = factory.LazyFunction(fake.text)
    project = factory.SubFactory(ProjectFactory)
    priority = factory.fuzzy.FuzzyChoice(Task.Priority.values)
    due_date = factory.Faker("date_this_year")
    pomodoro_count = factory.Faker("random_int", min=1, max=5)
