from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.PatientViewSet, basename='patient')

urlpatterns = [
    # Core patient CRUD operations
    path('', views.PatientListCreateView.as_view(), name='patient_list_create'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    
    # Advanced search functionality
    path('search/', views.PatientSearchView.as_view(), name='patient_search'),
    path('search/by-name/', views.SearchByNameView.as_view(), name='search_by_name'),
    path('search/by-dob/', views.SearchByDOBView.as_view(), name='search_by_dob'),
    path('search/by-mrn/', views.SearchByMRNView.as_view(), name='search_by_mrn'),
    path('search/advanced/', views.AdvancedPatientSearchView.as_view(), name='advanced_search'),
    
    # Patient-specific data endpoints
    path('<int:patient_id>/history/', views.PatientHistoryView.as_view(), name='patient_history'),
    path('<int:patient_id>/visits/', views.PatientVisitsView.as_view(), name='patient_visits'),
    path('<int:patient_id>/assessments/', views.PatientAssessmentsView.as_view(), name='patient_assessments'),
    path('<int:patient_id>/medications/', views.PatientMedicationsView.as_view(), name='patient_medications'),
    path('<int:patient_id>/allergies/', views.PatientAllergiesView.as_view(), name='patient_allergies'),
    path('<int:patient_id>/vitals/', views.PatientVitalsView.as_view(), name='patient_vitals'),
    path('<int:patient_id>/care-plan/', views.PatientCarePlanView.as_view(), name='patient_care_plan'),
    
    # Demographics and insurance
    path('<int:patient_id>/demographics/', views.PatientDemographicsView.as_view(), name='patient_demographics'),
    path('<int:patient_id>/insurance/', views.PatientInsuranceView.as_view(), name='patient_insurance'),
    
    # Include router URLs
    path('api/', include(router.urls)),
]
