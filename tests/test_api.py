import json
import uuid
from collections import OrderedDict
from unittest.mock import patch

import faker
import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from django.utils.crypto import get_random_string
from minio.error import NoSuchKey
from rest_framework import status

from apiqa_storage import settings
from apiqa_storage.files import file_info
from apiqa_storage.models import Attachment
from tests_storage.models import ModelWithAttachments
from .factories import AttachmentFactory, UserFactory, create_attach_with_file


@pytest.mark.django_db
def test_post_file(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_size = fake.random_int(min=1, max=settings.MAX_FILE_SIZE)
    file_data = get_random_string(file_size).encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    post_data = {
        'file': attachment,
    }

    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)
    assert res.status_code == status.HTTP_201_CREATED
    info = file_info(attachment)
    attachment = Attachment.objects.get(uid=res.data['uid'])
    assert attachment.user == api_client.user
    assert res.data == OrderedDict([
        ('uid', str(attachment.uid)),
        ('created', attachment.created.isoformat()),
        ('name', info.name),
        ('size', info.size),
        ('content_type', info.content_type),
        ('tags', []),
        ('linked_from', attachment.linked_from),
    ])


@pytest.mark.django_db
def test_post_file_with_custom_uid(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_data = get_random_string().encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    attachment_uid = uuid.uuid4()
    post_data = {'file': attachment}

    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url+f'?uid={attachment_uid}',
            data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)

    assert res.status_code == status.HTTP_201_CREATED
    info = file_info(attachment)
    attachment = Attachment.objects.get(uid=res.data['uid'])
    assert attachment.user == api_client.user
    assert res.data == OrderedDict([
        ('uid', str(attachment_uid)),
        ('created', attachment.created.isoformat()),
        ('name', info.name),
        ('size', info.size),
        ('content_type', info.content_type),
        ('tags', []),
        ('linked_from', attachment.linked_from),
    ])


@pytest.mark.django_db
def test_post_file_with_incorrect_uid(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_data = get_random_string().encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    attachment_uid = 'incorrect'
    post_data = {'file': attachment}

    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url+f'?uid={attachment_uid}',
            data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_post_file_with_duplicate_uid(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_data = get_random_string().encode()
    attachment = AttachmentFactory()
    attachment_file = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )

    post_data = {'file': attachment_file}
    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url+f'?uid={attachment.uid}',
            data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data[0] == (f'Attachment with uid = {attachment.uid} '
                           f'already exists.')

@pytest.mark.django_db
def test_post_file_size_validation_error(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_data = get_random_string(settings.MAX_FILE_SIZE + 1).encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    post_data = {'file': attachment}

    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data['file'][0] == (f'Max size of attach file:'
                                   f' {settings.MINIO_STORAGE_MAX_FILE_SIZE}')


@pytest.mark.django_db
def test_destroy_attachment(storage, api_client):
    attachment = create_attach_with_file(storage)
    url = reverse('file_upload-detail', args=(str(attachment.uid),))
    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.delete(url)

    assert res.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(NoSuchKey):
        storage.file_get(attachment.path)


@pytest.mark.django_db
def test_destroy_related_attachment_validation_error(storage, api_client):
    user = UserFactory()
    attachment = AttachmentFactory(
        object_content_type=ContentType.objects.get_for_model(user),
        object_id=user.id
    )
    url = reverse('file_upload-detail', args=(str(attachment.uid),))
    res = api_client.delete(url)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data[0] == 'Delete attachments with relations not allowed'


@pytest.mark.django_db
def test_post_model_with_attachment(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('modelwithattachments-list')
    attachments = AttachmentFactory.create_batch(
        size=settings.MINIO_STORAGE_MAX_FILES_COUNT)
    post_data = {
        'name': fake.name(),
        'attachment_ids': [str(attachment.pk) for attachment in attachments]
    }
    res = api_client.post(url, data=json.dumps(post_data),
                          content_type='application/json')
    assert res.status_code == status.HTTP_201_CREATED
    model_with_attachments = ModelWithAttachments.objects.get()
    assert res.data == OrderedDict([
        ('uid', str(model_with_attachments.uid)),
        ('name', model_with_attachments.name),
        ('attachments', [OrderedDict([
            ('uid', str(attachment.uid)),
            ('created', attachment.created.isoformat()),
            ('name', attachment.name),
            ('size', attachment.size),
            ('content_type', attachment.content_type),
            ('tags', []),
            ('linked_from', attachment.linked_from),
        ]) for attachment in model_with_attachments.attachments.all()])
    ])
    for attachment in attachments:
        attachment.refresh_from_db()
        assert attachment.object_id == model_with_attachments.pk
        assert (attachment.object_content_type == ContentType.objects
                .get_for_model(model_with_attachments))


@pytest.mark.django_db
def test_post_model_with_exising_attachments(storage, api_client):
    fake = faker.Faker('ru_RU')
    file_count = settings.MINIO_STORAGE_MAX_FILES_COUNT
    url = reverse('modelwithattachments-list')
    attachments = AttachmentFactory.create_batch(
        size=file_count)
    post_data = {
        'name': fake.name(),
        'attachment_ids': [str(attachment.pk) for attachment in attachments]
    }
    res = api_client.post(url, data=json.dumps(post_data),
                          content_type='application/json')
    assert res.status_code == status.HTTP_201_CREATED
    assert Attachment.objects.count() == file_count

    res = api_client.post(url, data=json.dumps(post_data),
                          content_type='application/json')
    assert res.status_code == status.HTTP_201_CREATED
    for attach in res.data['attachments']:
        assert attach['name'] == Attachment.objects.filter(
            pk=attach['linked_from'],
        ).first().name
    assert Attachment.objects.count() == file_count * 2
    attach = Attachment.objects.first()
    assert Attachment.objects.filter(path=attach.path).count() == 2


@pytest.mark.django_db
def test_post_model_with_max_files_count_validation_error(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('modelwithattachments-list')
    attachments = AttachmentFactory.create_batch(
        size=settings.MINIO_STORAGE_MAX_FILES_COUNT + 1)
    post_data = {
        'name': fake.name(),
        'attachment_ids': [str(attachment.pk) for attachment in attachments]
    }
    res = api_client.post(url, data=json.dumps(post_data),
                          content_type='application/json')
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert res.data['attachment_ids'][0] == (
        f'Max files count: {settings.MINIO_STORAGE_MAX_FILES_COUNT}')


@pytest.mark.django_db
def test_post_file_with_tags(storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_size = fake.random_int(min=1, max=settings.MAX_FILE_SIZE)
    file_data = get_random_string(file_size).encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    post_data = {
        'file': attachment,
        'tags': [fake.pystr(
            min_chars=1, max_chars=settings.TAGS_CHARACTER_LIMIT)
            for _ in range(fake.random_int(
                min=1, max=settings.TAGS_COUNT_MAX))]
    }

    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)
    assert res.status_code == status.HTTP_201_CREATED
    info = file_info(attachment)
    attachment = Attachment.objects.get(uid=res.data['uid'])
    assert attachment.user == api_client.user
    assert res.data == OrderedDict([
        ('uid', str(attachment.uid)),
        ('created', attachment.created.isoformat()),
        ('name', info.name),
        ('size', info.size),
        ('content_type', info.content_type),
        ('tags', post_data['tags']),
        ('linked_from', attachment.linked_from),
    ])


@pytest.mark.django_db
def test_post_file_with_tags_character_limit_validation_error(
        storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_size = fake.random_int(min=1, max=settings.MAX_FILE_SIZE)
    file_data = get_random_string(file_size).encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    tags_with_character_limit_error = [
        fake.pystr(min_chars=settings.TAGS_CHARACTER_LIMIT + 1,
                   max_chars=settings.TAGS_CHARACTER_LIMIT + 20)]
    post_data = {
        'file': attachment,
        'tags': tags_with_character_limit_error
    }
    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)
    assert res.data['tags'][0][0] == (
        f'Ensure this field has no more than '
        f'{settings.TAGS_CHARACTER_LIMIT} characters.')


@pytest.mark.django_db
def test_post_file_with_tags_count_max_validation_error(
        storage, api_client):
    fake = faker.Faker('ru_RU')
    url = reverse('file_upload-list')
    file_size = fake.random_int(min=1, max=settings.MAX_FILE_SIZE)
    file_data = get_random_string(file_size).encode()
    attachment = SimpleUploadedFile(
        fake.file_name(category='image', extension='jpeg'),
        file_data, content_type='image/jpeg'
    )
    tags_with_count_max_error = [fake.pystr() for _
                                 in range(settings.TAGS_COUNT_MAX + 1)]
    post_data = {
        'file': attachment,
        'tags': tags_with_count_max_error
    }
    with patch('apiqa_storage.serializers.storage', storage):
        res = api_client.post(
            url, data=encode_multipart(BOUNDARY, post_data),
            content_type=MULTIPART_CONTENT)
    assert res.data['tags'][0] == (
        f'Ensure this field has no more than {settings.TAGS_COUNT_MAX} '
        f'elements.')
