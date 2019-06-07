from typing import Type

from django.apps import apps
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apiqa_storage.file_response import get_file_response
from .models import AttachFilesMixin


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
