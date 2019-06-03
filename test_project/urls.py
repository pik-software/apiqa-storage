from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from tests_storage.models import UserAttachFile
from tests_storage.views import StaffViewSet

router = DefaultRouter()
router.register('files', StaffViewSet, basename='files')

urlpatterns = [  # noqa
    path(
        'attachments/',
        include('apiqa_storage.urls'),
        kwargs={'model': UserAttachFile},
    ),
    path(
        'attachments_staff/',
        include('apiqa_storage.staff_urls'),
        kwargs={'app_label': 'tests_storage', 'model_name': 'UserAttachFile'},
    ),
    path('admin/', admin.site.urls),
] + router.urls
