from django.db import models
from django.conf import settings
from patients.models import Patient


class MessageType(models.TextChoices):
    PHYSICIAN_UPDATE = 'physician_update', 'Physician Update'
    STATUS_REPORT = 'status_report', 'Status Report'
    URGENT_ALERT = 'urgent_alert', 'Urgent Alert'
    CARE_PLAN_UPDATE = 'care_plan', 'Care Plan Update'
    GENERAL = 'general', 'General Communication'


class CommunicationThread(models.Model):
    """A conversation thread about a specific patient"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='communication_threads')
    subject = models.CharField(max_length=200)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='communication_threads')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_urgent = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.patient.full_name} - {self.subject}"


class Message(models.Model):
    """Individual messages within a communication thread"""
    thread = models.ForeignKey(CommunicationThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    message_type = models.CharField(max_length=20, choices=MessageType.choices, default=MessageType.GENERAL)
    content = models.TextField()
    
    # AI-generated content
    is_ai_generated = models.BooleanField(default=False)
    ai_template_used = models.CharField(max_length=100, blank=True)
    
    # Attachments and references
    attached_files = models.JSONField(default=list, blank=True)  # File IDs
    referenced_visits = models.JSONField(default=list, blank=True)  # Visit IDs
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Read status
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, through='MessageReadStatus', related_name='read_messages')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.get_full_name()} - {self.message_type} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class MessageReadStatus(models.Model):
    """Track who has read which messages"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['message', 'user']


class MessageTemplate(models.Model):
    """Templates for AI-generated messages"""
    name = models.CharField(max_length=100)
    message_type = models.CharField(max_length=20, choices=MessageType.choices)
    template_content = models.TextField()
    
    # Template variables that can be filled with patient/visit data
    variables = models.JSONField(default=dict, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_message_type_display()})"
