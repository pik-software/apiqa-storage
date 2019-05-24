import io
import pytest

from django.urls import reverse
from django.core.files.uploadedfile import UploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient

from apiqa_storage import settings
from apiqa_storage.files import file_info
from apiqa_storage.serializers import upload_files
from apiqa_storage.minio_storage import storage

from .factories import (
    UserFactory,
    UserAttachFileFactory,
    MyAttachFileFactory)


@pytest.mark.django_db
def test_get_attachment_owner_access(client: APIClient):
    owner_user = UserFactory.create()
    nonowner_user = UserFactory.create()

    data = b"some initial byte data"
    test_file = io.BytesIO(data)
    upload_file = UploadedFile(file=test_file, name="test.jpg", size=len(data))

    data_dict = {
        'attachments': [upload_file]
    }
    upload_files(data_dict)

    UserAttachFileFactory(
        user=owner_user,
        **data_dict
    )

    url = reverse('attachments', kwargs={'file_path': data_dict['attachments'][0]['path']})

    client.force_login(owner_user)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.getvalue() == data
    assert res['Content-Length'] == str(len(data))
    assert res['Content-Type'] == 'image/jpeg'

    client.force_login(nonowner_user)
    some_res = client.get(url)
    assert some_res.status_code == status.HTTP_404_NOT_FOUND


@override_settings(ROOT_URLCONF='test_project.staff_urls')
@pytest.mark.django_db
def test_get_attachment_staff_access(client: APIClient):
    nonowner_user = UserFactory.create()

    data = b"some initial byte data"
    test_file = io.BytesIO(data)
    upload_file = UploadedFile(file=test_file, name="test.jpg", size=len(data))

    data_dict = {
        'attachments': [upload_file]
    }
    upload_files(data_dict)

    UserAttachFileFactory(
        user=nonowner_user,
        **data_dict
    )

    url = reverse('attachments_staff', kwargs={'file_path': data_dict['attachments'][0]['path']})

    client.force_login(nonowner_user)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.getvalue() == data
    assert res['Content-Length'] == str(len(data))
    assert res['Content-Type'] == 'image/jpeg'


@pytest.mark.django_db
def test_get_attachment_content_type_with_long_name(client: APIClient):
    owner_user = UserFactory.create()

    data = b"some initial byte data"
    test_file = io.BytesIO(data)
    file_name = 't' * (settings.MINIO_STORAGE_MAX_FILE_NAME_LEN + 100) + '.jpg'
    upload_file = UploadedFile(file=test_file, name=file_name, size=len(data))

    data_dict = {
        'attachments': [upload_file]
    }
    upload_files(data_dict)

    UserAttachFileFactory(
        user=owner_user,
        **data_dict
    )

    url = reverse('attachments', kwargs={'file_path': data_dict['attachments'][0]['path']})

    client.force_login(owner_user)
    res = client.get(url)
    assert res['Content-Type'] == 'image/jpeg'


@pytest.mark.django_db
def test_get_attachment_from_db(client: APIClient):
    data = b"some initial byte data"
    test_file = io.BytesIO(data)
    file_name = 't' * (settings.MINIO_STORAGE_MAX_FILE_NAME_LEN + 100) + '.jpg'
    upload_file = UploadedFile(file=test_file, name=file_name, size=len(data))

    data_dict = {
        'attachments': [upload_file]
    }
    upload_files(data_dict)

    obj = MyAttachFileFactory(
        **data_dict
    )

    url = reverse('files', args=(obj.pk, ))

    res = client.get(url)
    assert res.data['attachments'] == data_dict['attachments']
