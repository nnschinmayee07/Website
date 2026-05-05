import re

content = open('index.html', 'r', encoding='utf-8').read()

# Add ?v=2 to all search module scripts to bust cache
content = content.replace(
    'src="modules/search/utils/searchEngine.js"',
    'src="modules/search/utils/searchEngine.js?v=2"'
)
content = content.replace(
    'src="modules/search/components/SearchOverlay.js"',
    'src="modules/search/components/SearchOverlay.js?v=2"'
)
content = content.replace(
    'src="modules/search/components/SearchInput.js"',
    'src="modules/search/components/SearchInput.js?v=2"'
)
content = content.replace(
    'src="modules/search/components/FAQList.js"',
    'src="modules/search/components/FAQList.js?v=2"'
)
content = content.replace(
    'src="modules/search/components/SearchResultsPreview.js"',
    'src="modules/search/components/SearchResultsPreview.js?v=2"'
)
content = content.replace(
    'src="modules/search/index.js"',
    'src="modules/search/index.js?v=2"'
)
content = content.replace(
    'src="modules/search/data/searchData.js"',
    'src="modules/search/data/searchData.js?v=2"'
)
content = content.replace(
    'src="modules/search/data/chroniclesData.js"',
    'src="modules/search/data/chroniclesData.js?v=2"'
)

open('index.html', 'w', encoding='utf-8').write(content)
print('Done - cache busted')
