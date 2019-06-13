from django.core.files import File
from django.http import FileResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .minio_storage import storage
from .models import Attachment


class AttachmentView(APIView):

    def get(self, request, *args, **kwargs):
        attachment = get_object_or_404(
            Attachment.objects.all(), uid=kwargs['attachment_uid'])
        minio_file_resp = storage.file_get(
            attachment.path, attachment.bucket_name
        )

        resp = FileResponse(
            File(name=attachment.name, file=minio_file_resp)
        )
        resp['Content-Length'] = attachment.size

        return resp
