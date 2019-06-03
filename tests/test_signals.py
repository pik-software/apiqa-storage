import io
from unittest.mock import patch

import pytest

from django.core.files.uploadedfile import UploadedFile
from minio.error import NoSuchKey

from apiqa_storage.files import file_info
from apiqa_storage.signals import delete_file_from_storage

from .factories import MyAttachFile, MyAttachFileFactory


@pytest.fixture(params=[
    (MyAttachFile, MyAttachFileFactory),
])
def attachfile_model(request):
    return request.param


@pytest.mark.django_db
def test_delete_attach(attachfile_model, storage):
    model, factory = attachfile_model

    data = b"some initial byte data"
    test_file = io.BytesIO(data)
    upload_file = UploadedFile(file=test_file, name="test.jpg", size=len(data))
    file_i = file_info(upload_file)

    # upload file to storage
    storage.file_put(file_i)

    obj = factory(
        attachments=[
            {
                'path': file_i.path,
            }

        ]
    )
    with patch('apiqa_storage.signals.storage', storage):
        assert delete_file_from_storage(model, obj) is True
        with pytest.raises(NoSuchKey):
            storage.file_get(file_i.path)

        assert delete_file_from_storage(object, obj) is False


@pytest.mark.django_db
def test_delete_attach_nosuchkey(attachfile_model, storage):
    model, factory = attachfile_model

    obj = factory(
        attachments=[
            {
                'path': 'nosuchfile',
            }
        ]
    )
    with patch('apiqa_storage.signals.storage', storage):
        assert delete_file_from_storage(model, obj) is True
