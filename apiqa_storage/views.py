from typing import Type

from django.apps import apps
from django.core.files import File
from django.http import Http404, FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .file_response import get_file_response
from .minio_storage import storage
from .models import AttachFilesMixin, Attachment


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attachment_view(
        request,
        file_uid,
        model: Type[AttachFilesMixin] = None,
        app_label: str = None,
        model_name: str = None,
        app_labels: list = None,
        from_user: bool = False,
):
    user = request.user if from_user else None

    if app_labels and isinstance(app_labels, list):
        for app_label in app_labels:
            if isinstance(app_label, str):
                model = apps.get_model(app_label)
            else:
                raise TypeError("models must be list of str")

            file_resp = get_file_response(model, file_uid, user)
            if file_resp is not None:
                return file_resp
        raise Http404("File not found")

    if app_label:
        model = apps.get_model(app_label, model_name)

    if not model:
        raise ValueError('Set app_label\\model_name or app_labels on view kwargs')

    file_resp = get_file_response(model, file_uid, user)
    if file_resp is not None:
        return file_resp

    raise Http404("File not found")


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
