from rest_framework import serializers
from .models import Patient


class PatientBasicSerializer(serializers.ModelSerializer):
    """Basic patient information for use in other apps"""
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = ['id', 'mrn', 'first_name', 'last_name', 'full_name', 'age', 'date_of_birth']


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    assigned_physician_name = serializers.CharField(
        source='assigned_physician.get_full_name', 
        read_only=True
    )

    class Meta:
        model = Patient
        fields = [
            'id', 'mrn', 'first_name', 'last_name', 'full_name', 'age',
            'date_of_birth', 'gender', 'phone', 'email', 'address',
            'emergency_contact_name', 'emergency_contact_phone',
            'primary_diagnosis', 'secondary_diagnoses', 'allergies', 'medications',
            'insurance_provider', 'insurance_id', 'assigned_physician',
            'assigned_physician_name', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PatientSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100, help_text="Search by name, MRN, or DOB")
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)
    age_min = serializers.IntegerField(min_value=0, required=False)
    age_max = serializers.IntegerField(min_value=0, required=False)
