# apiqa-storage #

This project aim is to provide user storage backend on minio
for all apiqa django projects.

## HowToUse ##

* Add `apiqa-storage` to `requirements.txt`.

```
# Minio file storage
git+https://github.com/pik-software/apiqa-storage.git#egg=apiqa-storage
```

* Add `apiqa_storage` to `INSTALLED_APPS` in settings file.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...,
    'apiqa_storage'
]
```

* Add mixin `ModelWithAttachmentsMixin` to any model. Make and run migrations.

```python
from apiqa_storage.models import ModelWithAttachmentsMixin

class UserFile(ModelWithAttachmentsMixin, ...):
    ...
```

* Add serializer mixin at the beginning and add `attachments`,
 `attachment_ids` to fields.

```python
from apiqa_storage.serializers import AttachmentsSerializerMixin

class ModelWithAttachmentsSerializer(AttachmentsSerializerMixin, ...):
    ...

    class Meta:
        ...
        fields = (..., 'attachments', 'attachment_ids')
```

* Add download and upload file urls to urlpatterns.

```python
from django.urls import path, include

urlpatterns = [
    path('attachments/', include('apiqa_storage.urls')),
]
```

* Or add staff download file url to urlpatterns.

```python
from django.urls import path, include

urlpatterns = [  # noqa
    path('attachments/', include('apiqa_storage.staff_urls')),
]
```

* Add clean files task to celery beat config.

```python
from celery.schedules import crontab
beat_schedule = {
    # apiqa-storage clean files
    'purge_attachments': {
        'task': 'apiqa_storage.tasks.purge_attachments',
        'schedule': crontab(hour=5)
    },
}
```

* Add required minio settings. Create bucket on minio!
[django minio storage usage](https://django-minio-storage.readthedocs.io/en/latest/usage/)

```python
MINIO_STORAGE_ENDPOINT = 'minio:9000'
MINIO_STORAGE_ACCESS_KEY = ...
MINIO_STORAGE_SECRET_KEY = ...
MINIO_STORAGE_BUCKET_NAME = 'local-static'
```
* Other settings
  * **MINIO_STORAGE_MAX_FILE_SIZE**: File size limit for upload, humanfriendly value. 
  See https://humanfriendly.readthedocs.io/en/latest/readme.html#a-note-about-size-units. Default 100M
  * **MINIO_STORAGE_MAX_FILE_NAME_LEN**: File name length limit. Use for database char limit. Default 100
  * **MINIO_STORAGE_MAX_FILES_COUNT**: Limit of files in one object. For example 5 files in ticket. None - is unlimited. Default None
  * **MINIO_STORAGE_USE_HTTPS**: Use https for connect to minio. Default False
  * **MINIO_STORAGE_CLEAN_PERIOD**: Delete files without related objects after N days. Default 30
  
* Run test

```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
docker-compose up
pytest --cov .
```
