import io
from unittest.mock import patch

import factory.fuzzy
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.crypto import get_random_string

from apiqa_storage.serializers import upload_files
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


class UserAttachFileFactory(MyAttachFileFactory):
    class Meta:
        model = UserAttachFile

    user = factory.SubFactory(UserFactory)


def create_uploadfile(size=10, name_len=4, name_ext='.jpg'):
    data = get_random_string(size).encode()
    test_file = io.BytesIO(data)
    return UploadedFile(
        file=test_file,
        name=get_random_string(name_len) + name_ext,
        size=len(data)
    )


def create_file(storage, size=10, name_len=4, user=None):
    upload_file = create_uploadfile(size, name_len)
    data = upload_file.read()
    upload_file.seek(0)

    data_dict = {
        'attachments': [upload_file]
    }

    with patch('apiqa_storage.serializers.storage', storage):
        upload_files(data_dict)

    if user:
        UserAttachFileFactory(
            user=user,
            **data_dict
        )
    else:
        MyAttachFileFactory(
            **data_dict
        )

    return data, data_dict['attachments'][0]
