from rest_framework import generics, status, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.contrib.auth import get_user_model
from .models import CommunicationThread, Message, MessageTemplate, MessageReadStatus
from .serializers import (
    CommunicationThreadSerializer, CommunicationThreadDetailSerializer,
    CommunicationThreadCreateSerializer, MessageSerializer, MessageCreateSerializer,
    MessageTemplateSerializer, AIMessageGenerationSerializer, CommunicationStatsSerializer
)
from patients.models import Patient
import json
from datetime import datetime, timedelta

User = get_user_model()


class CommunicationThreadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling communication threads.
    """
    queryset = CommunicationThread.objects.all()
    serializer_class = CommunicationThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommunicationThreadCreateSerializer
        elif self.action == 'retrieve':
            return CommunicationThreadDetailSerializer
        return CommunicationThreadSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer


class CommunicationThreadListCreateView(generics.ListCreateAPIView):
    """List all communication threads or create a new one"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = CommunicationThread.objects.filter(
            participants=user
        ).select_related('patient', 'created_by').prefetch_related('participants', 'messages')
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by urgency
        is_urgent = self.request.query_params.get('is_urgent')
        if is_urgent is not None:
            queryset = queryset.filter(is_urgent=is_urgent.lower() == 'true')
        
        # Filter by status
        is_closed = self.request.query_params.get('is_closed')
        if is_closed is not None:
            queryset = queryset.filter(is_closed=is_closed.lower() == 'true')
        
        # Search in subject
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(subject__icontains=search) |
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search)
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunicationThreadCreateSerializer
        return CommunicationThreadSerializer


class CommunicationThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific communication thread"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CommunicationThread.objects.filter(
            participants=self.request.user
        ).select_related('patient', 'created_by').prefetch_related('participants', 'messages__sender')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommunicationThreadDetailSerializer
        return CommunicationThreadCreateSerializer
    
    def retrieve(self, request, *args, **kwargs):
        # Mark all messages in this thread as read for the current user
        thread = self.get_object()
        unread_messages = thread.messages.exclude(read_by=request.user)
        
        for message in unread_messages:
            MessageReadStatus.objects.get_or_create(
                message=message,
                user=request.user
            )
        
        return super().retrieve(request, *args, **kwargs)


class MessageListCreateView(generics.ListCreateAPIView):
    """List messages in a thread or create a new message"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(CommunicationThread, id=thread_id, participants=self.request.user)
        return Message.objects.filter(thread=thread).select_related('sender')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(CommunicationThread, id=thread_id, participants=self.request.user)
        serializer.save(thread=thread)
        
        # Update thread timestamp
        thread.updated_at = timezone.now()
        thread.save()


class MessageTemplateListView(generics.ListAPIView):
    """List available message templates"""
    queryset = MessageTemplate.objects.filter(is_active=True)
    serializer_class = MessageTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        message_type = self.request.query_params.get('message_type')
        if message_type:
            queryset = queryset.filter(message_type=message_type)
        
        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_ai_message(request, thread_id):
    """Generate an AI message for a communication thread"""
    thread = get_object_or_404(CommunicationThread, id=thread_id, participants=request.user)
    
    serializer = AIMessageGenerationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    message_type = data.get('message_type')
    template_id = data.get('template_id')
    context_data = data.get('context_data', {})
    custom_prompt = data.get('custom_prompt', '')
    
    # Mock AI message generation (in production, integrate with OpenAI or similar)
    if message_type == 'status_report':
        ai_content = f"""Status Update for {thread.patient.full_name}:

Current Condition: Patient is showing steady progress in their recovery plan.

Recent Assessments:
- Mobility: Improved ambulation with assistive device
- Pain Management: Well-controlled with current medication regimen
- Vital Signs: Within normal limits

Next Steps:
- Continue current therapy schedule
- Follow-up visit scheduled for next week
- Monitor pain levels and adjust medications as needed

Please contact me if you have any questions or concerns.

Best regards,
{request.user.full_name}"""
    
    elif message_type == 'physician_update':
        ai_content = f"""Physician Update for {thread.patient.full_name}:

Patient Summary: 
- Primary Diagnosis: {context_data.get('diagnosis', 'Multiple chronic conditions')}
- Current Status: Stable and progressing well with treatment plan

Clinical Updates:
- Medication compliance is excellent
- No adverse reactions reported
- Functional status improving gradually

Recommendations:
- Continue current treatment protocol
- Consider PT/OT evaluation for functional improvement
- Next physician visit in 2 weeks

Please let me know if you need any additional information.

Dr. {request.user.full_name}"""
    
    elif message_type == 'urgent_alert':
        ai_content = f"""URGENT ALERT - {thread.patient.full_name}:

Alert Type: {context_data.get('alert_type', 'Clinical Change')}
Priority: HIGH

Details:
{context_data.get('details', 'Significant change in patient condition requiring immediate attention.')}

Immediate Actions Required:
1. Contact primary physician
2. Review current medications
3. Consider emergency evaluation if symptoms worsen

Time Sensitive: Please respond within 2 hours.

Contact: {request.user.full_name} - {request.user.email}"""
    
    else:
        ai_content = f"""Update regarding {thread.patient.full_name}:

{custom_prompt if custom_prompt else 'General communication regarding patient care coordination.'}

Please review and provide your input as needed.

{request.user.full_name}"""
    
    # Create the AI-generated message
    message = Message.objects.create(
        thread=thread,
        sender=request.user,
        message_type=message_type,
        content=ai_content,
        is_ai_generated=True,
        ai_template_used=f"template_{template_id}" if template_id else "custom_generation"
    )
    
    # Update thread timestamp
    thread.updated_at = timezone.now()
    thread.save()
    
    serializer = MessageSerializer(message)
    return Response({
        'message': 'AI message generated successfully',
        'generated_message': serializer.data
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_thread_urgent(request, thread_id):
    """Mark a thread as urgent"""
    thread = get_object_or_404(CommunicationThread, id=thread_id, participants=request.user)
    
    is_urgent = request.data.get('is_urgent', True)
    thread.is_urgent = is_urgent
    thread.save()
    
    return Response({
        'message': f'Thread marked as {"urgent" if is_urgent else "normal"}',
        'is_urgent': is_urgent
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def close_thread(request, thread_id):
    """Close a communication thread"""
    thread = get_object_or_404(CommunicationThread, id=thread_id, participants=request.user)
    
    thread.is_closed = True
    thread.save()
    
    # Create a system message
    Message.objects.create(
        thread=thread,
        sender=request.user,
        message_type='general',
        content=f"Thread closed by {request.user.full_name}",
        is_ai_generated=True
    )
    
    return Response({'message': 'Thread closed successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_participants(request, thread_id):
    """Add participants to a communication thread"""
    thread = get_object_or_404(CommunicationThread, id=thread_id, participants=request.user)
    
    participant_ids = request.data.get('participant_ids', [])
    
    if not participant_ids:
        return Response({
            'error': 'participant_ids is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate that all participant IDs exist
    participants = User.objects.filter(id__in=participant_ids)
    if len(participants) != len(participant_ids):
        return Response({
            'error': 'Some participant IDs are invalid'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Add participants
    thread.participants.add(*participants)
    
    # Create notification message
    participant_names = ', '.join([p.full_name for p in participants])
    Message.objects.create(
        thread=thread,
        sender=request.user,
        message_type='general',
        content=f"Added participants: {participant_names}",
        is_ai_generated=True
    )
    
    return Response({
        'message': f'Added {len(participants)} participants to thread',
        'participants': [{'id': p.id, 'name': p.full_name} for p in participants]
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def communication_stats(request):
    """Get communication statistics"""
    user = request.user
    
    # Get user's threads
    user_threads = CommunicationThread.objects.filter(participants=user)
    
    # Calculate statistics
    total_threads = user_threads.count()
    active_threads = user_threads.filter(is_closed=False).count()
    urgent_threads = user_threads.filter(is_urgent=True, is_closed=False).count()
    
    # Unread messages
    unread_messages = Message.objects.filter(
        thread__in=user_threads
    ).exclude(read_by=user).count()
    
    # Messages by type
    messages_by_type = dict(
        Message.objects.filter(
            thread__in=user_threads
        ).values('message_type').annotate(count=Count('id')).values_list('message_type', 'count')
    )
    
    # Top participants (most active in conversations)
    top_participants = list(
        User.objects.filter(
            sent_messages__thread__in=user_threads
        ).annotate(
            message_count=Count('sent_messages')
        ).order_by('-message_count')[:5].values('id', 'first_name', 'last_name', 'message_count')
    )
    
    stats = {
        'total_threads': total_threads,
        'active_threads': active_threads,
        'urgent_threads': urgent_threads,
        'unread_messages': unread_messages,
        'avg_response_time': '2.5 hours',  # Mock calculation
        'messages_by_type': messages_by_type,
        'top_participants': top_participants
    }
    
    serializer = CommunicationStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def patient_communication_history(request, patient_id):
    """Get communication history for a specific patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    threads = CommunicationThread.objects.filter(
        patient=patient,
        participants=request.user
    ).prefetch_related('messages__sender')
    
    history = []
    for thread in threads:
        thread_data = {
            'id': thread.id,
            'subject': thread.subject,
            'created_at': thread.created_at,
            'is_urgent': thread.is_urgent,
            'is_closed': thread.is_closed,
            'message_count': thread.messages.count(),
            'last_activity': thread.updated_at,
            'participants': [
                {'id': p.id, 'name': p.full_name} 
                for p in thread.participants.all()
            ]
        }
        history.append(thread_data)
    
    return Response({
        'patient': {
            'id': patient.id,
            'name': patient.full_name
        },
        'communication_history': history,
        'total_threads': len(history)
    })


class SendNoteView(APIView):
    """Send a general note"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Send note endpoint - implement note sending logic',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class SendAIUpdateView(APIView):
    """Send an AI-generated update"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Send AI update endpoint - implement AI update logic',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class SendUrgentAlertView(APIView):
    """Send urgent alert"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Send urgent alert endpoint - implement urgent alert logic',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class PatientCommunicationThreadsView(APIView):
    """Get communication threads for a patient"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, patient_id):
        return Response({
            'message': f'Patient communication threads for patient {patient_id}',
            'threads': []
        }, status=status.HTTP_200_OK)


class ThreadMessagesView(APIView):
    """Get messages for a thread"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, thread_id):
        return Response({
            'message': f'Thread messages for thread {thread_id}',
            'messages': []
        }, status=status.HTTP_200_OK)


class ThreadParticipantsView(APIView):
    """Get participants for a thread"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, thread_id):
        return Response({
            'message': f'Thread participants for thread {thread_id}',
            'participants': []
        }, status=status.HTTP_200_OK)


class GenerateMDUpdateView(APIView):
    """Generate MD update"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Generate MD update endpoint - implement MD update generation',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class GenerateSummaryView(APIView):
    """Generate summary"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Generate summary endpoint - implement summary generation',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class GenerateHandoffNoteView(APIView):
    """Generate handoff note"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Generate handoff note endpoint - implement handoff note generation',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class GenerateCareSummaryView(APIView):
    """Generate care summary"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        return Response({
            'message': 'Generate care summary endpoint - implement care summary generation',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class MedicationAdjustmentsView(APIView):
    """Get medication adjustments"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Medication adjustments endpoint - implement medication adjustments logic',
            'adjustments': []
        }, status=status.HTTP_200_OK)


class InterventionRecommendationsView(APIView):
    """Get intervention recommendations"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Intervention recommendations endpoint - implement intervention recommendations',
            'recommendations': []
        }, status=status.HTTP_200_OK)


class CarePlanUpdatesView(APIView):
    """Get care plan updates"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Care plan updates endpoint - implement care plan updates',
            'updates': []
        }, status=status.HTTP_200_OK)


class NotificationListView(APIView):
    """List notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Notification list endpoint - implement notification listing',
            'notifications': []
        }, status=status.HTTP_200_OK)


class MarkNotificationReadView(APIView):
    """Mark notification as read"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, notification_id):
        return Response({
            'message': f'Mark notification {notification_id} as read - implement logic',
            'status': 'placeholder'
        }, status=status.HTTP_200_OK)


class UnreadNotificationsView(APIView):
    """Get unread notifications"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Unread notifications endpoint - implement unread notifications',
            'notifications': []
        }, status=status.HTTP_200_OK)


class TeamUpdatesView(APIView):
    """Get team updates"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Team updates endpoint - implement team updates',
            'updates': []
        }, status=status.HTTP_200_OK)


class UrgentAlertsView(APIView):
    """Get urgent alerts"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Urgent alerts endpoint - implement urgent alerts',
            'alerts': []
        }, status=status.HTTP_200_OK)


class ShiftHandoffsView(APIView):
    """Get shift handoffs"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Shift handoffs endpoint - implement shift handoffs',
            'handoffs': []
        }, status=status.HTTP_200_OK)


class InterdisciplinaryNotesView(APIView):
    """Get interdisciplinary notes"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Interdisciplinary notes endpoint - implement interdisciplinary notes',
            'notes': []
        }, status=status.HTTP_200_OK)


class ResponseTimeAnalyticsView(APIView):
    """Get response time analytics"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Response time analytics endpoint - implement analytics',
            'analytics': {}
        }, status=status.HTTP_200_OK)


class CommunicationPatternsView(APIView):
    """Get communication patterns"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({
            'message': 'Communication patterns endpoint - implement patterns analysis',
            'patterns': {}
        }, status=status.HTTP_200_OK)
