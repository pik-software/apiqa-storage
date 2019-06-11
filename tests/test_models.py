import pytest

from apiqa_storage.models import Attachment
from tests_storage.models import MyModelWithAttachments
from .factories import (
    MyAttachFile, MyAttachFileFactory, ModelWithAttachmentsFactory,
    AttachmentFactory
)


@pytest.fixture(params=[
    (MyAttachFile, MyAttachFileFactory),
    (Attachment, AttachmentFactory),
    (MyModelWithAttachments, ModelWithAttachmentsFactory),
])
def model_and_factory(request):
    return request.param


@pytest.fixture(params=[
    (MyAttachFile, MyAttachFileFactory),
    (MyModelWithAttachments, ModelWithAttachmentsFactory),
])
def model_and_factory_with_attachments(request):
    return request.param


@pytest.mark.django_db
def test_create_model_by_factory(model_and_factory):
    model, factory = model_and_factory
    obj1 = factory.create()
    obj2 = model.objects.last()
    assert obj1.pk == obj2.pk
    assert str(obj1) == str(obj2)


@pytest.mark.django_db
def test_model_protocol(model_and_factory_with_attachments):
    model, _ = model_and_factory_with_attachments
    fields = [field.name for field in model._meta.get_fields()]  # noqa
    assert 'attachments' in fields
