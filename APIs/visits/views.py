from rest_framework import status, generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Visit, VisitNote, DocumentationTemplate
from .serializers import (
    VisitSerializer, VisitNoteSerializer, 
    DocumentationTemplateSerializer, VisitSummaryRequestSerializer
)


class VisitListCreateView(generics.ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]


class VisitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]


class VisitViewSet(viewsets.ModelViewSet):
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter visits based on user role"""
        user = self.request.user
        if user.role == 'admin':
            return Visit.objects.all()
        elif user.role == 'physician':
            # Physicians see visits for their patients
            return Visit.objects.filter(patient__assigned_physician=user)
        else:
            # Clinicians see their own visits
            return Visit.objects.filter(clinician=user)

    @action(detail=True, methods=['post'])
    def start_visit(self, request, pk=None):
        """Start a visit - set start_time and status"""
        visit = self.get_object()
        if visit.status != 'scheduled':
            return Response(
                {'error': 'Visit must be scheduled to start'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        visit.start_time = timezone.now()
        visit.status = 'in_progress'
        visit.save()
        
        serializer = self.get_serializer(visit)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def end_visit(self, request, pk=None):
        """End a visit - set end_time and status"""
        visit = self.get_object()
        if visit.status != 'in_progress':
            return Response(
                {'error': 'Visit must be in progress to end'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        visit.end_time = timezone.now()
        visit.status = 'completed'
        visit.save()
        
        # TODO: Trigger AI summary generation here
        
        serializer = self.get_serializer(visit)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def notes(self, request, pk=None):
        """Add a note to a visit"""
        visit = self.get_object()
        serializer = VisitNoteSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(visit=visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def notes_list(self, request, pk=None):
        """Get all notes for a visit"""
        visit = self.get_object()
        notes = visit.notes.all()
        serializer = VisitNoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def summary(self, request, pk=None):
        """Generate AI summary for a visit"""
        visit = self.get_object()
        serializer = VisitSummaryRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Implement AI summary generation
        # For now, return a mock summary
        summary_data = {
            'visit_id': visit.id,
            'patient': visit.patient.full_name,
            'date': visit.scheduled_date.date(),
            'type': visit.get_visit_type_display(),
            'summary': f"Mock AI summary for {visit.patient.full_name} {visit.get_visit_type_display()} visit.",
            'recommendations': [
                "Continue current medication regimen",
                "Schedule follow-up in 1 week",
                "Monitor vital signs"
            ],
            'generated_at': timezone.now()
        }
        
        # Save the summary to the visit
        visit.ai_summary = summary_data['summary']
        visit.ai_recommendations = summary_data['recommendations']
        visit.save()
        
        return Response(summary_data)

    @action(detail=True, methods=['get'])
    def template(self, request, pk=None):
        """Get documentation template for visit type"""
        visit = self.get_object()
        try:
            template = DocumentationTemplate.objects.get(
                discipline=visit.visit_type, 
                is_active=True
            )
            serializer = DocumentationTemplateSerializer(template)
            return Response(serializer.data)
        except DocumentationTemplate.DoesNotExist:
            return Response(
                {'error': 'No template found for this visit type'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class VisitNoteViewSet(viewsets.ModelViewSet):
    serializer_class = VisitNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VisitNote.objects.filter(visit__clinician=self.request.user)


class DocumentationTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DocumentationTemplate.objects.filter(is_active=True)
    serializer_class = DocumentationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        discipline = self.request.query_params.get('discipline')
        if discipline:
            return self.queryset.filter(discipline=discipline)
        return self.queryset


class VisitNotesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        notes = VisitNote.objects.filter(visit=visit)
        serializer = VisitNoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    def post(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        serializer = VisitNoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(visit=visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VisitNote.objects.all()
    serializer_class = VisitNoteSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'note_id'


class StructuredNotesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        notes = VisitNote.objects.filter(visit=visit, note_type='structured')
        serializer = VisitNoteSerializer(notes, many=True)
        return Response(serializer.data)


class UnstructuredNotesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        notes = VisitNote.objects.filter(visit=visit, note_type='unstructured')
        serializer = VisitNoteSerializer(notes, many=True)
        return Response(serializer.data)


class VisitSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        serializer = VisitSummaryRequestSerializer(data=request.query_params)
        
        if serializer.is_valid():
            # Generate AI summary based on request parameters
            summary_data = {
                'visit_id': visit.id,
                'patient': visit.patient.full_name if hasattr(visit.patient, 'full_name') else str(visit.patient),
                'summary': visit.ai_summary or 'AI summary will be generated here',
                'recommendations': visit.ai_recommendations or [],
                'summary_type': serializer.validated_data.get('summary_type', 'brief')
            }
            return Response(summary_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIDocumentationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        # AI documentation generation logic would go here
        return Response({
            'visit_id': visit.id,
            'ai_documentation': 'AI-generated documentation will appear here',
            'confidence_score': 0.95,
            'generated_at': visit.updated_at
        })


class TranscriptToNoteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        transcript = request.data.get('transcript', '')
        
        # Convert transcript to structured note
        note_content = f"Converted from transcript: {transcript}"
        
        return Response({
            'visit_id': visit.id,
            'original_transcript': transcript,
            'structured_note': note_content,
            'confidence': 0.92
        })


class VoiceToTextView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        # Voice to text conversion logic
        return Response({
            'visit_id': visit.id,
            'transcribed_text': 'Voice transcription will appear here',
            'processing_status': 'completed'
        })


class VisitTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, visit_id):
        visit = get_object_or_404(Visit, id=visit_id)
        templates = DocumentationTemplate.objects.filter(
            discipline=getattr(visit, 'discipline', 'general'),
            is_active=True
        )
        serializer = DocumentationTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class DisciplineTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, discipline):
        templates = DocumentationTemplate.objects.filter(
            discipline=discipline,
            is_active=True
        )
        serializer = DocumentationTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class SpecificTemplateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, discipline, visit_type):
        templates = DocumentationTemplate.objects.filter(
            discipline=discipline,
            name__icontains=visit_type,
            is_active=True
        )
        serializer = DocumentationTemplateSerializer(templates, many=True)
        return Response(serializer.data)


class VisitTypeListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        visit_types = [
            {'code': 'SN', 'name': 'Skilled Nursing'},
            {'code': 'PT', 'name': 'Physical Therapy'},
            {'code': 'OT', 'name': 'Occupational Therapy'},
            {'code': 'ST', 'name': 'Speech Therapy'},
            {'code': 'MSW', 'name': 'Medical Social Worker'},
            {'code': 'HHA', 'name': 'Home Health Aide'},
        ]
        return Response(visit_types)


class DisciplineListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        disciplines = [
            {'code': 'nursing', 'name': 'Nursing'},
            {'code': 'physical_therapy', 'name': 'Physical Therapy'},
            {'code': 'occupational_therapy', 'name': 'Occupational Therapy'},
            {'code': 'speech_therapy', 'name': 'Speech Therapy'},
            {'code': 'social_work', 'name': 'Social Work'},
        ]
        return Response(disciplines)


class AIPromptTemplatesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        prompts = {
            'sn_note': 'Generate skilled nursing note based on this transcript...',
            'pt_note': 'Generate physical therapy note based on this assessment...',
            'summary': 'Summarize cardiovascular status for this patient...',
            'md_update': 'Generate summary for MD call regarding...'
        }
        return Response(prompts)


class SpecificAIPromptView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, template_type):
        prompts = {
            'sn_note': 'Generate skilled nursing note based on this transcript...',
            'pt_note': 'Generate physical therapy note based on this assessment...',
            'summary': 'Summarize cardiovascular status for this patient...',
            'md_update': 'Generate summary for MD call regarding...'
        }
        
        prompt = prompts.get(template_type, 'Default AI prompt template')
        return Response({'template_type': template_type, 'prompt': prompt})
