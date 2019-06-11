from django.db import models
from django.contrib.auth.models import User

from apiqa_storage.models import (
    AttachFilesMixin, Attachment, ModelWithAttachmentsMixin
)

__all__ = [
    'MyAttachFile',
    'UserAttachFile',
    'MyModelWithAttachments'
]


class MyAttachFile(AttachFilesMixin, models.Model):
    pass


class UserAttachFile(AttachFilesMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MyModelWithAttachments(ModelWithAttachmentsMixin):
    pass
