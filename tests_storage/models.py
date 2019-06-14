from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apiqa_storage.models import Attachment


class ModelWithAttachments(models.Model):
    name = models.CharField(
        max_length=255,
        default='',
        blank=True
    )
    attachments = GenericRelation(
        to=Attachment,
        content_type_field='object_content_type',
        object_id_field='object_id',
        related_query_name='models'
    )
