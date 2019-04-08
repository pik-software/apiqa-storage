from django.conf.urls import url
from django.contrib import admin

urlpatterns = [  # noqa
    url(r'^admin/', admin.site.urls),
]
