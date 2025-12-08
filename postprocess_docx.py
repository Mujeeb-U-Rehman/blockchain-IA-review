import sys
from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.shared import OxmlElement, qn

def set_two_columns(section, space_inches=0.2):
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
    section.top_margin = Inches(top)
    section.bottom_margin = Inches(bottom)
    section.left_margin = Inches(left)
    section.right_margin = Inches(right)

def set_base_font(doc, name="Times New Roman", size_pt=10):
    style = doc.styles['Normal']
    font = style.font
    font.name = name
    font.size = Pt(size_pt)

def set_heading_fonts(doc, name="Times New Roman"):
    for h in ["Heading 1", "Heading 2", "Heading 3"]:
        if h in doc.styles:
            s = doc.styles[h]
            s.font.name = name
            if h == "Heading 1":
                s.font.size = Pt(12)
            elif h == "Heading 2":
                s.font.size = Pt(11)
            else:
                s.font.size = Pt(10)

def main(path):
    doc = Document(path)
    # Apply margins/columns to first section
    first = doc.sections[0]
    set_margins(first)
    set_two_columns(first, space_inches=0.2)
    # Set base and heading fonts
    set_base_font(doc, "Times New Roman", 10)
    set_heading_fonts(doc, "Times New Roman")
    # Ensure no extra spacing after paragraphs
    for p in doc.paragraphs:
        if p.paragraph_format.space_after:
            p.paragraph_format.space_after = Pt(0)
    doc.save(path)

if __name__ == "__main__":
    main(sys.argv[1])
