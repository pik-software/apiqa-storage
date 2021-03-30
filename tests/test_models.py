from unittest import mock

import pytest
from minio import S3Error

from apiqa_storage.models import Attachment
from .factories import AttachmentFactory, create_attach_with_file


@pytest.fixture(params=[
    (Attachment, AttachmentFactory),
])
def model_and_factory(request):
    return request.param


@pytest.mark.django_db
def test_create_model_by_factory(model_and_factory):
    model, factory = model_and_factory
    obj1 = factory.create()
    obj2 = model.objects.last()
    assert obj1.pk == obj2.pk
    assert str(obj1) == str(obj2)


@pytest.mark.django_db
def test_model_protocol(model_and_factory):
    model, _ = model_and_factory
    fields = [field.name for field in model._meta.get_fields()]  # noqa
    assert 'uid' in fields
    assert 'created' in fields


@pytest.mark.django_db
def test_attachment_delete(model_and_factory, storage):
    attachments = [create_attach_with_file(storage) for _ in range(10)]
    paths = [attach.path for attach in attachments]

    for path in paths:
        storage.file_get(path)

    with mock.patch('apiqa_storage.serializers.storage', storage):
        Attachment.objects.delete()

    assert Attachment.objects.count() == 0
    for path in paths:
        with pytest.raises(S3Error):
            storage.file_get(path)


@pytest.mark.django_db
def test_delete_duplicate_links(model_and_factory, storage):
    attach = create_attach_with_file(storage)
    attach.pk = None
    attach.save()
    assert Attachment.objects.count() == 2

    storage.file_get(attach.path)

    with mock.patch('apiqa_storage.serializers.storage', storage):
        attach.delete()

    assert Attachment.objects.count() == 1
    attach = Attachment.objects.first()
    storage.file_get(attach.path)

    with mock.patch('apiqa_storage.serializers.storage', storage):
        attach.delete()
    with pytest.raises(S3Error):
        storage.file_get(attach.path)
