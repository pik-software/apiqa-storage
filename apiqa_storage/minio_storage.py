import minio
from urllib3 import HTTPResponse

from . import settings
from .files import FileInfo


def create_minio_client():
    client = minio.Minio(
        endpoint=settings.MINIO_STORAGE_ENDPOINT,
        access_key=settings.MINIO_STORAGE_ACCESS_KEY,
        secret_key=settings.MINIO_STORAGE_SECRET_KEY,
        secure=settings.MINIO_STORAGE_USE_HTTPS,
    )
    return client


class Storage:
    def __init__(self, bucket_name: str = None):
        if bucket_name is not None:
            self.bucket_name = bucket_name
        else:
            self.bucket_name = settings.MINIO_STORAGE_BUCKET_NAME
        self.client = create_minio_client()

    def get_bucket_name(self, bucket_name: str) -> str:
        return bucket_name if bucket_name is not None else self.bucket_name

    def file_get(self, name: str, bucket_name: str = None) -> HTTPResponse:
        return self.client.get_object(
            bucket_name=self.get_bucket_name(bucket_name),
            object_name=name,
        )

    def file_partial_get(self, name: str, bucket_name: str = None,
                         offset: int = 0, length: int = 0) -> HTTPResponse:
        return self.client.get_partial_object(
            bucket_name=self.get_bucket_name(bucket_name),
            object_name=name,
            offset=offset,
            length=length,
        )

    def file_put(self, file_info: FileInfo) -> str:
        return self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=file_info.path,
            data=file_info.data,
            length=file_info.size,
            content_type=file_info.content_type,
        )

    def file_delete(self, name: str):
        self.client.remove_object(self.bucket_name, name)


storage = Storage()  # noqa
