from django.db import models
from django.contrib.postgres.fields import ArrayField

from . import settings


class AttachFilesMixin(models.Model):
    attachments = ArrayField(models.CharField(
        max_length=settings.MINIO_STORAGE_MAX_FILE_NAME_LEN), default=list)

    class Meta:
        abstract = True
