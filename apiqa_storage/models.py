import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _


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
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    object_content_type = models.ForeignKey(
        to=ContentType,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    object_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    content_object = GenericForeignKey(
        ct_field='object_content_type',
        fk_field='object_id'
    )

    class Meta:
        verbose_name = _('Вложение')
        verbose_name_plural = _('Вложения')

    def __str__(self):
        return self.path
