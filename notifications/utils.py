from django.conf import settings
from twilio.rest import Client
from .models import NotificationLog
import datetime

class NotificationSender:
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

    def send_sms(self, recipient, message):
        try:
            self.client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=recipient
            )
            return True, None
        except Exception as e:
            return False, str(e)

    def send_whatsapp(self, recipient, message):
        try:
            self.client.messages.create(
                body=message,
                from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
                to=f'whatsapp:{recipient}'
            )
            return True, None
        except Exception as e:
            return False, str(e)

    def send_notification(self, notification_log):
        success = False
        error_message = None

        if notification_log.channel in ['SMS', 'BOTH']:
            sms_success, sms_error = self.send_sms(
                notification_log.recipient,
                notification_log.template.content
            )
            if not sms_success:
                error_message = f"SMS Error: {sms_error}"

        if notification_log.channel in ['WA', 'BOTH']:
            wa_success, wa_error = self.send_whatsapp(
                notification_log.recipient,
                notification_log.template.content
            )
            if not wa_success:
                error_message = f"{error_message}\nWhatsApp Error: {wa_error}" if error_message else f"WhatsApp Error: {wa_error}"

        success = error_message is None
        notification_log.status = NotificationLog.Status.SENT if success else NotificationLog.Status.FAILED
        notification_log.error_message = error_message or ''
        notification_log.sent_at = datetime.datetime.now() if success else None
        notification_log.save()

        return success, error_message