#!/usr/bin/env python3
"""
Script to format the DOCX document with IEEE style:
- Font: Times New Roman 11pt for body
- Proper heading sizes
- Two-column layout
"""

import sys
from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.shared import OxmlElement, qn

def set_two_columns(section, space_inches=0.2):
    """Set section to two-column layout"""
    sectPr = section._sectPr
    cols = sectPr.xpath("./w:cols")
    if cols:
        cols = cols[0]
    else:
        cols = OxmlElement('w:cols')
        sectPr.append(cols)
    cols.set(qn('w:num'), "2")
    # space is in twips (1 inch = 1440 twips)
    space_twips = int(space_inches * 1440)
    cols.set(qn('w:space'), str(space_twips))

def set_margins(section, top=0.75, bottom=1.0, left=0.625, right=0.625):
    """Set section margins"""
    section.top_margin = Inches(top)
    section.bottom_margin = Inches(bottom)
    section.left_margin = Inches(left)
    section.right_margin = Inches(right)

def format_document(doc_path, output_path=None):
    """
    Apply IEEE formatting to document:
    - Times New Roman 11pt for body text
    - Proper heading fonts
    - Two-column layout
    - IEEE margins
    """
    doc = Document(doc_path)
    
    # Apply margins and two-column layout to first section
    first = doc.sections[0]
    set_margins(first)
    set_two_columns(first, space_inches=0.2)
    
    # Set base font for Normal style
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    
    # Set heading fonts
    heading_styles = {
        "Heading 1": 12,
        "Heading 2": 11,
        "Heading 3": 11,
        "Title": 14,
    }
    
    for heading_name, size_pt in heading_styles.items():
        if heading_name in doc.styles:
            s = doc.styles[heading_name]
            s.font.name = 'Times New Roman'
            s.font.size = Pt(size_pt)
            s.font.bold = True
    
    # Apply formatting to all paragraphs
    for para in doc.paragraphs:
        # Ensure no extra spacing after paragraphs
        if para.paragraph_format.space_after:
            para.paragraph_format.space_after = Pt(0)
        
        # Apply Times New Roman 11pt to all runs that don't have explicit formatting
        for run in para.runs:
            if not run.font.name or run.font.name == 'Calibri':
                run.font.name = 'Times New Roman'
            if not run.font.size:
                run.font.size = Pt(11)
    
    # Save
    if output_path is None:
        output_path = doc_path
    
    doc.save(output_path)
    print(f"Document formatted successfully: {output_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python format_document.py <input.docx> [output.docx]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    format_document(input_path, output_path)
