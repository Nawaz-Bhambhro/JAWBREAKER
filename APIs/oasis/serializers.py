from rest_framework import serializers
from django.utils import timezone
from .models import OasisAssessment, OasisTemplate
from patients.serializers import PatientBasicSerializer
from authentication.serializers import UserBasicSerializer


class OasisTemplateSerializer(serializers.ModelSerializer):
    assessment_type_display = serializers.CharField(source='get_assessment_type_display', read_only=True)
    discipline_display = serializers.CharField(source='get_discipline_display', read_only=True)
    
    class Meta:
        model = OasisTemplate
        fields = '__all__'
    
    def validate_template_structure(self, value):
        """Validate template structure"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Template structure must be a valid JSON object")
        if not value.get('sections'):
            raise serializers.ValidationError("Template must have sections defined")
        return value


class OasisAssessmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    clinician_name = serializers.CharField(source='clinician.get_full_name', read_only=True)
    assessment_type_display = serializers.CharField(source='get_assessment_type_display', read_only=True)
    
    class Meta:
        model = OasisAssessment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_assessment_date(self, value):
        """Validate assessment date is not in the future"""
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Assessment date cannot be in the future")
        return value
    
    def validate(self, data):
        """Cross-field validation"""
        if data.get('is_completed') and not data.get('submitted_date'):
            data['submitted_date'] = timezone.now()
        
        if data.get('submitted_date') and not data.get('is_completed'):
            raise serializers.ValidationError("Cannot submit incomplete assessment")
        
        return data


class OasisAssessmentDetailSerializer(serializers.ModelSerializer):
    patient = PatientBasicSerializer(read_only=True)
    clinician = UserBasicSerializer(read_only=True)
    assessment_type_display = serializers.CharField(source='get_assessment_type_display', read_only=True)
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = OasisAssessment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_completion_percentage(self, obj):
        """Calculate assessment completion percentage"""
        if not obj.complete_data:
            return 0
        
        total_questions = 0
        answered_questions = 0
        
        for section in obj.complete_data.get('sections', []):
            for question in section.get('questions', []):
                total_questions += 1
                if question.get('answer') is not None:
                    answered_questions += 1
        
        return round((answered_questions / total_questions) * 100, 2) if total_questions > 0 else 0


class OasisAssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OasisAssessment
        exclude = ['created_at', 'updated_at']

    def validate_patient(self, value):
        """Validate patient exists and is active"""
        if not value.is_active:
            raise serializers.ValidationError("Cannot create assessment for inactive patient")
        return value

    def create(self, validated_data):
        # Auto-assign clinician if not provided
        if 'clinician' not in validated_data:
            validated_data['clinician'] = self.context['request'].user
        
        # Set default assessment date if not provided
        if 'assessment_date' not in validated_data:
            validated_data['assessment_date'] = timezone.now().date()
            
        return super().create(validated_data)


class OasisAssessmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OasisAssessment
        exclude = ['patient', 'clinician', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Prevent updates to completed assessments"""
        instance = self.instance
        if instance and instance.is_completed and instance.submitted_date:
            if 'complete_data' in data:
                raise serializers.ValidationError("Cannot modify completed assessment data")
        return data


class OasisSummarySerializer(serializers.ModelSerializer):
    """Summary view for listing assessments"""
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    assessment_type_display = serializers.CharField(source='get_assessment_type_display', read_only=True)
    days_since_assessment = serializers.SerializerMethodField()
    
    class Meta:
        model = OasisAssessment
        fields = [
            'id', 'patient_name', 'assessment_type', 'assessment_type_display',
            'assessment_date', 'is_completed', 'submitted_date', 'created_at',
            'days_since_assessment'
        ]
    
    def get_days_since_assessment(self, obj):
        """Calculate days since assessment"""
        if obj.assessment_date:
            return (timezone.now().date() - obj.assessment_date).days
        return None


class OasisAIAnalysisSerializer(serializers.Serializer):
    """Serializer for AI analysis results"""
    risk_scores = serializers.JSONField()
    insights = serializers.JSONField()
    recommendations = serializers.JSONField()
    quality_indicators = serializers.JSONField()
    analysis_timestamp = serializers.DateTimeField(default=serializers.CreateOnlyDefault(timezone.now))
    confidence_score = serializers.FloatField(min_value=0.0, max_value=1.0, required=False)
    
    def validate_risk_scores(self, value):
        """Validate risk scores structure"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Risk scores must be a dictionary")
        
        required_fields = ['overall_risk', 'fall_risk', 'hospitalization_risk']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"Missing required risk score: {field}")
            
            score = value[field]
            if not isinstance(score, (int, float)) or not (0 <= score <= 100):
                raise serializers.ValidationError(f"Risk score {field} must be between 0 and 100")
        
        return value
    
    def validate_insights(self, value):
        """Validate insights structure"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Insights must be a list")
        
        for insight in value:
            if not isinstance(insight, dict) or 'text' not in insight:
                raise serializers.ValidationError("Each insight must have a 'text' field")
        
        return value
    
    def validate_recommendations(self, value):
        """Validate recommendations structure"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Recommendations must be a list")
        
        for rec in value:
            if not isinstance(rec, dict):
                raise serializers.ValidationError("Each recommendation must be a dictionary")
            if 'action' not in rec or 'priority' not in rec:
                raise serializers.ValidationError("Recommendations must have 'action' and 'priority' fields")
        
        return value
    
    def validate_quality_indicators(self, value):
        """Validate quality indicators structure"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Quality indicators must be a dictionary")
        
        required_indicators = ['data_completeness', 'assessment_accuracy', 'timeliness']
        for indicator in required_indicators:
            if indicator not in value:
                raise serializers.ValidationError(f"Missing required quality indicator: {indicator}")
            
            score = value[indicator]
            if not isinstance(score, (int, float)) or not (0 <= score <= 100):
                raise serializers.ValidationError(f"Quality indicator {indicator} must be between 0 and 100")
        
        return value
