from django.urls import path, include

from tests_storage.models import UserAttachFile
from tests_storage.views import files


urlpatterns = [  # noqa
    path(
        'attachments/',
        include('apiqa_storage.urls'),
        kwargs={'model': UserAttachFile},
    ),
    path('files/<str:pk>/', files, name='files')
]
