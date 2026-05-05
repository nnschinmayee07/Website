/**
 * MLRIT Search System — index.js
 * Public API: SearchSystem.init(config), .open(), .close()
 *
 * LOADING ORDER (add to each HTML page in this order):
 *   <link rel="stylesheet" href="{path}modules/search/styles/search.css">
 *   <script src="{path}modules/search/utils/searchEngine.js"></script>
 *   <script src="{path}modules/search/components/SearchOverlay.js"></script>
 *   <script src="{path}modules/search/components/SearchInput.js"></script>
 *   <script src="{path}modules/search/components/FAQList.js"></script>
 *   <script src="{path}modules/search/components/SearchResultsPreview.js"></script>
 *   <script src="{path}modules/search/index.js"></script>
 *   Then call: SearchSystem.init({ basePath: '', apiBase: '', ... });
 */
(function () {
    'use strict';

    var _config      = null;
    var _initialized = false;

    // ── Default config ─────────────────────────────────────────────────
    var DEFAULTS = {
        basePath:   '',       // '' for root, '../' for /pages/ sub-pages
        apiBase:    '',       // '' = same origin; or 'http://host:port'
        faqItems:   [],       // [] = use FAQList defaults
        debounceMs: 300,
    };

    // ══════════════════════════════════════════════════════════════════
    // STICKY HEADER OVERFLOW AUDIT
    // Walks up from .top-header and warns if any ancestor has
    // overflow: hidden/auto/scroll (which breaks CSS sticky).
    // ══════════════════════════════════════════════════════════════════
    function auditStickyAncestors(headerEl) {
        var el = headerEl.parentElement;
        while (el && el !== document.body) {
            var style = window.getComputedStyle(el);
            var ov    = style.overflow + ' ' + style.overflowX + ' ' + style.overflowY;
            if (/hidden|auto|scroll/.test(ov)) {
                console.warn(
                    '[SearchSystem] Warning: sticky header may be broken by overflow on',
                    el,
                    '— overflow:', ov.trim()
                );
            }
            el = el.parentElement;
        }
    }

    // ══════════════════════════════════════════════════════════════════
    // INJECT SEARCH ICON into .top-header .header-right
    // ══════════════════════════════════════════════════════════════════
    function injectSearchIcon(basePath) {
        // Double-init guard
        if (document.getElementById('mlrit-search-icon')) return;

        var headerRight = document.querySelector('.top-header .header-right');
        if (!headerRight) {
            console.warn('[SearchSystem] .top-header .header-right not found — search icon not injected.');
            return;
        }

        var btn = document.createElement('button');
        btn.id        = 'mlrit-search-icon';
        btn.className = 'search-icon-btn';
        btn.setAttribute('aria-label', 'Open search');
        btn.setAttribute('title',      'Search MLRIT (Ctrl+K)');
        btn.innerHTML = '<i class="fas fa-search" aria-hidden="true"></i>';
        btn.addEventListener('click', function () {
            window.SearchSystem.open();
        });

        headerRight.appendChild(btn);

        // Audit ancestors for overflow issues
        var topHeader = document.querySelector('.top-header');
        if (topHeader) auditStickyAncestors(topHeader);
    }

    // ══════════════════════════════════════════════════════════════════
    // INJECT CHRONICLES LINK into .red-nav .main-nav
    // ══════════════════════════════════════════════════════════════════
    function injectChroniclesLink(basePath) {
        if (document.querySelector('.chronicles-nav-link')) return;
        var mainNav = document.querySelector('.red-nav .main-nav');
        if (!mainNav) return;

        var li = document.createElement('li');
        li.innerHTML = '<a href="' + basePath + 'pages/chronicles.html" class="chronicles-nav-link">CHRONICLES</a>';
        mainNav.appendChild(li);
    }

    // ══════════════════════════════════════════════════════════════════
    // INIT
    // ══════════════════════════════════════════════════════════════════
    function init(userConfig) {
        if (_initialized) return;
        _initialized = true;

        // Merge config with defaults
        _config = {
            basePath:   (userConfig && userConfig.basePath   !== undefined) ? String(userConfig.basePath)   : DEFAULTS.basePath,
            apiBase:    (userConfig && userConfig.apiBase    !== undefined) ? String(userConfig.apiBase)    : DEFAULTS.apiBase,
            faqItems:   (userConfig && Array.isArray(userConfig.faqItems))  ? userConfig.faqItems           : DEFAULTS.faqItems,
            debounceMs: (userConfig && typeof userConfig.debounceMs === 'number') ? userConfig.debounceMs   : DEFAULTS.debounceMs,
        };

        // 1. Build overlay DOM (appended to body)
        if (window.SearchOverlay) {
            window.SearchOverlay.build(_config);
        }

        var panel = document.getElementById('mlrit-search-panel');

        // 2. Render SearchInput inside panel
        if (window.SearchInput && panel) {
            window.SearchInput.render(panel, {
                onInput: function (value) {
                    if (value.trim().length > 0) {
                        if (window.FAQList) window.FAQList.hide();
                        if (window.SearchResultsPreview) {
                            window.SearchResultsPreview.showLoading(panel);
                        }
                        // Trigger debounced search
                        if (window.SearchEngine) {
                            window.SearchEngine.query(value, {
                                onLoading: function () {
                                    if (window.SearchResultsPreview) {
                                        window.SearchResultsPreview.showLoading(panel);
                                    }
                                },
                                onResults: function (siteResults, chroniclesResults) {
                                    if (window.SearchResultsPreview) {
                                        window.SearchResultsPreview.render(panel, {
                                            siteResults:       siteResults,
                                            chroniclesResults: chroniclesResults,
                                            query:             value,
                                            basePath:          _config.basePath,
                                        });
                                    }
                                },
                                onError: function (msg) {
                                    if (panel) {
                                        var errEl = document.getElementById('mlrit-search-preview');
                                        if (!errEl) {
                                            errEl = document.createElement('div');
                                            errEl.id = 'mlrit-search-preview';
                                            errEl.className = 'search-preview';
                                            panel.appendChild(errEl);
                                        }
                                        errEl.innerHTML =
                                            '<div class="search-empty">' +
                                            '<i class="fas fa-exclamation-triangle" aria-hidden="true"></i>' +
                                            '<p>' + String(msg || 'Search unavailable.') + '</p>' +
                                            '</div>';
                                    }
                                },
                            }, _config);
                        }
                    } else {
                        // Input cleared — show FAQ, clear preview
                        if (window.SearchResultsPreview) {
                            window.SearchResultsPreview.clear(panel);
                        }
                        if (window.FAQList) window.FAQList.show();
                    }
                },
                onClose: function () {
                    window.SearchSystem.close();
                },
                onSubmit: function (value) {
                    var q = value.trim();
                    if (!q) return;
                    window.SearchSystem.close();
                    window.location.href = _config.basePath + 'search-results.html?q=' + encodeURIComponent(q);
                },
            });
        }

        // 3. Render FAQList inside panel
        if (window.FAQList && panel) {
            window.FAQList.render(panel, {
                faqItems: _config.faqItems,
                basePath: _config.basePath,
            });
        }

        // 4. Inject search icon into .top-header
        injectSearchIcon(_config.basePath);

        // 5. Inject Chronicles link into red-nav
        injectChroniclesLink(_config.basePath);
    }

    function open() {
        if (window.SearchOverlay) window.SearchOverlay.open();
    }

    function close() {
        if (window.SearchOverlay) window.SearchOverlay.close();
    }

    window.SearchSystem = { init: init, open: open, close: close };

})();
