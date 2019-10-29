from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        'uid', 'created', '_name', 'size', 'content_type',
        'object_content_type', 'object_id'
    )
    search_fields = (
        'uid', 'name', 'content_type', 'object_id', 'bucket_name'
    )
    list_filter = ('content_type', 'bucket_name')
    readonly_fields = ('_name',)

    def _name(self, obj):
        url = reverse('staff-attachments', kwargs={'attachment_uid': obj.uid})
        return format_html(f'<a href="{url}">{obj.name}</a>')
    _name.short_description = _('Имя')
    _name.admin_order_field = 'name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user', 'object_content_type')
        return queryset
