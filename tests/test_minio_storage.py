import io
import pytest
from django.core.files.uploadedfile import UploadedFile
from minio.error import NoSuchKey

from apiqa_storage.files import file_info
from apiqa_storage.minio_storage import storage, MINIO_META_FILE_NAME


def test_storage():
    data = b"some initial byte data"
    test_file = io.BytesIO(data)
    upload_file = UploadedFile(file=test_file, name="test.jpg", size=len(data))

    file_i = file_info(upload_file)
    # TEST UPLOAD
    storage.file_put(file_i)

    # TEST GET
    file_resp = storage.file_get(file_i.path)

    assert file_resp.data == data
    assert file_resp.headers.get(MINIO_META_FILE_NAME) == upload_file.name
    assert file_resp.headers.get('Content-Length') == str(len(data))

    # TEST INFO
    assert storage.file_info(file_i.path) == {
        'content_type': 'image/jpeg',
        'name': 'test.jpg',
        'path': file_i.path,
        'size': len(data),
    }

    # TEST DELETE
    storage.file_delete(file_i.path)
    with pytest.raises(NoSuchKey):
        storage.file_get(file_i.path)


def test_storage_delete_nosuchkey():
    storage.file_delete('nosuchkey')
    storage.file_delete('nosuchkey')
