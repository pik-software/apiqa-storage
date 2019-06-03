from unittest.mock import patch

import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests_storage.models import MyAttachFile

from .factories import UserFactory, create_file


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
