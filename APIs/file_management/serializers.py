from rest_framework import serializers
from .models import UploadedFile


class FileUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    file_size_mb = serializers.ReadOnlyField()

    class Meta:
        model = UploadedFile
        fields = [
            'id', 'patient', 'patient_name', 'file', 'original_filename',
            'file_size', 'file_size_mb', 'file_type', 'category', 'description',
            'tags', 'ocr_text', 'structured_data', 'is_processed', 'processing_status',
            'uploaded_by', 'uploaded_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'file_size', 'file_type', 'ocr_text', 'structured_data',
            'is_processed', 'processing_status', 'uploaded_by', 'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        file = validated_data['file']
        validated_data['original_filename'] = file.name
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class OCRRequestSerializer(serializers.Serializer):
    extract_structured_data = serializers.BooleanField(default=True)
    data_type = serializers.ChoiceField(
        choices=[
            ('lab_values', 'Lab Values'),
            ('vital_signs', 'Vital Signs'),
            ('medication_list', 'Medication List'),
            ('insurance_info', 'Insurance Information'),
            ('general', 'General Text')
        ],
        default='general'
    )
