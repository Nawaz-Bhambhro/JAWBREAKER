from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import OasisAssessment, OasisTemplate
from .serializers import (
    OasisAssessmentSerializer, OasisAssessmentDetailSerializer,
    OasisAssessmentCreateSerializer, OasisAssessmentUpdateSerializer,
    OasisSummarySerializer, OasisTemplateSerializer, OasisAIAnalysisSerializer
)
from patients.models import Patient
import json
from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.views import APIView


class OasisAssessmentListCreateView(generics.ListCreateAPIView):
    """List all OASIS assessments or create a new one"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = OasisAssessment.objects.all()
        
        # Filter by patient if specified
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by assessment type
        assessment_type = self.request.query_params.get('assessment_type')
        if assessment_type:
            queryset = queryset.filter(assessment_type=assessment_type)
        
        # Filter by completion status
        is_completed = self.request.query_params.get('is_completed')
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(assessment_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(assessment_date__lte=end_date)
        
        return queryset.select_related('patient', 'clinician')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OasisAssessmentCreateSerializer
        return OasisSummarySerializer


class OasisAssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific OASIS assessment"""
    queryset = OasisAssessment.objects.select_related('patient', 'clinician')
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OasisAssessmentDetailSerializer
        return OasisAssessmentUpdateSerializer


class OasisTemplateListView(generics.ListAPIView):
    """List available OASIS templates"""
    queryset = OasisTemplate.objects.filter(is_active=True)
    serializer_class = OasisTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        assessment_type = self.request.query_params.get('assessment_type')
        if assessment_type:
            queryset = queryset.filter(assessment_type=assessment_type)
        
        discipline = self.request.query_params.get('discipline')
        if discipline:
            queryset = queryset.filter(discipline=discipline)
        
        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_oasis_assessment(request, assessment_id):
    """Submit a completed OASIS assessment"""
    assessment = get_object_or_404(OasisAssessment, id=assessment_id)
    
    # Validate that all required fields are completed
    required_fields = ['primary_diagnosis', 'assessment_date']
    missing_fields = []
    
    for field in required_fields:
        if not getattr(assessment, field):
            missing_fields.append(field)
    
    if missing_fields:
        return Response({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }, status=status.HTTP_400_BAD_REQUEST)
    
    assessment.is_completed = True
    assessment.submitted_date = timezone.now()
    assessment.save()
    
    serializer = OasisAssessmentDetailSerializer(assessment)
    return Response({
        'message': 'OASIS assessment submitted successfully',
        'assessment': serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_oasis_ai_analysis(request, assessment_id):
    """Generate AI analysis for OASIS assessment"""
    assessment = get_object_or_404(OasisAssessment, id=assessment_id)
    
    # Mock AI analysis (in production, this would integrate with actual AI services)
    ai_analysis = {
        'risk_scores': {
            'fall_risk': 'moderate',
            'rehospitalization_risk': 'low',
            'functional_decline_risk': 'high',
            'medication_adherence_risk': 'moderate'
        },
        'insights': {
            'functional_status': 'Patient shows significant limitations in ADLs, particularly in bathing and dressing',
            'cognitive_status': 'Alert and oriented, good potential for self-care improvement',
            'safety_concerns': 'Fall risk due to ambulation difficulties, recommend safety equipment'
        },
        'recommendations': [
            'Physical therapy evaluation for mobility improvement',
            'Occupational therapy for ADL training',
            'Fall prevention education and safety equipment',
            'Medication review for potential side effects affecting balance'
        ],
        'quality_indicators': {
            'improvement_in_ambulation': True,
            'improvement_in_bathing': False,
            'improvement_in_pain_management': True,
            'acute_care_hospitalization': False
        }
    }
    
    # Update assessment with AI insights
    assessment.ai_insights = ai_analysis['insights']
    assessment.risk_scores = ai_analysis['risk_scores']
    assessment.save()
    
    serializer = OasisAIAnalysisSerializer(ai_analysis)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def oasis_patient_timeline(request, patient_id):
    """Get OASIS assessment timeline for a patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    assessments = OasisAssessment.objects.filter(
        patient=patient
    ).order_by('assessment_date')
    
    timeline_data = []
    for assessment in assessments:
        timeline_data.append({
            'id': assessment.id,
            'assessment_type': assessment.assessment_type,
            'assessment_type_display': assessment.get_assessment_type_display(),
            'assessment_date': assessment.assessment_date,
            'is_completed': assessment.is_completed,
            'clinician': assessment.clinician.full_name,
            'primary_diagnosis': assessment.primary_diagnosis,
            'risk_scores': assessment.risk_scores
        })
    
    return Response({
        'patient': {
            'id': patient.id,
            'name': patient.full_name,
            'date_of_birth': patient.date_of_birth
        },
        'assessments': timeline_data,
        'total_assessments': len(timeline_data)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def oasis_quality_measures(request):
    """Get OASIS quality measures and outcomes"""
    # Mock quality measures calculation
    start_date = request.query_params.get('start_date', '2024-01-01')
    end_date = request.query_params.get('end_date', '2024-12-31')
    
    assessments = OasisAssessment.objects.filter(
        assessment_date__range=[start_date, end_date],
        is_completed=True
    )
    
    total_assessments = assessments.count()
    
    quality_measures = {
        'total_assessments': total_assessments,
        'improvement_rates': {
            'ambulation': 75.5,
            'bathing': 68.2,
            'pain_management': 82.1,
            'medication_adherence': 90.3
        },
        'risk_stratification': {
            'low_risk': assessments.filter(risk_scores__rehospitalization_risk='low').count(),
            'moderate_risk': assessments.filter(risk_scores__rehospitalization_risk='moderate').count(),
            'high_risk': assessments.filter(risk_scores__rehospitalization_risk='high').count()
        },
        'completion_metrics': {
            'average_completion_time': '24.5 hours',
            'on_time_completion_rate': 94.2,
            'overdue_assessments': 3
        }
    }
    
    return Response(quality_measures)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bulk_create_assessments(request):
    """Bulk create OASIS assessments from template"""
    data = request.data
    patients = data.get('patient_ids', [])
    assessment_type = data.get('assessment_type')
    template_id = data.get('template_id')
    
    if not patients or not assessment_type:
        return Response({
            'error': 'patient_ids and assessment_type are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    created_assessments = []
    
    for patient_id in patients:
        try:
            patient = Patient.objects.get(id=patient_id)
            assessment = OasisAssessment.objects.create(
                patient=patient,
                clinician=request.user,
                assessment_type=assessment_type,
                assessment_date=timezone.now().date()
            )
            created_assessments.append(assessment.id)
        except Patient.DoesNotExist:
            continue
    
    return Response({
        'message': f'Created {len(created_assessments)} assessments',
        'assessment_ids': created_assessments
    })


class OasisAssessmentViewSet(viewsets.ModelViewSet):
    queryset = OasisAssessment.objects.all()
    serializer_class = OasisAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class OasisTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OasisTemplate.objects.filter(is_active=True)
    serializer_class = OasisTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class OasisSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Submit a new OASIS assessment.
        """
        serializer = OasisAssessmentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            assessment = serializer.save()
            return Response({
                'message': 'OASIS assessment submitted successfully',
                'assessment': OasisAssessmentDetailSerializer(assessment).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OasisDraftSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Save a draft OASIS assessment (not marked as completed).
        """
        serializer = OasisAssessmentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            assessment = serializer.save(is_completed=False)
            return Response({
                'message': 'OASIS draft saved successfully',
                'assessment': OasisAssessmentDetailSerializer(assessment).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OasisFinalSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Submit a final/completed OASIS assessment.
        """
        serializer = OasisAssessmentCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            assessment = serializer.save(is_completed=True, submitted_date=timezone.now())
            return Response({
                'message': 'OASIS final assessment submitted successfully',
                'assessment': OasisAssessmentDetailSerializer(assessment).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OasisDisciplineTemplateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, discipline):
        """
        Get OASIS templates filtered by discipline.
        """
        templates = OasisTemplate.objects.filter(discipline=discipline, is_active=True)
        serializer = OasisTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class OasisSpecificTemplateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, discipline, assessment_type):
        """
        Get specific OASIS template by discipline and assessment type.
        """
        templates = OasisTemplate.objects.filter(
            discipline=discipline,
            assessment_type=assessment_type,
            is_active=True
        )
        serializer = OasisTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class SkilledNursingTemplateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get skilled nursing templates.
        """
        templates = OasisTemplate.objects.filter(discipline='SN', is_active=True)
        serializer = OasisTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class PhysicalTherapyTemplateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get physical therapy templates.
        """
        templates = OasisTemplate.objects.filter(discipline='PT', is_active=True)
        serializer = OasisTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class OccupationalTherapyTemplateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get occupational therapy templates.
        """
        templates = OasisTemplate.objects.filter(discipline='OT', is_active=True)
        serializer = OasisTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class OasisAIAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        """
        Get AI analysis for an OASIS assessment.
        """
        assessment = get_object_or_404(OasisAssessment, id=assessment_id)
        
        # Mock AI analysis data
        ai_analysis = {
            'risk_scores': {
                'overall_risk': 65,
                'fall_risk': 75,
                'hospitalization_risk': 45
            },
            'insights': [
                {'text': 'Patient shows high fall risk due to mobility limitations'},
                {'text': 'Cognitive function is stable, good potential for improvement'}
            ],
            'recommendations': [
                {'action': 'Implement fall prevention measures', 'priority': 'high'},
                {'action': 'Schedule physical therapy evaluation', 'priority': 'medium'}
            ],
            'quality_indicators': {
                'data_completeness': 95,
                'assessment_accuracy': 88,
                'timeliness': 92
            }
        }
        
        serializer = OasisAIAnalysisSerializer(ai_analysis)
        return Response(serializer.data)


class OasisRiskScoresView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        """
        Get risk scores for an OASIS assessment.
        """
        assessment = get_object_or_404(OasisAssessment, id=assessment_id)
        
        risk_scores = {
            'fall_risk': 75,
            'rehospitalization_risk': 30,
            'functional_decline_risk': 45,
            'medication_adherence_risk': 20
        }
        
        return Response(risk_scores)


class OasisRecommendationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        """
        Get recommendations for an OASIS assessment.
        """
        assessment = get_object_or_404(OasisAssessment, id=assessment_id)
        
        recommendations = [
            {
                'category': 'Safety',
                'action': 'Install grab bars in bathroom',
                'priority': 'high',
                'rationale': 'High fall risk due to mobility limitations'
            },
            {
                'category': 'Therapy',
                'action': 'Physical therapy evaluation',
                'priority': 'medium',
                'rationale': 'Potential for mobility improvement'
            },
            {
                'category': 'Education',
                'action': 'Medication management training',
                'priority': 'low',
                'rationale': 'Improve adherence rates'
            }
        ]
        
        return Response(recommendations)


class QualityIndicatorsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        """
        Get quality indicators for an OASIS assessment.
        """
        assessment = get_object_or_404(OasisAssessment, id=assessment_id)
        
        quality_indicators = {
            'data_completeness': 95,
            'assessment_accuracy': 88,
            'timeliness': 92,
            'clinical_appropriateness': 85,
            'patient_satisfaction': 90
        }
        
        return Response(quality_indicators)


class FallRiskPredictionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        """
        Get fall risk prediction for an OASIS assessment.
        """
        assessment = get_object_or_404(OasisAssessment, id=assessment_id)
        
        fall_risk_data = {
            'risk_level': 'high',
            'risk_score': 75,
            'contributing_factors': [
                'Mobility limitations',
                'History of falls',
                'Medication side effects'
            ],
            'interventions': [
                'Fall prevention education',
                'Home safety assessment',
                'Physical therapy referral'
            ]
        }
        
        return Response(fall_risk_data)


class ReadmissionRiskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        """
        Get readmission risk prediction for an OASIS assessment.
        """
        assessment = get_object_or_404(OasisAssessment, id=assessment_id)
        
        readmission_risk_data = {
            'risk_level': 'moderate',
            'risk_score': 45,
            'risk_factors': [
                'Complex medication regimen',
                'Limited social support',
                'Chronic conditions'
            ],
            'preventive_measures': [
                'Medication reconciliation',
                'Caregiver training',
                'Follow-up appointments'
            ]
        }
        
        return Response(readmission_risk_data)


class DeteriorationRiskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, assessment_id):
        """
        Get deterioration risk prediction for an OASIS assessment.
        """
        assessment = get_object_or_404(OasisAssessment, id=assessment_id)
        
        deterioration_risk_data = {
            'risk_level': 'low',
            'risk_score': 25,
            'risk_indicators': [
                'Stable vital signs',
                'Good medication adherence',
                'Family support present'
            ],
            'monitoring_plan': [
                'Weekly vital signs check',
                'Monthly medication review',
                'Quarterly assessment'
            ]
        }
        
        return Response(deterioration_risk_data)


class OasisBulkSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Submit multiple OASIS assessments in bulk.
        """
        assessment_ids = request.data.get('assessment_ids', [])
        
        if not assessment_ids:
            return Response({
                'error': 'assessment_ids is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        updated_assessments = []
        errors = []
        
        for assessment_id in assessment_ids:
            try:
                assessment = OasisAssessment.objects.get(id=assessment_id)
                assessment.is_completed = True
                assessment.submitted_date = timezone.now()
                assessment.save()
                updated_assessments.append(assessment_id)
            except OasisAssessment.DoesNotExist:
                errors.append(f"Assessment {assessment_id} not found")
        
        return Response({
            'message': f'Successfully submitted {len(updated_assessments)} assessments',
            'submitted_assessments': updated_assessments,
            'errors': errors
        })


class PendingAssessmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get all pending (incomplete) OASIS assessments.
        """
        assessments = OasisAssessment.objects.filter(is_completed=False)
        serializer = OasisSummarySerializer(assessments, many=True)
        return Response({
            'count': assessments.count(),
            'results': serializer.data
        })


class CompletedAssessmentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get all completed OASIS assessments.
        """
        assessments = OasisAssessment.objects.filter(is_completed=True)
        serializer = OasisSummarySerializer(assessments, many=True)
        return Response({
            'count': assessments.count(),
            'results': serializer.data
        })
