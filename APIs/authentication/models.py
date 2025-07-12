from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    PHYSICIAN = 'physician', 'Physician'
    NURSE = 'nurse', 'Nurse'
    PHYSICAL_THERAPIST = 'pt', 'Physical Therapist'
    OCCUPATIONAL_THERAPIST = 'ot', 'Occupational Therapist'
    SOCIAL_WORKER = 'sw', 'Social Worker'


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.NURSE)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
