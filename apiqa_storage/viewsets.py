from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import UploadAttachmentSerializer


class UploadAttachmentViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin):
    """
    create:
        Upload file
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadAttachmentSerializer
