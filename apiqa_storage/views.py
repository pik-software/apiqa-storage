from urllib.parse import quote

from django.core.files import File
from django.http import FileResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .http.range import parse_http_range, http_range_valid
from .http.response import PartialHttpResponse, HttpResponseNotSatisfiable
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

        http_range = request.META.get('HTTP_RANGE')
        if http_range:
            ranges = parse_http_range(http_range, attachment.size)
            if not http_range_valid(ranges):
                return HttpResponseNotSatisfiable(attachment.size)

            contents = []
            for file_range in ranges:
                minio_file_resp = storage.file_partial_get(
                    attachment.path, attachment.bucket_name,
                    offset=file_range.start, length=len(file_range)
                )
                contents.append(minio_file_resp)

            resp = PartialHttpResponse(
                ranges, contents, content_type=attachment.content_type
            )

        else:
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

        resp["Accept-Ranges"] = "bytes"
        return resp
