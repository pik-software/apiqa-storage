from django.db import models


class AttachmentQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()
        super().delete(*args, **kwargs)
