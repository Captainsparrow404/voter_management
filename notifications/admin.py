from django.contrib import admin
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter
from .models import NotificationType, NotificationTemplate, NotificationLog

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'notification_type', 'subject', 'created_at', 'updated_at')
    list_filter = ('notification_type',)
    search_fields = ('name', 'subject', 'content')
    ordering = ('notification_type', 'name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('notification_type')

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = (
        'recipient',
        'get_template',
        'channel',
        'status',
        'sent_at',
        'created_at'
    )
    list_filter = (
        'status',
        'channel',
        ('sent_at', DateRangeFilter),
        ('created_at', DateRangeFilter),
    )
    search_fields = ('recipient', 'error_message')
    readonly_fields = ('sent_at', 'created_at')
    ordering = ('-created_at',)

    def get_template(self, obj):
        if obj.template:
            return f"{obj.template.notification_type.name} - {obj.template.name}"
        return "N/A"
    get_template.short_description = 'Template'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'template',
            'template__notification_type'
        )