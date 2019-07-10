from urllib.parse import quote

from django.core.files import File
from django.http import FileResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .minio_storage import storage
from .models import Attachment


class AttachmentView(APIView):
    def get_queryset(self):
        return Attachment.objects.all()

    def get(self, request, *args, **kwargs):
        user_filter = {'user': request.user} if kwargs.get('from_user') else {}
        queryset = self.get_queryset()
        attachment = get_object_or_404(
            queryset, uid=kwargs['attachment_uid'], **user_filter
        )
        minio_file_resp = storage.file_get(
            attachment.path, attachment.bucket_name
        )

        resp = FileResponse(
            File(name=attachment.name, file=minio_file_resp),
            filename=attachment.name
        )
        resp['Content-Length'] = attachment.size
        resp['Content-Disposition'] = "filename*=utf-8''{}".format(quote(
            attachment.name))

        return resp
