"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse

def home(request):
    """API Documentation Homepage"""
    return HttpResponse("""
    <html>
    <head><title>Healthcare API Documentation</title></head>
    <body>
    <h1>🏥 Healthcare Management API</h1>
    <h2>Available Endpoints:</h2>
    
    <h3>🔐 Authentication:</h3>
    <ul>
        <li><strong>POST</strong> /api/v1/auth/login/ - User Login</li>
        <li><strong>POST</strong> /api/v1/auth/register/ - User Registration</li>
        <li><strong>GET</strong> /api/v1/auth/profile/ - User Profile</li>
    </ul>
    
    <h3>👥 Patient Management:</h3>
    <ul>
        <li><strong>GET/POST</strong> /api/v1/patients/ - List/Create Patients</li>
        <li><strong>GET/PUT/DELETE</strong> /api/v1/patients/{id}/ - Patient Details</li>
        <li><strong>GET</strong> /api/v1/patients/search/ - Search Patients</li>
    </ul>
    
    <h3>🏠 Visit Management:</h3>
    <ul>
        <li><strong>GET/POST</strong> /api/v1/visits/ - List/Create Visits</li>
        <li><strong>POST</strong> /api/v1/visits/{id}/notes/ - Add Visit Notes</li>
        <li><strong>GET</strong> /api/v1/visits/{id}/summary/ - AI Summary</li>
    </ul>
    
    <h3>📁 File Management & OCR:</h3>
    <ul>
        <li><strong>POST</strong> /api/v1/files/upload/ - Upload Files</li>
        <li><strong>POST</strong> /api/v1/files/ocr/ - Process OCR</li>
    </ul>
    
    <h3>📋 OASIS & Forms:</h3>
    <ul>
        <li><strong>POST</strong> /api/v1/oasis/submit/ - Submit OASIS</li>
        <li><strong>GET</strong> /api/v1/oasis/template/{discipline}/ - Get Templates</li>
    </ul>
    
    <h3>💬 Communication:</h3>
    <ul>
        <li><strong>POST</strong> /api/v1/communication/send-note/ - Send Messages</li>
        <li><strong>GET</strong> /api/v1/communication/threads/{patient_id}/ - Patient Communication</li>
    </ul>
    
    <h3>🔧 System:</h3>
    <ul>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/health/">Health Check</a></li>
    </ul>
    </body>
    </html>
    """)

urlpatterns = [
    # Homepage with API documentation
    path('', home, name='home'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API v1 endpoints
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/patients/', include('patients.urls')),
    path('api/v1/visits/', include('visits.urls')),
    path('api/v1/oasis/', include('oasis.urls')),
    path('api/v1/files/', include('files.urls')),
    path('api/v1/communication/', include('communication.urls')),
    
    # Health check endpoint
    path('health/', lambda request: JsonResponse({
        'status': 'healthy', 
        'version': '1.0',
        'services': {
            'authentication': 'active',
            'patients': 'active',
            'visits': 'active',
            'oasis': 'active',
            'files': 'active',
            'communication': 'active'
        }
    })),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
