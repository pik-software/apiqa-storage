import pytest

from apiqa_storage.models import Attachment
from .factories import AttachmentFactory


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
