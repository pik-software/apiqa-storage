import logging

from rest_framework import serializers

from .files import file_info, FileInfo
from .minio_storage import storage
from .models import Attachment
from .validators import file_size_validator

logger = logging.getLogger('apiqa-storage')  # noqa


__all__ = [
    'UploadAttachmentSerializer'
]


def delete_files(attach_file_info: FileInfo):
    # noinspection PyBroadException
    try:
        storage.file_delete(attach_file_info.path)
    except Exception:  # noqa
        logger.exception("Delete file failed: %s from bucket: %s",
                         attach_file_info.path, storage.bucket_name)


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

    def update(self, instance, validated_data):
        pass


class AttachmentsSerializerMixin(serializers.Serializer):
    attachments = UploadAttachmentSerializer(many=True, read_only=True)
    attachment_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Attachment.objects.all(),
        source='attachments'
    )
