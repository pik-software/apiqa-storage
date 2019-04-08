from django.db import models
from django.utils.translation import ugettext_lazy as _

from .storage import LazyMinioStorage


class AttachFileMixin(models.Model):
    minio_storage = LazyMinioStorage()

    attach_file = models.FileField(_('Вложение'), storage=minio_storage)

    @property
    def attach_content_type(self):
        if self.attach_file:
            return self.attach_file.file.obj.headers.get('Content-Type')

        return None

    class Meta:
        abstract = True
