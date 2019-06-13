from django.core.files import File
from django.http import FileResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .minio_storage import storage
from .models import Attachment


class AttachmentView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user if kwargs.get('from_user') else None
        user_filter = {'user': user} if user else {}
        attachment = get_object_or_404(
            Attachment.objects.all(), uid=kwargs['attachment_uid'],
            **user_filter
        )
        minio_file_resp = storage.file_get(
            attachment.path, attachment.bucket_name
        )

        resp = FileResponse(
            File(name=attachment.name, file=minio_file_resp),
            filename=attachment.name
        )
        resp['Content-Length'] = attachment.size

        return resp
