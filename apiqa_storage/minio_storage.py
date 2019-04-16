import minio

from . import settings
from .files import FileInfo

# Minio имеет определенный формат для сохранений меты информации,
# потому в начало добавлен X-Amz-Meta
MINIO_META_FILE_NAME = 'X-Amz-Meta-Name'


def create_minio_client():
    client = minio.Minio(
        endpoint=settings.MINIO_STORAGE_ENDPOINT,
        access_key=settings.MINIO_STORAGE_ACCESS_KEY,
        secret_key=settings.MINIO_STORAGE_SECRET_KEY,
        secure=settings.MINIO_STORAGE_USE_HTTPS,
    )
    return client


class Storage:
    def __init__(self):
        self.bucket_name = settings.MINIO_STORAGE_BUCKET_NAME
        self.client = create_minio_client()

    def file_get(self, name: str):
        return self.client.get_object(
            bucket_name=self.bucket_name,
            object_name=name,
        )

    def file_put(self, file_info: FileInfo) -> str:
        return self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=file_info.path,
            data=file_info.data,
            length=file_info.size,
            content_type=file_info.content_type,
            metadata={
                MINIO_META_FILE_NAME: file_info.name,
            }
        )

    def file_delete(self, name: str):
        self.client.remove_object(self.bucket_name, name)

    def file_info(self, name: str) -> dict:
        object_info = self.client.stat_object(self.bucket_name, name)
        return {
            'path': name,
            'name': object_info.metadata.get(MINIO_META_FILE_NAME, None),
            'size': object_info.size,
            'content_type': object_info.content_type,
        }


storage = Storage()  # noqa
