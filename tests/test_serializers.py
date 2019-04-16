import io
import pytest
from django.core.files.uploadedfile import UploadedFile
from minio.error import NoSuchKey

from apiqa_storage import settings
from apiqa_storage.minio_storage import storage
from apiqa_storage.serializers import (
    AttachmentField,
    AttachFilesSerializers,
    upload_files,
    delete_files,
)

from tests_storage.serializers import MyCreateAttachFilesSerializers
from tests_storage.models import MyAttachFile


def create_uploadfile(size=10, name_len=4, name_ext='.jpg'):
    data = b"b" * size
    test_file = io.BytesIO(data)
    return UploadedFile(
        file=test_file,
        name='a' * name_len + name_ext,
        size=len(data)
    )


def test_attachment_field():
    assert AttachmentField().to_representation("test") == "test"
    with pytest.raises(ValueError):
        AttachmentField().to_representation(object)


def test_attachment_serializers():
    serializer = AttachFilesSerializers(data={
        'attachment_set': [
            create_uploadfile()
        ]
    })
    assert serializer.is_valid()


def test_attachment_serializers_max_file_count():
    serializer = AttachFilesSerializers(data={
        'attachment_set': [create_uploadfile()] * settings.MINIO_STORAGE_MAX_FILES_COUNT  # noqa
    })
    assert serializer.is_valid()

    serializer = AttachFilesSerializers(data={
        'attachment_set': [create_uploadfile()] * (settings.MINIO_STORAGE_MAX_FILES_COUNT + 1)  # noqa
    })
    assert not serializer.is_valid()


def test_attachment_serializers_max_file_size():
    serializer = AttachFilesSerializers(data={
        'attachment_set': [create_uploadfile(settings.MAX_FILE_SIZE)]
    })
    assert serializer.is_valid()

    serializer = AttachFilesSerializers(data={
        'attachment_set': [create_uploadfile(settings.MAX_FILE_SIZE + 1)]
    })
    assert not serializer.is_valid()

    serializer = AttachFilesSerializers(data={
        'attachment_set': [
            create_uploadfile(settings.MAX_FILE_SIZE),
            create_uploadfile(settings.MAX_FILE_SIZE + 1)
        ]
    })
    assert not serializer.is_valid()


def test_attachment_serializers_upload_files():
    assert upload_files({'attachment_set': []}) == []

    data = {
        'attachment_set': [
            create_uploadfile(10),
            create_uploadfile(20)
        ]
    }

    files_info = upload_files(data)

    for file_info in files_info:
        file_info.data.seek(0)
        assert storage.file_get(file_info.path).data == file_info.data.read()

    assert data['attachment_set'] == [
        file_info.path for file_info in files_info
    ]


def test_attachment_serializers_delete_files():
    files_info = upload_files({
        'attachment_set': [
            create_uploadfile(10),
            create_uploadfile(20)
        ]
    })

    delete_files(files_info)

    for file_info in files_info:
        with pytest.raises(NoSuchKey):
            storage.file_get(file_info.path)


def test_attachment_serializers_delete_files_failes(mocker):
    files_info = upload_files({
        'attachment_set': [
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
def test_attachment_serializers_create():
    data = {
        'attachment_set': [
            create_uploadfile(10),
            create_uploadfile(20)
        ]
    }
    MyCreateAttachFilesSerializers().create(data)

    db_obj = MyAttachFile.objects.first()
    assert db_obj.attachment_set == data['attachment_set']

    for file_path in data['attachment_set']:
        assert storage.file_get(file_path)


@pytest.mark.django_db
def test_attachment_serializers_failed_create(mocker):
    data = {
        'attachment_set': [
            create_uploadfile(10),
            create_uploadfile(20),
            create_uploadfile(15)
        ]
    }
    # Провоцируем фейл сохранения модели
    with mocker.patch('apiqa_storage.serializers.'
                      'serializers.ModelSerializer.create',
                      side_effect=Exception()):

        with pytest.raises(Exception):
            MyCreateAttachFilesSerializers().create(data)

    # Проверяем что файлы были удалены
    for file_path in data['attachment_set']:
        with pytest.raises(NoSuchKey):
            storage.file_get(file_path)


@pytest.mark.django_db
def test_attachment_serializers_with_long_name():
    # Проверим что при сохранении в базу имя уже обрезано до достаточной длины
    # В миграции указано что макс длина 100
    assert settings.MINIO_STORAGE_MAX_FILE_NAME_LEN < 200
    data = {
        'attachment_set': [
            create_uploadfile(
                name_len=200
            ),
        ]
    }
    MyCreateAttachFilesSerializers().create(data)

    db_obj = MyAttachFile.objects.first()
    assert db_obj.attachment_set == data['attachment_set']
