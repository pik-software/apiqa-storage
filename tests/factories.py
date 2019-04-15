import factory.fuzzy
from django.contrib.auth.models import User

from tests_storage.models import MyAttachFile, UserAttachFile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    is_active = True
    email = factory.Faker('email')


class MyAttachFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MyAttachFile


class UserAttachFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAttachFile

    user = factory.SubFactory(UserFactory)
