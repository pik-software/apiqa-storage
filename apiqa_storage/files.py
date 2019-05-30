import uuid
from collections import namedtuple
from datetime import datetime
import mimetypes
from pathlib import PurePath
import re

from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import UploadedFile
from slugify import slugify

from . import settings

RE_FILE_NAME_SLUGIFY = re.compile(r'[^\w\-.]+')
FileInfo = namedtuple(
    'FileInfo',
    'uid,  '          # uniq id of file
    'name, '          # file name
    'created, '       # datetime of create file
    'path, '          # file path in minio
    'size, '          # file size
    'content_type, '  # content type of file
    'data'            # Instance of django UploadedFile
)


def trim_name(
        name: str,
        max_length=settings.MINIO_STORAGE_MAX_FILE_NAME_LEN,
        suffix_count=2,
) -> str:
    """ Trim path name by max_length

    :param name: name with extension
    :param max_length:  max length of result name
    :param suffix_count:  max count of extension without trim
    :return: trimmed name
    """
    pure_path = PurePath(name)

    # Берем только последние suffix_count расширений
    pure_suffix = "".join(pure_path.suffixes[-suffix_count:])
    # Получаем имя без суффикса
    pure_name = name[:-len(pure_suffix)] if pure_suffix else name

    if len(pure_name) + len(pure_suffix) <= max_length:
        return name

    # Отдаем обрезанное имя с расширением
    if len(pure_suffix) <= max_length:
        return pure_name[:max_length - len(pure_suffix)] + pure_suffix

    # Если у файла длинный конец, то обрезаем его
    return pure_name[:max_length]


def slugify_name(name: str) -> str:
    """Return slugify name of file

    >>> slugify_name('test.jpg')
    test.jpg
    >>> slugify_name('тест.jpg')
    test.jpg
    >>> slugify_name('long_size_name.jpg')
    'long_size_na.jpg
    """
    slug_name = slugify(name, regex_pattern=RE_FILE_NAME_SLUGIFY)
    return slug_name


def create_path(file_name: str) -> str:
    date_now = datetime.now()
    date_path = date_now.strftime("%Y/%m/%d")
    rand_id = get_random_string(8)
    return trim_name(f"{date_path}/{rand_id}-{file_name}")


def content_type(file_name: str) -> str:
    file_type = mimetypes.guess_type(file_name, strict=False)
    return file_type[0] or "application/octet-stream"


def file_info(file: UploadedFile) -> FileInfo:
    file_name = slugify_name(file.name)

    return FileInfo(
        str(uuid.uuid4()),
        file.name,
        datetime.utcnow().isoformat(),
        create_path(file_name),
        file.size,
        content_type(file.name),
        file,
    )
