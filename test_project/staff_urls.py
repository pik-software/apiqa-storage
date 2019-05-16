from django.urls import path, include

from tests_storage.models import UserAttachFile


urlpatterns = [  # noqa
    path(
        'attachments/',
        include('apiqa_storage.staff_urls'),
    ),
]
