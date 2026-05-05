#!/usr/bin/env python3
# Fix the head section of index.html

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the malformed CSS links section
old_text = '  <link rel="stylesheet" href="css/mobile.css" />`n  <!-- Search module CSS -->`n  <link rel="stylesheet" href="css/search-integration.css" />`n  <link rel="stylesheet" href="modules/search/styles/search.css" />`n  <!-- Font Awesome for search icon -->`n  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />'

new_text = '''  <link rel="stylesheet" href="css/mobile.css" />
  <!-- Search module CSS -->
  <link rel="stylesheet" href="css/search-integration.css" />
  <link rel="stylesheet" href="modules/search/styles/search.css" />
  <!-- Font Awesome for search icon -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />'''

content = content.replace(old_text, new_text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed head section successfully!")
