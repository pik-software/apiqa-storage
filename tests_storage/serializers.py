from apiqa_storage.serializers import (
    AttachFilesSerializers,
    CreateAttachFilesSerializers,
)

from .models import MyAttachFile


class MyAttachFilesSerializers(AttachFilesSerializers):
    class Meta:
        model = MyAttachFile
        fields = '__all__'


class MyCreateAttachFilesSerializers(CreateAttachFilesSerializers):
    class Meta:
        model = MyAttachFile
        fields = '__all__'
