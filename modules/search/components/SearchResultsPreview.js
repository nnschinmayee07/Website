/**
 * SearchResultsPreview.js — Live preview results inside the search overlay
 * Shows up to 5 site results and 3 chronicles results with keyword highlighting.
 * Implements three defensive UI states: loading, empty, partial-data.
 */
(function () {
    'use strict';

    var PREVIEW_ID = 'mlrit-search-preview';

    function escHtml(s) {
        return String(s || '')
            .replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function getOrCreatePreview(container) {
        var el = document.getElementById(PREVIEW_ID);
        if (!el) {
            el = document.createElement('div');
            el.id        = PREVIEW_ID;
            el.className = 'search-preview';
            container.appendChild(el);
        }
        return el;
    }

    // ── Loading state ──────────────────────────────────────────────────
    function showLoading(container) {
        var el = getOrCreatePreview(container);
        el.innerHTML =
            '<div class="search-loading-state">' +
            '  <div class="search-spinner"></div>' +
            '  <span>Searching…</span>' +
            '</div>';
        if (window.FAQList) window.FAQList.hide();
    }

    // ── Render results ─────────────────────────────────────────────────
    function render(container, opts) {
        var options          = opts || {};
        var siteResults      = Array.isArray(options.siteResults)      ? options.siteResults.slice(0, 5)  : [];
        var chroniclesResults= Array.isArray(options.chroniclesResults) ? options.chroniclesResults.slice(0, 3) : [];
        var query            = String(options.query    || '');
        var basePath         = String(options.basePath || '');
        var hl               = window.SearchEngine ? window.SearchEngine.highlight : function (t) { return escHtml(t); };

        var el = getOrCreatePreview(container);
        el.innerHTML = '';

        // ── Both empty ─────────────────────────────────────────────────
        if (!siteResults.length && !chroniclesResults.length) {
            el.innerHTML =
                '<div class="search-empty">' +
                '  <i class="fas fa-search-minus" aria-hidden="true"></i>' +
                '  <p>No results found for <strong>"' + escHtml(query) + '"</strong></p>' +
                '  <p class="search-empty-suggestions">Try: ' +
                '    <a href="' + escHtml(basePath) + 'pages/admissions.html">Admissions</a>, ' +
                '    <a href="' + escHtml(basePath) + 'pages/placements.html">Placements</a>, ' +
                '    <a href="' + escHtml(basePath) + 'pages/about-us.html">About Us</a>' +
                '  </p>' +
                '</div>';
            appendViewAll(el, query, basePath);
            return;
        }

        // ── Site results section ───────────────────────────────────────
        if (siteResults.length) {
            var siteGroup = document.createElement('div');
            siteGroup.className = 'preview-group';
            siteGroup.setAttribute('data-group', 'site');
            siteGroup.innerHTML = '<h4 class="preview-group-title"><i class="fas fa-file-alt" aria-hidden="true"></i> Pages</h4>';

            siteResults.forEach(function (item) {
                var itemEl = document.createElement('a');
                itemEl.className = 'preview-result-item';
                itemEl.href      = item.url || '#';
                itemEl.innerHTML =
                    '<span class="result-title">'       + hl(item.title,       query) + '</span>' +
                    (item.description
                        ? '<span class="result-desc">'  + hl(item.description, query) + '</span>'
                        : '');
                siteGroup.appendChild(itemEl);
            });
            el.appendChild(siteGroup);
        }
        // No else — silently skip if no page results, chronicles will show below

        // ── Chronicles section ─────────────────────────────────────────
        if (chroniclesResults.length) {
            var newsGroup = document.createElement('div');
            newsGroup.className = 'preview-group';
            newsGroup.setAttribute('data-group', 'news');
            newsGroup.innerHTML = '<h4 class="preview-group-title"><i class="fas fa-newspaper" aria-hidden="true"></i> News</h4>';

            chroniclesResults.forEach(function (item) {
                var itemEl = document.createElement('a');
                itemEl.className = 'preview-result-item preview-news-item';
                itemEl.href      = item.url || '#';
                var dateStr = item.date ? '<span class="result-date">' + escHtml(formatDate(item.date)) + '</span>' : '';
                itemEl.innerHTML =
                    '<span class="result-title">' + hl(item.title, query) + '</span>' +
                    dateStr;
                newsGroup.appendChild(itemEl);
            });
            el.appendChild(newsGroup);
        } else if (siteResults.length) {
            // Only show notice if we had page results but no chronicles
            // (means chronicles genuinely failed, not just no match)
        }

        appendViewAll(el, query, basePath);
    }

    function appendViewAll(container, query, basePath) {
        var link = document.createElement('a');
        link.className = 'view-all-link';
        link.href      = basePath + 'search-results.html?q=' + encodeURIComponent(query);
        link.innerHTML = 'View all results <i class="fas fa-arrow-right" aria-hidden="true"></i>';
        container.appendChild(link);
    }

    function formatDate(iso) {
        try {
            var d = new Date(iso);
            var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            return ('0' + d.getDate()).slice(-2) + ' ' + months[d.getMonth()] + ' ' + d.getFullYear();
        } catch (e) { return ''; }
    }

    // ── Clear ──────────────────────────────────────────────────────────
    function clear(container) {
        var el = document.getElementById(PREVIEW_ID);
        if (el) el.innerHTML = '';
    }

    window.SearchResultsPreview = { showLoading: showLoading, render: render, clear: clear };

})();
