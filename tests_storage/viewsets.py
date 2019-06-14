from rest_framework import viewsets

from .models import ModelWithAttachments
from .serializers import ModelWithAttachmentsSerializer


class ModelWithAttachmentsViewSet(viewsets.ModelViewSet):
    serializer_class = ModelWithAttachmentsSerializer
    queryset = ModelWithAttachments.objects.all()
