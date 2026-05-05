content = open('index.html', 'r', encoding='utf-8').read()

# Add chronicles CSS after mobile.css
old = 'href="css/mobile.css" />'
new = 'href="css/mobile.css" />\n  <link rel="stylesheet" href="css/chronicles-section.css" />'
content = content.replace(old, new, 1)

# Add chronicles JS init after DOMContentLoaded SearchSystem init
old_js = """  document.addEventListener('DOMContentLoaded', function () {
      if (window.SearchSystem) {
          window.SearchSystem.init({
              basePath:   '',
              apiBase:    '',
              debounceMs: 300,
              faqItems:   []
          });
      }
  });"""

new_js = """  document.addEventListener('DOMContentLoaded', function () {
      if (window.SearchSystem) {
          window.SearchSystem.init({
              basePath:   '',
              apiBase:    '',
              debounceMs: 300,
              faqItems:   []
          });
      }

      // Load chronicles on homepage
      if (window.ChroniclesData) {
          var grid = document.getElementById('chroniclesHomeGrid');
          if (!grid) return;

          // Sort by date newest first, take top 6
          var items = window.ChroniclesData.data.slice().sort(function(a, b) {
              return new Date(b.date) - new Date(a.date);
          }).slice(0, 6);

          var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

          grid.innerHTML = items.map(function(item) {
              var d = new Date(item.date);
              var dateStr = d.getDate() + ' ' + months[d.getMonth()] + ' ' + d.getFullYear();
              return '<a class="chronicle-card-home" href="chronicles.html">' +
                  '<span class="chronicle-category-badge">' + item.category + '</span>' +
                  '<div class="chronicle-date-home"><i class="far fa-calendar-alt"></i> ' + dateStr + '</div>' +
                  '<h3 class="chronicle-title-home">' + item.title + '</h3>' +
                  '<p class="chronicle-description-home">' + item.description + '</p>' +
                  '</a>';
          }).join('');
      }
  });"""

content = content.replace(old_js, new_js, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('Done')
