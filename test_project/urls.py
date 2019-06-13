from django.contrib import admin
from django.urls import path, include

urlpatterns = [  # noqa: pylint=invalid-name
    path('admin/', admin.site.urls),
    path('attachments/', include('apiqa_storage.staff_urls')),
    path('user-attachments/', include('apiqa_storage.urls')),
]
