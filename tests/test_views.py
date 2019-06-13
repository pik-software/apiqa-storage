import faker
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apiqa_storage.files import file_info

from .factories import AttachmentFactory, UserFactory


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
    url = reverse('attachments', kwargs={
        'attachment_uid': str(attach_file_info.uid)
    })
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.filename == attach_file_info.name
    assert res._headers['content-type'] == ('Content-Type',
                                            attach_file_info.content_type)
    assert res._headers['content-length'] == ('Content-Length',
                                              str(attach_file_info.size))


@pytest.mark.django_db
def test_get_attachment_fail(client: APIClient, storage):
    fake = faker.Faker()
    url = reverse('attachments', kwargs={
        'attachment_uid': fake.uuid4()
    })
    res = client.get(url)
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_user_attachment(api_client, storage):
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
        content_type=attach_file_info.content_type,
        user=api_client.user
    )
    url = reverse('user-attachments', kwargs={
        'attachment_uid': str(attach_file_info.uid)
    })
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.filename == attach_file_info.name
    assert res._headers['content-type'] == ('Content-Type',
                                            attach_file_info.content_type)
    assert res._headers['content-length'] == ('Content-Length',
                                              str(attach_file_info.size))


@pytest.mark.django_db
def test_get_user_attachment_fail(api_client, storage):
    fake = faker.Faker()
    user = UserFactory()
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
        content_type=attach_file_info.content_type,
        user=user
    )
    url = reverse('user-attachments', kwargs={
        'attachment_uid': str(attach_file_info.uid)
    })
    res = api_client.get(url)
    assert res.status_code == status.HTTP_404_NOT_FOUND
