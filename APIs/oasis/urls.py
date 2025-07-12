from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'assessments', views.OasisAssessmentViewSet, basename='oasis_assessment')
router.register(r'templates', views.OasisTemplateViewSet, basename='oasis_template')

app_name = 'oasis'

urlpatterns = [
    # OASIS submission endpoints
    path('submit/', views.OasisSubmissionView.as_view(), name='oasis_submit'),
    path('submit/draft/', views.OasisDraftSubmissionView.as_view(), name='oasis_draft_submit'),
    path('submit/final/', views.OasisFinalSubmissionView.as_view(), name='oasis_final_submit'),
    
    # AI-ready templates by discipline
    path('template/<str:discipline>/', views.OasisDisciplineTemplateView.as_view(), name='oasis_discipline_template'),
    path('template/<str:discipline>/<str:assessment_type>/', views.OasisSpecificTemplateView.as_view(), name='oasis_specific_template'),
    path('templates/sn/', views.SkilledNursingTemplateView.as_view(), name='sn_template'),
    path('templates/pt/', views.PhysicalTherapyTemplateView.as_view(), name='pt_template'),
    path('templates/ot/', views.OccupationalTherapyTemplateView.as_view(), name='ot_template'),
    
    # AI analysis and insights
    path('assessments/<int:assessment_id>/ai-analysis/', views.OasisAIAnalysisView.as_view(), name='oasis_ai_analysis'),
    path('assessments/<int:assessment_id>/risk-scores/', views.OasisRiskScoresView.as_view(), name='oasis_risk_scores'),
    path('assessments/<int:assessment_id>/recommendations/', views.OasisRecommendationsView.as_view(), name='oasis_recommendations'),
    path('assessments/<int:assessment_id>/quality-indicators/', views.QualityIndicatorsView.as_view(), name='quality_indicators'),
    
    # Predictive analytics
    path('assessments/<int:assessment_id>/fall-risk/', views.FallRiskPredictionView.as_view(), name='fall_risk'),
    path('assessments/<int:assessment_id>/readmission-risk/', views.ReadmissionRiskView.as_view(), name='readmission_risk'),
    path('assessments/<int:assessment_id>/deterioration-risk/', views.DeteriorationRiskView.as_view(), name='deterioration_risk'),
    
    # Bulk operations
    path('bulk-submit/', views.OasisBulkSubmissionView.as_view(), name='oasis_bulk_submit'),
    path('assessments/pending/', views.PendingAssessmentsView.as_view(), name='pending_assessments'),
    path('assessments/completed/', views.CompletedAssessmentsView.as_view(), name='completed_assessments'),
    
    # Include router URLs
    path('', include(router.urls)),
]
