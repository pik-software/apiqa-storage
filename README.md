# apiqa-storage #

This project aim is to provide user storage backend on minio
for all apiqa django projects.

## HowToUse ##

* Add apiqa-storage to requirements.txt
```
# Minio file storage
git+ssh://git@gitlab.pik-software.ru:22022/apiqa/apiqa-storage.git#egg=apiqa-storage
```

* Add mixin AttachFileMixin to owned user file model

```python
from apiqa_storage.models import AttachFilesMixin

class UserFile(..., AttachFilesMixin):
    ...
```

* Add serializator mixin at the beginning and add attachment_set to fields

```python
from apiqa_storage.serializers import CreateAttachFilesSerializers

class SomeSerializer(CreateAttachFilesSerializers, ...):
    ...

    class Meta:
        ...
        fields = (
            ...
            'attachment_set',
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
from django.urls import path
from apiqa_storage.view import attachment_view

urlpatterns = [  # noqa: pylint=invalid-name
    ...,
    path('attachment-file/<str:file_path>', attachment_view,
         kwargs={'model': UserFile}),
    ...
]
```

* Add required minio settings. Create bucket on minio!
[django minio storage usage](https://django-minio-storage.readthedocs.io/en/latest/usage/)

```python
MINIO_STORAGE_ENDPOINT = 'minio:9000'
MINIO_STORAGE_ACCESS_KEY = ...
MINIO_STORAGE_SECRET_KEY = ...
MINIO_STORAGE_BUCKET_NAME = 'local-static'
```
