#!/usr/bin/env python3
"""
Add chronicles script to all pages
"""
import os
import re

def add_chronicles(filepath):
    """Add chronicles script after searchData.js"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already added
    if 'chroniclesData.js' in content:
        print(f"  ✓ Chronicles already added, skipping")
        return False
    
    # Add after searchData.js
    if 'modules/search/data/searchData.js' in content:
        content = content.replace(
            '<script src="../modules/search/data/searchData.js"></script>',
            '<script src="../modules/search/data/searchData.js"></script>\n  <script src="../modules/search/data/chroniclesData.js"></script>'
        )
        print(f"  ✓ Added chronicles script")
    else:
        print(f"  ✗ searchData.js not found!")
        return False
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Successfully updated")
    return True

def main():
    pages = [
        'departments/cse.html',
        'departments/ece.html',
        'departments/eee.html',
        'departments/aeronautical.html',
        'departments/mechanical.html',
        'departments/aiml.html',
        'departments/cse-cs.html',
        'departments/cse-ds.html',
        'departments/freshman.html',
        'departments/mba.html',
        'departments/ug.html',
        'departments/pg.html',
        'placements/placements.html',
    ]
    
    updated = 0
    for page in pages:
        if os.path.exists(page):
            if add_chronicles(page):
                updated += 1
        print()
    
    print(f"✅ Updated {updated} pages")

if __name__ == '__main__':
    main()
