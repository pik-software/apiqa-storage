from datetime import datetime, timedelta

from celery import shared_task

from apiqa_storage.models import Attachment
from apiqa_storage import settings


@shared_task()
def purge_attachments():
    """ Удаляет непривязанные вложения
    старше MINIO_STORAGE_CLEAN_PERIOD дней
    """
    now = datetime.now()
    delta = timedelta(days=settings.MINIO_STORAGE_CLEAN_PERIOD)

    Attachment.objects.filter(
        created__lt=now - delta,
        object_id__isnull=True,
    ).delete()
