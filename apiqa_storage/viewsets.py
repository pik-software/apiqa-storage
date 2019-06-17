from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _

from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin):
    """
    create:
        Upload file
    ---
    destroy:
        Delete file
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = AttachmentSerializer
    queryset = Attachment.objects.all()

    def perform_destroy(self, instance):
        if instance.content_object:
            raise ValidationError(
                _("Delete attachments with relations not allowed"))
        super().perform_destroy(instance)
