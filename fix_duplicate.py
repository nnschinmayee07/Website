content = open('index.html', 'r', encoding='utf-8').read()

# Remove the duplicate chronicles section
duplicate = """    <!-- =====================
         8. MLRIT CHRONICLES
         ===================== -->
    <section class="chronicles-section" id="chronicles">
      <div class="section-wrap">
        <div class="chronicles-header">
          <span class="section-label reveal">Latest Updates</span>
          <h2 class="section-heading reveal" data-delay="1">MLRIT Chronicles</h2>
          <p class="section-sub reveal" data-delay="2">Stay updated with the latest news, achievements, and events from MLRIT</p>
        </div>

        <div class="chronicles-grid" id="chroniclesHomeGrid">
          <!-- Chronicles will be loaded here by JavaScript -->
        </div>

        <div class="chronicles-view-all">
          <a href="chronicles.html" class="btn-view-all">View All Chronicles <i class="fas fa-arrow-right"></i></a>
        </div>
      </div>
    </section>

    <!-- =====================
         8. MLRIT CHRONICLES
         ===================== -->
    <section class="chronicles-section" id="chronicles">"""

replacement = """    <!-- =====================
         8. MLRIT CHRONICLES
         ===================== -->
    <section class="chronicles-section" id="chronicles">"""

content = content.replace(duplicate, replacement, 1)

open('index.html', 'w', encoding='utf-8').write(content)
print('Done - duplicate removed')
print('Chronicles sections remaining:', content.count('id="chronicles"'))
