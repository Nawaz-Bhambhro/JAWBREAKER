import pytesseract
from PIL import Image
import json
import re
from typing import Dict, Any


class OCRProcessor:
    """Handle OCR processing of uploaded files"""
    
    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            return f"OCR Error: {str(e)}"
    
    @staticmethod
    def extract_structured_data(text: str, data_type: str) -> Dict[str, Any]:
        """Extract structured data based on document type"""
        
        if data_type == 'lab_values':
            return OCRProcessor._extract_lab_values(text)
        elif data_type == 'vital_signs':
            return OCRProcessor._extract_vital_signs(text)
        elif data_type == 'medication_list':
            return OCRProcessor._extract_medications(text)
        elif data_type == 'insurance_info':
            return OCRProcessor._extract_insurance_info(text)
        else:
            return OCRProcessor._extract_general_info(text)
    
    @staticmethod
    def _extract_lab_values(text: str) -> Dict[str, Any]:
        """Extract lab values from text"""
        lab_data = {}
        
        # Common lab value patterns
        patterns = {
            'glucose': r'glucose[:\s]*(\d+\.?\d*)',
            'hemoglobin': r'h[bg|emoglobin][:\s]*(\d+\.?\d*)',
            'cholesterol': r'cholesterol[:\s]*(\d+\.?\d*)',
            'blood_pressure': r'bp[:\s]*(\d+/\d+)',
            'heart_rate': r'hr[:\s]*(\d+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                lab_data[key] = match.group(1)
        
        return lab_data
    
    @staticmethod
    def _extract_vital_signs(text: str) -> Dict[str, Any]:
        """Extract vital signs from text"""
        vitals = {}
        
        patterns = {
            'blood_pressure': r'bp[:\s]*(\d+/\d+)',
            'heart_rate': r'hr[:\s]*(\d+)',
            'temperature': r'temp[:\s]*(\d+\.?\d*)',
            'respiratory_rate': r'rr[:\s]*(\d+)',
            'oxygen_saturation': r'o2[:\s]*(\d+)%?',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                vitals[key] = match.group(1)
        
        return vitals
    
    @staticmethod
    def _extract_medications(text: str) -> Dict[str, Any]:
        """Extract medication information from text"""
        medications = []
        
        # Simple medication pattern (this would be more sophisticated in production)
        med_pattern = r'([A-Za-z]+)\s+(\d+(?:\.\d+)?)\s*(mg|mcg|g)\s*(?:(daily|bid|tid|qid))?'
        matches = re.finditer(med_pattern, text, re.IGNORECASE)
        
        for match in matches:
            medication = {
                'name': match.group(1),
                'dose': match.group(2),
                'unit': match.group(3),
                'frequency': match.group(4) if match.group(4) else 'as directed'
            }
            medications.append(medication)
        
        return {'medications': medications}
    
    @staticmethod
    def _extract_insurance_info(text: str) -> Dict[str, Any]:
        """Extract insurance information from text"""
        insurance_data = {}
        
        patterns = {
            'policy_number': r'policy[:\s#]*(\w+)',
            'group_number': r'group[:\s#]*(\w+)',
            'member_id': r'member[:\s#]*(\w+)',
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                insurance_data[key] = match.group(1)
        
        return insurance_data
    
    @staticmethod
    def _extract_general_info(text: str) -> Dict[str, Any]:
        """Extract general structured information"""
        return {
            'word_count': len(text.split()),
            'contains_numbers': bool(re.search(r'\d+', text)),
            'contains_dates': bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)),
            'summary': text[:200] + '...' if len(text) > 200 else text
        }
