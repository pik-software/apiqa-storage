from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from tests_storage.viewsets import ModelWithAttachmentsViewSet

router = routers.SimpleRouter()
router.register('modelwithattachments', ModelWithAttachmentsViewSet,
                base_name='modelwithattachments')

urlpatterns = [  # noqa: pylint=invalid-name
    path('admin/', admin.site.urls),
    path('attachments/', include('apiqa_storage.staff_urls')),
    path('user-attachments/', include('apiqa_storage.urls')),
] + router.urls
