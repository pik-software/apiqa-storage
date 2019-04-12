from django.conf import settings
import humanfriendly

# humanfriendly value
# see: https://humanfriendly.readthedocs.io/en/latest/readme.html#a-note-about-size-units  # noqa
MINIO_STORAGE_MAX_FILE_SIZE = getattr(
    settings, 'MINIO_STORAGE_MAX_FILE_SIZE', "100M")
MAX_FILE_SIZE = humanfriendly.parse_size(MINIO_STORAGE_MAX_FILE_SIZE)

MINIO_STORAGE_MAX_FILE_NAME_LEN = getattr(
    settings, 'MINIO_STORAGE_MAX_FILE_NAME_LEN', 100)

# Max count of files in one object.
# For example 5 attachment file in one ticket
# If None - inlimited
MINIO_STORAGE_MAX_FILES_COUNT = getattr(
    settings, 'MINIO_STORAGE_MAX_FILES_COUNT', None)

MINIO_STORAGE_USE_HTTPS = getattr(
    settings, 'MINIO_STORAGE_USE_HTTPS', False)

# Проверяем, что пользователь добавил все необходимые настройки
MINIO_STORAGE_ENDPOINT = settings.MINIO_STORAGE_ENDPOINT
MINIO_STORAGE_ACCESS_KEY = settings.MINIO_STORAGE_ACCESS_KEY
MINIO_STORAGE_SECRET_KEY = settings.MINIO_STORAGE_SECRET_KEY
MINIO_STORAGE_BUCKET_NAME = settings.MINIO_STORAGE_BUCKET_NAME
