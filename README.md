# ai-resume-cover-letter-generator
A Streamlit-based project that generates resumes and cover letters using Google Gemini API (Generative AI).
# AI Resume & Cover Letter Generator

A Streamlit-based web application that uses Google Gemini AI to generate professional resumes and cover letters. Perfect for students and professionals who want to create high-quality job application documents quickly and easily.

## 🌟 Features

- **AI-Powered Content Generation**: Uses Google Gemini AI to create professional, compelling content
- **Student-Friendly**: Works even without work experience - perfect for students  
- **Multiple Templates**: 5 professional resume templates for different industries
- **Cover Letter Generator**: Creates personalized cover letters for specific job applications
- **PDF Download**: Instant PDF generation ready for job applications
- **Free to Use**: No credit card required, completely free with Google Gemini
- **User-Friendly Interface**: Simple, intuitive design with step-by-step guidance

## 📋 How It Works

1. **Enter Personal Information**: Add your contact details and basic info
2. **Add Education**: Include your academic background and achievements  
3. **Add Work Experience** (Optional): Perfect for students - work experience is optional
4. **List Your Skills**: Organize skills by category (technical, soft skills, etc.)
5. **Generate Resume**: AI creates professional content based on your input
6. **Create Cover Letters**: Generate personalized cover letters for job applications 
7. **Download PDF**: Get professional documents ready for job applications

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Service**: Google Gemini AI (Free tier)
- **PDF Generation**: ReportLab  
- **Language**: Python 3.11+
- **Deployment**: Replit (or any Python hosting service)

## 📦 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Google Gemini API key (free from Google AI Studio)

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/palaksharma121106/ai-resume-cover-letter-generator.git
cd ai-resume-cover-letter-generator


2. Install dependencies:
```bash
pip install streamlit google-genai reportlab

3. Set up your Google Gemini API key:

- Get a free API key from Google AI Studio
- Open app.py file
- Find line 13: os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY_HERE'
- Replace YOUR_API_KEY_HERE with your actual API key
4. Run the application:
streamlit run app.py --server.port 5000
5. Open your browser and go to http://localhost:5000
🔧 Configuration
The application uses Google Gemini AI, which offers a generous free tier. To set up:

  1. Visit Google AI Studio
 2. Create a free account (no credit card needed)
3. Generate an API key
4. Update the API key in app.py:
os.environ['GEMINI_API_KEY'] = 'your-actual-api-key'

ai-resume-cover-letter-generator/
├── app.py                          # Main Streamlit application
├── resume_generator.py             # AI resume generation logic
├── cover_letter_generator.py       # AI cover letter generation logic
├── pdf_generator.py                # PDF creation and formatting
├── templates.py                    # Resume template definitions
├── utils.py                        # Validation utilities
├── README.md                       # This file
└── LICENSE                         # MIT License

🎯 Use Cases
For Students
Create your first professional resume
Generate compelling content even without work experience
Learn professional resume writing standards
Free alternative to expensive resume services
For Professionals
Quick resume updates for job applications
Generate tailored cover letters for specific positions
Maintain consistent professional formatting
Save time on document formatting
🏆 Templates Available
Professional: Traditional corporate-friendly layout
Modern: Contemporary design for tech and creative industries
Executive: Sophisticated format for senior-level positions
Technical: Structured layout optimized for technical roles
Creative: Balanced creative design maintaining ATS compliance
🤖 AI Integration
This project demonstrates practical application of Generative AI:

Natural Language Processing: Understands and enhances user input
Content Generation: Creates professional, contextually appropriate content
Personalization: Adapts content to individual backgrounds and career levels
Quality Assurance: Maintains professional standards and ATS compatibility
📈 Benefits
Accessibility: Makes professional resume creation available to everyone
Quality: AI ensures consistent, professional writing standards
Efficiency: Reduces resume creation time from hours to minutes
Customization: Easy to adapt for different job applications
Learning: Helps users understand professional writing standards
🔮 Future Enhancements
Multi-language support
Additional resume templates
LinkedIn profile optimization
Interview question generation
Skills gap analysis
Job matching integration
👤 About
Creator: Palak
Purpose: Academic project demonstrating practical AI application
Goal: Democratize access to professional resume and cover letter writing

📄 License
This project is created for educational purposes as part of an academic submission.

🤝 Contributing
This is an academic project, but suggestions and feedback are welcome!

Note: This application requires an internet connection for AI functionality. All user data is processed in-session and not permanently stored, ensuring privacy and security.
