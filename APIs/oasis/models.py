from django.db import models
from django.conf import settings
from patients.models import Patient


class OasisAssessmentType(models.TextChoices):
    START_OF_CARE = 'SOC', 'Start of Care'
    RESUMPTION_OF_CARE = 'ROC', 'Resumption of Care'
    RECERTIFICATION = 'RECERT', 'Recertification'
    OTHER_FOLLOW_UP = 'FU', 'Other Follow-up'
    TRANSFER = 'TRANSFER', 'Transfer'
    DISCHARGE = 'DC', 'Discharge'


class OasisAssessment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='oasis_assessments')
    clinician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    assessment_type = models.CharField(max_length=10, choices=OasisAssessmentType.choices)
    assessment_date = models.DateField()
    
    # OASIS-E Data (simplified version - in reality this would have 100+ fields)
    # Patient Demographics
    zip_code = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    race_ethnicity = models.JSONField(default=dict, blank=True)
    
    # Prior Functioning
    prior_functioning_adl = models.JSONField(default=dict, blank=True)
    prior_functioning_iadl = models.JSONField(default=dict, blank=True)
    
    # Clinical Record Items
    primary_diagnosis = models.CharField(max_length=200)
    other_diagnoses = models.JSONField(default=list, blank=True)
    
    # Functional Status
    grooming = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    dressing_upper = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    dressing_lower = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    bathing = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    toileting = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    transferring = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    ambulation = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    feeding = models.IntegerField(choices=[(0, 'Able'), (1, 'Supervision'), (2, 'Assistance'), (3, 'Unable')], null=True, blank=True)
    
    # Cognitive Functioning
    cognitive_functioning = models.IntegerField(choices=[
        (0, 'Alert/oriented'), (1, 'Requires prompting'), (2, 'Requires assistance'), 
        (3, 'Requires considerable assistance'), (4, 'Unable to care')
    ], null=True, blank=True)
    
    # Sensory Status
    vision = models.IntegerField(choices=[
        (0, 'Normal'), (1, 'Partially impaired'), (2, 'Severely impaired')
    ], null=True, blank=True)
    hearing = models.IntegerField(choices=[
        (0, 'Normal'), (1, 'Minimal difficulty'), (2, 'Moderate difficulty'), (3, 'Severe difficulty')
    ], null=True, blank=True)
    
    # Complete assessment data (all OASIS items as JSON)
    complete_data = models.JSONField(default=dict, blank=True)
    
    # AI Generated Content
    ai_insights = models.JSONField(default=dict, blank=True)
    risk_scores = models.JSONField(default=dict, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    submitted_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-assessment_date']

    def __str__(self):
        return f"{self.patient.full_name} - {self.get_assessment_type_display()} ({self.assessment_date})"


class OasisTemplate(models.Model):
    """Templates for different OASIS assessment types and disciplines"""
    name = models.CharField(max_length=100)
    assessment_type = models.CharField(max_length=10, choices=OasisAssessmentType.choices)
    discipline = models.CharField(max_length=5, choices=[
        ('SN', 'Skilled Nursing'),
        ('PT', 'Physical Therapy'),
        ('OT', 'Occupational Therapy'),
        ('ST', 'Speech Therapy'),
        ('MSW', 'Medical Social Work'),
    ])
    
    template_structure = models.JSONField()  # Dynamic form structure
    version = models.CharField(max_length=10, default='E')  # OASIS-E
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_discipline_display()}"
