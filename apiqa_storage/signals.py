from .models import AttachFilesMixin
from .minio_storage import storage


def delete_file_from_storage(
        sender, instance: AttachFilesMixin, **kwargs
) -> bool:
    """
    Func for connect to django signal
    :return:
        True if deleted
        False if sender is not subclass of AttachFile
        raise exception if storage is not available
    """
    if not issubclass(sender, AttachFilesMixin):
        return False

    for file_path in instance.attachments:
        storage.file_delete(file_path)
    return True
