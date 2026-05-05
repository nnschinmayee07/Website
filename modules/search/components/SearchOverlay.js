/**
 * SearchOverlay.js — Slide-out right-sidebar search panel
 * Appended directly to <body> to avoid stacking context issues.
 */
(function () {
    'use strict';

    var _config  = null;
    var _overlay = null;
    var _panel   = null;
    var _isOpen  = false;

    function build(config) {
        if (document.getElementById('mlrit-search-overlay')) return;
        _config = config || {};

        var el = document.createElement('div');
        el.id        = 'mlrit-search-overlay';
        el.className = 'search-overlay';
        el.setAttribute('role',       'dialog');
        el.setAttribute('aria-modal', 'true');
        el.setAttribute('aria-label', 'Search MLRIT');

        el.innerHTML = [
            '<div class="search-backdrop" id="mlrit-search-backdrop"></div>',
            '<aside class="search-panel" id="mlrit-search-panel" tabindex="-1">',
            '  <!-- SearchInput, FAQList, SearchResultsPreview injected here -->',
            '</aside>',
        ].join('');

        // Append to body — NOT inside header — to avoid stacking context inheritance
        document.body.appendChild(el);

        _overlay = el;
        _panel   = document.getElementById('mlrit-search-panel');

        // Backdrop click → close
        document.getElementById('mlrit-search-backdrop').addEventListener('click', function () {
            window.SearchOverlay.close();
        });

        // Escape key → close; Ctrl+K → toggle
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                window.SearchOverlay.close();
                return;
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                _isOpen ? window.SearchOverlay.close() : window.SearchOverlay.open();
            }
        });
    }

    function open() {
        if (!_overlay) return;
        _overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
        _isOpen = true;
        // Focus the input after transition starts
        setTimeout(function () {
            if (window.SearchInput) window.SearchInput.focus();
        }, 50);
    }

    function close() {
        if (!_overlay) return;
        _overlay.classList.remove('open');
        document.body.style.overflow = '';
        _isOpen = false;
        if (window.SearchInput) window.SearchInput.clear();
        if (window.SearchResultsPreview) {
            window.SearchResultsPreview.clear(document.getElementById('mlrit-search-panel'));
        }
        if (window.FAQList) window.FAQList.show();
    }

    function getPanel() { return _panel; }
    function isOpen()   { return _isOpen; }

    window.SearchOverlay = { build: build, open: open, close: close, getPanel: getPanel, isOpen: isOpen };

})();
