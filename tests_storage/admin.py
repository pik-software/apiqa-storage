import json

from django.contrib import admin

from .models import MyAttachFile


@admin.register(MyAttachFile)
class MyAttachFileAdmin(admin.ModelAdmin):
    pass

    def attachments(self, instance):
        data = json.loads(instance.data)
        return data
