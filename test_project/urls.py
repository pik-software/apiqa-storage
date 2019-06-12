from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tests_storage.views import StaffViewSet

router = DefaultRouter()
router.register('files', StaffViewSet, basename='files')

urlpatterns = [  # noqa
    path(
        'attachments/',
        include('apiqa_storage.attachment_urls'),
        kwargs={'app_label': 'tests_storage.UserAttachFile'},
    ),
    path(
        'attachments_staff/',
        include('apiqa_storage.staff_urls'),
        kwargs={'app_label': 'tests_storage', 'model_name': 'UserAttachFile'},
    ),
    path(
        'all_attachments/',
        include(('apiqa_storage.staff_urls', 'test_project')),
        kwargs={'app_labels': ['tests_storage.UserAttachFile', 'tests_storage.MyAttachFile']},
    ),
    path('admin/', admin.site.urls),
    path('attachments-list/', include('apiqa_storage.urls')),
] + router.urls
