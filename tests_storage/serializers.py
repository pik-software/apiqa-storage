from apiqa_storage.serializers import CreateAttachFilesSerializers

from .models import MyAttachFile


class MyCreateAttachFilesSerializers(CreateAttachFilesSerializers):
    class Meta:
        model = MyAttachFile
        fields = '__all__'
