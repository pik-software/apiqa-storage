import io

import factory.fuzzy
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.utils.crypto import get_random_string

from apiqa_storage.models import Attachment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    is_active = True
    email = factory.Faker('email')


class AttachmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attachment

    name = factory.Faker('file_name')
    path = factory.Faker('uri_path')
    size = factory.Faker('random_int', min=1, max=999999)
    bucket_name = settings.MINIO_STORAGE_BUCKET_NAME
    content_type = factory.Faker('mime_type')


def create_uploadfile(size=10, name_len=4, name_ext='.jpg'):
    data = get_random_string(size).encode()
    test_file = io.BytesIO(data)
    return UploadedFile(
        file=test_file,
        name=get_random_string(name_len) + name_ext,
        size=len(data)
    )
