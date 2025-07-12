from django.db import models
from django.conf import settings
from patients.models import Patient


class VisitType(models.TextChoices):
    SKILLED_NURSING = 'SN', 'Skilled Nursing'
    PHYSICAL_THERAPY = 'PT', 'Physical Therapy'
    OCCUPATIONAL_THERAPY = 'OT', 'Occupational Therapy'
    SPEECH_THERAPY = 'ST', 'Speech Therapy'
    MEDICAL_SOCIAL = 'MSW', 'Medical Social Work'
    HOME_HEALTH_AIDE = 'HHA', 'Home Health Aide'


class VisitStatus(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    NO_SHOW = 'no_show', 'No Show'


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    clinician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visits')
    visit_type = models.CharField(max_length=5, choices=VisitType.choices)
    status = models.CharField(max_length=15, choices=VisitStatus.choices, default=VisitStatus.SCHEDULED)
    
    scheduled_date = models.DateTimeField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Clinical data
    chief_complaint = models.TextField(blank=True)
    vital_signs = models.JSONField(default=dict, blank=True)  # BP, HR, Temp, etc.
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)
    
    # AI-generated content
    ai_summary = models.TextField(blank=True)
    ai_recommendations = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.get_visit_type_display()} ({self.scheduled_date.date()})"


class VisitNote(models.Model):
    NOTE_TYPES = [
        ('structured', 'Structured'),
        ('unstructured', 'Unstructured'),
        ('voice_transcript', 'Voice Transcript'),
        ('ai_generated', 'AI Generated'),
    ]

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='notes')
    note_type = models.CharField(max_length=20, choices=NOTE_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    structured_data = models.JSONField(default=dict, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.visit} - {self.title}"


class DocumentationTemplate(models.Model):
    name = models.CharField(max_length=100)
    discipline = models.CharField(max_length=5, choices=VisitType.choices)
    template_data = models.JSONField()  # Dynamic form structure
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_discipline_display()})"
