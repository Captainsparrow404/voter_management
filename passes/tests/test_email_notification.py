import unittest
from django.core import mail
from django.test import TestCase, override_settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import User
from passes.models import Pass
import os

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.gmail.com',
    EMAIL_PORT=587,
    EMAIL_USE_TLS=True,
    EMAIL_HOST_USER='captainsparrow2814@gmail.com',
    EMAIL_HOST_PASSWORD='kzwe emau uowy gyzw'
)
class EmailNotificationTest(TestCase):
    databases = '__all__'

    @classmethod
    def setUpTestData(cls):
        # Create test user and pass once for all test methods
        cls.admin_user = User.objects.create_superuser(
            username='Captainsparrow404',
            email='captainsparrow2814@gmail.com',
            password='kzwe emau uowy gyzw'
        )

        cls.test_pass = Pass.objects.create(
            name='Aditi Tomar',
            email='adititomar201098@gmail.com',
            phone='9934567890',
            temple='Sri Mahakaaleshwar Mandir',
            num_persons=2,
            visit_date=timezone.now().date(),
            id_proof_type='AADHAR',
            id_proof_number='123456789012',
            status='PENDING'
        )

    def test_send_approval_email(self):
        """Test sending approval email notification"""
        try:
            # Simulate pass approval
            self.test_pass.status = 'APPROVED'
            self.test_pass.processed_at = timezone.now()
            self.test_pass.processed_by = self.admin_user
            self.test_pass.save()

            # Create email content
            context = {
                'name': self.test_pass.name,
                'temple': self.test_pass.temple,
                'visit_date': self.test_pass.visit_date,
                'num_persons': self.test_pass.num_persons,
                'id_proof_type': self.test_pass.get_id_proof_type_display(),
                'id_proof_number': self.test_pass.id_proof_number,
                'approved_at': self.test_pass.processed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'approved_by': self.test_pass.processed_by.username,
            }

            # Load email template
            html_message = render_to_string(
                'passes/email_templates/pass_approved.html',
                context
            )

            # Send test email
            mail.send_mail(
                subject='Temple Pass Approved',
                message='Your temple pass has been approved.',
                from_email='captainsparrow2814@gmail.com',
                recipient_list=[self.test_pass.email],
                html_message=html_message,
                fail_silently=False,
            )

            print("\nEmail Test Results:")
            print(f"Email sent successfully to: {self.test_pass.email}")
            print(f"From: captainsparrow2814@gmail.com")
            print("\nPass Details:")
            print(f"- Name: {self.test_pass.name}")
            print(f"- Temple: {self.test_pass.temple}")
            print(f"- Visit Date: {self.test_pass.visit_date}")
            print(f"- Number of Persons: {self.test_pass.num_persons}")
            print(f"- ID Proof: {self.test_pass.get_id_proof_type_display()}")
            print(f"- Approved by: {self.test_pass.processed_by.username}")
            print(f"- Approved at: {self.test_pass.processed_at}")

        except Exception as e:
            self.fail(f"Failed to send email: {str(e)}")

if __name__ == '__main__':
    unittest.main()