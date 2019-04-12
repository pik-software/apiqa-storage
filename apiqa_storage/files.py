from collections import namedtuple
from datetime import datetime
import mimetypes
import re

from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import UploadedFile
from slugify import slugify

RE_FILE_NAME_SLUGIFY = re.compile(r'[^\w\-.]+')
FileInfo = namedtuple(
    'FileInfo',
    'name, '
    'path, '
    'size, '
    'content_type, '
    'data'
)


def slugify_name(name: str) -> str:
    return slugify(name, regex_pattern=RE_FILE_NAME_SLUGIFY)


def create_path(file_name: str) -> str:
    date_now = datetime.now()
    date_path = date_now.strftime("%Y-%m-%d")
    rand_id = get_random_string(8)
    return f"{date_path}-{rand_id}-{file_name}"


def content_type(file_name: str) -> str:
    file_type = mimetypes.guess_type(file_name, strict=False)
    return file_type[0] or "application/octet-stream"


def file_info(file: UploadedFile) -> FileInfo:
    """
    :return:
        слагифицированное имя файла
        путь для сохранения в storage
        размер файла
        content type файла
    """
    file_name = slugify_name(file.name)

    return FileInfo(
        file_name,
        create_path(file_name),
        file.size,
        content_type(file_name),
        file,
    )
