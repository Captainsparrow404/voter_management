from django.http import JsonResponse
from django.utils import timezone
from .models import NotificationTemplate, NotificationLog
from django.views.decorators.http import require_http_methods
import json
from django.views.decorators.http import require_http_methods
from .models import NotificationTemplate, NotificationLog


@require_http_methods(["GET"])
def get_templates(request, type_id):
    """Get templates for a specific notification type"""
    templates = NotificationTemplate.objects.filter(
        notification_type_id=type_id
    ).values('id', 'name')
    return JsonResponse({'templates': list(templates)})


@require_http_methods(["POST"])
def send_notifications(request):
    """Send notifications to selected voters"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        channel = data.get('channel')
        recipients = data.get('recipients', [])

        if not all([template_id, channel, recipients]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required parameters'
            })

        template = NotificationTemplate.objects.get(id=template_id)

        # Create notification logs
        logs = []
        for recipient in recipients:
            logs.append(NotificationLog(
                recipient=recipient,
                template=template,
                channel=channel
            ))

        # Bulk create logs
        NotificationLog.objects.bulk_create(logs)

        # Here you would integrate with your actual notification service
        # For now, we'll just mark them as sent
        NotificationLog.objects.filter(
            template=template,
            recipient__in=recipients
        ).update(
            status=NotificationLog.Status.SENT,
            sent_at=timezone.now()
        )

        return JsonResponse({'success': True})

    except NotificationTemplate.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Template not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })