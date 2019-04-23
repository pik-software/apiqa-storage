from collections import namedtuple
from datetime import datetime
import mimetypes
import re

from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import UploadedFile
from slugify import slugify

from . import settings

RE_FILE_NAME_SLUGIFY = re.compile(r'[^\w\-.]+')
FileInfo = namedtuple(
    'FileInfo',
    'name, '          # file name
    'path, '          # file path in minio
    'size, '          # file size
    'content_type, '  # content type of file
    'data'            # Instance of django UploadedFile
)


def slugify_name(name: str) -> str:
    slug_name = slugify(name, regex_pattern=RE_FILE_NAME_SLUGIFY)
    max_length = settings.MINIO_STORAGE_MAX_FILE_NAME_LEN
    # Just trim begin of file name to max length
    if len(slug_name) > max_length:
        return slug_name[len(slug_name) - max_length:]

    return slug_name


def create_path(file_name: str) -> str:
    date_now = datetime.now()
    date_path = date_now.strftime("%Y/%m/%d")
    rand_id = get_random_string(8)
    return f"{date_path}/{rand_id}-{file_name}"[:settings.MINIO_STORAGE_MAX_FILE_NAME_LEN]  # noqa


def content_type(file_name: str) -> str:
    file_type = mimetypes.guess_type(file_name, strict=False)
    return file_type[0] or "application/octet-stream"


def file_info(file: UploadedFile) -> FileInfo:
    file_name = slugify_name(file.name)

    return FileInfo(
        file_name,
        create_path(file_name),
        file.size,
        content_type(file.name),
        file,
    )
