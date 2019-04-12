from django.urls import path
from apiqa_storage.view import attachment_view

from tests_storage.models import UserAttachFile

urlpatterns = [  # noqa
    path('attachments/<str:file_path>', attachment_view,
         kwargs={'model': UserAttachFile}, name='attachments')
]
