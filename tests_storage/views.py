from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import MyAttachFile
from .serializers import MyCreateAttachFilesSerializers


@api_view(['GET'])
def files(request, pk):
    instance = MyAttachFile.objects.get(pk=pk)
    serializer = MyCreateAttachFilesSerializers(instance)
    return Response(serializer.data)
