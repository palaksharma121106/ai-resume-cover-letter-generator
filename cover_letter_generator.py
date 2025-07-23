import json
import os
from google import genai
from google.genai import types

class CoverLetterGenerator:
    def __init__(self):
        # Using Google Gemini AI which offers better free tier options
        # Note that the newest Gemini model series is "gemini-2.5-flash" or gemini-2.5-pro"
        # do not change this unless explicitly requested by the user
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY environment variable is required. Get your free key at https://makersuite.google.com/app/apikey")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    def generate_cover_letter(self, user_data, job_info):
        """Generate a personalized cover letter based on user data and job information"""
        try:
            # Extract relevant information
            personal_info = user_data['personal_info']
            work_experience = user_data['work_experience']
            skills = user_data['skills']
            education = user_data['education']
            
            # Prepare context for AI
            context = self._prepare_context(user_data, job_info)
            
            # Generate cover letter
            cover_letter = self._generate_cover_letter_content(context, job_info)
            
            return cover_letter
            
        except Exception as e:
            raise Exception(f"Failed to generate cover letter: {str(e)}")
    
    def _prepare_context(self, user_data, job_info):
        """Prepare context for AI generation"""
        # Extract most relevant work experience (last 2-3 positions)
        relevant_experience = user_data['work_experience'][:3]
        
        # Extract technical skills
        technical_skills = [skill['name'] for skill in user_data['skills'] if skill['category'] == 'Technical']
        
        # Extract latest education
        latest_education = user_data['education'][0] if user_data['education'] else None
        
        context = {
            'personal_info': user_data['personal_info'],
            'relevant_experience': relevant_experience,
            'technical_skills': technical_skills,
            'latest_education': latest_education,
            'job_info': job_info
        }
        
        return context
    
    def _generate_cover_letter_content(self, context, job_info):
        """Generate the actual cover letter content using AI"""
        try:
            # Determine tone instructions
            tone_instructions = self._get_tone_instructions(job_info['tone'])
            
            prompt = f"""
            Write a professional cover letter based on the following information:
            
            CANDIDATE INFORMATION:
            Name: {context['personal_info']['first_name']} {context['personal_info']['last_name']}
            Email: {context['personal_info']['email']}
            Location: {context['personal_info']['location']}
            
            WORK EXPERIENCE:
            {json.dumps(context['relevant_experience'])}
            
            TECHNICAL SKILLS:
            {', '.join(context['technical_skills'])}
            
            EDUCATION:
            {json.dumps(context['latest_education'])}
            
            JOB INFORMATION:
            Company: {job_info['company_name']}
            Position: {job_info['job_title']}
            Hiring Manager: {job_info.get('hiring_manager', 'Hiring Manager')}
            Company Info: {job_info.get('company_info', '')}
            Job Description: {job_info['job_description']}
            
            TONE: {tone_instructions}
            
            REQUIREMENTS:
            1. Write a complete, professional cover letter
            2. Address it to the hiring manager or company
            3. Include proper formatting with date and addresses
            4. Write 3-4 paragraphs:
               - Opening: Express interest and briefly state qualifications
               - Body 1-2: Highlight relevant experience and skills that match the job
               - Closing: Express enthusiasm and next steps
            5. Match skills and experience to the job requirements
            6. Use specific examples from work experience
            7. Keep it to 250-400 words
            8. Make it ATS-friendly
            9. Include proper salutation and closing
            
            Generate the complete cover letter text with proper formatting.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ]
            )
            
            return response.text.strip() if response.text else "Cover letter could not be generated."
            
        except Exception as e:
            raise Exception(f"Failed to generate cover letter content: {str(e)}")
    
    def _get_tone_instructions(self, tone):
        """Get tone-specific instructions for the AI"""
        tone_map = {
            'Professional': 'Use a formal, professional tone. Be respectful and straightforward.',
            'Enthusiastic': 'Show genuine excitement about the role and company. Use energetic but professional language.',
            'Conservative': 'Use very formal language. Be traditional and respectful in approach.',
            'Creative': 'Show personality while remaining professional. Use engaging language that demonstrates creativity.'
        }
        
        return tone_map.get(tone, tone_map['Professional'])
    
    def customize_for_industry(self, cover_letter, industry):
        """Customize cover letter for specific industry"""
        try:
            prompt = f"""
            Customize this cover letter for the {industry} industry. 
            Adjust language, terminology, and emphasis to better fit industry expectations.
            
            Original Cover Letter:
            {cover_letter}
            
            Industry: {industry}
            
            Make appropriate adjustments while keeping the core content and structure.
            Return the customized cover letter.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ]
            )
            
            return response.text.strip() if response.text else cover_letter
            
        except Exception as e:
            return cover_letter  # Return original if customization fails
    
    def analyze_job_match(self, user_data, job_description):
        """Analyze how well the candidate matches the job requirements"""
        try:
            user_skills = [skill['name'] for skill in user_data['skills']]
            user_experience = [exp['description'] for exp in user_data['work_experience']]
            
            prompt = f"""
            Analyze the match between this candidate and job requirements.
            
            CANDIDATE SKILLS: {', '.join(user_skills)}
            CANDIDATE EXPERIENCE: {' '.join(user_experience)}
            
            JOB DESCRIPTION: {job_description}
            
            Provide analysis in JSON format:
            {{
                "match_percentage": number_between_0_and_100,
                "matching_skills": ["skill1", "skill2"],
                "missing_skills": ["skill1", "skill2"],
                "strengths": ["strength1", "strength2"],
                "recommendations": ["recommendation1", "recommendation2"]
            }}
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            if response.text:
                return json.loads(response.text)
            else:
                return {
                    "match_percentage": 50,
                    "matching_skills": [],
                    "missing_skills": [],
                    "strengths": [],
                    "recommendations": ["Analysis could not be completed."]
                }
            
        except Exception as e:
            return {
                "match_percentage": 50,
                "matching_skills": [],
                "missing_skills": [],
                "strengths": [],
                "recommendations": [f"Analysis failed: {str(e)}"]
            }
