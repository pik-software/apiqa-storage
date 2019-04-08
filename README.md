# apiqa-storage #

This project aim is to provide user storage backend on minio
for all apiqa django projects.

## HowToUse ##

* Add mixin AttachFileMixin to owned user file model

```python
from pik.core.models import BasePHistorical, Owned
from apiqa_storage.mixins import AttachFileMixin

class UserFile(BasePHistorical, Owned, AttachFileMixin):
    permitted_fields = {
        '{app_label}.change_{model_name}': ['attach_file'],
        ...
    }
    ...
    class Meta:
        ...
        permissions = (
            ("change_user_userfile", _("Может менять владельца файла")),
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
from apiqa_storage.view import attach_view

urlpatterns = [  # noqa: pylint=invalid-name
    ...,
    path('download_file/<uuid:uid>/', attach_view, {'model': UserFile}),
    ...
]
```

* Delete file from minio if save transaction failed
* Add minio settings.
[django minio storage usage](https://django-minio-storage.readthedocs.io/en/latest/usage/)

```python
MINIO_STORAGE_ENDPOINT = 'minio:9000'
MINIO_STORAGE_ACCESS_KEY = 'KBP6WXGPS387090EZMG8'
MINIO_STORAGE_SECRET_KEY = 'DRjFXylyfMqn2zilAr33xORhaYz5r9e8r37XPz3A'
MINIO_STORAGE_USE_HTTPS = False
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'local-media'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_STATIC_BUCKET_NAME = 'local-static'
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
```
