from django.contrib import admin
from django.urls import path, include

urlpatterns = [  # noqa
    path('admin/', admin.site.urls),
    path('attachments/', include('apiqa_storage.urls')),
]
