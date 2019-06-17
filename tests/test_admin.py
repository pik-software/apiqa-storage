import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import AttachmentFactory


@pytest.mark.django_db
def test_attachment_changelist(api_client):
    AttachmentFactory.create_batch(size=5)
    url = reverse('admin:apiqa_storage_attachment_changelist')
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_attachment_changeform(api_client):
    attachments = AttachmentFactory.create_batch(size=5)
    url = reverse(
        'admin:apiqa_storage_attachment_change', args=(attachments[0].pk,))
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_attachment_add(api_client):
    url = reverse('admin:apiqa_storage_attachment_add')
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_attachment_delete(api_client):
    attachments = AttachmentFactory.create_batch(size=5)
    url = reverse(
        'admin:apiqa_storage_attachment_delete', args=(attachments[0].pk,))
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK
