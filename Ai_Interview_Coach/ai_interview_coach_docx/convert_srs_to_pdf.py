#!/usr/bin/env python3
"""
Convert SRS Markdown document to Professional PDF using ReportLab
"""
import re
import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


def markdown_to_reportlab(text):
    """Convert markdown formatting to ReportLab XML safely"""
    # Escape HTML entities first to prevent parsing issues
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    # Now apply markdown conversions carefully with regex
    # **bold** -> <b>bold</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # *italic* -> <i>italic</i>
    text = re.sub(r'\*([^ ].*?[^ ])\*', r'<i>\1</i>', text)
    # `code` -> <font face="Courier">code</font>
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    
    return text


def parse_markdown_to_elements(md_content):
    """Parse markdown and convert to ReportLab elements"""
    
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=12,
        spaceBefore=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#003366'),
        spaceAfter=8,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=13
    )
    
    elements = []
    lines = md_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            elements.append(Spacer(1, 0.08*inch))
            i += 1
            continue
        
        # Title (# without ##)
        if line.startswith('# ') and not line.startswith('## '):
            title_text = line[2:].strip()
            elements.append(Paragraph(title_text, title_style))
            elements.append(Spacer(1, 0.15*inch))
            i += 1
            continue
        
        # Heading 1 (## without ###)
        if line.startswith('## ') and not line.startswith('### '):
            heading_text = line[3:].strip()
            elements.append(Paragraph(heading_text, heading1_style))
            i += 1
            continue
        
        # Heading 2 (###)
        if line.startswith('### '):
            heading_text = line[4:].strip()
            elements.append(Paragraph(heading_text, heading2_style))
            i += 1
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            elements.append(Spacer(1, 0.1*inch))
            i += 1
            continue
        
        # Regular paragraph
        if line.strip():
            # Convert markdown to ReportLab
            text = markdown_to_reportlab(line.strip())
            
            try:
                elements.append(Paragraph(text, body_style))
            except Exception as e:
                # If there's a parsing error, fallback to plain text
                plain_text = line.strip()
                plain_text = plain_text.replace('**', '')
                plain_text = plain_text.replace('*', '')
                plain_text = plain_text.replace('`', '')
                elements.append(Paragraph(plain_text, body_style))
        
        i += 1
    
    return elements


def convert_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF"""
    try:
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title="AI Interview Coach - SRS Document"
        )
        
        # Parse content to ReportLab elements
        elements = parse_markdown_to_elements(content)
        
        # Build PDF
        doc.build(elements)
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    # Get file paths
    project_dir = Path(__file__).parent
    md_file = project_dir / 'SRS_AI_INTERVIEW_COACH.md'
    pdf_file = project_dir / 'SRS_AI_INTERVIEW_COACH.pdf'
    
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False
    
    print(f"Converting {md_file.name} to PDF...")
    
    if convert_to_pdf(str(md_file), str(pdf_file)):
        size_kb = os.path.getsize(pdf_file) / 1024
        print(f"SUCCESS: Created {pdf_file.name}")
        print(f"PDF Size: {size_kb:.1f} KB")
        return True
    else:
        print("FAILED: Could not convert markdown to PDF")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
