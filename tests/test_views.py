import faker
import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import UserFactory, create_attach_with_file


@pytest.mark.django_db
def test_get_attachment(client: APIClient, storage):
    attach = create_attach_with_file(storage)
    url = reverse('staff-attachments', kwargs={
        'attachment_uid': str(attach.uid)
    })
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert b''.join(res) == storage.file_get(attach.path).read()
    assert res.filename == attach.name
    assert res._headers['content-type'] == ('Content-Type',
                                            attach.content_type)
    assert res._headers['content-length'] == ('Content-Length',
                                              str(attach.size))


@pytest.mark.django_db
def test_get_attachment_partial(client: APIClient, storage):
    attach = create_attach_with_file(storage)
    url = reverse('staff-attachments', kwargs={
        'attachment_uid': str(attach.uid)
    })
    res = client.get(url, HTTP_RANGE='bytes=0-3')
    assert res.status_code == status.HTTP_206_PARTIAL_CONTENT
    assert b''.join(res) == storage.file_get(attach.path).read()[0:4]
    assert res._headers['content-type'] == ('Content-Type',
                                            attach.content_type)
    assert res._headers['content-length'] == ('Content-Length', '4')
    assert res._headers['content-range'] == ('Content-Range', 'bytes 0-3/10')


@pytest.mark.django_db
def test_get_attachment_fail(client: APIClient, storage):
    fake = faker.Faker()
    url = reverse('staff-attachments', kwargs={
        'attachment_uid': fake.uuid4()
    })
    res = client.get(url)
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_user_attachment(api_client, storage):
    attach_file_info = create_attach_with_file(storage, api_client.user)
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
    user = UserFactory()
    attach_file_info = create_attach_with_file(storage, user)
    url = reverse('user-attachments', kwargs={
        'attachment_uid': str(attach_file_info.uid)
    })
    res = api_client.get(url)
    assert res.status_code == status.HTTP_404_NOT_FOUND
