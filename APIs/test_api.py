import requests
import json
import time
from datetime import datetime, date

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

class APITester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.test_user_id = None
        self.test_patient_id = None
        self.test_visit_id = None
        self.test_assessment_id = None
        self.session = requests.Session()
        
    def log_test(self, test_name, status, response=None):
        """Log test results"""
        status_symbol = "✅" if status == "PASS" else "❌"
        print(f"{status_symbol} {test_name}")
        if response and response.status_code >= 400:
            print(f"   Status: {response.status_code}")
            try:
                print(f"   Response: {response.json()}")
            except:
                print(f"   Response: {response.text}")
        print()

    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/health/")
            if response.status_code == 200:
                self.log_test("Health Check", "PASS")
                return True
            else:
                self.log_test("Health Check", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Health Check - Error: {str(e)}")
            return False

    def test_homepage(self):
        """Test homepage endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("Homepage", "PASS")
                return True
            else:
                self.log_test("Homepage", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Homepage - Error: {str(e)}")
            return False

    def test_user_registration(self):
        """Test user registration"""
        registration_data = {
            "username": "testuser123",
            "email": "testuser123@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "nurse",
            "license_number": "LN123456",
            "phone": "555-0123",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/v1/auth/register/",
                json=registration_data
            )
            
            if response.status_code == 201:
                data = response.json()
                self.access_token = data.get('access')
                self.refresh_token = data.get('refresh')
                self.test_user_id = data.get('user', {}).get('id')
                self.log_test("User Registration", "PASS")
                return True
            else:
                self.log_test("User Registration", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ User Registration - Error: {str(e)}")
            return False

    def test_user_login(self):
        """Test user login"""
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/v1/auth/login/",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                self.refresh_token = data.get('refresh')
                self.log_test("User Login", "PASS")
                return True
            else:
                self.log_test("User Login", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ User Login - Error: {str(e)}")
            return False

    def get_auth_headers(self):
        """Get authorization headers"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def test_user_profile(self):
        """Test user profile endpoint"""
        try:
            response = self.session.get(
                f"{BASE_URL}/api/v1/auth/profile/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("User Profile", "PASS")
                return True
            else:
                self.log_test("User Profile", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ User Profile - Error: {str(e)}")
            return False

    def test_token_refresh(self):
        """Test token refresh"""
        try:
            response = self.session.post(
                f"{BASE_URL}/api/v1/auth/token/refresh/",
                json={"refresh": self.refresh_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                self.log_test("Token Refresh", "PASS")
                return True
            else:
                self.log_test("Token Refresh", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Token Refresh - Error: {str(e)}")
            return False

    def test_patient_creation(self):
        """Test patient creation"""
        patient_data = {
            "mrn": f"MRN{int(time.time())}",
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1985-05-15",
            "gender": "F",
            "phone": "555-0123",
            "email": "jane.doe@example.com",
            "address": "123 Main St, City, State 12345",
            "emergency_contact_name": "John Doe",
            "emergency_contact_phone": "555-0124",
            "primary_diagnosis": "Diabetes Type 2",
            "secondary_diagnoses": "Hypertension",
            "allergies": "Penicillin",
            "medications": "Metformin 500mg",
            "insurance_provider": "Blue Cross",
            "insurance_id": "BC123456789"
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/v1/patients/",
                json=patient_data,
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 201:
                data = response.json()
                self.test_patient_id = data.get('id')
                self.log_test("Patient Creation", "PASS")
                return True
            else:
                self.log_test("Patient Creation", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Patient Creation - Error: {str(e)}")
            return False

    def test_patient_list(self):
        """Test patient list endpoint"""
        try:
            response = self.session.get(
                f"{BASE_URL}/api/v1/patients/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("Patient List", "PASS")
                return True
            else:
                self.log_test("Patient List", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Patient List - Error: {str(e)}")
            return False

    def test_patient_detail(self):
        """Test patient detail endpoint"""
        if not self.test_patient_id:
            print("❌ Patient Detail - No patient ID available")
            return False
            
        try:
            response = self.session.get(
                f"{BASE_URL}/api/v1/patients/{self.test_patient_id}/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("Patient Detail", "PASS")
                return True
            else:
                self.log_test("Patient Detail", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Patient Detail - Error: {str(e)}")
            return False

    def test_visit_creation(self):
        """Test visit creation"""
        if not self.test_patient_id:
            print("❌ Visit Creation - No patient ID available")
            return False
            
        visit_data = {
            "patient": self.test_patient_id,
            "visit_type": "routine",
            "visit_date": date.today().isoformat(),
            "chief_complaint": "Follow-up visit",
            "assessment": "Patient doing well",
            "plan": "Continue current medications"
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/v1/visits/",
                json=visit_data,
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 201:
                data = response.json()
                self.test_visit_id = data.get('id')
                self.log_test("Visit Creation", "PASS")
                return True
            else:
                self.log_test("Visit Creation", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Visit Creation - Error: {str(e)}")
            return False

    def test_visit_list(self):
        """Test visit list endpoint"""
        try:
            response = self.session.get(
                f"{BASE_URL}/api/v1/visits/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("Visit List", "PASS")
                return True
            else:
                self.log_test("Visit List", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Visit List - Error: {str(e)}")
            return False

    def test_oasis_assessment_creation(self):
        """Test OASIS assessment creation"""
        if not self.test_patient_id:
            print("❌ OASIS Assessment Creation - No patient ID available")
            return False
            
        assessment_data = {
            "patient": self.test_patient_id,
            "assessment_type": "SOC",
            "assessment_date": date.today().isoformat(),
            "primary_diagnosis": "Diabetes with complications",
            "grooming": 1,
            "dressing_upper": 1,
            "dressing_lower": 2,
            "bathing": 2,
            "toileting": 1,
            "transferring": 1,
            "ambulation": 2,
            "feeding": 0
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/v1/oasis/submit/",
                json=assessment_data,
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 201:
                data = response.json()
                self.test_assessment_id = data.get('assessment', {}).get('id')
                self.log_test("OASIS Assessment Creation", "PASS")
                return True
            else:
                self.log_test("OASIS Assessment Creation", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ OASIS Assessment Creation - Error: {str(e)}")
            return False

    def test_oasis_templates(self):
        """Test OASIS templates endpoint"""
        try:
            response = self.session.get(
                f"{BASE_URL}/api/v1/oasis/templates/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("OASIS Templates", "PASS")
                return True
            else:
                self.log_test("OASIS Templates", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ OASIS Templates - Error: {str(e)}")
            return False

    def test_communication_threads(self):
        """Test communication threads endpoint"""
        try:
            response = self.session.get(
                f"{BASE_URL}/api/v1/communication/threads/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("Communication Threads", "PASS")
                return True
            else:
                self.log_test("Communication Threads", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Communication Threads - Error: {str(e)}")
            return False

    def test_files_upload(self):
        """Test files upload endpoint"""
        try:
            response = self.session.post(
                f"{BASE_URL}/api/v1/files/upload/",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            # This will likely fail due to missing file, but we're testing the endpoint accessibility
            if response.status_code in [400, 200, 201]:  # Bad request is expected without file
                self.log_test("Files Upload Endpoint", "PASS")
                return True
            else:
                self.log_test("Files Upload Endpoint", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Files Upload Endpoint - Error: {str(e)}")
            return False

    def test_patient_search(self):
        """Test patient search endpoint"""
        try:
            response = self.session.get(
                f"{BASE_URL}/api/v1/patients/search/?q=Jane",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("Patient Search", "PASS")
                return True
            else:
                self.log_test("Patient Search", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Patient Search - Error: {str(e)}")
            return False

    def test_roles_and_permissions(self):
        """Test roles and permissions endpoints"""
        try:
            # Test roles
            response = self.session.get(
                f"{BASE_URL}/api/v1/auth/roles/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("User Roles", "PASS")
            else:
                self.log_test("User Roles", "FAIL", response)
                return False
            
            # Test permissions
            response = self.session.get(
                f"{BASE_URL}/api/v1/auth/permissions/",
                headers=self.get_auth_headers()
            )
            
            if response.status_code == 200:
                self.log_test("User Permissions", "PASS")
                return True
            else:
                self.log_test("User Permissions", "FAIL", response)
                return False
        except Exception as e:
            print(f"❌ Roles and Permissions - Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting API Tests...\n")
        print("=" * 50)
        
        # Test basic endpoints (no auth required)
        print("📋 Testing Basic Endpoints:")
        self.test_homepage()
        self.test_health_endpoint()
        
        # Test authentication
        print("\n🔐 Testing Authentication:")
        if not self.test_user_login():
            print("❌ Login failed, trying registration...")
            if not self.test_user_registration():
                print("❌ Cannot proceed without authentication")
                return
        
        self.test_user_profile()
        self.test_token_refresh()
        self.test_roles_and_permissions()
        
        # Test patient management
        print("\n👥 Testing Patient Management:")
        self.test_patient_creation()
        self.test_patient_list()
        self.test_patient_detail()
        self.test_patient_search()
        
        # Test visit management
        print("\n🏠 Testing Visit Management:")
        self.test_visit_creation()
        self.test_visit_list()
        
        # Test OASIS
        print("\n📋 Testing OASIS Assessment:")
        self.test_oasis_assessment_creation()
        self.test_oasis_templates()
        
        # Test communication
        print("\n💬 Testing Communication:")
        self.test_communication_threads()
        
        # Test file management
        print("\n📁 Testing File Management:")
        self.test_files_upload()
        
        print("\n" + "=" * 50)
        print("🎉 API Testing Complete!")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
