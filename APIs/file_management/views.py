from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import UploadedFile
from .serializers import FileUploadSerializer, OCRRequestSerializer
from .ocr_utils import OCRProcessor


class FileUploadViewSet(viewsets.ModelViewSet):
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter files based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return UploadedFile.objects.all()
        elif user.role == 'physician':
            return UploadedFile.objects.filter(patient__assigned_physician=user)
        else:
            # Nurses and other staff can see files for all patients
            return UploadedFile.objects.all()

    def create(self, request, *args, **kwargs):
        """Upload a new file"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            file_instance = serializer.save()
            
            # Check if file is an image and trigger OCR processing
            if file_instance.file_type.startswith('image/'):
                file_instance.processing_status = 'pending'
                file_instance.save()
                
                # In a production environment, this would be handled by a background task
                # For now, we'll process it synchronously
                self._process_file_ocr(file_instance)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _process_file_ocr(self, file_instance):
        """Process file for OCR (would be async in production)"""
        try:
            file_instance.processing_status = 'processing'
            file_instance.save()
            
            # Extract text using OCR
            file_path = file_instance.file.path
            ocr_text = OCRProcessor.extract_text_from_image(file_path)
            
            # Extract structured data based on category
            data_type = 'general'
            if file_instance.category == 'lab_results':
                data_type = 'lab_values'
            elif file_instance.category == 'forms':
                data_type = 'vital_signs'
            
            structured_data = OCRProcessor.extract_structured_data(ocr_text, data_type)
            
            # Update file instance
            file_instance.ocr_text = ocr_text
            file_instance.structured_data = structured_data
            file_instance.is_processed = True
            file_instance.processing_status = 'completed'
            file_instance.save()
            
        except Exception as e:
            file_instance.processing_status = 'failed'
            file_instance.structured_data = {'error': str(e)}
            file_instance.save()

    @action(detail=True, methods=['post'])
    def process_ocr(self, request, pk=None):
        """Manually trigger OCR processing for a file"""
        file_instance = self.get_object()
        
        if not file_instance.file_type.startswith('image/'):
            return Response(
                {'error': 'OCR is only available for image files'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = OCRRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Process OCR
        self._process_file_ocr(file_instance)
        
        # Return updated file data
        response_serializer = self.get_serializer(file_instance)
        return Response(response_serializer.data)

    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get files for a specific patient"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        files = self.get_queryset().filter(patient_id=patient_id)
        serializer = self.get_serializer(files, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search files by various criteria"""
        queryset = self.get_queryset()
        
        # Filter by category
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by processing status
        processing_status = request.query_params.get('processing_status')
        if processing_status:
            queryset = queryset.filter(processing_status=processing_status)
        
        # Text search in OCR content
        search_text = request.query_params.get('search')
        if search_text:
            queryset = queryset.filter(ocr_text__icontains=search_text)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
