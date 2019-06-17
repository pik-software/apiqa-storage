from django.urls import path

from .routers import router
from .views import AttachmentView

urlpatterns = [
    path('<uuid:attachment_uid>', AttachmentView.as_view(),
         name='staff-attachments')
] + router.urls
