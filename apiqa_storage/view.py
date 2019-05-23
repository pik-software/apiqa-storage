from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.core.files.base import File
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import AttachFilesMixin
from .minio_storage import storage, MINIO_META_FILE_NAME


def get_file(file_path):
    minio_file_resp = storage.file_get(file_path)

    filename = minio_file_resp.headers.get(MINIO_META_FILE_NAME) or file_path
    content_length = minio_file_resp.headers.get('Content-Length')
    content_type = minio_file_resp.headers.get('Content-Type')

    resp = FileResponse(File(
        name=filename,
        file=minio_file_resp,
    ))
    if content_length is not None:
        resp['Content-Length'] = content_length

    if content_type is not None:
        resp['Content-Type'] = content_type

    return resp


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attachment_view(request, file_path: str, model: AttachFilesMixin):
    # Проверим, что данному юзеру доступен заданный файл
    get_object_or_404(model, attachments__contains=[{'path': file_path}],
                      user=request.user)

    return get_file(file_path)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attachment_view_staff(request, file_path: str):
    return get_file(file_path)
