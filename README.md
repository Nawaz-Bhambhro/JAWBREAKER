# 🏥 Home Health AI API System - Complete Documentation

## 📋 Overview
This is a comprehensive Home Health AI API system built with Django REST Framework that provides:

- **Authentication & User Management** with RBAC (Role-based Access Control)
- **Patient Record Management** with search capabilities
- **Visit Notes & Documentation** with AI summary generation
- **File Uploads & OCR** for document processing
- **OASIS & Specialized Forms** integration
- **Communication & Coordination** features

## 🔧 Technical Stack
- **Backend**: Django 4.2+ with Django REST Framework
- **Authentication**: JWT-based security
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **File Processing**: OCR with pytesseract, AI integration ready
- **API Documentation**: Auto-generated with DRF

## 🏗️ Project Structure
```
myproject/
├── authentication/          # User management & JWT auth
├── patients/               # Patient records management
├── visits/                 # Visit documentation & notes
├── file_management/        # File upload & OCR processing
├── oasis/                  # OASIS forms & assessments
├── communication/          # Inter-provider communication
├── api/                    # Original employee API
├── settings.py             # Main configuration
├── urls.py                 # URL routing
└── manage.py              # Django management
```

## 🔐 User Roles & Permissions
- **Admin**: Full system access
- **Physician**: Access to assigned patients
- **Nurse**: Full patient access, documentation
- **Physical Therapist (PT)**: Therapy-specific documentation
- **Occupational Therapist (OT)**: OT-specific documentation
- **Social Worker**: Social services documentation

## 📊 Core API Endpoints

### Authentication
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login (returns JWT tokens)
- `GET /auth/profile/` - Get/update user profile

### Patient Management
- `GET /api/patients/` - List patients
- `POST /api/patients/` - Create new patient
- `GET /api/patients/{id}/` - Get patient details
- `PUT /api/patients/{id}/` - Update patient
- `GET /api/patients/search/` - Search patients

### Visit Management
- `GET /api/visits/` - List visits
- `POST /api/visits/` - Create new visit
- `POST /api/visits/{id}/start_visit/` - Start visit
- `POST /api/visits/{id}/end_visit/` - End visit
- `POST /api/visits/{id}/notes/` - Add visit notes
- `GET /api/visits/{id}/notes_list/` - Get all visit notes
- `POST /api/visits/{id}/summary/` - Generate AI summary
- `GET /api/visits/{id}/template/` - Get documentation template

### File Management & OCR
- `POST /api/files/` - Upload files
- `GET /api/files/` - List files
- `POST /api/files/{id}/process_ocr/` - Process OCR
- `GET /api/files/by_patient/` - Get files by patient
- `GET /api/files/search/` - Search files

### OASIS & Forms
- `POST /api/oasis/` - Submit OASIS assessment
- `GET /api/oasis/template/{discipline}/` - Get OASIS templates

### Communication
- `POST /api/communication/` - Send messages
- `GET /api/communication/threads/{patient_id}/` - Get communication threads

## 🤖 AI Integration Features

### 1. Visit Summary Generation
```json
POST /api/visits/{id}/summary/
{
    "include_notes": true,
    "include_vitals": true,
    "summary_type": "physician"
}
```

### 2. OCR Document Processing
- Automatic text extraction from uploaded images
- Structured data extraction for:
  - Lab values
  - Vital signs
  - Medication lists
  - Insurance information

### 3. Smart Documentation Templates
- Dynamic forms based on visit type and discipline
- AI-assisted note generation
- Clinical decision support prompts

## 🔒 Security Features
- **JWT Authentication** with refresh tokens
- **Role-based access control** (RBAC)
- **CORS support** for frontend integration
- **File upload validation** and security
- **HIPAA-compliant** data handling ready

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## 📱 Frontend Integration

### Authentication Flow
1. Register/Login to get JWT tokens
2. Include `Authorization: Bearer <token>` in headers
3. Refresh tokens before expiration

### Example API Calls
```javascript
// Login
const response = await fetch('/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: 'nurse_jane',
        password: 'password123'
    })
});

// Create Patient
const patient = await fetch('/api/patients/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({
        mrn: 'MRN001',
        first_name: 'John',
        last_name: 'Doe',
        // ... other fields
    })
});
```

## 🔄 AI Integration Roadmap

### Phase 1: Input Processing ✅
- NLP ingestion of free-text notes
- Auto-categorization into structured templates
- Patient-specific tagging

### Phase 2: AI Documentation ✅
- Prompt templates for visit summaries
- AI-generated clinical notes
- Integration with patient history

### Phase 3: Analytics & Insights (Next)
- Predictive modeling for fall risk
- Readmission risk assessment
- Trend analysis

### Phase 4: Care Recommendations (Future)
- Auto-generated care plan updates
- Medication adjustment suggestions
- Clinical decision support

## 🏥 Healthcare Compliance
- **HIPAA-ready** data handling
- **Audit trails** for all patient data access
- **Secure file storage** with encryption
- **Role-based access** controls
- **Data anonymization** capabilities

## 📈 Scalability Features
- **Modular architecture** for easy extension
- **Database optimization** ready
- **Caching support** with Redis
- **Background task processing** with Celery
- **API rate limiting** ready

## 🧪 Testing
Use the provided `api_test.http` file with VS Code REST Client extension or Postman for comprehensive API testing.

## 🚀 Deployment Ready
- **Docker** containerization ready
- **Environment variables** configuration
- **Production settings** separation
- **Static file handling** configured
- **Database migration** support

This system provides a solid foundation for a modern, AI-integrated home health management platform with enterprise-grade security and scalability features.
