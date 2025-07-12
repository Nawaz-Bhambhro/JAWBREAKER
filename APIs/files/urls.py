from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='document')

urlpatterns = [
    # File upload endpoints
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('upload/multiple/', views.MultipleFileUploadView.as_view(), name='multiple_file_upload'),
    path('upload/patient/<int:patient_id>/', views.PatientFileUploadView.as_view(), name='patient_file_upload'),
    path('upload/visit/<int:visit_id>/', views.VisitFileUploadView.as_view(), name='visit_file_upload'),
    
    # OCR processing endpoints
    path('ocr/', views.OCRProcessingView.as_view(), name='ocr_processing'),
    path('ocr/batch/', views.BatchOCRProcessingView.as_view(), name='batch_ocr_processing'),
    path('documents/<int:document_id>/ocr/', views.DocumentOCRView.as_view(), name='document_ocr'),
    path('ocr/lab-results/', views.LabResultsOCRView.as_view(), name='lab_results_ocr'),
    path('ocr/forms/', views.FormsOCRView.as_view(), name='forms_ocr'),
    
    # AI-powered data extraction
    path('extract-data/', views.DataExtractionView.as_view(), name='data_extraction'),
    path('documents/<int:document_id>/extract/', views.DocumentDataExtractionView.as_view(), name='document_data_extraction'),
    path('extract/structured-data/', views.StructuredDataExtractionView.as_view(), name='structured_data_extraction'),
    path('auto-insert-ehr/', views.AutoInsertEHRView.as_view(), name='auto_insert_ehr'),
    
    # Document management
    path('documents/<int:document_id>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('documents/<int:document_id>/download/', views.DocumentDownloadView.as_view(), name='document_download'),
    path('documents/<int:document_id>/preview/', views.DocumentPreviewView.as_view(), name='document_preview'),
    path('documents/<int:document_id>/thumbnail/', views.DocumentThumbnailView.as_view(), name='document_thumbnail'),
    
    # File categorization and tagging
    path('categories/', views.FileCategoryListView.as_view(), name='file_categories'),
    path('documents/<int:document_id>/categorize/', views.DocumentCategorizationView.as_view(), name='document_categorization'),
    path('documents/<int:document_id>/tags/', views.DocumentTaggingView.as_view(), name='document_tagging'),
    
    # File security and encryption
    path('documents/<int:document_id>/encrypt/', views.DocumentEncryptionView.as_view(), name='document_encryption'),
    path('documents/<int:document_id>/decrypt/', views.DocumentDecryptionView.as_view(), name='document_decryption'),
    
    # Include router URLs
    path('', include(router.urls)),
]
