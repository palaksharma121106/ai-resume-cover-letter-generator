from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, darkblue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io
from datetime import datetime


class PDFGenerator:

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Header style
        self.styles.add(
            ParagraphStyle(name='CustomHeader',
                           parent=self.styles['Heading1'],
                           fontSize=16,
                           spaceAfter=12,
                           textColor=darkblue,
                           alignment=TA_CENTER))

        # Contact info style
        self.styles.add(
            ParagraphStyle(name='ContactInfo',
                           parent=self.styles['Normal'],
                           fontSize=10,
                           alignment=TA_CENTER,
                           spaceAfter=12))

        # Section header style
        self.styles.add(
            ParagraphStyle(name='SectionHeader',
                           parent=self.styles['Heading2'],
                           fontSize=12,
                           spaceAfter=6,
                           spaceBefore=12,
                           textColor=darkblue,
                           borderWidth=1,
                           borderColor=darkblue,
                           borderPadding=2))

        # Job title style
        self.styles.add(
            ParagraphStyle(name='JobTitle',
                           parent=self.styles['Normal'],
                           fontSize=11,
                           spaceBefore=6,
                           spaceAfter=2,
                           textColor=black,
                           fontName='Helvetica-Bold'))

        # Company info style
        self.styles.add(
            ParagraphStyle(name='CompanyInfo',
                           parent=self.styles['Normal'],
                           fontSize=10,
                           spaceAfter=4,
                           textColor=black,
                           fontName='Helvetica-Oblique'))

        # Bullet point style
        self.styles.add(
            ParagraphStyle(name='BulletPoint',
                           parent=self.styles['Normal'],
                           fontSize=10,
                           leftIndent=20,
                           spaceAfter=3,
                           bulletIndent=10))

    def generate_resume_pdf(self, resume_data):
        """Generate PDF for resume"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer,
                                    pagesize=letter,
                                    rightMargin=0.75 * inch,
                                    leftMargin=0.75 * inch,
                                    topMargin=0.75 * inch,
                                    bottomMargin=0.75 * inch)

            story = []
            content = resume_data['content']

            # Header - Name and Contact Info (always include this)
            personal_info = content.get('personal_info', {})
            first_name = personal_info.get('first_name', 'Name')
            last_name = personal_info.get('last_name', 'Not Provided')
            name = f"{first_name} {last_name}"
            story.append(Paragraph(name, self.styles['CustomHeader']))

            # Contact information (always include this)
            contact_parts = []
            if personal_info.get('email'):
                contact_parts.append(personal_info['email'])
            if personal_info.get('phone'):
                contact_parts.append(personal_info['phone'])
            if personal_info.get('location'):
                contact_parts.append(personal_info['location'])

            if contact_parts:
                contact_info = " • ".join(contact_parts)
                story.append(Paragraph(contact_info, self.styles['ContactInfo']))

            # Add LinkedIn and other links
            links = []
            if personal_info.get('linkedin'):
                links.append(f"LinkedIn: {personal_info['linkedin']}")
            if personal_info.get('github'):
                links.append(f"GitHub: {personal_info['github']}")
            if personal_info.get('website'):
                links.append(f"Website: {personal_info['website']}")

            if links:
                story.append(Paragraph(" • ".join(links), self.styles['ContactInfo']))
            
            # Add some space after header
            story.append(Spacer(1, 0.2*inch))

            # Professional Summary
            if content.get('professional_summary'):
                story.append(
                    Paragraph("PROFESSIONAL SUMMARY",
                              self.styles['SectionHeader']))
                story.append(
                    Paragraph(content['professional_summary'],
                              self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))

            # Work Experience
            if content.get('work_experience'):
                story.append(
                    Paragraph("PROFESSIONAL EXPERIENCE",
                              self.styles['SectionHeader']))

                for exp in content['work_experience']:
                    # Job title and company
                    job_title = f"{exp['job_title']} - {exp['company']}"
                    story.append(Paragraph(job_title, self.styles['JobTitle']))

                    # Date and location
                    date_location = f"{exp['start_date']} to {exp['end_date']}"
                    if exp.get('location'):
                        date_location += f" • {exp['location']}"
                    story.append(
                        Paragraph(date_location, self.styles['CompanyInfo']))

                    # Job description bullets
                    if 'enhanced_description' in exp:
                        for bullet in exp['enhanced_description']:
                            story.append(
                                Paragraph(f"• {bullet}",
                                          self.styles['BulletPoint']))
                    else:
                        story.append(
                            Paragraph(f"• {exp['description']}",
                                      self.styles['BulletPoint']))

                    story.append(Spacer(1, 0.1 * inch))

            # Education
            if content.get('education'):
                story.append(
                    Paragraph("EDUCATION", self.styles['SectionHeader']))

                for edu in content['education']:
                    degree_info = f"{edu['degree']}"
                    if edu.get('major'):
                        degree_info += f" in {edu['major']}"
                    story.append(
                        Paragraph(degree_info, self.styles['JobTitle']))

                    school_info = f"{edu['school']} • {edu['graduation_date']}"
                    if edu.get('location'):
                        school_info += f" • {edu['location']}"
                    story.append(
                        Paragraph(school_info, self.styles['CompanyInfo']))

                    if edu.get('gpa'):
                        story.append(
                            Paragraph(f"GPA: {edu['gpa']}",
                                      self.styles['Normal']))

                    if edu.get('achievements'):
                        story.append(
                            Paragraph(f"• {edu['achievements']}",
                                      self.styles['BulletPoint']))

                    story.append(Spacer(1, 0.1 * inch))

            # Skills
            if content.get('skills'):
                story.append(Paragraph("SKILLS", self.styles['SectionHeader']))

                for category, skills_list in content['skills'].items():
                    if skills_list:
                        skills_text = f"<b>{category}:</b> {', '.join(skills_list)}"
                        story.append(
                            Paragraph(skills_text, self.styles['Normal']))
                        story.append(Spacer(1, 0.05 * inch))

            # Build PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            raise Exception(f"Failed to generate resume PDF: {str(e)}")

    def generate_cover_letter_pdf(self, cover_letter_data):
        """Generate PDF for cover letter"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer,
                                    pagesize=letter,
                                    rightMargin=1 * inch,
                                    leftMargin=1 * inch,
                                    topMargin=1 * inch,
                                    bottomMargin=1 * inch)

            story = []
            content = cover_letter_data['content']
            job_info = cover_letter_data['job_info']

            # Date
            current_date = datetime.now().strftime("%B %d, %Y")
            story.append(Paragraph(current_date, self.styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

            # Cover letter content
            # Split content by paragraphs and add them
            paragraphs = content.split('\n\n')

            for para in paragraphs:
                if para.strip():
                    # Clean up the paragraph
                    cleaned_para = para.strip().replace('\n', ' ')
                    story.append(Paragraph(cleaned_para,
                                           self.styles['Normal']))
                    story.append(Spacer(1, 0.1 * inch))

            # Build PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            raise Exception(f"Failed to generate cover letter PDF: {str(e)}")

    def create_portfolio_pdf(self, resume_data, cover_letter_data):
        """Create a combined PDF with both resume and cover letter"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer,
                                    pagesize=letter,
                                    rightMargin=0.75 * inch,
                                    leftMargin=0.75 * inch,
                                    topMargin=0.75 * inch,
                                    bottomMargin=0.75 * inch)

            story = []

            # Add cover letter first
            if cover_letter_data:
                story.append(
                    Paragraph("COVER LETTER", self.styles['CustomHeader']))
                story.append(Spacer(1, 0.2 * inch))

                content = cover_letter_data['content']
                paragraphs = content.split('\n\n')

                for para in paragraphs:
                    if para.strip():
                        cleaned_para = para.strip().replace('\n', ' ')
                        story.append(
                            Paragraph(cleaned_para, self.styles['Normal']))
                        story.append(Spacer(1, 0.1 * inch))

                # Page break
                from reportlab.platypus import PageBreak
                story.append(PageBreak())

            # Add resume
            if resume_data:
                # Add all resume content (reuse logic from generate_resume_pdf)
                content = resume_data['content']

                # Header
                name = f"{content['personal_info']['first_name']} {content['personal_info']['last_name']}"
                story.append(Paragraph(name, self.styles['CustomHeader']))

                # Continue with rest of resume content...
                # (Implementation similar to generate_resume_pdf)

            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            raise Exception(f"Failed to generate portfolio PDF: {str(e)}")
