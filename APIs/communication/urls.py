from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'threads', views.CommunicationThreadViewSet, basename='communication_thread')
router.register(r'messages', views.MessageViewSet, basename='message')

app_name = 'communication'

urlpatterns = [
    # Core communication endpoints
    path('send-note/', views.SendNoteView.as_view(), name='send_note'),
    path('send-ai-update/', views.SendAIUpdateView.as_view(), name='send_ai_update'),
    path('send-urgent-alert/', views.SendUrgentAlertView.as_view(), name='send_urgent_alert'),
    
    # Thread management
    path('threads/<int:patient_id>/', views.PatientCommunicationThreadsView.as_view(), name='patient_threads'),
    path('threads/<int:thread_id>/messages/', views.ThreadMessagesView.as_view(), name='thread_messages'),
    path('threads/<int:thread_id>/participants/', views.ThreadParticipantsView.as_view(), name='thread_participants'),
    
    # AI-generated communications
    path('generate-md-update/', views.GenerateMDUpdateView.as_view(), name='generate_md_update'),
    path('generate-summary/', views.GenerateSummaryView.as_view(), name='generate_summary'),
    path('generate-handoff-note/', views.GenerateHandoffNoteView.as_view(), name='generate_handoff_note'),
    path('generate-care-summary/', views.GenerateCareSummaryView.as_view(), name='generate_care_summary'),
    
    # AI decision support
    path('medication-adjustments/', views.MedicationAdjustmentsView.as_view(), name='medication_adjustments'),
    path('intervention-recommendations/', views.InterventionRecommendationsView.as_view(), name='intervention_recommendations'),
    path('care-plan-updates/', views.CarePlanUpdatesView.as_view(), name='care_plan_updates'),
    
    # Notifications and alerts
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/read/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('notifications/unread/', views.UnreadNotificationsView.as_view(), name='unread_notifications'),
    
    # Team coordination
    path('team-updates/', views.TeamUpdatesView.as_view(), name='team_updates'),
    path('urgent-alerts/', views.UrgentAlertsView.as_view(), name='urgent_alerts'),
    path('shift-handoffs/', views.ShiftHandoffsView.as_view(), name='shift_handoffs'),
    path('interdisciplinary-notes/', views.InterdisciplinaryNotesView.as_view(), name='interdisciplinary_notes'),
    
    # Communication analytics
    path('analytics/response-times/', views.ResponseTimeAnalyticsView.as_view(), name='response_time_analytics'),
    path('analytics/communication-patterns/', views.CommunicationPatternsView.as_view(), name='communication_patterns'),
    
    # Include router URLs
    path('', include(router.urls)),
]
