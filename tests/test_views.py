from unittest.mock import patch

import faker
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apiqa_storage.files import file_info
from tests_storage.models import MyAttachFile

from .factories import UserFactory, create_file, AttachmentFactory


@pytest.mark.django_db
def test_get_attachment_owner_access(client: APIClient, storage):
    owner_user = UserFactory.create()
    data, meta = create_file(storage, user=owner_user)

    url = reverse('attachments', kwargs={'file_uid': meta['uid']})

    client.force_login(owner_user)
    with patch('apiqa_storage.serializers.storage', storage):
        res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.getvalue() == data


@pytest.mark.django_db
def test_get_attachment_nonowner_access(client: APIClient, storage):
    owner_user = UserFactory.create()
    nonowner_user = UserFactory.create()
    data, meta = create_file(storage, user=owner_user)

    url = reverse('attachments', kwargs={'file_uid': meta['uid']})

    client.force_login(nonowner_user)
    with patch('apiqa_storage.serializers.storage', storage):
        some_res = client.get(url)
    assert some_res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_attachment_staff_access(client: APIClient, storage):
    owner_user = UserFactory.create()
    nonowner_user = UserFactory.create()

    data, meta = create_file(storage, user=owner_user)

    url = reverse('attachments_staff', kwargs={
        'file_uid': meta['uid']
    })

    client.force_login(nonowner_user)
    with patch('apiqa_storage.serializers.storage', storage):
        res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.getvalue() == data


@pytest.mark.django_db
def test_get_attachments_from_db(client: APIClient, storage):
    create_file(storage)
    obj = MyAttachFile.objects.last()
    url = reverse('files-detail', args=(obj.pk, ))

    with patch('apiqa_storage.serializers.storage', storage):
        res = client.get(url)
    file = obj.attachments[0]

    assert res.data['attachments'] == [{
        'uid': file['uid'],
        'name': file['name'],
        'size': file['size'],
        'content_type': file['content_type'],
        'created': file['created'],
    }]


@pytest.mark.django_db
def test_get_attachments_from_another_bucket(client: APIClient, storage):
    owner_user = UserFactory.create()
    nonowner_user = UserFactory.create()

    data, meta = create_file(storage, user=owner_user)

    url = reverse('attachments_staff', kwargs={
        'file_uid': meta['uid']
    })

    client.force_login(nonowner_user)
    # Должен взять не из bucket прописанного в settings, а из test bucket'a
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.getvalue() == data


@pytest.mark.django_db
def test_get_attachment_from_few_models(client: APIClient, storage):
    owner_user = UserFactory.create()
    data, meta = create_file(storage)

    url = reverse('test_project:attachments_staff', kwargs={
        'file_uid': meta['uid']
    })

    client.force_login(owner_user)
    with patch('apiqa_storage.serializers.storage', storage):
        res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.getvalue() == data


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
