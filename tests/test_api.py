import unittest
from collections import OrderedDict

import faker
import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import encode_multipart, BOUNDARY, MULTIPART_CONTENT
from django.urls import reverse
from rest_framework import status

from apiqa_storage.files import file_info
from apiqa_storage.models import Attachment


@pytest.mark.django_db
@pytest.mark.usefixtures('logged_client_for_class')
class UploadFileApiTestCase(unittest.TestCase):

    def setUp(self):
        self.fake = faker.Faker('ru_RU')
        self.url = reverse('file_upload-list')

    def test_post_file(self):
        attachment = SimpleUploadedFile(
            self.fake.file_name(category='image', extension='jpeg'),
            b'Data', content_type='image/jpeg'
        )
        post_data = {'file': attachment}

        res = self.logged_user_client.post(
            self.url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)

        assert res.status_code == status.HTTP_201_CREATED
        info = file_info(attachment)
        attachment = Attachment.objects.get(uid=res.data['uid'])
        assert res.data == OrderedDict([
            ('uid', str(attachment.uid)),
            ('created', attachment.created.isoformat()),
            ('name', info.name),
            ('path', attachment.path),
            ('size', info.size),
            ('bucket_name', settings.MINIO_STORAGE_BUCKET_NAME),
            ('content_type', info.content_type),
        ])
