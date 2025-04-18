from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Pass(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    TEMPLE_CHOICES = [
        ('Sri Mahakaaleshwar Mandir', 'Sri Mahakaaleshwar Mandir'),
        ('Tirumala Tirupati Devasthanam', 'Tirumala Tirupati Devasthanam'),
        ('Dwaraka Tirumala Devasthanam', 'Dwaraka Tirumala Devasthanam'),
        ('Sree Padmanabha Swamy Devasthanam', 'Sree Padmanabha Swamy Devasthanam'),
        (
        'Sri Bhramaramba Mallikarjuna Swamy Varla Devasthanam', 'Sri Bhramaramba Mallikarjuna Swamy Varla Devasthanam'),
        ('Sri Gnanaprasunambika Sametha Srikalahasteeswara Temple',
         'Sri Gnanaprasunambika Sametha Srikalahasteeswara Temple'),
        ('Shri Shirdi Sayee Samsthan', 'Shri Shirdi Sayee Samsthan'),
        ('Sabarimala Sree Ayyappa Devasthanam', 'Sabarimala Sree Ayyappa Devasthanam'),
        ('Shree Jagannath Temple', 'Shree Jagannath Temple'),
        ('Shri Kashi Vishwanath Temple', 'Shri Kashi Vishwanath Temple'),
        ('Swayambhu Sri Varasiddhi Vinayaka Swamy', 'Swayambhu Sri Varasiddhi Vinayaka Swamy'),
        ('Sri Kamakshi Ambal Devasthanam', 'Sri Kamakshi Ambal Devasthanam'),
        ('Ram Lala Ayodha', 'Ram Lala Ayodha'),
        ('Arulmigu Arunachaleswarar Temple', 'Arulmigu Arunachaleswarar Temple'),
    ]

    ID_PROOF_CHOICES = [
        ('AADHAR', 'Aadhar Card'),
        ('VOTER', 'Voter ID'),
        ('PAN', 'PAN Card'),
        ('DL', 'Driving License'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    temple = models.CharField(max_length=100, choices=TEMPLE_CHOICES)
    num_persons = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Number of persons must be at least 1"),
            MaxValueValidator(6, message="Maximum 6 persons allowed per pass")
        ],
        help_text="Maximum 6 persons allowed per pass"
    )
    visit_date = models.DateField()
    # Add ID proof fields
    id_proof_type = models.CharField(
        max_length=10,
        choices=ID_PROOF_CHOICES,
        verbose_name='ID Proof Type'
    )
    id_proof_number = models.CharField(
        max_length=50,
        verbose_name='ID Proof Number'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_passes'
    )

    class Meta:
        verbose_name = 'Pass'
        verbose_name_plural = 'Passes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.temple} - {self.status}"

    def save(self, *args, **kwargs):
        # Capitalize ID proof number
        if self.id_proof_number:
            self.id_proof_number = self.id_proof_number.upper()
        super().save(*args, **kwargs)

    @staticmethod
    def has_approval_today():
        return Pass.objects.filter(
            status='APPROVED',
            processed_at__date=timezone.now().date()
        ).exists()