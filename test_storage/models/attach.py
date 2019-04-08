from pik.core.models import Owned

from apiqa_storage.mixins import AttachFileMixin

__all__ = [
    'MyAttachFile',
]


class MyAttachFile(AttachFileMixin, Owned):
    pass
