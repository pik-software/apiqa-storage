import logging
import uuid
from typing import Union

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import settings
from .files import FileInfo, file_info
from .minio_storage import storage
from .models import Attachment
from .validators import file_size_validator

logger = logging.getLogger('apiqa-storage')  # noqa


__all__ = [
    'AttachmentSerializer',
    'AttachmentsSerializerMixin'
]


def delete_file(attach_file_info: Union[FileInfo, Attachment]):
    # noinspection PyBroadException
    try:
        storage.file_delete(attach_file_info.path)
    except Exception:  # noqa
        logger.exception("Delete file failed: %s from bucket: %s",
                         attach_file_info.path, storage.bucket_name)


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True,
                                 validators=[file_size_validator])
    tags = serializers.ListField(
        child=serializers.CharField(
            max_length=settings.TAGS_CHARACTER_LIMIT),
        required=False, max_length=settings.TAGS_COUNT_MAX)

    class Meta:
        model = Attachment
        fields = (
            'file', 'uid', 'created', 'name', 'size', 'content_type', 'tags'
        )
        read_only_fields = (
            'uid', 'created', 'name', 'size', 'content_type', 'tags'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        custom_uid = self.context['request'].query_params.get('uid')
        if custom_uid:
            try:
                uuid.UUID(custom_uid)
            except ValueError:
                raise ValidationError("Incorrect uid")
            if Attachment.objects.filter(uid=custom_uid).exists():
                raise ValidationError(
                    f'Attachment with uid = {custom_uid} already exists.'
                )
        attach_file = validated_data.pop('file')
        attach_file_info = file_info(attach_file)
        storage.file_put(attach_file_info)
        data = {
            'uid': custom_uid or attach_file_info.uid,
            'bucket_name': storage.bucket_name,
            'name': attach_file_info.name,
            'path': attach_file_info.path,
            'size': attach_file_info.size,
            'content_type': attach_file_info.content_type,
            'user': user
        }
        validated_data.update(data)
        try:
            return super().create(validated_data)
        except Exception:
            # Delete files if save model failed
            delete_file(attach_file_info)
            raise


class AttachmentsSerializerMixin(serializers.Serializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    attachment_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Attachment.objects.all(),
        source='attachments', required=False
    )

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', [])
        instance = super().create(validated_data)
        instance.attachments.set(attachments)
        return instance

    @staticmethod
    def validate_attachment_ids(value):
        if len(value) > settings.MINIO_STORAGE_MAX_FILES_COUNT:
            raise serializers.ValidationError(
                _('Max files count: %s' % settings
                  .MINIO_STORAGE_MAX_FILES_COUNT))
        return value
