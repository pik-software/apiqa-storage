import faker
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apiqa_storage.files import file_info

from .factories import AttachmentFactory


@pytest.mark.django_db
def test_get_attachment(client: APIClient, storage):
    fake = faker.Faker()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        b'Data', content_type='image/jpeg'
    )
    attach_file_info = file_info(attachment)
    storage.file_put(attach_file_info)
    AttachmentFactory(
        uid=attach_file_info.uid, name=attach_file_info.name,
        path=attach_file_info.path, size=attach_file_info.size,
        bucket_name=storage.bucket_name,
        content_type=attach_file_info.content_type
    )
    url = reverse('attachments-list', kwargs={
        'attachment_uid': str(attach_file_info.uid)
    })
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
