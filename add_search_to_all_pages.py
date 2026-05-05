#!/usr/bin/env python3
"""
Add search functionality to all HTML pages in the project
"""
import os
import re
from pathlib import Path

# CSS and JS to add
CSS_LINKS = '''  <!-- Search module CSS -->
  <link rel="stylesheet" href="../css/search-integration.css" />
  <link rel="stylesheet" href="../modules/search/styles/search.css" />
  <!-- Font Awesome for search icon -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />'''

JS_SCRIPTS = '''  <!-- Search module scripts -->
  <script src="../modules/search/data/searchData.js"></script>
  <script src="../modules/search/utils/searchEngine.js"></script>
  <script src="../modules/search/components/SearchOverlay.js"></script>
  <script src="../modules/search/components/SearchInput.js"></script>
  <script src="../modules/search/components/FAQList.js"></script>
  <script src="../modules/search/components/SearchResultsPreview.js"></script>
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
  </script>'''

PLACEMENTS_JS_SCRIPTS = '''  <!-- Search module scripts -->
  <script src="../modules/search/data/searchData.js"></script>
  <script src="../modules/search/utils/searchEngine.js"></script>
  <script src="../modules/search/components/SearchOverlay.js"></script>
  <script src="../modules/search/components/SearchInput.js"></script>
  <script src="../modules/search/components/FAQList.js"></script>
  <script src="../modules/search/components/SearchResultsPreview.js"></script>
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
  </script>'''

def add_search_to_page(filepath, is_placements=False):
    """Add search functionality to a single HTML page"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if search is already added
    if 'modules/search' in content:
        print(f"  ✓ Search already added, skipping")
        return False
    
    # Add top-header class to masthead if not present
    if 'class="masthead"' in content and 'class="masthead top-header"' not in content:
        content = content.replace('class="masthead"', 'class="masthead top-header"')
        print(f"  ✓ Added top-header class to masthead")
    
    # Add header-right container after EAPCET button
    if '<a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>' in content:
        # Check if header-right already exists
        if '<div class="header-right">' not in content:
            # Move EAPCET button inside header-right
            old_pattern = r'(<div class="masthead__tagline">.*?</div>)\s*<a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>'
            new_replacement = r'\1\n        <div class="header-right">\n          <a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>\n          <!-- Search icon will be injected here by SearchSystem.init() -->\n        </div>'
            content = re.sub(old_pattern, new_replacement, content, flags=re.DOTALL)
            print(f"  ✓ Added header-right container")
    
    # Add CSS links before </head>
    if '</head>' in content and 'search-integration.css' not in content:
        content = content.replace('</head>', CSS_LINKS + '\n</head>')
        print(f"  ✓ Added CSS links")
    
    # Add JS scripts before </body>
    if '</body>' in content and 'SearchSystem.init' not in content:
        js_to_add = PLACEMENTS_JS_SCRIPTS if is_placements else JS_SCRIPTS
        content = content.replace('</body>', js_to_add + '\n</body>')
        print(f"  ✓ Added JS scripts")
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✅ Successfully updated {filepath}")
    return True

def main():
    """Process all HTML files"""
    updated_count = 0
    
    # Department pages
    dept_pages = [
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
    ]
    
    # Placements page
    placements_pages = [
        'placements/placements.html',
    ]
    
    print("=" * 60)
    print("Adding search functionality to all pages")
    print("=" * 60)
    
    for page in dept_pages:
        if os.path.exists(page):
            if add_search_to_page(page):
                updated_count += 1
        else:
            print(f"⚠️  File not found: {page}")
        print()
    
    for page in placements_pages:
        if os.path.exists(page):
            if add_search_to_page(page, is_placements=True):
                updated_count += 1
        else:
            print(f"⚠️  File not found: {page}")
        print()
    
    print("=" * 60)
    print(f"✅ Updated {updated_count} pages")
    print("=" * 60)

if __name__ == '__main__':
    main()
