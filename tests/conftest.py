import pytest


@pytest.fixture(scope="session", autouse=True)
def minio_storage():
    """
    Создаем и подчищаем minio bucket для тестов
    """
    from apiqa_storage.minio_storage import storage
    if not storage.client.bucket_exists(storage.bucket_name):
        storage.client.make_bucket(storage.bucket_name)

    yield

    if storage.client.bucket_exists(storage.bucket_name):
        item_iter = storage.client.list_objects_v2(storage.bucket_name,
                                                   recursive=True)

        for item in item_iter:
            storage.client.remove_object(storage.bucket_name, item.object_name)

        storage.client.remove_bucket(storage.bucket_name)
