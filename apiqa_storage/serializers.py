import logging
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import settings
from .minio_storage import storage
from .files import file_info

logger = logging.getLogger('apiqa-storage')  # noqa


class AttachmentFile(serializers.FileField):
    def to_representation(self, value):
        # Из базы должен прилетать str
        if not isinstance(value, str):
            raise ValueError(f"Instance is not string: {type(value)}")

        return value


class AttachFilesSerializers(serializers.Serializer):
    attachment_set = serializers.ListField(child=AttachmentFile())

    def validate_attachment_set(self, value):  # noqa
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

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')


class CreateAttachFilesSerializers(AttachFilesSerializers):
    def create(self, validated_data):
        attachment_set = validated_data.pop('attachment_set', [])

        attach_files_info = [
            file_info(attach_file) for attach_file in attachment_set
        ]

        # Upload files
        for attach_file in attach_files_info:
            storage.file_put(attach_file)

        validated_data['attachment_set'] = [
            attach_file.path[:settings.MINIO_STORAGE_MAX_FILE_NAME_LEN]
            for attach_file in attach_files_info
        ]

        try:
            return super().create(validated_data)
        except Exception:
            # Delete files if save model failed
            for attach_file in attach_files_info:
                # noinspection PyBroadException
                try:
                    storage.file_delete(attach_file.path)
                except Exception:  # noqa
                    logger.exception("Delete file failed: %s from bucket: %s",
                                     attach_file.path, storage.bucket_name)
            raise

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')
