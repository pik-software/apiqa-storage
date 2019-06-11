from django.urls import path

from .routers import router
from .views import AttachmentView

urlpatterns = [  # noqa
    path('<uuid:attachment_uid>', AttachmentView.as_view(),
         name='attachments-list')
] + router.urls
