#!/usr/bin/env python3
"""
Force add search scripts to all pages
"""
import os

JS_SCRIPTS = '''
  <!-- Search module scripts -->
  <script src="../modules/search/data/searchData.js"></script>
  <script src="../modules/search/components/SearchOverlay.js"></script>
  <script src="../modules/search/components/SearchInput.js"></script>
  <script src="../modules/search/components/FAQList.js"></script>
  <script src="../modules/search/components/SearchResultsPreview.js"></script>
  <script src="../modules/search/utils/searchEngine.js"></script>
  <script src="../modules/search/index.js"></script>
  <script>
  document.addEventListener('DOMContentLoaded', function () {
      if (window.SearchSystem) {
          window.SearchSystem.init({
              basePath:   '../',
              apiBase:    '',
              debounceMs: 300,
              faqItems:   []
          });
      }
  });
  </script>
'''

def add_scripts(filepath):
    """Add search scripts before </body> tag"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if modules/search/index.js is already there
    if 'modules/search/index.js' in content:
        print(f"  ✓ Scripts already added, skipping")
        return False
    
    # Add before </body>
    if '</body>' in content:
        content = content.replace('</body>', JS_SCRIPTS + '\n</body>')
        print(f"  ✓ Added search scripts")
    else:
        print(f"  ✗ No </body> tag found!")
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
            if add_scripts(page):
                updated += 1
        print()
    
    print(f"✅ Updated {updated} pages")

if __name__ == '__main__':
    main()
