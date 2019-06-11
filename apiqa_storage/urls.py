from django.urls import path

from .views import attachment_view


urlpatterns = [  # noqa
    path('<uuid:file_uid>',
        attachment_view,
        name='attachments',
        kwargs={'from_user': True},
    ),
]
