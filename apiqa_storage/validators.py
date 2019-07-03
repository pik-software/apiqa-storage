from . import settings
from rest_framework.exceptions import ValidationError


def file_size_validator(attach_file):
    if attach_file.size > settings.MAX_FILE_SIZE:
        raise ValidationError(
            f'Max size of attach file: '
            f'{settings.MINIO_STORAGE_MAX_FILE_SIZE}'
        )
