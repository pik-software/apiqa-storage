import pytest
from django.utils.crypto import get_random_string


@pytest.fixture(scope="session")
def storage():
    """
    Создаем и подчищаем minio bucket для тестов
    """
    from apiqa_storage.minio_storage import Storage

    bucket_name = f'test-{get_random_string().lower()}'
    storage = Storage(bucket_name=bucket_name)

    if not storage.client.bucket_exists(storage.bucket_name):
        storage.client.make_bucket(storage.bucket_name)

    yield storage

    if storage.client.bucket_exists(storage.bucket_name):
        item_iter = storage.client.list_objects_v2(storage.bucket_name,
                                                   recursive=True)

        for item in item_iter:
            storage.client.remove_object(storage.bucket_name, item.object_name)

        storage.client.remove_bucket(storage.bucket_name)
