import uuid

from django.conf import settings
from django.db import models
from django.db.models import ManyToManyRel
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

    class Meta:
        verbose_name = _('Вложение')
        verbose_name_plural = _('Вложения')

    def __str__(self):
        return self.path

    @property
    def has_relation(self):
        for rel in self._meta.get_fields():
            if isinstance(rel, ManyToManyRel):
                try:
                    related = rel.related_model.objects.filter(
                        **{rel.field.name: self})
                    if related.exists():
                        return True, related
                except AttributeError:
                    pass
                return False, None


class ModelWithAttachmentsMixin(models.Model):
    attachments = models.ManyToManyField(
        verbose_name=_('Вложения'),
        to=Attachment
    )

    class Meta:
        abstract = True
