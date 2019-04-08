from django.core.files.storage import Storage

from minio_storage.storage import MinioMediaStorage


class LazyMinioStorage(Storage):
    """
    Initilize minio storage on first call on storage
    By default minio storage initilize on load application
    """
    def __init__(self, *args, **kwargs):
        self._storage = None
        super().__init__(*args, **kwargs)

    @property
    def storage(self):
        if self._storage is None:
            self._storage = MinioMediaStorage()

        return self._storage

    def _open(self, name, mode='rb'):
        # pylint: disable=protected-access
        return self.storage._open(name, mode)

    def _save(self, name, content):
        # pylint: disable=protected-access
        return self.storage._save(name, content)

    def delete(self, name):
        return self.storage.delete(name)

    def exists(self, name):
        return self.storage.exists(name)

    def listdir(self, path):
        return self.storage.listdir(path)

    def size(self, name):
        return self.storage.size(name)

    def url(self, name):
        return self.storage.url(name)

    def path(self, name):
        return self.storage.path(name)

    def get_accessed_time(self, name):
        return self.storage.get_accessed_time(name)

    def get_created_time(self, name):
        return self.storage.get_created_time(name)

    def get_modified_time(self, name):
        return self.storage.get_modified_time(name)
