import glob, re

# Add onclick to all faculty-item divs in all department pages
# Each faculty-item should navigate to faculty-profile.html with params

for f in glob.glob('c:/mlr/homepage/departments/*.html'):
    if 'faculty-profile' in f:
        continue

    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Skip if already wired
    if 'faculty-profile.html' in content:
        print(f'{f}: already wired, skipping')
        continue

    # Add CSS for clickable faculty items (cursor is already pointer)
    # Add JS at the bottom that attaches click handlers to faculty items
    # The JS reads data from the popup and builds a URL

    click_js = '''
    // ── Faculty profile click handler ──
    (function () {
      document.querySelectorAll('.faculty-item').forEach(function (item) {
        item.addEventListener('click', function () {
          var popup = item.querySelector('.faculty-popup');
          if (!popup) return;
          var name = popup.querySelector('.faculty-popup__name');
          var role = popup.querySelector('.faculty-popup__role');
          var qual = popup.querySelector('.faculty-popup__detail');
          var photo = item.querySelector('.faculty-item__photo img');
          var tags = popup.querySelectorAll('.faculty-popup__tag');

          var n = name ? name.textContent : '';
          var r = role ? role.textContent : '';
          var q = qual ? qual.textContent.replace('Qualification: ', '') : '';
          var p = photo ? photo.getAttribute('src') : '';
          var areas = [];
          tags.forEach(function(t) { areas.push(t.textContent); });

          var id = n.toLowerCase().replace(/dr\\.|mr\\.|mrs\\.|ms\\.|prof\\./g, '').trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

          var url = 'faculty-profile.html?' +
            'name=' + encodeURIComponent(n) +
            '&role=' + encodeURIComponent(r) +
            '&qual=' + encodeURIComponent(q) +
            '&photo=' + encodeURIComponent(p) +
            '&areas=' + encodeURIComponent(areas.join(',')) +
            '#' + id;

          window.location.href = url;
        });
      });
    })();'''

    # Insert before </script>
    content = content.replace('  </script>', click_js + '\n  </script>')

    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(content)
    print(f'{f}: wired')
