import pytest

from apiqa_storage.http.range import Range, parse_http_range, http_range_valid


@pytest.mark.parametrize(
    'start,finish,size',
    ((0, 0, 1), (0, 1, 2), (1, 1, 2))
)
def test_range_class_valid(start, finish, size):
    assert Range(start, finish, size).valid


@pytest.mark.parametrize(
    'start,finish,size',
    ((-1, 0, 2), (0, -1, 2), (1, 0, 2), (0, 1, 1))
)
def test_range_class_invalid(start, finish, size):
    assert Range(start, finish, size).valid is False


def test_range_class_len():
    # Просим отдать 2 байта, нулевой и первый
    assert len(Range(0, 1, 1)) == 2
    assert len(Range(3, 5, 1)) == 3


def test_range_class_str():
    assert str(Range(0, 1, 2)) == 'bytes 0-1/2'


def test_parse_http_range():
    assert parse_http_range('foo=-5', 10) == [Range(5, 9, 10)]
    assert parse_http_range('foo=0-5', 10) == [Range(0, 5, 10)]
    assert parse_http_range('foo=0-11', 10) == [Range(0, 9, 10)]
    assert parse_http_range('foo=0-', 10) == [Range(0, 9, 10)]
    assert parse_http_range('foo=0-,3-5', 10) == [Range(0, 9, 10),
                                                  Range(3, 5, 10)]


def test_parse_http_range_invalid():
    assert parse_http_range(None, 10) is None
    assert parse_http_range('broken', 10) is None

    assert parse_http_range('foo==', 10) is None
    assert parse_http_range('foo= - = ', 10) is None
    assert parse_http_range('foo=0-1, ', 10) is None
    assert parse_http_range('foo=0-1, -', 10) is None

    assert parse_http_range('foo=-a', 10) is None
    assert parse_http_range('foo=a-1', 10) is None
    assert parse_http_range('foo=0-a', 10) is None

    assert parse_http_range('foo=0-a', 10) is None
    assert parse_http_range('foo=0-a', 10) is None
    assert parse_http_range('foo=0-a', 10) is None

    assert parse_http_range('foo=0-1,1-0', 10) is None
    assert parse_http_range('foo=0-1,,', 10) is None
    assert parse_http_range('foo=0--1', 10) is None
    assert parse_http_range('foo=-15', 10) is None


def test_http_range_valid():
    assert http_range_valid([Range(0, 9, 10), Range(3, 5, 10)]) is True

    assert http_range_valid(None) is False
    assert http_range_valid([]) is False
    assert http_range_valid([Range(-1, 9, 10), Range(3, 5, 10)]) is False
    assert http_range_valid([Range(0, 9, 10), Range(-1, 5, 10)]) is False
