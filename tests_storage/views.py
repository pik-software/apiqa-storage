from rest_framework import viewsets

from .models import MyAttachFile
from .serializers import MyCreateAttachFilesSerializers


class StaffViewSet(viewsets.ModelViewSet):
    queryset = MyAttachFile.objects.all()
    serializer_class = MyCreateAttachFilesSerializers
    permission_classes = ()
