from uuid import UUID

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attach_view(request, uid: UUID, model):
    employee = getattr(request.user, 'employee', None)

    # Сотрудникам доступны все файлы на просмотр
    user_filter = {'user': request.user} if employee is None else {}

    instance = get_object_or_404(model, pk=uid, **user_filter)

    response = FileResponse(instance.attach_file.file)
    if instance.attach_file.size:
        response['Content-Length'] = instance.attach_file.size

    return response
