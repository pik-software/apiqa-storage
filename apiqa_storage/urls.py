from django.urls import path

from .routers import router
from .views import AttachmentView

urlpatterns = [  # noqa: pylint=invalid-name
    path('<uuid:attachment_uid>', AttachmentView.as_view(),
         name='user-attachments', kwargs={'from_user': True})
] + router.urls
