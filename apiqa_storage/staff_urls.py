from django.urls import path

from .routers import router
from .views import attachment_view


urlpatterns = [  # noqa
    path('<uuid:file_uid>',
        attachment_view,
        name='attachments_staff'
    ),
] + router.urls
