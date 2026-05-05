#!/usr/bin/env python3
"""
Fix the script loading order - searchEngine must load before components
"""
import os
import re

def fix_order(filepath):
    """Fix script loading order"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if scripts are in wrong order
    if 'modules/search/components/SearchOverlay.js' in content:
        # Find and replace the entire script block
        old_pattern = r'<!-- Search module scripts -->\s*<script src="../modules/search/data/searchData\.js"></script>\s*<script src="../modules/search/components/SearchOverlay\.js"></script>\s*<script src="../modules/search/components/SearchInput\.js"></script>\s*<script src="../modules/search/components/FAQList\.js"></script>\s*<script src="../modules/search/components/SearchResultsPreview\.js"></script>\s*<script src="../modules/search/utils/searchEngine\.js"></script>\s*<script src="../modules/search/index\.js"></script>'
        
        new_scripts = '''<!-- Search module scripts -->
  <script src="../modules/search/data/searchData.js"></script>
  <script src="../modules/search/utils/searchEngine.js"></script>
  <script src="../modules/search/components/SearchOverlay.js"></script>
  <script src="../modules/search/components/SearchInput.js"></script>
  <script src="../modules/search/components/FAQList.js"></script>
  <script src="../modules/search/components/SearchResultsPreview.js"></script>
  <script src="../modules/search/index.js"></script>'''
        
        content = re.sub(old_pattern, new_scripts, content)
        print(f"  ✓ Fixed script order")
    else:
        print(f"  ✓ Scripts already in correct order or not found")
        return False
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Successfully updated")
    return True

def main():
    pages = [
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
            if fix_order(page):
                updated += 1
        print()
    
    print(f"✅ Fixed {updated} pages")

if __name__ == '__main__':
    main()
