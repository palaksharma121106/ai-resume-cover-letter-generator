import streamlit as st
import json
import os  # Add this line
from datetime import datetime
from resume_generator import ResumeGenerator
from cover_letter_generator import CoverLetterGenerator
from pdf_generator import PDFGenerator
from templates import get_available_templates
from utils import validate_email, validate_phone

# Add your API key here

os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY_HERE'

if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {}
if 'work_experience' not in st.session_state:
    st.session_state.work_experience = []
if 'education' not in st.session_state:
    st.session_state.education = []
if 'skills' not in st.session_state:
    st.session_state.skills = []
if 'generated_resume' not in st.session_state:
    st.session_state.generated_resume = None
if 'generated_cover_letter' not in st.session_state:
    st.session_state.generated_cover_letter = None

def main():
    st.set_page_config(
        page_title="AI Resume & Cover Letter Generator",
        page_icon="📄",
        layout="wide"
    )
    
    # Custom CSS for better UI
    st.markdown("""
    <style>
    /* Remove default Streamlit padding and margins */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    /* Remove extra spacing */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        margin-top: -80px;
    }
    
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
        margin-top: 0;
    }
    
    .creator-credit {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background: rgba(102, 126, 234, 0.1);
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 12px;
        color: #667eea;
        border: 1px solid rgba(102, 126, 234, 0.3);
        z-index: 999;
    }
    
    .section-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 1rem;
        margin-top: 0;
    }
    
    .section-header h2 {
        margin: 0;
        padding: 0;
    }
    
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        margin-top: 0;
    }
    
    /* Reduce form spacing */
    .stForm {
        border: none;
        padding: 0;
    }
    
    /* Compact layout */
    div[data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Remove excessive spacing between elements */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Resume & Cover Letter Generator</h1>
        <p>Create professional resumes and cover letters powered by AI - Perfect for students and professionals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Creator credit
    st.markdown("""
    <div class="creator-credit">
        ✨ Created by Palak
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with progress tracking
    st.sidebar.markdown("""
    <style>
    .sidebar-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .progress-item {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 5px;
        background: #f0f2f6;
    }
    .progress-complete {
        background: #d4edda;
        border-left: 4px solid #28a745;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-header"><h3>📋 Navigation</h3></div>', unsafe_allow_html=True)
    
    # Progress tracking
    progress_items = [
        ("Personal Information", bool(st.session_state.personal_info.get('first_name'))),
        ("Work Experience", len(st.session_state.work_experience) > 0),
        ("Education", len(st.session_state.education) > 0),
        ("Skills", len(st.session_state.skills) > 0),
        ("Resume Generated", bool(st.session_state.generated_resume)),
        ("Cover Letter", bool(st.session_state.generated_cover_letter))
    ]
    
    st.sidebar.markdown("**📊 Progress Tracker:**")
    for item, completed in progress_items:
        status = "✅" if completed else "⏳"
        css_class = "progress-complete" if completed else "progress-item"
        st.sidebar.markdown(f'<div class="{css_class}">{status} {item}</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Personal Information", "Work Experience", "Education", "Skills", "Resume Generator", "Cover Letter Generator", "Document Preview"]
    )
    
    if page == "Personal Information":
        personal_info_page()
    elif page == "Work Experience":
        work_experience_page()
    elif page == "Education":
        education_page()
    elif page == "Skills":
        skills_page()
    elif page == "Resume Generator":
        resume_generator_page()
    elif page == "Cover Letter Generator":
        cover_letter_page()
    elif page == "Document Preview":
        document_preview_page()

def personal_info_page():
    st.markdown('<div class="section-header"><h2>📋 Personal Information</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>💡 Getting Started:</strong> Fill in your basic information below. All fields marked with * are required.
        Perfect for students and professionals at any career stage!
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("personal_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", value=st.session_state.personal_info.get('first_name', ''))
            last_name = st.text_input("Last Name *", value=st.session_state.personal_info.get('last_name', ''))
            email = st.text_input("Email *", value=st.session_state.personal_info.get('email', ''))
            phone = st.text_input("Phone Number *", value=st.session_state.personal_info.get('phone', ''))
        
        with col2:
            linkedin = st.text_input("LinkedIn Profile (Optional)", value=st.session_state.personal_info.get('linkedin', ''), help="e.g., linkedin.com/in/yourname")
            location = st.text_input("Location (City, State) *", value=st.session_state.personal_info.get('location', ''))
            
            # Show optional fields in an expander
            with st.expander("Additional Information (Optional)"):
                github = st.text_input("GitHub Profile", value=st.session_state.personal_info.get('github', ''), help="Only add if relevant to your field")
                website = st.text_input("Personal Website/Portfolio", value=st.session_state.personal_info.get('website', ''))
        
        professional_summary = st.text_area(
            "Professional Summary (Optional - AI will generate if empty)",
            value=st.session_state.personal_info.get('professional_summary', ''),
            height=100
        )
        
        submitted = st.form_submit_button("Save Personal Information")
        
        if submitted:
            # Validation
            errors = []
            if not first_name.strip():
                errors.append("First name is required")
            if not last_name.strip():
                errors.append("Last name is required")
            if not email.strip():
                errors.append("Email is required")
            elif not validate_email(email):
                errors.append("Please enter a valid email address")
            if phone and not validate_phone(phone):
                errors.append("Please enter a valid phone number")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.session_state.personal_info = {
                    'first_name': first_name.strip() if first_name else '',
                    'last_name': last_name.strip() if last_name else '',
                    'email': email.strip() if email else '',
                    'phone': phone.strip() if phone else '',
                    'linkedin': linkedin.strip() if linkedin else '',
                    'github': github.strip() if github else '',
                    'website': website.strip() if website else '',
                    'location': location.strip() if location else '',
                    'professional_summary': professional_summary.strip() if professional_summary else ''
                }
                st.success("Personal information saved successfully!")

def work_experience_page():
    st.markdown('<div class="section-header"><h2>💼 Work Experience</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>🎓 For Students & New Graduates:</strong> Don't have work experience yet? No problem! You can include:
        <br>• Internships (paid or unpaid)
        <br>• Part-time jobs or summer work
        <br>• Volunteer work or community service  
        <br>• Personal projects or freelance work
        <br>• Leadership roles in clubs or organizations
        <br><br>
        <strong>Note:</strong> Work experience is optional - you can generate a resume without it!
    </div>
    """, unsafe_allow_html=True)
    
    # Add new experience
    with st.expander("Add New Work Experience", expanded=False):
        with st.form("work_experience_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                job_title = st.text_input("Job Title")
                company = st.text_input("Company Name")
                start_date = st.date_input("Start Date")
            
            with col2:
                location = st.text_input("Location")
                end_date = st.date_input("End Date (Leave as today if current)")
                current_job = st.checkbox("This is my current position")
            
            job_description = st.text_area(
                "Job Description/Responsibilities (AI will enhance this)",
                height=100,
                help="Describe your key responsibilities and achievements"
            )
            
            submitted = st.form_submit_button("Add Work Experience")
            
            if submitted:
                if job_title and company and job_description:
                    experience = {
                        'job_title': job_title,
                        'company': company,
                        'location': location,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': 'Present' if current_job else end_date.strftime('%Y-%m-%d'),
                        'description': job_description,
                        'current': current_job
                    }
                    st.session_state.work_experience.append(experience)
                    st.success("Work experience added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")
    
    # Display existing experiences
    if st.session_state.work_experience:
        st.subheader("Your Work Experience")
        for i, exp in enumerate(st.session_state.work_experience):
            with st.expander(f"{exp['job_title']} at {exp['company']}", expanded=False):
                st.write(f"**Location:** {exp['location']}")
                st.write(f"**Duration:** {exp['start_date']} to {exp['end_date']}")
                st.write(f"**Description:** {exp['description']}")
                
                if st.button(f"Remove", key=f"remove_exp_{i}"):
                    st.session_state.work_experience.pop(i)
                    st.rerun()

def education_page():
    st.markdown('<div class="section-header"><h2>🎓 Education</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>📚 Education Tips:</strong> Include all relevant education - high school, college, online courses, certifications, or bootcamps. 
        Even if you're currently studying, add your expected graduation date!
    </div>
    """, unsafe_allow_html=True)
    
    # Add new education
    with st.expander("Add New Education", expanded=False):
        with st.form("education_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                degree = st.text_input("Degree")
                school = st.text_input("School/University")
                graduation_date = st.date_input("Graduation Date")
            
            with col2:
                major = st.text_input("Major/Field of Study")
                gpa = st.text_input("GPA (Optional)")
                location = st.text_input("Location")
            
            achievements = st.text_area(
                "Achievements/Honors (Optional)",
                height=80,
                help="List any relevant achievements, honors, or coursework"
            )
            
            submitted = st.form_submit_button("Add Education")
            
            if submitted:
                if degree and school:
                    education = {
                        'degree': degree,
                        'major': major,
                        'school': school,
                        'location': location,
                        'graduation_date': graduation_date.strftime('%Y-%m-%d'),
                        'gpa': gpa,
                        'achievements': achievements
                    }
                    st.session_state.education.append(education)
                    st.success("Education added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in degree and school name")
    
    # Display existing education
    if st.session_state.education:
        st.subheader("Your Education")
        for i, edu in enumerate(st.session_state.education):
            with st.expander(f"{edu['degree']} from {edu['school']}", expanded=False):
                st.write(f"**Major:** {edu['major']}")
                st.write(f"**Location:** {edu['location']}")
                st.write(f"**Graduation:** {edu['graduation_date']}")
                if edu['gpa']:
                    st.write(f"**GPA:** {edu['gpa']}")
                if edu['achievements']:
                    st.write(f"**Achievements:** {edu['achievements']}")
                
                if st.button(f"Remove", key=f"remove_edu_{i}"):
                    st.session_state.education.pop(i)
                    st.rerun()

def skills_page():
    st.markdown('<div class="section-header"><h2>🛠️ Skills</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>💪 Skills Matter:</strong> Include both technical skills (software, programming languages) and soft skills (communication, leadership). 
        Even basic computer skills count for entry-level positions!
    </div>
    """, unsafe_allow_html=True)
    
    # Add skills
    with st.form("skills_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            technical_skills = st.text_area(
                "Technical Skills",
                value=", ".join([s['name'] for s in st.session_state.skills if s['category'] == 'Technical']),
                help="Enter skills separated by commas (e.g., Python, JavaScript, SQL)"
            )
        
        with col2:
            soft_skills = st.text_area(
                "Soft Skills",
                value=", ".join([s['name'] for s in st.session_state.skills if s['category'] == 'Soft']),
                help="Enter skills separated by commas (e.g., Leadership, Communication, Problem Solving)"
            )
        
        languages = st.text_input(
            "Languages",
            value=", ".join([s['name'] for s in st.session_state.skills if s['category'] == 'Language']),
            help="Enter languages separated by commas (e.g., English (Native), Spanish (Fluent))"
        )
        
        certifications = st.text_area(
            "Certifications",
            value=", ".join([s['name'] for s in st.session_state.skills if s['category'] == 'Certification']),
            help="Enter certifications separated by commas"
        )
        
        submitted = st.form_submit_button("Save Skills")
        
        if submitted:
            skills = []
            
            # Process technical skills
            if technical_skills:
                for skill in technical_skills.split(','):
                    skills.append({'name': skill.strip(), 'category': 'Technical'})
            
            # Process soft skills
            if soft_skills:
                for skill in soft_skills.split(','):
                    skills.append({'name': skill.strip(), 'category': 'Soft'})
            
            # Process languages
            if languages:
                for skill in languages.split(','):
                    skills.append({'name': skill.strip(), 'category': 'Language'})
            
            # Process certifications
            if certifications:
                for skill in certifications.split(','):
                    skills.append({'name': skill.strip(), 'category': 'Certification'})
            
            st.session_state.skills = skills
            st.success("Skills saved successfully!")

def resume_generator_page():
    st.markdown('<div class="section-header"><h2>📄 Resume Generator</h2></div>', unsafe_allow_html=True)
    
    # Check if user has entered basic information
    if not st.session_state.personal_info:
        st.warning("Please complete your personal information before generating a resume.")
        return
    
    # Show helpful message for students
    if not st.session_state.work_experience:
        st.markdown("""
        <div class="info-box">
            <strong>🎓 Student-Friendly Resume:</strong> No work experience? Perfect! The AI will create a resume that highlights your:
            <br>• Education and academic achievements
            <br>• Skills and certifications  
            <br>• Personal projects and coursework
            <br>• Leadership and volunteer activities
        </div>
        """, unsafe_allow_html=True)
    
    # Template selection
    templates = get_available_templates()
    selected_template = st.selectbox("Choose Resume Template", list(templates.keys()))
    
    # Template preview
    st.subheader("Template Preview")
    st.markdown(templates[selected_template]['description'])
    
    # Generate resume
    if st.button("Generate Resume with AI"):
        with st.spinner("Generating your resume..."):
            try:
                generator = ResumeGenerator()
                
                user_data = {
                    'personal_info': st.session_state.personal_info,
                    'work_experience': st.session_state.work_experience,
                    'education': st.session_state.education,
                    'skills': st.session_state.skills
                }
                
                resume_content = generator.generate_resume(user_data, selected_template)
                st.session_state.generated_resume = {
                    'content': resume_content,
                    'template': selected_template,
                    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                st.success("Resume generated successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating resume: {str(e)}")
    
    # Display generated resume
    if st.session_state.generated_resume:
        st.subheader("Generated Resume")
        st.markdown("---")
        
        # Display resume content
        content = st.session_state.generated_resume['content']
        
        # Personal Info Section
        if 'personal_summary' in content:
            st.markdown(f"**{content['personal_info']['first_name']} {content['personal_info']['last_name']}**")
            st.markdown(f"*{content['personal_info']['email']} • {content['personal_info']['phone']} • {content['personal_info']['location']}*")
            if content['personal_info'].get('linkedin'):
                st.markdown(f"LinkedIn: {content['personal_info']['linkedin']}")
            st.markdown("---")
            st.markdown("**Professional Summary**")
            st.markdown(content['professional_summary'])
            st.markdown("---")
        
        # Work Experience
        if 'work_experience' in content:
            st.markdown("**Professional Experience**")
            for exp in content['work_experience']:
                st.markdown(f"**{exp['job_title']}** - {exp['company']}")
                st.markdown(f"*{exp['start_date']} to {exp['end_date']} • {exp['location']}*")
                for bullet in exp['enhanced_description']:
                    st.markdown(f"• {bullet}")
                st.markdown("")
            st.markdown("---")
        
        # Education
        if content.get('education'):
            st.markdown("**Education**")
            for edu in content['education']:
                st.markdown(f"**{edu['degree']}** in {edu['major']}")
                st.markdown(f"*{edu['school']} • {edu['graduation_date']}*")
                if edu.get('gpa'):
                    st.markdown(f"GPA: {edu['gpa']}")
                st.markdown("")
            st.markdown("---")
        
        # Skills
        if content.get('skills'):
            st.markdown("**Skills**")
            for category, skills_list in content['skills'].items():
                if skills_list:
                    st.markdown(f"**{category}:** {', '.join(skills_list)}")

def cover_letter_page():
    st.markdown('<div class="section-header"><h2>📝 Cover Letter Generator</h2></div>', unsafe_allow_html=True)
    
    # Check if user has basic information
    if not st.session_state.personal_info:
        st.warning("Please complete your personal information before generating a cover letter.")
        return
    
    st.markdown("""
    <div class="info-box">
        <strong>💼 Cover Letter Magic:</strong> A great cover letter can make up for limited experience! 
        The AI will create a personalized letter that highlights your potential and enthusiasm.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("cover_letter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name")
            job_title = st.text_input("Job Title")
            hiring_manager = st.text_input("Hiring Manager Name (Optional)")
        
        with col2:
            company_info = st.text_area(
                "Company Information (Optional)",
                help="Brief information about the company or why you want to work there"
            )
        
        job_description = st.text_area(
            "Job Description",
            height=150,
            help="Paste the job description or key requirements"
        )
        
        tone = st.selectbox(
            "Cover Letter Tone",
            ["Professional", "Enthusiastic", "Conservative", "Creative"]
        )
        
        submitted = st.form_submit_button("Generate Cover Letter")
        
        if submitted:
            if company_name and job_title and job_description:
                with st.spinner("Generating your cover letter..."):
                    try:
                        generator = CoverLetterGenerator()
                        
                        job_info = {
                            'company_name': company_name,
                            'job_title': job_title,
                            'hiring_manager': hiring_manager,
                            'company_info': company_info,
                            'job_description': job_description,
                            'tone': tone
                        }
                        
                        user_data = {
                            'personal_info': st.session_state.personal_info,
                            'work_experience': st.session_state.work_experience,
                            'education': st.session_state.education,
                            'skills': st.session_state.skills
                        }
                        
                        cover_letter = generator.generate_cover_letter(user_data, job_info)
                        st.session_state.generated_cover_letter = {
                            'content': cover_letter,
                            'job_info': job_info,
                            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        st.success("Cover letter generated successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error generating cover letter: {str(e)}")
            else:
                st.error("Please fill in company name, job title, and job description")
    
    # Display generated cover letter
    if st.session_state.generated_cover_letter:
        st.subheader("Generated Cover Letter")
        st.markdown("---")
        st.markdown(st.session_state.generated_cover_letter['content'])

def document_preview_page():
    st.markdown('<div class="section-header"><h2>📋 Document Preview & Export</h2></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>📄 Ready to Apply:</strong> Download your professional documents as PDFs and start applying to your dream jobs!
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resume")
        if st.session_state.generated_resume:
            st.success("✅ Resume generated")
            if st.button("Download Resume as PDF"):
                try:
                    pdf_gen = PDFGenerator()
                    pdf_bytes = pdf_gen.generate_resume_pdf(st.session_state.generated_resume)
                    
                    st.download_button(
                        label="📄 Download Resume PDF",
                        data=pdf_bytes,
                        file_name=f"resume_{st.session_state.personal_info.get('first_name', 'user')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
        else:
            st.info("No resume generated yet")
    
    with col2:
        st.subheader("Cover Letter")
        if st.session_state.generated_cover_letter:
            st.success("✅ Cover letter generated")
            if st.button("Download Cover Letter as PDF"):
                try:
                    pdf_gen = PDFGenerator()
                    pdf_bytes = pdf_gen.generate_cover_letter_pdf(st.session_state.generated_cover_letter)
                    
                    st.download_button(
                        label="📝 Download Cover Letter PDF",
                        data=pdf_bytes,
                        file_name=f"cover_letter_{st.session_state.personal_info.get('first_name', 'user')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
        else:
            st.info("No cover letter generated yet")

if __name__ == "__main__":
    main()
