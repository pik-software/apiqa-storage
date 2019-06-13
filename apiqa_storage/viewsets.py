from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _

from .serializers import UploadAttachmentSerializer


class UploadAttachmentViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin):
    """
    create:
        Upload file
    destroy:
        Delete file
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadAttachmentSerializer

    def perform_destroy(self, instance):
        if instance.has_relation:
            raise ValidationError(
                _("Delete attachments with relations not allowed"))
        super().perform_destroy(instance)
