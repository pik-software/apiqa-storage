import logging

from rest_framework import serializers

from . import settings
from .files import file_info
from .minio_storage import storage
from .models import Attachment
from .validators import file_size_validator

logger = logging.getLogger('apiqa-storage')  # noqa


__all__ = [
    'CreateAttachFilesSerializers',
    'AttachFilesSerializers',
    'UploadAttachmentSerializer'
]


class AttachmentField(serializers.FileField):
    def to_representation(self, data):
        return {
            key: value for key, value in data.items()
            if key in ('uid', 'name', 'size', 'content_type', 'created')
        }


class AttachFilesSerializers(serializers.Serializer):  # noqa: pylint=abstract-method
    attachments = serializers.ListField(
        child=AttachmentField(),
        max_length=settings.MINIO_STORAGE_MAX_FILES_COUNT,
        default=list,
    )

    def validate_attachments(self, value):  # noqa
        """
        Длина имени файла тут не валидируется. Смотри files.py # slugify_name
        """
        # Validate files size
        for attach_file in value:
            file_size_validator(attach_file)
        return value


def upload_files(validated_data: dict):
    attachments = validated_data.pop('attachments', [])

    attach_files_info = [
        file_info(attach_file) for attach_file in attachments
    ]

    # Upload files
    for attach_file in attach_files_info:
        # TODO: В середине процесса может случиться ошибка
        # из хранилки не удалятся загруженные данные
        storage.file_put(attach_file)

    validated_data['attachments'] = [
        {
            'uid': attach_file.uid,
            'bucket_name': storage.bucket_name,
            'name': attach_file.name,
            'created': attach_file.created,
            'path': attach_file.path,
            'size': attach_file.size,
            'content_type': attach_file.content_type,
        }
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


class CreateAttachFilesSerializers(AttachFilesSerializers, serializers.ModelSerializer):  # noqa: pylint=abstract-method
    def create(self, validated_data):
        attach_files_info = upload_files(validated_data)

        try:
            return super().create(validated_data)
        except Exception:
            # Delete files if save model failed
            delete_files(attach_files_info)
            raise


class UploadAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True,
                                 validators=[file_size_validator])

    class Meta:
        model = Attachment
        fields = (
            'file', 'uid', 'created', 'name', 'path', 'size', 'bucket_name',
            'content_type'
        )
        read_only_fields = (
            'uid', 'created', 'name', 'path', 'size', 'bucket_name',
            'content_type'
        )

    def create(self, validated_data):
        attach_file = validated_data.pop('file')
        attach_file_info = file_info(attach_file)
        storage.file_put(attach_file_info)
        validated_data = {
            'uid': attach_file_info.uid,
            'bucket_name': storage.bucket_name,
            'name': attach_file_info.name,
            'path': attach_file_info.path,
            'size': attach_file_info.size,
            'content_type': attach_file_info.content_type,
        }
        return super().create(validated_data)
