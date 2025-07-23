import re
import streamlit as st
from datetime import datetime, date
import json

def validate_email(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Remove all non-digit characters
    digits_only = re.sub(r'[^\d]', '', phone)
    
    # Check if it's a valid US phone number (10 digits)
    if len(digits_only) == 10:
        return True
    elif len(digits_only) == 11 and digits_only.startswith('1'):
        return True
    
    # Check for international formats (7-15 digits)
    if 7 <= len(digits_only) <= 15:
        return True
    
    return False

def format_phone(phone):
    """Format phone number for display"""
    digits_only = re.sub(r'[^\d]', '', phone)
    
    if len(digits_only) == 10:
        return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
    elif len(digits_only) == 11 and digits_only.startswith('1'):
        return f"+1 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"
    
    return phone  # Return original if can't format

def validate_url(url):
    """Validate URL format"""
    if not url:
        return True  # Empty URL is valid (optional field)
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return re.match(pattern, url) is not None

def format_date_range(start_date, end_date, current=False):
    """Format date range for display"""
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str) and end_date != 'Present':
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    start_formatted = start_date.strftime('%B %Y')
    
    if current or end_date == 'Present':
        return f"{start_formatted} - Present"
    else:
        end_formatted = end_date.strftime('%B %Y')
        return f"{start_formatted} - {end_formatted}"

def calculate_experience_duration(start_date, end_date=None, current=False):
    """Calculate duration of experience in months"""
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    
    if current or end_date == 'Present':
        end_date = date.today()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Calculate difference in months
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''}"
    else:
        years = months // 12
        remaining_months = months % 12
        
        if remaining_months == 0:
            return f"{years} year{'s' if years != 1 else ''}"
        else:
            return f"{years} year{'s' if years != 1 else ''}, {remaining_months} month{'s' if remaining_months != 1 else ''}"

def sanitize_filename(filename):
    """Sanitize filename for safe file system usage"""
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)  # Replace spaces with underscores
    sanitized = sanitized.strip('.')  # Remove leading/trailing dots
    
    # Ensure filename isn't too long
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    return sanitized

def export_user_data():
    """Export all user data as JSON"""
    user_data = {
        'personal_info': st.session_state.get('personal_info', {}),
        'work_experience': st.session_state.get('work_experience', []),
        'education': st.session_state.get('education', []),
        'skills': st.session_state.get('skills', []),
        'export_date': datetime.now().isoformat()
    }
    
    return json.dumps(user_data, indent=2)

def import_user_data(json_data):
    """Import user data from JSON"""
    try:
        data = json.loads(json_data)
        
        # Validate required fields
        required_fields = ['personal_info', 'work_experience', 'education', 'skills']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Update session state
        st.session_state.personal_info = data['personal_info']
        st.session_state.work_experience = data['work_experience']
        st.session_state.education = data['education']
        st.session_state.skills = data['skills']
        
        return True, "Data imported successfully"
        
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, f"Import failed: {str(e)}"

def get_experience_level(work_experience):
    """Determine experience level based on work history"""
    if not work_experience:
        return "entry_level"
    
    total_months = 0
    for exp in work_experience:
        start_date = datetime.strptime(exp['start_date'], '%Y-%m-%d').date()
        
        if exp.get('current') or exp['end_date'] == 'Present':
            end_date = date.today()
        else:
            end_date = datetime.strptime(exp['end_date'], '%Y-%m-%d').date()
        
        months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        total_months += months
    
    years = total_months / 12
    
    if years < 2:
        return "entry_level"
    elif years < 5:
        return "mid_level"
    elif years < 10:
        return "senior_level"
    else:
        return "executive"

def extract_keywords_from_job_description(job_description):
    """Extract potential keywords from job description for ATS optimization"""
    import re
    from collections import Counter
    
    # Common stop words to ignore
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Extract words and phrases
    words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())
    
    # Filter out stop words
    filtered_words = [word for word in words if word not in stop_words]
    
    # Count frequency
    word_counts = Counter(filtered_words)
    
    # Get most common words (potential keywords)
    keywords = [word for word, count in word_counts.most_common(20) if count > 1]
    
    return keywords

def check_ats_compatibility(content):
    """Check content for ATS compatibility issues"""
    issues = []
    recommendations = []
    
    # Check for common ATS issues
    text_content = str(content)
    
    # Check for special characters that might cause issues
    problematic_chars = ['•', '→', '★', '◆', '▪', '▫']
    for char in problematic_chars:
        if char in text_content:
            issues.append(f"Contains special character '{char}' that might not be ATS-friendly")
            recommendations.append(f"Replace '{char}' with standard bullet points or dashes")
    
    # Check for very long lines
    lines = text_content.split('\n')
    long_lines = [i for i, line in enumerate(lines) if len(line) > 100]
    if long_lines:
        issues.append("Some lines are very long and might not parse well")
        recommendations.append("Break long sentences into shorter, more digestible bullet points")
    
    # Check for proper section headers
    required_headers = ['experience', 'education', 'skills']
    text_lower = text_content.lower()
    missing_headers = [header for header in required_headers if header not in text_lower]
    
    if missing_headers:
        issues.append(f"Missing standard section headers: {', '.join(missing_headers)}")
        recommendations.append("Include standard section headers for better ATS parsing")
    
    return {
        'issues': issues,
        'recommendations': recommendations,
        'ats_score': max(0, 100 - len(issues) * 10)  # Simple scoring system
    }

def generate_filename_suggestions(personal_info, document_type):
    """Generate filename suggestions for downloads"""
    first_name = personal_info.get('first_name', 'user').lower()
    last_name = personal_info.get('last_name', '').lower()
    current_date = datetime.now().strftime('%Y%m%d')
    
    suggestions = [
        f"{first_name}_{last_name}_{document_type}_{current_date}",
        f"{first_name}{last_name}_{document_type}",
        f"{last_name}_{first_name}_{document_type}",
        f"{document_type}_{first_name}_{last_name}",
    ]
    
    # Clean up suggestions
    cleaned_suggestions = []
    for suggestion in suggestions:
        cleaned = sanitize_filename(suggestion)
        if cleaned and len(cleaned) > 3:  # Ensure meaningful filename
            cleaned_suggestions.append(cleaned)
    
    return cleaned_suggestions[:3]  # Return top 3 suggestions

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present and not empty"""
    missing_fields = []
    empty_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            empty_fields.append(field)
    
    return {
        'valid': len(missing_fields) == 0 and len(empty_fields) == 0,
        'missing_fields': missing_fields,
        'empty_fields': empty_fields
    }

def format_currency(amount, currency='USD'):
    """Format currency amounts for display"""
    if currency == 'USD':
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def mask_sensitive_data(data, fields_to_mask):
    """Mask sensitive data for logging or display"""
    masked_data = data.copy()
    
    for field in fields_to_mask:
        if field in masked_data and masked_data[field]:
            if field == 'email':
                # Mask email: j***@***.com
                email = masked_data[field]
                if '@' in email:
                    local, domain = email.split('@', 1)
                    masked_local = local[0] + '*' * (len(local) - 1)
                    masked_domain = '*' * len(domain.split('.')[0]) + '.' + domain.split('.')[-1]
                    masked_data[field] = f"{masked_local}@{masked_domain}"
            elif field == 'phone':
                # Mask phone: (***) ***-1234
                phone = masked_data[field]
                if len(phone) >= 4:
                    masked_data[field] = '*' * (len(phone) - 4) + phone[-4:]
            else:
                # General masking
                value = str(masked_data[field])
                if len(value) > 4:
                    masked_data[field] = value[:2] + '*' * (len(value) - 4) + value[-2:]
                else:
                    masked_data[field] = '*' * len(value)
    
    return masked_data
