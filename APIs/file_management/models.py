from django.db import models
from django.conf import settings
from patients.models import Patient
import uuid
import os


def upload_to(instance, filename):
    """Generate upload path for files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('patient_files', str(instance.patient.id), filename)


class FileCategory(models.TextChoices):
    LAB_RESULTS = 'lab_results', 'Lab Results'
    IMAGING = 'imaging', 'Imaging'
    FORMS = 'forms', 'Forms'
    PRESCRIPTIONS = 'prescriptions', 'Prescriptions'
    INSURANCE = 'insurance', 'Insurance Documents'
    OTHER = 'other', 'Other'


class UploadedFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='files')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    file = models.FileField(upload_to=upload_to)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # in bytes
    file_type = models.CharField(max_length=50)  # MIME type
    category = models.CharField(max_length=20, choices=FileCategory.choices, default=FileCategory.OTHER)
    
    # OCR and AI processing
    ocr_text = models.TextField(blank=True)
    structured_data = models.JSONField(default=dict, blank=True)
    is_processed = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    
    # Metadata
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.full_name} - {self.original_filename}"

    @property
    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)

    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            self.file_size = self.file.size
            self.file_type = getattr(self.file.file, 'content_type', 'application/octet-stream')
        super().save(*args, **kwargs)
