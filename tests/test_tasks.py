import pytest
from freezegun import freeze_time

from apiqa_storage.models import Attachment
from apiqa_storage.tasks import purge_attachments
from tests.factories import AttachmentFactory
from tests_storage.models import ModelWithAttachments


@pytest.mark.django_db
def test_clean_attachments():
    with freeze_time("2012-01-14"):
        AttachmentFactory.create_batch(size=10)
    assert Attachment.objects.count() == 10

    purge_attachments()

    assert Attachment.objects.count() == 0


@pytest.mark.django_db
def test_clean_attachments_with_related_models():
    with freeze_time("2012-01-01"):
        attach1, attach2 = AttachmentFactory.create_batch(2)

    user_inst = ModelWithAttachments.objects.create()
    user_inst.attachments.add(attach2)

    purge_attachments()

    assert not Attachment.objects.filter(pk=attach1.pk).exists()
    assert Attachment.objects.filter(pk=attach2.pk).exists()
