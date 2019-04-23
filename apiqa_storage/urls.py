from django.urls import re_path
from apiqa_storage.view import attachment_view


urlpatterns = [  # noqa
    re_path(
        r'(?P<file_path>.+)$',
        attachment_view,
        name='attachments'
    )
]
