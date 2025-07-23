import json
import os
from google import genai
from google.genai import types

class ResumeGenerator:
    def __init__(self):
        # Using Google Gemini AI which offers better free tier options
        # Note that the newest Gemini model series is "gemini-2.5-flash" or gemini-2.5-pro"
        # do not change this unless explicitly requested by the user
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY environment variable is required. Get your free key at https://makersuite.google.com/app/apikey")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
    
    def generate_resume(self, user_data, template_name):
        """Generate a complete resume using AI"""
        try:
            # Generate professional summary if not provided
            if not user_data['personal_info'].get('professional_summary'):
                professional_summary = self._generate_professional_summary(user_data)
            else:
                professional_summary = user_data['personal_info']['professional_summary']
            
            # Enhance work experience descriptions
            enhanced_work_experience = self._enhance_work_experience(user_data['work_experience'])
            
            # Organize skills by category
            organized_skills = self._organize_skills(user_data['skills'])
            
            # Create complete resume structure
            resume_content = {
                'personal_info': user_data['personal_info'],
                'professional_summary': professional_summary,
                'work_experience': enhanced_work_experience,
                'education': user_data['education'],
                'skills': organized_skills,
                'template': template_name
            }
            
            return resume_content
            
        except Exception as e:
            raise Exception(f"Failed to generate resume: {str(e)}")
    
    def _generate_professional_summary(self, user_data):
        """Generate a professional summary based on user's experience and skills"""
        try:
            # Prepare context for AI
            has_work_experience = bool(user_data.get('work_experience'))
            context = {
                'work_experience': user_data.get('work_experience', []),
                'education': user_data.get('education', []),
                'skills': [skill['name'] for skill in user_data.get('skills', []) if skill['category'] == 'Technical']
            }
            
            # Different prompts based on experience level
            if has_work_experience:
                experience_context = "professional work experience"
                summary_focus = "years of experience and professional accomplishments"
            else:
                experience_context = "education, skills, and academic/personal projects"
                summary_focus = "educational background, technical skills, and potential"
            
            prompt = f"""
            Based on the following information, write a compelling professional summary for a resume. 
            The candidate has {experience_context}. Focus on {summary_focus}.
            The summary should be 3-4 sentences, highlight key strengths, and be tailored to the candidate's background.
            
            Work Experience: {json.dumps(context['work_experience']) if has_work_experience else "No formal work experience yet"}
            Education: {json.dumps(context['education'])}
            Key Skills: {', '.join(context['skills'])}
            
            Write a professional summary that:
            {"1. Highlights years of experience and key accomplishments" if has_work_experience else "1. Starts with educational level or recent graduate status"}
            2. Highlights 2-3 key areas of expertise or learning
            3. Mentions relevant skills and potential contributions
            4. Ends with career goals or value proposition
            {"5. Keep it professional and achievement-focused" if has_work_experience else "5. Focus on potential, enthusiasm, and readiness to contribute"}
            
            Respond with just the professional summary text, no additional formatting.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ]
            )
            
            return response.text.strip() if response.text else "Professional summary could not be generated."
            
        except Exception as e:
            raise Exception(f"Failed to generate professional summary: {str(e)}")
    
    def _enhance_work_experience(self, work_experience):
        """Enhance work experience descriptions with AI"""
        enhanced_experiences = []
        
        # Handle empty work experience
        if not work_experience:
            return enhanced_experiences
        
        for exp in work_experience:
            try:
                prompt = f"""
                Transform the following job description into 3-5 professional bullet points for a resume. 
                Use action verbs, quantify achievements where possible, and focus on impact and results.
                
                Job Title: {exp['job_title']}
                Company: {exp['company']}
                Description: {exp['description']}
                
                Guidelines:
                1. Start each bullet point with a strong action verb
                2. Focus on achievements and results, not just responsibilities
                3. Use specific numbers, percentages, or metrics where applicable
                4. Keep each bullet point to 1-2 lines
                5. Make it ATS-friendly
                
                Return the response as a JSON object with this format:
                {{"bullet_points": ["bullet point 1", "bullet point 2", "bullet point 3"]}}
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
                    result = json.loads(response.text)
                    enhanced_description = result.get('bullet_points', [exp['description']])
                else:
                    enhanced_description = [exp['description']]
                
                enhanced_exp = exp.copy()
                enhanced_exp['enhanced_description'] = enhanced_description
                enhanced_experiences.append(enhanced_exp)
                
            except Exception as e:
                # Fallback to original description if AI enhancement fails
                enhanced_exp = exp.copy()
                enhanced_exp['enhanced_description'] = [exp['description']]
                enhanced_experiences.append(enhanced_exp)
        
        return enhanced_experiences
    
    def _organize_skills(self, skills):
        """Organize skills by category"""
        organized = {
            'Technical Skills': [],
            'Soft Skills': [],
            'Languages': [],
            'Certifications': []
        }
        
        category_mapping = {
            'Technical': 'Technical Skills',
            'Soft': 'Soft Skills',
            'Language': 'Languages',
            'Certification': 'Certifications'
        }
        
        for skill in skills:
            category = category_mapping.get(skill['category'], 'Technical Skills')
            organized[category].append(skill['name'])
        
        # Remove empty categories
        return {k: v for k, v in organized.items() if v}
    
    def suggest_improvements(self, resume_content, target_job_description=""):
        """Suggest improvements for the resume based on job description"""
        try:
            prompt = f"""
            Analyze the following resume and provide 3-5 specific improvement suggestions.
            
            Resume Content: {json.dumps(resume_content)}
            Target Job Description: {target_job_description}
            
            Provide suggestions for:
            1. Missing keywords for ATS optimization
            2. Areas where more quantifiable results could be added
            3. Skills or experiences that should be emphasized
            4. Overall structure or formatting improvements
            
            Return suggestions as a JSON object:
            {{"suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]}}
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
                result = json.loads(response.text)
                return result.get('suggestions', [])
            else:
                return []
            
        except Exception as e:
            return [f"Unable to generate suggestions: {str(e)}"]
