from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from datetime import date, timedelta
from .models import Patient
from .serializers import PatientSerializer, PatientSearchSerializer, PatientBasicSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter patients based on user role"""
        user = self.request.user
        if user.role == 'admin':
            return Patient.objects.filter(is_active=True)
        elif user.role == 'physician':
            return Patient.objects.filter(assigned_physician=user, is_active=True)
        else:
            # Nurses and other staff can see all patients
            return Patient.objects.filter(is_active=True)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search patients by name, MRN, or date of birth
        Example: /api/patients/search/?query=John&gender=M&age_min=18&age_max=65
        """
        serializer = PatientSearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data.get('query', '')
        gender = serializer.validated_data.get('gender')
        age_min = serializer.validated_data.get('age_min')
        age_max = serializer.validated_data.get('age_max')

        patients = self.get_queryset()

        # Text search
        if query:
            patients = patients.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(mrn__icontains=query)
            )

        # Gender filter
        if gender:
            patients = patients.filter(gender=gender)

        # Age filters
        if age_min is not None or age_max is not None:
            today = date.today()
            if age_max is not None:
                date_min = today - timedelta(days=(age_max + 1) * 365)
                patients = patients.filter(date_of_birth__gte=date_min)
            if age_min is not None:
                date_max = today - timedelta(days=age_min * 365)
                patients = patients.filter(date_of_birth__lte=date_max)

        serializer = PatientSerializer(patients, many=True, context={'request': request})
        return Response({
            'count': patients.count(),
            'results': serializer.data
        })


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class PatientSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            patients = Patient.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(mrn__icontains=query) |
                Q(email__icontains=query)
            )
        else:
            patients = Patient.objects.all()

        serializer = PatientBasicSerializer(patients, many=True)
        return Response(serializer.data)


class AdvancedPatientSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.GET.get('name')
        dob = request.GET.get('dob')
        mrn = request.GET.get('mrn')

        filters = Q()
        if name:
            filters &= Q(first_name__icontains=name) | Q(last_name__icontains=name)
        if dob:
            filters &= Q(date_of_birth=dob)
        if mrn:
            filters &= Q(mrn=mrn)

        patients = Patient.objects.filter(filters)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


class PatientHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        # Return patient medical history
        return Response({
            'patient_id': patient.id,
            'medical_history': getattr(patient, 'medical_history', []),
            'message': 'Patient history retrieved successfully'
        })


class PatientVisitsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        # Return patient visits - you'll need to implement this based on your Visit model
        return Response({
            'patient_id': patient.id,
            'visits': [],
            'message': 'Patient visits retrieved successfully'
        })


class PatientAssessmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        return Response({
            'patient_id': patient.id,
            'assessments': [],
            'message': 'Patient assessments retrieved successfully'
        })


class PatientMedicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        return Response({
            'patient_id': patient.id,
            'medications': getattr(patient, 'medications', []),
            'message': 'Patient medications retrieved successfully'
        })


class PatientAllergiesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        return Response({
            'patient_id': patient.id,
            'allergies': getattr(patient, 'allergies', []),
            'message': 'Patient allergies retrieved successfully'
        })


class PatientVitalsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        return Response({
            'patient_id': patient.id,
            'vitals': [],
            'message': 'Patient vitals retrieved successfully'
        })


class PatientCarePlanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        return Response({
            'patient_id': patient.id,
            'care_plan': getattr(patient, 'care_plan', {}),
            'message': 'Patient care plan retrieved successfully'
        })


class PatientDemographicsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


class PatientInsuranceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        return Response({
            'patient_id': patient.id,
            'insurance': getattr(patient, 'insurance_info', {}),
            'message': 'Patient insurance retrieved successfully'
        })


class SearchByNameView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        name = request.GET.get('name', '')
        if name:
            patients = Patient.objects.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )
        else:
            patients = Patient.objects.none()
        
        serializer = PatientBasicSerializer(patients, many=True)
        return Response({
            'count': patients.count(),
            'results': serializer.data
        })

class SearchByDOBView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        dob = request.GET.get('dob', '')
        if dob:
            patients = Patient.objects.filter(date_of_birth=dob)
        else:
            patients = Patient.objects.none()
        
        serializer = PatientBasicSerializer(patients, many=True)
        return Response({
            'count': patients.count(),
            'results': serializer.data
        })

class SearchByMRNView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        mrn = request.GET.get('mrn', '')
        if mrn:
            patients = Patient.objects.filter(mrn__icontains=mrn)
        else:
            patients = Patient.objects.none()
        
        serializer = PatientBasicSerializer(patients, many=True)
        return Response({
            'count': patients.count(),
            'results': serializer.data
        })
