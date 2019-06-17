from rest_framework import serializers

from apiqa_storage.serializers import AttachmentsSerializerMixin
from .models import ModelWithAttachments


class ModelWithAttachmentsSerializer(AttachmentsSerializerMixin,
                                     serializers.ModelSerializer):

    class Meta:
        model = ModelWithAttachments
        fields = ('id', 'name', 'attachments', 'attachment_ids')
