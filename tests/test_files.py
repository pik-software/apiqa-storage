import io

from datetime import datetime
from freezegun import freeze_time
from django.core.files.uploadedfile import UploadedFile

from apiqa_storage.settings import MINIO_STORAGE_MAX_FILE_NAME_LEN
from apiqa_storage.files import (
    FileInfo,
    trim_name,
    slugify_name,
    create_path,
    content_type,
    file_info)


def test_trim_name_by_length():
    # test normal input
    assert trim_name('12', 3) == '12'
    assert trim_name('123', 3) == '123'
    assert trim_name('12345', 3) == '123'

    # test trim name without ex
    assert trim_name('12345.exe', 7) == '123.exe'
    assert trim_name('12345.exe.exe', 11) == '123.exe.exe'
    assert trim_name('12345.exe.exe.exe', 11) == '123.exe.exe'

    # test trim suffix if len suffix are long
    assert trim_name('12345.exe', 3) == '123'
    assert trim_name('12345.exec', 3) == '123'


def test_slugify_name_normal_input():
    assert slugify_name('ex.exe') == 'ex.exe'
    assert slugify_name('ex') == 'ex'
    assert slugify_name('../ex.exe') == '..-ex.exe'
    assert slugify_name('1-1') == '1-1'

    assert slugify_name(' ex.exe') == 'ex.exe'
    assert slugify_name('ex.exe ') == 'ex.exe'
    assert slugify_name('ex. exe') == 'ex.-exe'

    assert slugify_name('ex_ex.exe') == 'ex_ex.exe'

    assert slugify_name('абв') == 'abv'


def test_slugify_name_extreme_input():
    assert slugify_name('') == ''

    assert slugify_name('.') == '.'
    assert slugify_name('.ex') == '.ex'
    assert slugify_name('ex.') == 'ex.'

    assert slugify_name('-') == ''
    assert slugify_name('1-') == '1'
    assert slugify_name('-1') == '1'
    assert slugify_name('-1-') == '1'

    assert slugify_name('/') == ''


@freeze_time("2012-01-14")
def test_create_path(mocker):
    with mocker.patch('apiqa_storage.files.get_random_string',
                      return_value='random_s'):
        assert create_path('test_path') == '2012/01/14/random_s-test_path'
        assert create_path('') == '2012/01/14/random_s-'


@freeze_time("2012-01-14")
def test_create_path_with_long_name(mocker):
    max_length = MINIO_STORAGE_MAX_FILE_NAME_LEN
    with mocker.patch('apiqa_storage.files.get_random_string',
                      return_value='random_s'):
        long_name = 'a' * (max_length + 100) + '.jpg'
        correct_name = '2012/01/14/random_s-' + 'a' * (max_length - 24) + '.jpg'  # noqa
        assert create_path(long_name) == correct_name


def test_content_type_normal_input():
    assert content_type('t.jpg') == 'image/jpeg'
    assert content_type('t.png') == 'image/png'
    assert content_type('t.pdf') == 'application/pdf'
    assert content_type('t.doc') == 'application/msword'
    assert content_type('t.docx') == 'application/vnd.openxmlformats-office' \
                                     'document.wordprocessingml.document'


def test_content_type_extreme_input():
    assert content_type('t') == 'application/octet-stream'
    assert content_type('') == 'application/octet-stream'
    assert content_type('jpg') == 'application/octet-stream'


@freeze_time("2012-01-14")
def test_file_info(mocker):
    test_file = io.StringIO("some initial text data")
    upload_file = UploadedFile(file=test_file, name="test")

    with mocker.patch('apiqa_storage.files.get_random_string',
                      return_value='random_s'), \
         mocker.patch('apiqa_storage.files.uuid.uuid4',
                      return_value='random_uid'):
        assert file_info(upload_file) == FileInfo(
            name='test', path='2012/01/14/random_s-test', size=None,
            content_type='application/octet-stream', data=upload_file,
            uid='random_uid', created=datetime.now().isoformat()
        )


def test_file_info_content_type():
    upload_file = UploadedFile(
        file=io.StringIO("some initial text data"),
        name='name.jpg'
    )

    assert file_info(upload_file).content_type == 'image/jpeg'


def test_file_info_content_type_with_long_name():
    upload_file = UploadedFile(
        file=io.StringIO("some initial text data"),
        name='b' * MINIO_STORAGE_MAX_FILE_NAME_LEN + '.jpg'
    )

    assert file_info(upload_file).content_type == 'image/jpeg'
