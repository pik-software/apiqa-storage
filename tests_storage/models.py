from django.contrib.auth.models import User

from apiqa_storage.models import Attachment, ModelWithAttachmentsMixin

__all__ = [
    'ModelWithAttachments'
]


class ModelWithAttachments(ModelWithAttachmentsMixin):
    pass
