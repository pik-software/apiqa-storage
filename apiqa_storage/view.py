from django.apps import apps
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apiqa_storage.file_response import get_file_response
from .models import AttachFilesMixin


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attachment_view(
        request,
        file_uid,
        model: AttachFilesMixin = None,
        app_label: str = None,
        model_name: str = None,
        from_user=False
):
    if app_label and model_name:
        model = apps.get_model(app_label, model_name)

    if not model:
        raise ValueError('Set app_label and model_name on view kwargs')

    if from_user:
        return get_file_response(model, file_uid, request.user)
    else:
        return get_file_response(model, file_uid)
