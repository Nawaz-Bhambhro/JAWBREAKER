# 🏥 Healthcare Management API - Complete Endpoints List

## Base URL: `http://127.0.0.1:8000`

---

## 🔐 AUTHENTICATION ENDPOINTS (`/api/v1/auth/`)

```
POST   /api/v1/auth/register/                    - Register new user
POST   /api/v1/auth/login/                       - User login
POST   /api/v1/auth/logout/                      - User logout
POST   /api/v1/auth/token/refresh/               - Refresh JWT token
GET    /api/v1/auth/profile/                     - Get user profile
PUT    /api/v1/auth/profile/update/              - Update user profile
POST   /api/v1/auth/change-password/             - Change password
GET    /api/v1/auth/roles/                       - List available roles
GET    /api/v1/auth/permissions/                 - List permissions
POST   /api/v1/auth/users/{user_id}/assign-role/ - Assign role to user
DELETE /api/v1/auth/users/{user_id}/assign-role/ - Remove role from user
```

---

## 👥 PATIENT MANAGEMENT (`/api/v1/patients/`)

### Core CRUD Operations
```
GET    /api/v1/patients/                         - List all patients
POST   /api/v1/patients/                         - Create new patient
GET    /api/v1/patients/{id}/                    - Get patient details
PUT    /api/v1/patients/{id}/                    - Update patient
PATCH  /api/v1/patients/{id}/                    - Partial update patient
DELETE /api/v1/patients/{id}/                    - Delete patient
```

### Search & Filter
```
GET    /api/v1/patients/search/                  - General patient search
GET    /api/v1/patients/search/by-name/          - Search by name
GET    /api/v1/patients/search/by-dob/           - Search by date of birth
GET    /api/v1/patients/search/by-mrn/           - Search by MRN
GET    /api/v1/patients/search/advanced/         - Advanced search
```

### Patient Data
```
GET    /api/v1/patients/{id}/history/            - Patient medical history
GET    /api/v1/patients/{id}/visits/             - Patient visits
GET    /api/v1/patients/{id}/assessments/        - Patient assessments
GET    /api/v1/patients/{id}/medications/        - Patient medications
GET    /api/v1/patients/{id}/allergies/          - Patient allergies
GET    /api/v1/patients/{id}/vitals/             - Patient vital signs
GET    /api/v1/patients/{id}/care-plan/          - Patient care plan
GET    /api/v1/patients/{id}/demographics/       - Patient demographics
GET    /api/v1/patients/{id}/insurance/          - Patient insurance info
```

---

## 🏠 VISIT MANAGEMENT (`/api/v1/visits/`)

### Core Visit Operations
```
GET    /api/v1/visits/                           - List all visits
POST   /api/v1/visits/                           - Create new visit
GET    /api/v1/visits/{id}/                      - Get visit details
PUT    /api/v1/visits/{id}/                      - Update visit
PATCH  /api/v1/visits/{id}/                      - Partial update visit
DELETE /api/v1/visits/{id}/                      - Delete visit
```

### Visit Notes & Documentation
```
GET    /api/v1/visits/{id}/notes/                - Get visit notes
POST   /api/v1/visits/{id}/notes/                - Add visit note
GET    /api/v1/visits/{id}/notes/{note_id}/      - Get specific note
PUT    /api/v1/visits/{id}/notes/{note_id}/      - Update note
DELETE /api/v1/visits/{id}/notes/{note_id}/      - Delete note
GET    /api/v1/visits/{id}/structured-notes/     - Get structured notes
GET    /api/v1/visits/{id}/unstructured-notes/   - Get unstructured notes
```

### AI-Powered Features
```
GET    /api/v1/visits/{id}/summary/              - AI-generated visit summary
POST   /api/v1/visits/{id}/ai-documentation/     - AI documentation
POST   /api/v1/visits/{id}/transcript-to-note/   - Convert transcript to note
POST   /api/v1/visits/{id}/voice-to-text/        - Voice to text conversion
```

### Templates & Configuration
```
GET    /api/v1/visits/{id}/template/             - Get visit template
GET    /api/v1/visits/templates/{discipline}/    - Get discipline templates
GET    /api/v1/visits/templates/{discipline}/{visit_type}/ - Get specific template
GET    /api/v1/visits/types/                     - List visit types
GET    /api/v1/visits/disciplines/               - List disciplines
GET    /api/v1/visits/ai-prompts/                - AI prompt templates
GET    /api/v1/visits/ai-prompts/{template_type}/ - Specific AI prompt
```

---

## 📋 OASIS ASSESSMENT (`/api/v1/oasis/`)

### Core Assessment Operations
```
GET    /api/v1/oasis/assessments/                - List OASIS assessments
POST   /api/v1/oasis/assessments/                - Create assessment
GET    /api/v1/oasis/assessments/{id}/           - Get assessment details
PUT    /api/v1/oasis/assessments/{id}/           - Update assessment
DELETE /api/v1/oasis/assessments/{id}/           - Delete assessment
```

### Assessment Submission
```
POST   /api/v1/oasis/submit/                     - Submit OASIS assessment
POST   /api/v1/oasis/submit/draft/               - Save draft assessment
POST   /api/v1/oasis/submit/final/               - Submit final assessment
POST   /api/v1/oasis/bulk-submit/                - Bulk submit assessments
```

### Templates & Disciplines
```
GET    /api/v1/oasis/templates/                  - List OASIS templates
GET    /api/v1/oasis/template/{discipline}/      - Get discipline templates
GET    /api/v1/oasis/template/{discipline}/{assessment_type}/ - Get specific template
GET    /api/v1/oasis/templates/sn/               - Skilled nursing templates
GET    /api/v1/oasis/templates/pt/               - Physical therapy templates
GET    /api/v1/oasis/templates/ot/               - Occupational therapy templates
```

### AI Analysis & Risk Assessment
```
GET    /api/v1/oasis/assessments/{id}/ai-analysis/     - AI analysis
GET    /api/v1/oasis/assessments/{id}/risk-scores/     - Risk scores
GET    /api/v1/oasis/assessments/{id}/recommendations/ - Recommendations
GET    /api/v1/oasis/assessments/{id}/quality-indicators/ - Quality indicators
GET    /api/v1/oasis/assessments/{id}/fall-risk/       - Fall risk prediction
GET    /api/v1/oasis/assessments/{id}/readmission-risk/ - Readmission risk
GET    /api/v1/oasis/assessments/{id}/deterioration-risk/ - Deterioration risk
```

### Assessment Management
```
GET    /api/v1/oasis/assessments/pending/        - Pending assessments
GET    /api/v1/oasis/assessments/completed/      - Completed assessments
```

---

## 📁 FILE MANAGEMENT & OCR (`/api/v1/files/`)

### Core Document Operations
```
GET    /api/v1/files/documents/                  - List documents
POST   /api/v1/files/documents/                  - Create document
GET    /api/v1/files/documents/{id}/             - Get document details
PUT    /api/v1/files/documents/{id}/             - Update document
DELETE /api/v1/files/documents/{id}/             - Delete document
```

### File Upload
```
POST   /api/v1/files/upload/                     - Upload single file
POST   /api/v1/files/upload/multiple/            - Upload multiple files
POST   /api/v1/files/upload/patient/{patient_id}/ - Upload patient file
POST   /api/v1/files/upload/visit/{visit_id}/    - Upload visit file
```

### OCR Processing
```
POST   /api/v1/files/ocr/                        - General OCR processing
POST   /api/v1/files/ocr/batch/                  - Batch OCR processing
POST   /api/v1/files/documents/{id}/ocr/         - Document OCR
POST   /api/v1/files/ocr/lab-results/            - Lab results OCR
POST   /api/v1/files/ocr/forms/                  - Forms OCR
```

### Data Extraction
```
POST   /api/v1/files/extract-data/               - General data extraction
POST   /api/v1/files/documents/{id}/extract/     - Document data extraction
POST   /api/v1/files/extract/structured-data/    - Structured data extraction
POST   /api/v1/files/auto-insert-ehr/            - Auto-insert into EHR
```

### Document Management
```
GET    /api/v1/files/documents/{id}/download/    - Download document
GET    /api/v1/files/documents/{id}/preview/     - Preview document
GET    /api/v1/files/documents/{id}/thumbnail/   - Document thumbnail
```

### Categorization & Tagging
```
GET    /api/v1/files/categories/                 - List file categories
POST   /api/v1/files/documents/{id}/categorize/  - Categorize document
GET    /api/v1/files/documents/{id}/tags/        - Get document tags
POST   /api/v1/files/documents/{id}/tags/        - Add document tags
```

### Security
```
POST   /api/v1/files/documents/{id}/encrypt/     - Encrypt document
POST   /api/v1/files/documents/{id}/decrypt/     - Decrypt document
```

---

## 💬 COMMUNICATION (`/api/v1/communication/`)

### Core Communication
```
GET    /api/v1/communication/threads/            - List communication threads
POST   /api/v1/communication/threads/            - Create thread
GET    /api/v1/communication/threads/{id}/       - Get thread details
PUT    /api/v1/communication/threads/{id}/       - Update thread
DELETE /api/v1/communication/threads/{id}/       - Delete thread
GET    /api/v1/communication/messages/           - List messages
POST   /api/v1/communication/messages/           - Create message
```

### Message Operations
```
POST   /api/v1/communication/send-note/          - Send note
POST   /api/v1/communication/send-ai-update/     - Send AI update
POST   /api/v1/communication/send-urgent-alert/  - Send urgent alert
```

### Thread Management
```
GET    /api/v1/communication/threads/{patient_id}/    - Patient threads
GET    /api/v1/communication/threads/{thread_id}/messages/ - Thread messages
GET    /api/v1/communication/threads/{thread_id}/participants/ - Thread participants
```

### AI-Generated Communications
```
POST   /api/v1/communication/generate-md-update/      - Generate MD update
POST   /api/v1/communication/generate-summary/        - Generate summary
POST   /api/v1/communication/generate-handoff-note/   - Generate handoff note
POST   /api/v1/communication/generate-care-summary/   - Generate care summary
```

### Clinical Decision Support
```
GET    /api/v1/communication/medication-adjustments/  - Medication adjustments
GET    /api/v1/communication/intervention-recommendations/ - Intervention recommendations
GET    /api/v1/communication/care-plan-updates/       - Care plan updates
```

### Notifications
```
GET    /api/v1/communication/notifications/           - List notifications
POST   /api/v1/communication/notifications/{id}/read/ - Mark notification read
GET    /api/v1/communication/notifications/unread/    - Unread notifications
```

### Team Coordination
```
GET    /api/v1/communication/team-updates/            - Team updates
GET    /api/v1/communication/urgent-alerts/           - Urgent alerts
GET    /api/v1/communication/shift-handoffs/          - Shift handoffs
GET    /api/v1/communication/interdisciplinary-notes/ - Interdisciplinary notes
```

### Analytics
```
GET    /api/v1/communication/analytics/response-times/    - Response time analytics
GET    /api/v1/communication/analytics/communication-patterns/ - Communication patterns
```

---

## 🔧 SYSTEM ENDPOINTS

```
GET    /                                         - API documentation homepage
GET    /health/                                  - Health check endpoint
GET    /admin/                                   - Django admin interface
```

---

## 📊 SUMMARY BY CATEGORY

| Category | Total Endpoints |
|----------|----------------|
| 🔐 Authentication | 11 endpoints |
| 👥 Patient Management | 19 endpoints |
| 🏠 Visit Management | 20 endpoints |
| 📋 OASIS Assessment | 19 endpoints |
| 📁 File Management & OCR | 22 endpoints |
| 💬 Communication | 24 endpoints |
| 🔧 System | 3 endpoints |

**TOTAL: 118 API Endpoints**

---

## 🔑 AUTHENTICATION REQUIREMENTS

- ✅ **Auth Required**: Most endpoints (115/118)
- ❌ **No Auth Required**: Only 3 endpoints (homepage, health, admin login page)

---

## 🚀 QUICK START ENDPOINTS

**Test these first (No authentication required):**
```
GET    /                                         - API Documentation
GET    /health/                                  - Health Check
POST   /api/v1/auth/register/                    - Register User
POST   /api/v1/auth/login/                       - Login User
```

**Authentication Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Test Credentials:**
- Username: `admin`
- Password: `admin123`
