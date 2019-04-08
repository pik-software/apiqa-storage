import pytest
from pik.core.tests.fixtures import create_user

from apiqa_storage.signals import delete_file_from_storage

from .factories import MyAttachFile, MyAttachFileFactory


@pytest.fixture(params=[
    (MyAttachFile, MyAttachFileFactory),
])
def attachfile_model(request):
    return request.param


def test_delete_attach(attachfile_model):
    model, factory = attachfile_model
    obj = factory.create(user=create_user())
    assert delete_file_from_storage(model, obj) is True
    assert delete_file_from_storage(object, obj) is False
