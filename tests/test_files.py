import io
from freezegun import freeze_time
from django.core.files.uploadedfile import UploadedFile

from apiqa_storage.files import (
    FileInfo,
    slugify_name,
    create_path,
    content_type,
    file_info
)


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
        assert create_path('test_path') == '2012-01-14-random_s-test_path'
        assert create_path('') == '2012-01-14-random_s-'


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
                      return_value='random_s'):
        assert file_info(upload_file) == FileInfo(
            name='test', path='2012-01-14-random_s-test', size=None,
            content_type='application/octet-stream', data=upload_file
        )
