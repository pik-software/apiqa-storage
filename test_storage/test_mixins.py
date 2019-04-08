import pytest
from pik.core.tests.fixtures import create_user

from .factories import MyAttachFile, MyAttachFileFactory


@pytest.fixture(params=[
    (MyAttachFile, MyAttachFileFactory),
])
def attachfile_model(request):
    return request.param


@pytest.mark.django_db
def test_attach_file_protocol(attachfile_model):
    _, factory = attachfile_model
    user = create_user()
    obj = factory.create(user=user)

    assert obj.minio_storage
    assert not obj.attach_file
    assert obj.attach_content_type is None
