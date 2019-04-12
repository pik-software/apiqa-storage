import io
import pytest

from django.urls import reverse
from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from apiqa_storage.files import file_info
from apiqa_storage.minio_storage import storage

from .factories import (
    UserFactory,
    UserAttachFileFactory,
)


@pytest.mark.django_db
def test_get_attachment_owner_access(client: APIClient):
    owner_user = UserFactory.create()
    nonowner_user = UserFactory.create()

    data = b"some initial byte data"
    test_file = io.BytesIO(data)
    upload_file = UploadedFile(file=test_file, name="test.jpg", size=len(data))
    file_i = file_info(upload_file)

    # upload file to storage
    storage.file_put(file_i)

    UserAttachFileFactory(
        user=owner_user,
        attachment_set=[
            file_i.path
        ]
    )

    url = reverse('attachments', kwargs={'file_path': file_i.path})

    client.force_login(owner_user)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert res.getvalue() == data
    assert res['Content-Length'] == str(len(data))
    assert res['Content-Type'] == 'image/jpeg'

    client.force_login(nonowner_user)
    some_res = client.get(url)
    assert some_res.status_code == status.HTTP_404_NOT_FOUND
