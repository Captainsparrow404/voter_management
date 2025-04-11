from django.db import migrations


def create_initial_data(apps, schema_editor):
    NotificationType = apps.get_model('voters', 'NotificationType')
    NotificationTemplate = apps.get_model('voters', 'NotificationTemplate')

    # Create notification types
    sms_type = NotificationType.objects.create(name='SMS')
    whatsapp_type = NotificationType.objects.create(name='WhatsApp')

    # Create some sample templates
    NotificationTemplate.objects.create(
        name='Welcome Message',
        type=sms_type,
        content='Welcome {voter_name}, Your voter ID is {card_no}'
    )
    NotificationTemplate.objects.create(
        name='Voting Day Reminder',
        type=sms_type,
        content='Dear {voter_name}, Please remember to vote on Election Day.'
    )
    NotificationTemplate.objects.create(
        name='WhatsApp Welcome',
        type=whatsapp_type,
        content='Welcome {voter_name} to our voter management system!'
    )


def reverse_func(apps, schema_editor):
    NotificationType = apps.get_model('voters', 'NotificationType')
    NotificationType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('voters', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_func),
    ]