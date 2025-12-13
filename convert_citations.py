#!/usr/bin/env python3
"""
Script to convert detailed author-name citations to numbered citations.
Replaces patterns like "Nakamoto [1]" with just "[1]"
"""

import re
from docx import Document
import sys

def convert_citations_to_numbered(doc_path, output_path=None):
    """
    Convert detailed citations (e.g., "Author et al. [1]") to numbered citations (e.g., "[1]")
    
    Args:
        doc_path: Path to the input DOCX file
        output_path: Path to save the output (if None, overwrites input)
    """
    # Load document
    doc = Document(doc_path)
    
    # Pattern to match author names followed by citation numbers
    # This handles:
    # - "Author et al. [N]"
    # - "Author and Author [N]" 
    # - "Author-Author et al. [N]" (hyphenated names like Ben-Sasson)
    # - Single "Author [N]"
    # We match any capital letter starting a word, followed by word characters or hyphens,
    # optionally followed by "et al." or "and Author", then the citation number
    
    # Pattern: One or more author names (possibly with "et al." or "and") followed by [N]
    citation_pattern = r'\b[A-Z][\w\-]+(?:(?:\s+et\s+al\.|\s+and\s+[A-Z][\w\-]+))*\s*\[(\d+)\]'
    
    changes_made = 0
    changed_paragraphs = []
    
    # Process each paragraph
    for i, para in enumerate(doc.paragraphs):
        original_text = para.text
        
        # Replace author citations with just the number
        new_text = re.sub(citation_pattern, r'[\1]', original_text)
        
        # If text changed, update the paragraph
        if new_text != original_text:
            changes_made += 1
            changed_paragraphs.append(i)
            # Clear existing runs and add new text
            para.clear()
            para.add_run(new_text)
    
    # Save the document
    if output_path is None:
        output_path = doc_path
    
    doc.save(output_path)
    print(f"Conversion complete. {changes_made} paragraphs modified.")
    print(f"Output saved to: {output_path}")
    
    return changes_made

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_citations.py <input.docx> [output.docx]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_citations_to_numbered(input_path, output_path)
