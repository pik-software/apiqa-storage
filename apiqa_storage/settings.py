from django.conf import settings
import humanfriendly

# humanfriendly value
# see: https://humanfriendly.readthedocs.io/en/latest/readme.html#a-note-about-size-units  # noqa
MINIO_STORAGE_MAX_FILE_SIZE = getattr(
    settings, 'MINIO_STORAGE_MAX_FILE_SIZE', "100M")
MAX_FILE_SIZE = humanfriendly.parse_size(MINIO_STORAGE_MAX_FILE_SIZE)

assert MAX_FILE_SIZE > 0, "File size is small"

# Необходимо промигрировать базу при изменении этого значения
MINIO_STORAGE_MAX_FILE_NAME_LEN = getattr(
    settings, 'MINIO_STORAGE_MAX_FILE_NAME_LEN', 100)

assert MINIO_STORAGE_MAX_FILE_NAME_LEN > 0, "File name is small"

# Максимальное колмчество файлов в одном объекте
# Например 5 вложений в одном тикете
# None - неограничено
MINIO_STORAGE_MAX_FILES_COUNT = getattr(
    settings, 'MINIO_STORAGE_MAX_FILES_COUNT', None)

MINIO_STORAGE_USE_HTTPS = getattr(
    settings, 'MINIO_STORAGE_USE_HTTPS', False)

# Проверяем, что пользователь добавил все необходимые настройки
MINIO_STORAGE_ENDPOINT = settings.MINIO_STORAGE_ENDPOINT
MINIO_STORAGE_ACCESS_KEY = settings.MINIO_STORAGE_ACCESS_KEY
MINIO_STORAGE_SECRET_KEY = settings.MINIO_STORAGE_SECRET_KEY
MINIO_STORAGE_BUCKET_NAME = settings.MINIO_STORAGE_BUCKET_NAME

MINIO_STORAGE_CLEAN_PERIOD = getattr(
    settings, 'MINIO_STORAGE_CLEAN_PERIOD', 30)

TAGS_COUNT_MAX = 10
TAGS_CHARACTER_LIMIT = 100
