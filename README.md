# apiqa-storage #

This project aim is to provide user storage backend on minio
for all apiqa django projects.

## HowToUse ##

* Add apiqa-storage to requirements.txt
```
# Minio file storage
git+https://github.com/pik-software/apiqa-storage.git#egg=apiqa-storage
```

* Add mixin AttachFileMixin to owned user file model. Make and run migrations

```python
from apiqa_storage.models import AttachFilesMixin

class UserFile(..., AttachFilesMixin):
    ...
```

* Add serializator mixin at the beginning and add attachments to fields.

```python
from apiqa_storage.serializers import CreateAttachFilesSerializers

class SomeSerializer(CreateAttachFilesSerializers, ...):
    ...

    class Meta:
        ...
        fields = (
            ...
            'attachments',
        )

```

* Register signal delete_file_from_storage on pre_delete. Otherwise file willn't be delete from minio

```python
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from apiqa_storage.signals import delete_file_from_storage

@receiver(pre_delete, sender=UserFile)
def user_file_delete_signal(sender, instance, **kwargs):
    delete_file_from_storage(sender, instance, **kwargs)
```

* Add download file url to urlpatterns. Add kwargs model for get user file object

```python
from django.urls import path, include

urlpatterns = [  # noqa
    path(
        'attachments/',
        include('apiqa_storage.urls'),
        kwargs={'app_label': 'app.UserFile'},
    ),
]
```

* Or add staff download file url to urlpatterns.

```python
from django.urls import path, include

urlpatterns = [  # noqa
    path(
        'attachments/',
        include('apiqa_storage.staff_urls'),
        kwargs={'app_label': 'app.UserFile'},
    ),
]
```

* Insted app_label you can set app_labels in urlpatterns

```python
kwargs={'app_labels': ['app.UserFile', 'app.StaffFile']}
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
* Run test

```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
docker-compose up
pytest --cov .
```
