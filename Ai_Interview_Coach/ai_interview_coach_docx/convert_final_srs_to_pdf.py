#!/usr/bin/env python3
"""
SRS PDF Generator - Converts markdown SRS document to professional PDF
Matches sample SRS document format with precision styling
"""

import re
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from datetime import datetime

def create_title_page(doc):
    """Create professional title page matching sample format"""
    elements = []
    
    # Spacer
    elements.append(Spacer(1, 2.5 * inch))
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        fontSize=42,
        fontName='Helvetica-Bold',
        textColor=HexColor('#0066cc'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    elements.append(Paragraph("AI INTERVIEW COACH", title_style))
    elements.append(Spacer(1, 0.3 * inch))
    
    # Subtitle
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        fontSize=18,
        fontName='Helvetica',
        textColor=HexColor('#003366'),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    elements.append(Paragraph("Software Requirements Specification", subtitle_style))
    elements.append(Spacer(1, 0.8 * inch))
    
    # Document info
    info_style = ParagraphStyle(
        'Info',
        fontSize=11,
        fontName='Helvetica',
        textColor=black,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    elements.append(Paragraph(f"<b>Document Version:</b> 3.0", info_style))
    elements.append(Paragraph(f"<b>Date:</b> March 4, 2026", info_style))
    elements.append(Paragraph(f"<b>Status:</b> Final Release", info_style))
    elements.append(Spacer(1, 1 * inch))
    
    # Tagline
    tagline_style = ParagraphStyle(
        'Tagline',
        fontSize=13,
        fontName='Helvetica-Oblique',
        textColor=HexColor('#666666'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Intelligent AI-Powered Interview Preparation Platform", tagline_style))
    
    return elements

def safe_html_entity(text):
    """Convert text to safe HTML entities for ReportLab"""
    if not text:
        return ""
    
    try:
        # Replace common problematic characters
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    except Exception as e:
        return text[:50] + "..."

def parse_markdown_to_pdf_elements(content):
    """Parse markdown to ReportLab elements with safe entity handling"""
    elements = []
    styles = getSampleStyleSheet()
    
    # Define custom styles
    styles.add(ParagraphStyle(
        name='Heading1Custom',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#0066cc'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Heading2Custom',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='Heading3Custom',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=HexColor('#004080'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='BodyCustom',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    ))
    
    lines = content.split('\n')
    i = 0
    skip_toc = False
    
    while i < len(lines):
        line = lines[i]
        
        # Skip TOC section
        if 'TABLE OF CONTENTS' in line.upper():
            skip_toc = True
            i += 1
            continue
        if skip_toc and line.strip() and not line.startswith('#') and not line.startswith('-'):
            i += 1
            continue
        if skip_toc and (line.startswith('# ') or line.startswith('---')):
            skip_toc = False
        
        # Heading 1
        if line.startswith('# ') and not line.startswith('# '):
            try:
                heading_text = safe_html_entity(line.replace('# ', '').strip())
                elements.append(Paragraph(heading_text, styles['Heading1Custom']))
                elements.append(Spacer(1, 0.1 * inch))
            except:
                pass
            i += 1
        
        # Heading 2
        elif line.startswith('## '):
            try:
                heading_text = safe_html_entity(line.replace('## ', '').strip())
                elements.append(Paragraph(heading_text, styles['Heading2Custom']))
                elements.append(Spacer(1, 0.08 * inch))
            except:
                pass
            i += 1
        
        # Heading 3
        elif line.startswith('### '):
            try:
                heading_text = safe_html_entity(line.replace('### ', '').strip())
                elements.append(Paragraph(heading_text, styles['Heading3Custom']))
                elements.append(Spacer(1, 0.06 * inch))
            except:
                pass
            i += 1
        
        # Horizontal line / page break
        elif line.strip() == '---':
            elements.append(Spacer(1, 0.2 * inch))
            if len(elements) > 5:  # Don't break too early
                elements.append(PageBreak())
            i += 1
        
        # Code blocks
        elif line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(safe_html_entity(lines[i]))
                i += 1
            
            code_text = '\n'.join(code_lines)
            code_style = ParagraphStyle(
                'CodeStyle',
                parent=styles['BodyText'],
                fontName='Courier',
                fontSize=8,
                textColor=HexColor('#333333'),
                backColor=HexColor('#f5f5f5'),
                spaceAfter=10
            )
            
            try:
                elements.append(Paragraph(f"<font color='#333333'>{code_text}</font>", code_style))
            except:
                elements.append(Paragraph("Code block", code_style))
            
            i += 1
        
        # Tables - basic handling
        elif '|' in line:
            # Extract table rows
            table_rows = []
            table_start = i
            while i < len(lines) and '|' in lines[i]:
                cells = [safe_html_entity(cell.strip()) for cell in lines[i].split('|')[1:-1]]
                if cells:
                    table_rows.append(cells)
                i += 1
            
            # Skip separator line if exists
            if table_rows and all(c in '-:' or c.strip() == '' for row in table_rows[1:2] for c in ''.join(row)):
                table_rows.pop(1) if len(table_rows) > 1 else None
            
            if table_rows:
                try:
                    table = Table(table_rows, colWidths=[2*inch] * len(table_rows[0]))
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0066cc')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
                        ('GRID', (0, 0), (-1, -1), 1, black),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ]))
                    elements.append(table)
                    elements.append(Spacer(1, 0.15 * inch))
                except:
                    pass
        
        # Regular paragraphs
        elif line.strip() and not line.startswith('#') and not line.startswith('-'):
            try:
                safe_text = safe_html_entity(line.strip())
                elements.append(Paragraph(safe_text, styles['BodyCustom']))
            except:
                elements.append(Spacer(1, 0.05 * inch))
            i += 1
        
        # Empty lines or bullets
        else:
            if line.startswith('- '):
                bullet_text = safe_html_entity(line[2:].strip())
                bullet_style = ParagraphStyle(
                    'BulletStyle',
                    parent=styles['BodyText'],
                    fontSize=10,
                    leftIndent=20,
                    spaceAfter=6
                )
                try:
                    elements.append(Paragraph(f"• {bullet_text}", bullet_style))
                except:
                    pass
            else:
                elements.append(Spacer(1, 0.05 * inch))
            i += 1
    
    return elements

def convert_to_pdf(md_file, pdf_file):
    """Convert markdown SRS to professional PDF"""
    try:
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Converting {md_file} to PDF...")
        
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title="AI Interview Coach - SRS",
            author="Development Team",
            subject="Software Requirements Specification"
        )
        
        # Build elements
        elements = create_title_page(doc)
        elements.append(PageBreak())
        
        # Add TOC
        toc_style = ParagraphStyle(
            'TOCStyle',
            fontSize=12,
            fontName='Helvetica',
            leftIndent=20,
            spaceAfter=6
        )
        elements.append(Paragraph("<b>TABLE OF CONTENTS</b>", toc_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Extract TOC items
        toc_pattern = r'^(\d+\.|#+\s+)'
        for match in re.finditer(r'^(#+)\s+([^#\n]+)', content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            if level <= 2 and title not in ['TABLE OF CONTENTS', 'Executive Summary']:
                indent = (level - 1) * 0.1 * inch
                toc_item_style = ParagraphStyle(
                    f'TOCItem{level}',
                    fontSize=10 - level,
                    leftIndent=20 + indent,
                    spaceAfter=4
                )
                try:
                    elements.append(Paragraph(f"{title}", toc_item_style))
                except:
                    pass
        
        elements.append(PageBreak())
        
        # Parse and add markdown content
        content_elements = parse_markdown_to_pdf_elements(content)
        elements.extend(content_elements)
        
        # Build PDF
        doc.build(elements)
        
        # Get file size
        pdf_size = Path(pdf_file).stat().st_size / 1024
        
        print(f"SUCCESS: Created {Path(pdf_file).name}")
        print(f"File Size: {pdf_size:.1f} KB")
        print(f"Format: Professional Multi-page SRS Document")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    project_dir = Path(r'c:\projects\ai_coach_demo_p2')
    md_file = project_dir / 'SRS_FINAL_AI_INTERVIEW_COACH.md'
    pdf_file = project_dir / 'SRS_FINAL_AI_INTERVIEW_COACH.pdf'
    
    if not md_file.exists():
        print(f"ERROR: {md_file} not found")
        sys.exit(1)
    
    success = convert_to_pdf(str(md_file), str(pdf_file))
    sys.exit(0 if success else 1)
