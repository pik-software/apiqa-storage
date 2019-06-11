import uuid

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext as _


class AttachFilesMixin(models.Model):
    attachments = JSONField(_('Вложения'), default=list, blank=True)

    class Meta:
        abstract = True


class Attachment(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created = models.DateTimeField(
        verbose_name=_('created'),
        editable=False,
        auto_now_add=True
    )
    name = models.CharField(
        verbose_name=_('Имя'),
        max_length=settings.MINIO_STORAGE_MAX_FILE_NAME_LEN
    )
    path = models.CharField(
        verbose_name=_('Путь'),
        max_length=512
    )
    size = models.BigIntegerField(
        verbose_name=_('Размер')
    )
    bucket_name = models.CharField(
        max_length=255,
        default=settings.MINIO_STORAGE_BUCKET_NAME
    )
    content_type = models.CharField(
        max_length=255
    )

    class Meta:
        verbose_name = _('Вложение')
        verbose_name_plural = _('Вложения')


class ModelWithAttachmentsMixin(models.Model):
    attachments = models.ManyToManyField(
        verbose_name=_('Вложения'),
        to=Attachment
    )

    class Meta:
        abstract = True
