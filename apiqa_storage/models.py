import uuid

from django.conf import settings as django_settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _

from . import settings
from .managers import AttachmentQuerySet


class Attachment(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created = models.DateTimeField(
        verbose_name=_('Создано'),
        editable=False,
        auto_now_add=True
    )
    name = models.CharField(
        verbose_name=_('Имя'),
        max_length=255
    )
    path = models.CharField(
        verbose_name=_('Путь'),
        max_length=512
    )
    size = models.BigIntegerField(
        verbose_name=_('Размер')
    )
    bucket_name = models.CharField(
        max_length=255
    )
    content_type = models.CharField(
        max_length=255
    )
    user = models.ForeignKey(
        to=django_settings.AUTH_USER_MODEL,
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
    object_id = models.UUIDField(
        null=True,
        blank=True
    )
    content_object = GenericForeignKey(
        ct_field='object_content_type',
        fk_field='object_id'
    )
    tags = ArrayField(
        base_field=models.CharField(
            max_length=settings.TAGS_CHARACTER_LIMIT),
        verbose_name=_('Тэги'),
        default=list,
    )

    objects = AttachmentQuerySet.as_manager()

    class Meta:
        verbose_name = _('Вложение')
        verbose_name_plural = _('Вложения')
        ordering = ('-created',)
        indexes = [
            models.Index(
                fields=['object_id'], name='attachment_object_id_idx'),
        ]

    def __str__(self):
        return self.path

    def delete(self, *args, **kwargs):
        from apiqa_storage.serializers import delete_file
        if not self.content_object:
            delete_file(self)
            return super().delete(*args, **kwargs)


class ModelWithAttachmentsMixin(models.Model):
    attachments = GenericRelation(
        to=Attachment,
        object_id_field='object_id',
        content_type_field='object_content_type'
    )

    class Meta:
        abstract = True
