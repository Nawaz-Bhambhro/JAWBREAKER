from rest_framework import serializers
from .models import Visit, VisitNote, DocumentationTemplate
from patients.serializers import PatientSerializer


class VisitSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    clinician_name = serializers.CharField(source='clinician.get_full_name', read_only=True)
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Visit
        fields = [
            'id', 'patient', 'patient_name', 'clinician', 'clinician_name',
            'visit_type', 'status', 'scheduled_date', 'start_time', 'end_time',
            'chief_complaint', 'vital_signs', 'assessment', 'plan',
            'ai_summary', 'ai_recommendations', 'duration_minutes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'ai_summary', 'ai_recommendations']

    def get_duration_minutes(self, obj):
        if obj.start_time and obj.end_time:
            delta = obj.end_time - obj.start_time
            return int(delta.total_seconds() / 60)
        return None

    def create(self, validated_data):
        validated_data['clinician'] = self.context['request'].user
        return super().create(validated_data)


class VisitNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = VisitNote
        fields = [
            'id', 'visit', 'note_type', 'title', 'content', 'structured_data',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class DocumentationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentationTemplate
        fields = ['id', 'name', 'discipline', 'template_data', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class VisitSummaryRequestSerializer(serializers.Serializer):
    include_notes = serializers.BooleanField(default=True)
    include_vitals = serializers.BooleanField(default=True)
    summary_type = serializers.ChoiceField(
        choices=[('brief', 'Brief'), ('detailed', 'Detailed'), ('physician', 'For Physician')],
        default='brief'
    )
