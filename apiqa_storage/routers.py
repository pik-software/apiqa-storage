from rest_framework import routers

from .viewsets import AttachmentViewSet

router = routers.SimpleRouter()
router.register('file-upload', AttachmentViewSet, base_name='file_upload')
