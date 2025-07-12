from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.VisitViewSet, basename='visit')

urlpatterns = [
    # Core visit management
    path('', views.VisitListCreateView.as_view(), name='visit_list_create'),
    path('<int:pk>/', views.VisitDetailView.as_view(), name='visit_detail'),
    
    # Visit notes and documentation
    path('<int:visit_id>/notes/', views.VisitNotesView.as_view(), name='visit_notes'),
    path('<int:visit_id>/notes/<int:note_id>/', views.VisitNoteDetailView.as_view(), name='visit_note_detail'),
    path('<int:visit_id>/structured-notes/', views.StructuredNotesView.as_view(), name='structured_notes'),
    path('<int:visit_id>/unstructured-notes/', views.UnstructuredNotesView.as_view(), name='unstructured_notes'),
    
    # AI-powered documentation features
    path('<int:visit_id>/summary/', views.VisitSummaryView.as_view(), name='visit_summary'),
    path('<int:visit_id>/ai-documentation/', views.AIDocumentationView.as_view(), name='ai_documentation'),
    path('<int:visit_id>/transcript-to-note/', views.TranscriptToNoteView.as_view(), name='transcript_to_note'),
    path('<int:visit_id>/voice-to-text/', views.VoiceToTextView.as_view(), name='voice_to_text'),
    
    # Dynamic templates
    path('<int:visit_id>/template/', views.VisitTemplateView.as_view(), name='visit_template'),
    path('templates/<str:discipline>/', views.DisciplineTemplateView.as_view(), name='discipline_template'),
    path('templates/<str:discipline>/<str:visit_type>/', views.SpecificTemplateView.as_view(), name='specific_template'),
    
    # Visit types and disciplines
    path('types/', views.VisitTypeListView.as_view(), name='visit_types'),
    path('disciplines/', views.DisciplineListView.as_view(), name='disciplines'),
    
    # AI prompt templates
    path('ai-prompts/', views.AIPromptTemplatesView.as_view(), name='ai_prompts'),
    path('ai-prompts/<str:template_type>/', views.SpecificAIPromptView.as_view(), name='specific_ai_prompt'),
    
    # Include router URLs
    path('api/', include(router.urls)),
]
