from rest_framework import routers

from .viewsets import UploadAttachmentViewSet

router = routers.SimpleRouter()
router.register('file-upload', UploadAttachmentViewSet,
                base_name='file_upload')
