# 🏥 Healthcare Management API - Complete Endpoints List

## Base URL: `http://127.0.0.1:8000`

---

## 🔐 Authentication Endpoints (`/api/v1/auth/`)

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/auth/register/` | ❌ | Register new user |
| `POST` | `/api/v1/auth/login/` | ❌ | User login |
| `POST` | `/api/v1/auth/logout/` | ✅ | User logout |
| `POST` | `/api/v1/auth/token/refresh/` | ❌ | Refresh JWT token |
| `GET` | `/api/v1/auth/profile/` | ✅ | Get user profile |
| `PUT` | `/api/v1/auth/profile/update/` | ✅ | Update user profile |
| `POST` | `/api/v1/auth/change-password/` | ✅ | Change password |
| `GET` | `/api/v1/auth/roles/` | ✅ | List available roles |
| `GET` | `/api/v1/auth/permissions/` | ✅ | List permissions |
| `POST` | `/api/v1/auth/users/{user_id}/assign-role/` | ✅ | Assign role to user |
| `DELETE` | `/api/v1/auth/users/{user_id}/assign-role/` | ✅ | Remove role from user |

---

## 👥 Patient Management (`/api/v1/patients/`)

### Core CRUD Operations
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/patients/` | ✅ | List all patients |
| `POST` | `/api/v1/patients/` | ✅ | Create new patient |
| `GET` | `/api/v1/patients/{id}/` | ✅ | Get patient details |
| `PUT` | `/api/v1/patients/{id}/` | ✅ | Update patient |
| `PATCH` | `/api/v1/patients/{id}/` | ✅ | Partial update patient |
| `DELETE` | `/api/v1/patients/{id}/` | ✅ | Delete patient |

### Search & Filter
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/patients/search/` | ✅ | General patient search |
| `GET` | `/api/v1/patients/search/by-name/` | ✅ | Search by name |
| `GET` | `/api/v1/patients/search/by-dob/` | ✅ | Search by date of birth |
| `GET` | `/api/v1/patients/search/by-mrn/` | ✅ | Search by MRN |
| `GET` | `/api/v1/patients/search/advanced/` | ✅ | Advanced search |

### Patient Data
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/patients/{id}/history/` | ✅ | Patient medical history |
| `GET` | `/api/v1/patients/{id}/visits/` | ✅ | Patient visits |
| `GET` | `/api/v1/patients/{id}/assessments/` | ✅ | Patient assessments |
| `GET` | `/api/v1/patients/{id}/medications/` | ✅ | Patient medications |
| `GET` | `/api/v1/patients/{id}/allergies/` | ✅ | Patient allergies |
| `GET` | `/api/v1/patients/{id}/vitals/` | ✅ | Patient vital signs |
| `GET` | `/api/v1/patients/{id}/care-plan/` | ✅ | Patient care plan |
| `GET` | `/api/v1/patients/{id}/demographics/` | ✅ | Patient demographics |
| `GET` | `/api/v1/patients/{id}/insurance/` | ✅ | Patient insurance info |

---

## 🏠 Visit Management (`/api/v1/visits/`)

### Core Visit Operations
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/visits/` | ✅ | List all visits |
| `POST` | `/api/v1/visits/` | ✅ | Create new visit |
| `GET` | `/api/v1/visits/{id}/` | ✅ | Get visit details |
| `PUT` | `/api/v1/visits/{id}/` | ✅ | Update visit |
| `PATCH` | `/api/v1/visits/{id}/` | ✅ | Partial update visit |
| `DELETE` | `/api/v1/visits/{id}/` | ✅ | Delete visit |

### Visit Notes & Documentation
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/visits/{id}/notes/` | ✅ | Get visit notes |
| `POST` | `/api/v1/visits/{id}/notes/` | ✅ | Add visit note |
| `GET` | `/api/v1/visits/{id}/notes/{note_id}/` | ✅ | Get specific note |
| `PUT` | `/api/v1/visits/{id}/notes/{note_id}/` | ✅ | Update note |
| `DELETE` | `/api/v1/visits/{id}/notes/{note_id}/` | ✅ | Delete note |
| `GET` | `/api/v1/visits/{id}/structured-notes/` | ✅ | Get structured notes |
| `GET` | `/api/v1/visits/{id}/unstructured-notes/` | ✅ | Get unstructured notes |

### AI-Powered Features
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/visits/{id}/summary/` | ✅ | AI-generated visit summary |
| `POST` | `/api/v1/visits/{id}/ai-documentation/` | ✅ | AI documentation |
| `POST` | `/api/v1/visits/{id}/transcript-to-note/` | ✅ | Convert transcript to note |
| `POST` | `/api/v1/visits/{id}/voice-to-text/` | ✅ | Voice to text conversion |

### Templates & Configuration
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/visits/{id}/template/` | ✅ | Get visit template |
| `GET` | `/api/v1/visits/templates/{discipline}/` | ✅ | Get discipline templates |
| `GET` | `/api/v1/visits/templates/{discipline}/{visit_type}/` | ✅ | Get specific template |
| `GET` | `/api/v1/visits/types/` | ✅ | List visit types |
| `GET` | `/api/v1/visits/disciplines/` | ✅ | List disciplines |
| `GET` | `/api/v1/visits/ai-prompts/` | ✅ | AI prompt templates |
| `GET` | `/api/v1/visits/ai-prompts/{template_type}/` | ✅ | Specific AI prompt |

---

## 📋 OASIS Assessment (`/api/v1/oasis/`)

### Core Assessment Operations
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/oasis/assessments/` | ✅ | List OASIS assessments |
| `POST` | `/api/v1/oasis/assessments/` | ✅ | Create assessment |
| `GET` | `/api/v1/oasis/assessments/{id}/` | ✅ | Get assessment details |
| `PUT` | `/api/v1/oasis/assessments/{id}/` | ✅ | Update assessment |
| `DELETE` | `/api/v1/oasis/assessments/{id}/` | ✅ | Delete assessment |

### Assessment Submission
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/oasis/submit/` | ✅ | Submit OASIS assessment |
| `POST` | `/api/v1/oasis/submit/draft/` | ✅ | Save draft assessment |
| `POST` | `/api/v1/oasis/submit/final/` | ✅ | Submit final assessment |
| `POST` | `/api/v1/oasis/bulk-submit/` | ✅ | Bulk submit assessments |

### Templates & Disciplines
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/oasis/templates/` | ✅ | List OASIS templates |
| `GET` | `/api/v1/oasis/template/{discipline}/` | ✅ | Get discipline templates |
| `GET` | `/api/v1/oasis/template/{discipline}/{assessment_type}/` | ✅ | Get specific template |
| `GET` | `/api/v1/oasis/templates/sn/` | ✅ | Skilled nursing templates |
| `GET` | `/api/v1/oasis/templates/pt/` | ✅ | Physical therapy templates |
| `GET` | `/api/v1/oasis/templates/ot/` | ✅ | Occupational therapy templates |

### AI Analysis & Risk Assessment
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/oasis/assessments/{id}/ai-analysis/` | ✅ | AI analysis |
| `GET` | `/api/v1/oasis/assessments/{id}/risk-scores/` | ✅ | Risk scores |
| `GET` | `/api/v1/oasis/assessments/{id}/recommendations/` | ✅ | Recommendations |
| `GET` | `/api/v1/oasis/assessments/{id}/quality-indicators/` | ✅ | Quality indicators |
| `GET` | `/api/v1/oasis/assessments/{id}/fall-risk/` | ✅ | Fall risk prediction |
| `GET` | `/api/v1/oasis/assessments/{id}/readmission-risk/` | ✅ | Readmission risk |
| `GET` | `/api/v1/oasis/assessments/{id}/deterioration-risk/` | ✅ | Deterioration risk |

### Assessment Management
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/oasis/assessments/pending/` | ✅ | Pending assessments |
| `GET` | `/api/v1/oasis/assessments/completed/` | ✅ | Completed assessments |

---

## 📁 File Management & OCR (`/api/v1/files/`)

### Core Document Operations
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/files/documents/` | ✅ | List documents |
| `POST` | `/api/v1/files/documents/` | ✅ | Create document |
| `GET` | `/api/v1/files/documents/{id}/` | ✅ | Get document details |
| `PUT` | `/api/v1/files/documents/{id}/` | ✅ | Update document |
| `DELETE` | `/api/v1/files/documents/{id}/` | ✅ | Delete document |

### File Upload
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/files/upload/` | ✅ | Upload single file |
| `POST` | `/api/v1/files/upload/multiple/` | ✅ | Upload multiple files |
| `POST` | `/api/v1/files/upload/patient/{patient_id}/` | ✅ | Upload patient file |
| `POST` | `/api/v1/files/upload/visit/{visit_id}/` | ✅ | Upload visit file |

### OCR Processing
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/files/ocr/` | ✅ | General OCR processing |
| `POST` | `/api/v1/files/ocr/batch/` | ✅ | Batch OCR processing |
| `POST` | `/api/v1/files/documents/{id}/ocr/` | ✅ | Document OCR |
| `POST` | `/api/v1/files/ocr/lab-results/` | ✅ | Lab results OCR |
| `POST` | `/api/v1/files/ocr/forms/` | ✅ | Forms OCR |

### Data Extraction
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/files/extract-data/` | ✅ | General data extraction |
| `POST` | `/api/v1/files/documents/{id}/extract/` | ✅ | Document data extraction |
| `POST` | `/api/v1/files/extract/structured-data/` | ✅ | Structured data extraction |
| `POST` | `/api/v1/files/auto-insert-ehr/` | ✅ | Auto-insert into EHR |

### Document Management
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/files/documents/{id}/download/` | ✅ | Download document |
| `GET` | `/api/v1/files/documents/{id}/preview/` | ✅ | Preview document |
| `GET` | `/api/v1/files/documents/{id}/thumbnail/` | ✅ | Document thumbnail |

### Categorization & Tagging
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/files/categories/` | ✅ | List file categories |
| `POST` | `/api/v1/files/documents/{id}/categorize/` | ✅ | Categorize document |
| `GET` | `/api/v1/files/documents/{id}/tags/` | ✅ | Get document tags |
| `POST` | `/api/v1/files/documents/{id}/tags/` | ✅ | Add document tags |

### Security
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/files/documents/{id}/encrypt/` | ✅ | Encrypt document |
| `POST` | `/api/v1/files/documents/{id}/decrypt/` | ✅ | Decrypt document |

---

## 💬 Communication (`/api/v1/communication/`)

### Core Communication
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/communication/threads/` | ✅ | List communication threads |
| `POST` | `/api/v1/communication/threads/` | ✅ | Create thread |
| `GET` | `/api/v1/communication/threads/{id}/` | ✅ | Get thread details |
| `PUT` | `/api/v1/communication/threads/{id}/` | ✅ | Update thread |
| `DELETE` | `/api/v1/communication/threads/{id}/` | ✅ | Delete thread |
| `GET` | `/api/v1/communication/messages/` | ✅ | List messages |
| `POST` | `/api/v1/communication/messages/` | ✅ | Create message |

### Message Operations
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/communication/send-note/` | ✅ | Send note |
| `POST` | `/api/v1/communication/send-ai-update/` | ✅ | Send AI update |
| `POST` | `/api/v1/communication/send-urgent-alert/` | ✅ | Send urgent alert |

### Thread Management
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/communication/threads/{patient_id}/` | ✅ | Patient threads |
| `GET` | `/api/v1/communication/threads/{thread_id}/messages/` | ✅ | Thread messages |
| `GET` | `/api/v1/communication/threads/{thread_id}/participants/` | ✅ | Thread participants |

### AI-Generated Communications
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/v1/communication/generate-md-update/` | ✅ | Generate MD update |
| `POST` | `/api/v1/communication/generate-summary/` | ✅ | Generate summary |
| `POST` | `/api/v1/communication/generate-handoff-note/` | ✅ | Generate handoff note |
| `POST` | `/api/v1/communication/generate-care-summary/` | ✅ | Generate care summary |

### Clinical Decision Support
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/communication/medication-adjustments/` | ✅ | Medication adjustments |
| `GET` | `/api/v1/communication/intervention-recommendations/` | ✅ | Intervention recommendations |
| `GET` | `/api/v1/communication/care-plan-updates/` | ✅ | Care plan updates |

### Notifications
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/communication/notifications/` | ✅ | List notifications |
| `POST` | `/api/v1/communication/notifications/{id}/read/` | ✅ | Mark notification read |
| `GET` | `/api/v1/communication/notifications/unread/` | ✅ | Unread notifications |

### Team Coordination
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/communication/team-updates/` | ✅ | Team updates |
| `GET` | `/api/v1/communication/urgent-alerts/` | ✅ | Urgent alerts |
| `GET` | `/api/v1/communication/shift-handoffs/` | ✅ | Shift handoffs |
| `GET` | `/api/v1/communication/interdisciplinary-notes/` | ✅ | Interdisciplinary notes |

### Analytics
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/v1/communication/analytics/response-times/` | ✅ | Response time analytics |
| `GET` | `/api/v1/communication/analytics/communication-patterns/` | ✅ | Communication patterns |

---

## 🔧 System Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/` | ❌ | API documentation homepage |
| `GET` | `/health/` | ❌ | Health check endpoint |
| `GET` | `/admin/` | ❌ | Django admin interface |

---

## 📝 Common Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `patient_id` | Filter by patient ID | `?patient_id=123` |
| `start_date` | Filter by start date | `?start_date=2024-01-01` |
| `end_date` | Filter by end date | `?end_date=2024-12-31` |
| `is_completed` | Filter by completion status | `?is_completed=true` |
| `search` | Search by keyword | `?search=diabetes` |
| `page` | Page number for pagination | `?page=2` |
| `page_size` | Items per page | `?page_size=20` |
| `assessment_type` | Filter by assessment type | `?assessment_type=SOC` |
| `discipline` | Filter by discipline | `?discipline=SN` |
| `visit_type` | Filter by visit type | `?visit_type=routine` |
| `is_urgent` | Filter urgent items | `?is_urgent=true` |

---

## 🔑 Authentication

### Headers for Authenticated Requests:
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

### Test Credentials:
- **Username:** `admin`
- **Password:** `admin123`

### Getting Started:
1. **Login:** `POST /api/v1/auth/login/`
2. **Copy the access token** from the response
3. **Use the token** in the Authorization header for all subsequent requests

---

## 🚀 Quick Test URLs (No Auth Required):

- **API Documentation:** `GET http://127.0.0.1:8000/`
- **Health Check:** `GET http://127.0.0.1:8000/health/`
- **User Login:** `POST http://127.0.0.1:8000/api/v1/auth/login/`
- **User Registration:** `POST http://127.0.0.1:8000/api/v1/auth/register/`

---

## 📊 Total Endpoints Summary

| Category | Count |
|----------|-------|
| Authentication | 11 |
| Patient Management | 18 |
| Visit Management | 19 |
| OASIS Assessment | 26 |
| File Management & OCR | 25 |
| Communication | 23 |
| System | 3 |
| **Total Endpoints** | **125** |

---

## 📖 Sample Request Examples

### Login Example:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### Create Patient Example:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/patients/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "mrn": "MRN123456",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1985-01-15",
    "gender": "M",
    "phone": "555-0123",
    "email": "john.doe@example.com",
    "address": "123 Main St, City, State 12345",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "555-0124",
    "primary_diagnosis": "Diabetes Type 2"
  }'
```

### Submit OASIS Assessment Example:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/oasis/submit/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "assessment_type": "SOC",
    "assessment_date": "2024-01-15",
    "primary_diagnosis": "Diabetes with complications",
    "grooming": 1,
    "dressing_upper": 1,
    "bathing": 2,
    "toileting": 1,
    "ambulation": 2
  }'
```

---

*This healthcare management API provides comprehensive endpoints for patient care, assessments, communication, and file management with AI-powered features for enhanced clinical workflows.*
