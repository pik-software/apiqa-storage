from django.urls import path

from .views import attachment_view
from .routers import router


urlpatterns = [  # noqa
    path('<uuid:file_uid>',
        attachment_view,
        name='attachments',
        kwargs={'from_user': True},
    ),
] + router.urls
