from django.db import models
from django.utils.translation import gettext_lazy as _

class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_types'
        verbose_name = 'Notification Type'
        verbose_name_plural = 'Notification Types'
        ordering = ['name']

    def __str__(self):
        return self.name

class NotificationTemplate(models.Model):
    name = models.CharField(max_length=100)
    notification_type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        related_name='templates'
    )
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_templates'
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
        ordering = ['notification_type', 'name']

    def __str__(self):
        return f"{self.notification_type.name} - {self.name}"

class NotificationLog(models.Model):
    class Channel(models.TextChoices):
        SMS = 'SMS', _('SMS')
        WHATSAPP = 'WA', _('WhatsApp')
        BOTH = 'BOTH', _('Both')

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        SENT = 'SENT', _('Sent')
        FAILED = 'FAILED', _('Failed')

    recipient = models.CharField(max_length=20)
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs'
    )
    channel = models.CharField(
        max_length=5,
        choices=Channel.choices,
        default=Channel.SMS
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification_logs'
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status'], name='notif_status_idx'),
            models.Index(fields=['sent_at'], name='notif_sent_idx'),
            models.Index(fields=['recipient'], name='notif_recipient_idx'),
        ]

    def __str__(self):
        return f"{self.recipient} - {self.template} - {self.status}"