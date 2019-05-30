from unittest.mock import patch

import pytest
from minio.error import NoSuchKey

from apiqa_storage import settings
from apiqa_storage.serializers import (
    AttachmentField,
    upload_files,
    delete_files,
)
from tests.factories import create_uploadfile

from tests_storage.serializers import MyCreateAttachFilesSerializers
from tests_storage.models import MyAttachFile


def test_attachment_field():
    # ('uid', 'name', 'size', 'content_type')
    assert AttachmentField().to_representation({
        'uid': 1,
        'name': 1,
        'size': 1,
        'content_type': 1,
        'foo': 'buz',
    }) == {
        'uid': 1,
        'name': 1,
        'size': 1,
        'content_type': 1,
    }


def test_attachment_serializers():
    serializer = MyCreateAttachFilesSerializers(data={
        'attachments': [
            create_uploadfile()
        ]
    })
    assert serializer.is_valid()


def test_attachment_serializers_max_file_count():
    serializer = MyCreateAttachFilesSerializers(data={
        'attachments': [create_uploadfile()] * settings.MINIO_STORAGE_MAX_FILES_COUNT  # noqa
    })
    assert serializer.is_valid()

    serializer = MyCreateAttachFilesSerializers(data={
        'attachments': [create_uploadfile()] * (settings.MINIO_STORAGE_MAX_FILES_COUNT + 1)  # noqa
    })
    assert not serializer.is_valid()


def test_attachment_serializers_max_file_size():
    serializer = MyCreateAttachFilesSerializers(data={
        'attachments': [create_uploadfile(settings.MAX_FILE_SIZE)]
    })
    assert serializer.is_valid()

    serializer = MyCreateAttachFilesSerializers(data={
        'attachments': [create_uploadfile(settings.MAX_FILE_SIZE + 1)]
    })
    assert not serializer.is_valid()

    serializer = MyCreateAttachFilesSerializers(data={
        'attachments': [
            create_uploadfile(settings.MAX_FILE_SIZE),
            create_uploadfile(settings.MAX_FILE_SIZE + 1)
        ]
    })
    assert not serializer.is_valid()


def test_attachment_serializers_upload_files(storage):
    with patch('apiqa_storage.serializers.storage', storage):
        assert upload_files({'attachments': []}) == []

        data = {
            'attachments': [
                create_uploadfile(10),
                create_uploadfile(20)
            ]
        }

        files_info = upload_files(data)

    for file_info in files_info:
        file_info.data.seek(0)
        assert storage.file_get(file_info.path).data == file_info.data.read()

    assert data['attachments'] == [
        {'uid': file_info.uid,
         'bucket_name': storage.bucket_name,
         'name': file_info.name,
         'created': file_info.created,
         'path': file_info.path,
         'content_type': file_info.content_type,
         'size': file_info.size
         } for file_info in files_info
    ]


def test_attachment_serializers_delete_files(storage):
    with patch('apiqa_storage.serializers.storage', storage):
        files_info = upload_files({
            'attachments': [
                create_uploadfile(10),
                create_uploadfile(20)
            ]
        })

        delete_files(files_info)

    for file_info in files_info:
        with pytest.raises(NoSuchKey):
            storage.file_get(file_info.path)


def test_attachment_serializers_delete_files_failes(mocker, storage):
    with patch('apiqa_storage.serializers.storage', storage):
        files_info = upload_files({
            'attachments': [
                create_uploadfile(10),
                create_uploadfile(20)
            ]
        })
    # Провоцируем фейл удаления файлов
    with mocker.patch('apiqa_storage.serializers.storage.file_delete',
                      side_effect=Exception()):
        # Убеждаемся что exception не вылает наверх
        delete_files(files_info)


@pytest.mark.django_db
def test_attachment_serializers_create(storage):
    data = {
        'attachments': [
            create_uploadfile(10),
            create_uploadfile(20)
        ]
    }
    with patch('apiqa_storage.serializers.storage', storage):
        MyCreateAttachFilesSerializers().create(data)

    db_obj = MyAttachFile.objects.first()
    assert db_obj.attachments == data['attachments']

    for file in data['attachments']:
        assert storage.file_get(file['path'])


@pytest.mark.django_db
def test_attachment_serializers_failed_create(mocker, storage):
    data = {
        'attachments': [
            create_uploadfile(10),
            create_uploadfile(20),
            create_uploadfile(15)
        ]
    }
    # Провоцируем фейл сохранения модели
    with mocker.patch('apiqa_storage.serializers.'
                      'serializers.ModelSerializer.create',
                      side_effect=Exception()), \
         pytest.raises(Exception), \
         patch('apiqa_storage.serializers.storage', storage):
            MyCreateAttachFilesSerializers().create(data)

    # Проверяем что файлы были удалены
    for file in data['attachments']:
        with pytest.raises(NoSuchKey):
            storage.file_get(file['path'])


@pytest.mark.django_db
def test_attachment_serializers_with_long_name(storage):
    # Проверим что при сохранении в базу имя уже обрезано до достаточной длины
    # В миграции указано что макс длина 100
    assert settings.MINIO_STORAGE_MAX_FILE_NAME_LEN < 200
    data = {
        'attachments': [
            create_uploadfile(
                name_len=200
            ),
        ]
    }
    with patch('apiqa_storage.serializers.storage', storage):
        MyCreateAttachFilesSerializers().create(data)

    db_obj = MyAttachFile.objects.first()
    assert db_obj.attachments == data['attachments']
