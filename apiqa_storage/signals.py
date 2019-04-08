from .mixins import AttachFileMixin


def delete_file_from_storage(sender,
                             instance: AttachFileMixin,
                             **kwargs) -> bool:
    """
    Func for connect to django signal
    :return:
        True if deleted
        False if sender is not subclass of AttachFile
        raise exception if storage is not available
    """
    if not issubclass(sender, AttachFileMixin):
        return False

    instance.attach_file.delete()
    return True
