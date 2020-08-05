import uuid

from django.db import models

from apiqa_storage.models import ModelWithAttachmentsMixin


class ModelWithAttachments(ModelWithAttachmentsMixin,
                           models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255,
        default='',
        blank=True
    )
