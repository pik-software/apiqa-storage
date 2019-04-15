from django.db import models
from django.contrib.auth.models import User

from apiqa_storage.models import AttachFilesMixin

__all__ = [
    'MyAttachFile',
    'UserAttachFile',
]


class MyAttachFile(AttachFilesMixin, models.Model):
    pass


class UserAttachFile(AttachFilesMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
