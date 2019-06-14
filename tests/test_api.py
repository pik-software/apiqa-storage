import json
from collections import OrderedDict
from unittest.mock import patch

import faker
import pytest
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status

from apiqa_storage.files import file_info
from apiqa_storage.models import Attachment
from tests_storage.models import ModelWithAttachments
from .factories import AttachmentFactory


@pytest.mark.django_db
def test_post_file(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_size = fake.random_int(min=1, max=settings.MAX_FILE_SIZE)
    file_data = get_random_string(file_size).encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    post_data = {'file': attachment}

    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)

    assert res.status_code == status.HTTP_201_CREATED
    info = file_info(attachment)
    attachment = Attachment.objects.get(uid=res.data['uid'])
    assert attachment.user == api_client.user
    assert res.data == OrderedDict([
        ('uid', str(attachment.uid)),
        ('created', attachment.created.isoformat()),
        ('name', info.name),
        ('path', attachment.path),
        ('size', info.size),
        ('bucket_name', storage.bucket_name),
        ('content_type', info.content_type),
        ('object_content_type', attachment.object_content_type),
        ('object_id', attachment.object_id),
    ])


@pytest.mark.django_db
def test_post_file_size_validation_error(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_data = get_random_string(settings.MAX_FILE_SIZE + 1).encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    post_data = {'file': attachment}

    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data['file'][0] == (f'Max size of attach file:'
                                   f' {settings.MINIO_STORAGE_MAX_FILE_SIZE}')


@pytest.mark.django_db
def test_post_model_with_attachment(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('modelwithattachments-list')
    attachment = AttachmentFactory()
    post_data = {
        'name': fake.name(),
        'attachment_ids': [str(attachment.pk)]
    }
    res = api_client.post(url, data=json.dumps(post_data),
                          content_type='application/json')
    assert res.status_code == status.HTTP_201_CREATED
    model_with_attachments = ModelWithAttachments.objects.get()
    assert res.data == OrderedDict([
        ('id', model_with_attachments.id),
        ('name', model_with_attachments.name),
        ('attachments', [OrderedDict([
            ('uid', str(attachment.uid)),
            ('created', attachment.created.isoformat()),
            ('name', attachment.name),
            ('path', attachment.path),
            ('size', attachment.size),
            ('bucket_name', attachment.bucket_name),
            ('content_type', attachment.content_type),
            ('object_content_type', attachment.object_content_type.id),
            ('object_id', attachment.object_id),
        ]) for attachment in model_with_attachments.attachments.all()])
    ])
    attachment.refresh_from_db()
    assert attachment.object_id == str(model_with_attachments.pk)
    assert attachment.object_content_type == ContentType.objects.get_for_model(
        model_with_attachments)
