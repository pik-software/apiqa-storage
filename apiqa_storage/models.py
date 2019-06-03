from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext as _


class AttachFilesMixin(models.Model):
    attachments = JSONField(_('Вложения'), default=list, blank=True)

    class Meta:
        abstract = True
