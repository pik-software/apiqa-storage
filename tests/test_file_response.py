import pytest
from django.http import Http404

from apiqa_storage.file_response import get_file_response
from tests.factories import create_file
from tests_storage.models import MyAttachFile


@pytest.mark.django_db
def test_get_file_response(storage):
    data, meta = create_file(storage)

    resp = get_file_response(MyAttachFile, meta['uid'])
    assert resp.getvalue() == data
    assert resp['Content-Length'] == str(len(data))
    assert resp['Content-Type'] == 'image/jpeg'
    assert meta['name'] in resp['Content-Disposition']


@pytest.mark.django_db
def test_get_file_response_not_found(storage):
    create_file(storage)

    with pytest.raises(Http404):
        get_file_response(MyAttachFile, 'undefined')
