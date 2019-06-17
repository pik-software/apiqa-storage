from django.db import models

from apiqa_storage.models import Attachment, ModelWithAttachmentsMixin


class ModelWithAttachments(ModelWithAttachmentsMixin,
                           models.Model):
    name = models.CharField(
        max_length=255,
        default='',
        blank=True
    )
