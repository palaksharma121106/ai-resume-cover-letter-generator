def get_available_templates():
    """Return available resume templates with descriptions"""
    templates = {
        "Professional": {
            "name": "Professional",
            "description": "Clean, traditional layout perfect for corporate environments and established industries. Features clear section headers, consistent formatting, and ATS-friendly structure.",
            "style": "traditional",
            "best_for": ["Corporate", "Finance", "Legal", "Healthcare", "Government"]
        },
        
        "Modern": {
            "name": "Modern",
            "description": "Contemporary design with subtle visual elements. Balances professionalism with modern aesthetics. Great for tech, marketing, and creative industries.",
            "style": "contemporary",
            "best_for": ["Technology", "Marketing", "Design", "Startups", "Media"]
        },
        
        "Executive": {
            "name": "Executive",
            "description": "Sophisticated layout designed for senior-level positions. Emphasizes leadership experience and strategic accomplishments with elegant formatting.",
            "style": "executive",
            "best_for": ["Executive", "Management", "Consulting", "Investment", "Leadership roles"]
        },
        
        "Technical": {
            "name": "Technical",
            "description": "Structured format optimized for technical roles. Provides clear sections for technical skills, projects, and certifications. Highly scannable for ATS systems.",
            "style": "technical",
            "best_for": ["Software Engineering", "Data Science", "DevOps", "Cybersecurity", "Engineering"]
        },
        
        "Creative": {
            "name": "Creative",
            "description": "Balanced creative design that maintains professionalism. Includes space for portfolio links and creative achievements while staying ATS-compliant.",
            "style": "creative",
            "best_for": ["Graphic Design", "UX/UI", "Content Creation", "Advertising", "Arts"]
        }
    }
    
    return templates

def get_template_structure(template_name):
    """Get the structure and styling preferences for a specific template"""
    
    structures = {
        "Professional": {
            "sections": [
                "contact_info",
                "professional_summary", 
                "work_experience",
                "education",
                "skills",
                "certifications"
            ],
            "formatting": {
                "font": "Arial",
                "header_color": "#2C3E50",
                "accent_color": "#34495E",
                "layout": "single_column"
            }
        },
        
        "Modern": {
            "sections": [
                "contact_info",
                "professional_summary",
                "technical_skills",
                "work_experience", 
                "education",
                "projects"
            ],
            "formatting": {
                "font": "Calibri",
                "header_color": "#3498DB",
                "accent_color": "#2980B9",
                "layout": "single_column"
            }
        },
        
        "Executive": {
            "sections": [
                "contact_info",
                "executive_summary",
                "core_competencies",
                "professional_experience",
                "leadership_achievements",
                "education",
                "board_positions"
            ],
            "formatting": {
                "font": "Times New Roman",
                "header_color": "#1C2833",
                "accent_color": "#2C3E50",
                "layout": "single_column"
            }
        },
        
        "Technical": {
            "sections": [
                "contact_info",
                "technical_summary",
                "technical_skills",
                "programming_languages",
                "work_experience",
                "projects",
                "education",
                "certifications"
            ],
            "formatting": {
                "font": "Arial",
                "header_color": "#16A085",
                "accent_color": "#138D75",
                "layout": "single_column"
            }
        },
        
        "Creative": {
            "sections": [
                "contact_info",
                "creative_summary",
                "core_skills",
                "work_experience",
                "portfolio_highlights",
                "education",
                "awards"
            ],
            "formatting": {
                "font": "Helvetica",
                "header_color": "#8E44AD",
                "accent_color": "#7D3C98",
                "layout": "single_column"
            }
        }
    }
    
    return structures.get(template_name, structures["Professional"])

def get_industry_recommendations():
    """Get template recommendations based on industry"""
    
    industry_templates = {
        "Technology": ["Technical", "Modern", "Professional"],
        "Finance": ["Professional", "Executive", "Modern"],
        "Healthcare": ["Professional", "Executive", "Technical"],
        "Legal": ["Professional", "Executive"],
        "Education": ["Professional", "Modern"],
        "Marketing": ["Modern", "Creative", "Professional"],
        "Design": ["Creative", "Modern", "Professional"],
        "Engineering": ["Technical", "Professional", "Modern"],
        "Consulting": ["Executive", "Professional", "Modern"],
        "Startups": ["Modern", "Technical", "Creative"],
        "Non-profit": ["Professional", "Modern"],
        "Government": ["Professional", "Executive"],
        "Manufacturing": ["Professional", "Technical"],
        "Retail": ["Professional", "Modern"],
        "Media": ["Creative", "Modern", "Professional"]
    }
    
    return industry_templates

def customize_template_for_experience_level(template_name, experience_level):
    """Customize template based on experience level"""
    
    customizations = {
        "entry_level": {
            "emphasis": ["education", "skills", "projects", "internships"],
            "de_emphasize": ["executive_summary", "leadership_achievements"],
            "sections_to_add": ["relevant_coursework", "academic_projects"],
            "summary_style": "objective_focused"
        },
        
        "mid_level": {
            "emphasis": ["work_experience", "skills", "achievements"],
            "de_emphasize": ["academic_projects", "coursework"],
            "sections_to_add": ["professional_development"],
            "summary_style": "experience_focused"
        },
        
        "senior_level": {
            "emphasis": ["leadership_experience", "strategic_achievements", "team_management"],
            "de_emphasize": ["technical_details", "individual_contributions"],
            "sections_to_add": ["leadership_achievements", "strategic_initiatives"],
            "summary_style": "leadership_focused"
        },
        
        "executive": {
            "emphasis": ["strategic_vision", "organizational_impact", "board_experience"],
            "de_emphasize": ["technical_skills", "day_to_day_tasks"],
            "sections_to_add": ["board_positions", "speaking_engagements", "thought_leadership"],
            "summary_style": "executive_focused"
        }
    }
    
    return customizations.get(experience_level, customizations["mid_level"])

def get_ats_optimization_tips():
    """Get ATS optimization tips for resume templates"""
    
    tips = {
        "formatting": [
            "Use standard fonts (Arial, Calibri, Times New Roman)",
            "Avoid images, graphics, and complex formatting",
            "Use standard section headers (Experience, Education, Skills)",
            "Save as both PDF and Word formats",
            "Avoid tables, text boxes, and columns",
            "Use bullet points for easy scanning"
        ],
        
        "content": [
            "Include relevant keywords from job descriptions",
            "Use standard job titles and industry terminology",
            "Spell out acronyms (e.g., 'Search Engine Optimization (SEO)')",
            "Include both hard and soft skills",
            "Use action verbs to start bullet points",
            "Quantify achievements with numbers and percentages"
        ],
        
        "sections": [
            "Always include Contact Information",
            "Professional Summary or Objective",
            "Work Experience with dates",
            "Education with degrees and dates",
            "Relevant Skills section",
            "Certifications if applicable"
        ],
        
        "keywords": [
            "Research job-specific keywords",
            "Include industry-standard terminology",
            "Match skills mentioned in job postings",
            "Use both spelled-out and abbreviated versions",
            "Include relevant software and tools",
            "Add location-specific keywords if relevant"
        ]
    }
    
    return tips

def validate_template_content(content, template_name):
    """Validate that content matches template requirements"""
    
    template_structure = get_template_structure(template_name)
    required_sections = template_structure["sections"]
    
    validation_results = {
        "valid": True,
        "missing_sections": [],
        "recommendations": []
    }
    
    # Check for required sections
    content_sections = set(content.keys())
    required_sections_set = set(required_sections)
    
    missing = required_sections_set - content_sections
    if missing:
        validation_results["valid"] = False
        validation_results["missing_sections"] = list(missing)
    
    # Add recommendations based on template type
    if template_name == "Technical":
        if not content.get("technical_skills"):
            validation_results["recommendations"].append("Add detailed technical skills section")
        if not content.get("projects"):
            validation_results["recommendations"].append("Include relevant projects or portfolio")
    
    elif template_name == "Executive":
        if not content.get("leadership_achievements"):
            validation_results["recommendations"].append("Highlight leadership and management experience")
        if not content.get("strategic_initiatives"):
            validation_results["recommendations"].append("Include strategic accomplishments and business impact")
    
    elif template_name == "Creative":
        if not content.get("portfolio_highlights"):
            validation_results["recommendations"].append("Add portfolio links or creative work samples")
        if not content.get("creative_skills"):
            validation_results["recommendations"].append("Showcase creative software and design skills")
    
    return validation_results
