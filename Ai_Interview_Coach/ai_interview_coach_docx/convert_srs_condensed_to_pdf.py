#!/usr/bin/env python3
"""
Convert SRS Markdown to Professional PDF (20-slide format)
"""
import re
import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


def create_title_page(elements):
    """Create professional title page"""
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=40,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("AI INTERVIEW COACH", title_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Software Requirements Specification", subtitle_style))
    elements.append(Spacer(1, 1*inch))
    
    elements.append(Paragraph("Document Version: 1.0", info_style))
    elements.append(Paragraph("Date: March 4, 2026", info_style))
    elements.append(Paragraph("Status: Final Release", info_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Professional Interview Preparation Platform", info_style))
    
    elements.append(PageBreak())
    return elements


def markdown_to_reportlab(text):
    """Convert markdown to ReportLab safely"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^ ].*?[^ ])\*', r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`', r'<font face="Courier" size="9">\1</font>', text)
    
    return text


def parse_markdown_to_pdf_elements(md_content):
    """Parse markdown and create ReportLab elements optimized for 20-page format"""
    
    styles = getSampleStyleSheet()
    
    heading1_style = ParagraphStyle(
        'Heading1PDF',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=12,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'Heading2PDF',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#003366'),
        spaceAfter=8,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'BodyPDF',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=6,
        leading=12
    )
    
    bullet_style = ParagraphStyle(
        'BulletPDF',
        parent=styles['BodyText'],
        fontSize=9.5,
        alignment=TA_LEFT,
        spaceAfter=4,
        leftIndent=20,
        leading=11
    )
    
    elements = []
    lines = md_content.split('\n')
    skip_mode = False
    
    for i, line in enumerate(lines):
        if not line.strip():
            elements.append(Spacer(1, 0.05*inch))
            continue
        
        # Skip document header
        if 'Document Version' in line or 'Date:' in line or 'Status:' in line:
            continue
        
        # Main title
        if line.startswith('# ') and '---' not in line:
            elements.append(Paragraph(line[2:].strip(), heading1_style))
            continue
        
        # Section headings
        if line.startswith('## '):
            elements.append(Paragraph(line[3:].strip(), heading2_style))
            continue
        
        # Code blocks - simplified
        if line.strip().startswith('```'):
            skip_mode = not skip_mode
            continue
        
        if skip_mode:
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            elements.append(Spacer(1, 0.08*inch))
            continue
        
        # Bullet points
        if line.strip().startswith('- '):
            bullet_text = markdown_to_reportlab(line[2:].strip())
            elements.append(Paragraph(bullet_text, bullet_style))
        
        # Regular content
        elif line.strip():
            text = markdown_to_reportlab(line.strip())
            
            try:
                elements.append(Paragraph(text, body_style))
            except:
                # Fallback for problematic text
                clean_text = line.strip().replace('**', '').replace('*', '').replace('`', '')
                elements.append(Paragraph(clean_text, body_style))
    
    return elements


def convert_to_pdf(md_file, pdf_file):
    """Convert markdown to optimized PDF"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=letter,
            rightMargin=0.6*inch,
            leftMargin=0.6*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch,
            title="AI Interview Coach - SRS Document"
        )
        
        elements = []
        
        # Add title page
        elements = create_title_page(elements)
        
        # Add table of contents
        toc_style = ParagraphStyle(
            'TOC',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=12
        )
        
        elements.append(Paragraph("TABLE OF CONTENTS", 
                                 ParagraphStyle('TOCTitle', parent=getSampleStyleSheet()['Heading1'],
                                              fontSize=16, textColor=colors.HexColor('#0066cc'),
                                              spaceAfter=12)))
        
        toc_items = [
            "1. Executive Summary",
            "2. Project Scope & Objectives",
            "3. Functional Requirements",
            "4. System Architecture",
            "5. Database Design",
            "6. API Specification",
            "7. User Interface",
            "8. Non-Functional Requirements",
            "9. Use Cases & Workflows",
            "10. Security & Compliance",
            "11. Deployment & Maintenance",
            "12. Testing Requirements",
            "13. Glossary & Technical Terms",
            "14. Appendices"
        ]
        
        for item in toc_items:
            elements.append(Paragraph(item, toc_style))
        
        elements.append(PageBreak())
        
        # Parse and add main content
        content_elements = parse_markdown_to_pdf_elements(content)
        elements.extend(content_elements)
        
        # Build PDF
        doc.build(elements)
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    project_dir = Path(__file__).parent
    md_file = project_dir / 'SRS_CONDENSED.md'
    pdf_file = project_dir / 'SRS_CONDENSED.pdf'
    
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False
    
    print(f"Converting {md_file.name} to professional PDF...")
    
    if convert_to_pdf(str(md_file), str(pdf_file)):
        size_kb = os.path.getsize(pdf_file) / 1024
        print(f"SUCCESS: Created {pdf_file.name}")
        print(f"File Size: {size_kb:.1f} KB")
        print(f"Format: Professional 20-slide SRS document")
        return True
    else:
        print("FAILED: Could not convert")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
