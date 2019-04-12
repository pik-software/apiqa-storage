import logging
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import settings
from .minio_storage import storage
from .files import file_info

logger = logging.getLogger('apiqa-storage')  # noqa


__all__ = [
    'CreateAttachFilesSerializers',
    'AttachFilesSerializers',
]


class AttachmentField(serializers.FileField):
    def to_representation(self, value):
        # Из базы должен прилетать str
        if not isinstance(value, str):
            raise ValueError(f"Instance is not string: {type(value)}")

        return value


class AttachFilesSerializers(serializers.ModelSerializer):  # noqa: pylint=abstract-method
    attachment_set = serializers.ListField(child=AttachmentField())

    def validate_attachment_set(self, value):  # noqa
        """
        Длина имени файла тут не валидируется. Смотри files.py # slugify_name
        """
        # Validate files count
        max_file_count = settings.MINIO_STORAGE_MAX_FILES_COUNT
        if max_file_count is not None and len(value) > max_file_count:
            raise ValidationError(f"Max count of files: {max_file_count}")

        # Validate files size
        for attach_file in value:
            if attach_file.size > settings.MAX_FILE_SIZE:
                raise ValidationError(
                    f'Max size of attach file: '
                    f'{settings.MINIO_STORAGE_MAX_FILE_SIZE}'
                )

        return value


def upload_files(validated_data: dict):
    attachment_set = validated_data.pop('attachment_set', [])

    attach_files_info = [
        file_info(attach_file) for attach_file in attachment_set
    ]

    # Upload files
    for attach_file in attach_files_info:
        # TODO: В середине процесса может случиться ошибка
        # из хранилки не удалятся загруженные данные
        storage.file_put(attach_file)

    validated_data['attachment_set'] = [
        attach_file.path[:settings.MINIO_STORAGE_MAX_FILE_NAME_LEN]
        for attach_file in attach_files_info
    ]
    return attach_files_info


def delete_files(attach_files_info: list):
    for attach_file in attach_files_info:
        # noinspection PyBroadException
        try:
            storage.file_delete(attach_file.path)
        except Exception:  # noqa
            logger.exception("Delete file failed: %s from bucket: %s",
                             attach_file.path, storage.bucket_name)


class CreateAttachFilesSerializers(AttachFilesSerializers):  # noqa: pylint=abstract-method
    def create(self, validated_data):
        attach_files_info = upload_files(validated_data)

        try:
            return super().create(validated_data)
        except Exception:
            # Delete files if save model failed
            delete_files(attach_files_info)
            raise
