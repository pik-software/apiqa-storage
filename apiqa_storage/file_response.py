import logging
from typing import Type

from django.core.files import File
from django.db import models
from django.http import FileResponse

from apiqa_storage.minio_storage import storage

logger = logging.getLogger(__name__)


def get_file_response(model: Type[models.Model], file_uid: str, user=None):
    user_filter = {'user': user} if user else {}

    obj = model.objects.filter(
        attachments__contains=[{'uid': str(file_uid)}],
        **user_filter,
    ).first()

    if obj is None:
        return None

    attachments = [
        file for file in obj.attachments if file['uid'] == str(file_uid)
    ]

    if len(attachments) > 1:
        logger.warning("Few files with uid %s", file_uid)

    file = attachments[0]

    minio_file_resp = storage.file_get(file['path'], file['bucket_name'])

    resp = FileResponse(File(
        name=file['name'],
        file=minio_file_resp,
    ), as_attachment=True)
    resp['Content-Length'] = file['size']

    return resp
