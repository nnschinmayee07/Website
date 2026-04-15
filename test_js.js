    (function(){var tabs=document.querySelectorAll('.dept-tab');var panels=document.querySelectorAll('.dept-panel');var qbtns=document.querySelectorAll('.qbar__btn');function sw(id){tabs.forEach(function(t){t.classList.remove('is-active')});panels.forEach(function(p){p.classList.remove('is-active')});qbtns.forEach(function(q){q.classList.remove('is-active')});var tab=document.querySelector('[data-tab="'+id+'"]');var panel=document.getElementById('panel-'+id);var qbtn=document.querySelector('[data-qtab="'+id+'"]');if(tab)tab.classList.add('is-active');if(panel)panel.classList.add('is-active');if(qbtn)qbtn.classList.add('is-active')}tabs.forEach(function(t){t.addEventListener('click',function(){sw(t.getAttribute('data-tab'))})});qbtns.forEach(function(b){b.addEventListener('click',function(){sw(b.getAttribute('data-qtab'))})});var hash=window.location.hash.replace('#','');if(hash)sw(hash)})();
    (function(){document.querySelectorAll('[data-achieve]').forEach(function(card){var toggle=card.querySelector('.achieve-toggle');card.addEventListener('click',function(){var expanded=card.classList.toggle('is-expanded');if(toggle)toggle.textContent=expanded?'Read Less':'Read More'})})})();
    (function(){document.querySelectorAll('.fcard').forEach(function(item){item.addEventListener('click',function(){var backBtn=item.querySelector('.fcard__back-btn');if(backBtn){var n=item.querySelector('.fcard__back-name');var r=item.querySelector('.fcard__back-role');var img=item.querySelector('.fcard__front img');window.location.href='faculty-profile.html?name='+encodeURIComponent(n?n.textContent:'')+'&role='+encodeURIComponent(r?r.textContent:'')+'&photo='+encodeURIComponent(img?img.getAttribute('src'):'')}})})})();
    // Dark sidebar — show items for active tab
    (function () {
      var dsItems = document.querySelectorAll('.ds-item');
      var streak = document.getElementById('navStreak');

      function fireStreak() {
        if (!streak) return;
        streak.classList.remove('is-firing');
        void streak.offsetWidth;
        streak.classList.add('is-firing');
        setTimeout(function () { streak.classList.remove('is-firing'); }, 600);
      }

      function updateSidebar(activeTab) {
        dsItems.forEach(function (item) {
          var show = item.getAttribute('data-ds-tab') === activeTab;
          item.style.display = show ? 'flex' : 'none';
          item.classList.remove('is-active');
        });
        // Activate first visible item
        var first = document.querySelector('.ds-item[data-ds-tab="' + activeTab + '"]');
        if (first) first.classList.add('is-active');
      }

      // Hook into tab clicks
      document.querySelectorAll('.dept-tab').forEach(function (tab) {
        tab.addEventListener('click', function () {
          updateSidebar(tab.getAttribute('data-tab'));
          fireStreak();
        });
      });

      // Hook into qbar clicks
      document.querySelectorAll('.qbar__btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          updateSidebar(btn.getAttribute('data-qtab'));
          fireStreak();
        });
      });

      // Sidebar item click — mark active + fire streak
      dsItems.forEach(function (item) {
        item.addEventListener('click', function () {
          var siblings = document.querySelectorAll('.ds-item[data-ds-tab="' + item.getAttribute('data-ds-tab') + '"]');
          siblings.forEach(function (s) { s.classList.remove('is-active'); });
          item.classList.add('is-active');
          fireStreak();
        });
      });

      // Initialize
      updateSidebar('overview');
    })();
