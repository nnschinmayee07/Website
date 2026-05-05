/**
 * searchEngine.js — MLRIT Search Engine Utility
 * Handles: debounce, AbortController, Promise.allSettled,
 *          response normalization, highlight, typo correction
 */
(function () {
    'use strict';

    // ── Module-level state ─────────────────────────────────────────────
    let _debounceTimer = null;
    let _controller    = null;   // AbortController for in-flight requests

    // ══════════════════════════════════════════════════════════════════
    // RESPONSE NORMALIZATION
    // Maps raw API responses to a consistent shape before rendering.
    // Never returns undefined/null fields.
    // ══════════════════════════════════════════════════════════════════
    function normalizeResults(raw, type) {
        if (!raw || !Array.isArray(raw)) return [];
        return raw.map(function (item) {
            if (!item || typeof item !== 'object') {
                return { title: '', description: '', type: type, date: null, url: '#' };
            }
            return {
                title:       String(item.title       || ''),
                description: String(item.snippet     || item.summary     || item.description || ''),
                type:        type === 'news' ? 'news' : 'search',
                date:        item.date ? String(item.date) : null,
                url:         String(item.url         || item.link        || '#'),
            };
        });
    }

    // ══════════════════════════════════════════════════════════════════
    // TYPO CORRECTION — ported from legacy search.js
    // ══════════════════════════════════════════════════════════════════
    var TYPO_DICT = {
        'csee': 'cse', 'csse': 'cse', 'cse ': 'cse',
        'ecee': 'ece', 'eece': 'ece',
        'eeee': 'eee',
        'admissons': 'admissions', 'admision': 'admissions',
        'admisssions': 'admissions', 'addmissions': 'admissions',
        'placments': 'placements', 'placemants': 'placements',
        'placeements': 'placements', 'placemets': 'placements',
        'scholrships': 'scholarships', 'scholarhips': 'scholarships',
        'scolarships': 'scholarships',
        'examinatons': 'examinations', 'exams ': 'examinations',
        'mechnical': 'mechanical', 'mechanicl': 'mechanical',
        'aeronuatical': 'aeronautical', 'aeronatical': 'aeronautical',
        'infomation': 'information', 'infromation': 'information',
        'reserach': 'research', 'reasearch': 'research',
        'inovation': 'innovation', 'innovaton': 'innovation',
        'hostle': 'hostel', 'hostl': 'hostel',
        'campas': 'campus', 'campu': 'campus',
        'contect': 'contact', 'contcat': 'contact',
        'carees': 'careers', 'carers': 'careers',
        'sporst': 'sports', 'spors': 'sports',
        'placment': 'placements',
        'addmision': 'admissions',
    };

    var KNOWN_TERMS = [
        'cse','ece','eee','mechanical','aeronautical','it','mba','aiml',
        'csit','csbs','civil','freshman','admissions','placements','about',
        'contact','campus','sports','events','research','iqac','examinations',
        'scholarships','careers','innovation','hostel','fees','nirf','aicte',
        'naac','aqar','circulars','news','blog','virtual tour','data science',
        'cyber security','artificial intelligence','chronicles',
    ];

    function levenshtein(a, b) {
        var m = a.length, n = b.length;
        var dp = [];
        for (var i = 0; i <= m; i++) {
            dp[i] = [];
            for (var j = 0; j <= n; j++) {
                dp[i][j] = i === 0 ? j : j === 0 ? i : 0;
            }
        }
        for (var i = 1; i <= m; i++) {
            for (var j = 1; j <= n; j++) {
                dp[i][j] = a[i-1] === b[j-1]
                    ? dp[i-1][j-1]
                    : 1 + Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]);
            }
        }
        return dp[m][n];
    }

    function correctTypo(raw) {
        var q = String(raw || '').trim().toLowerCase();
        if (!q || q.length < 3) return { corrected: q, original: q, wasFixed: false };

        if (TYPO_DICT[q]) {
            return { corrected: TYPO_DICT[q], original: q, wasFixed: true };
        }

        if (q.length <= 15) {
            var best = null, bestDist = Infinity;
            for (var i = 0; i < KNOWN_TERMS.length; i++) {
                var term = KNOWN_TERMS[i];
                if (Math.abs(term.length - q.length) > 3) continue;
                var d = levenshtein(q, term);
                var threshold = q.length <= 5 ? 1 : 2;
                if (d <= threshold && d < bestDist) {
                    bestDist = d;
                    best = term;
                }
            }
            if (best && best !== q) {
                return { corrected: best, original: q, wasFixed: true };
            }
        }

        return { corrected: q, original: q, wasFixed: false };
    }

    // ══════════════════════════════════════════════════════════════════
    // KEYWORD HIGHLIGHT
    // Wraps ALL case-insensitive occurrences of query in <mark> tags.
    // ══════════════════════════════════════════════════════════════════
    function highlight(text, query) {
        if (!query || !query.trim()) return String(text || '');
        var safeText  = String(text || '');
        // Escape regex special characters in query
        var escaped   = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        var re        = new RegExp('(' + escaped + ')', 'gi');
        return safeText.replace(re, '<mark>$1</mark>');
    }

    // ══════════════════════════════════════════════════════════════════
    // QUERY — debounce + AbortController + Promise.allSettled
    // callbacks: { onLoading, onResults(siteResults, chroniclesResults), onError(msg) }
    // ══════════════════════════════════════════════════════════════════
    function query(rawQ, callbacks, config) {
        var cfg = config || {};
        var apiBase    = cfg.apiBase    || '';
        var debounceMs = cfg.debounceMs || 300;
        var cb         = callbacks || {};

        // Clear pending debounce
        if (_debounceTimer) {
            clearTimeout(_debounceTimer);
            _debounceTimer = null;
        }

        var q = String(rawQ || '').trim();
        if (!q) return;

        _debounceTimer = setTimeout(function () {
            _debounceTimer = null;

            // Cancel any in-flight request
            if (_controller) {
                try { _controller.abort(); } catch (e) { /* ignore */ }
            }
            _controller = new AbortController();
            var signal = _controller.signal;

            // Notify loading state
            if (typeof cb.onLoading === 'function') cb.onLoading();

            // Use static search data if available, otherwise fall back to API
            if (window.StaticSearchData) {
                // Static search (no API needed)
                setTimeout(function() {
                    // Get basePath from config ('' for root, '../' for subdirectories)
                    var basePath = cfg.basePath || '';
                    var siteResults = normalizeResults(window.StaticSearchData.search(q, basePath), 'search');
                    
                    // Search chronicles if available
                    var chroniclesResults = [];
                    if (window.ChroniclesData) {
                        var chroniclesRaw = window.ChroniclesData.search(q);
                        chroniclesResults = normalizeResults(chroniclesRaw.map(function(item) {
                            return {
                                title: item.title,
                                snippet: item.snippet,
                                date: item.date,
                                url: basePath + item.url
                            };
                        }), 'news');
                    }
                    
                    if (typeof cb.onResults === 'function') {
                        cb.onResults(siteResults, chroniclesResults);
                    }
                }, 100); // Small delay to simulate loading
            } else {
                // API-based search (original code)
                var searchUrl     = apiBase + '/search?q='          + encodeURIComponent(q);
                var chroniclesUrl = apiBase + '/api/chronicles?q='  + encodeURIComponent(q);

                Promise.allSettled([
                    fetch(searchUrl,     { signal: signal }).then(function (r) { return r.json(); }),
                    fetch(chroniclesUrl, { signal: signal }).then(function (r) { return r.json(); }),
                ]).then(function (results) {
                    var searchResult     = results[0];
                    var chroniclesResult = results[1];

                    // Silently ignore AbortError — a new query is already in flight
                    var searchAborted     = searchResult.status     === 'rejected' && searchResult.reason     && searchResult.reason.name === 'AbortError';
                    var chroniclesAborted = chroniclesResult.status === 'rejected' && chroniclesResult.reason && chroniclesResult.reason.name === 'AbortError';
                    if (searchAborted || chroniclesAborted) return;

                    var siteResults = searchResult.status === 'fulfilled'
                        ? normalizeResults(searchResult.value && searchResult.value.results ? searchResult.value.results : [], 'search')
                        : [];

                    var chroniclesResults = chroniclesResult.status === 'fulfilled'
                        ? normalizeResults(chroniclesResult.value && chroniclesResult.value.articles ? chroniclesResult.value.articles : [], 'news')
                        : [];

                    // Log non-abort errors as warnings (non-blocking)
                    if (searchResult.status === 'rejected' && !searchAborted) {
                        console.warn('[SearchEngine] /search failed:', searchResult.reason);
                    }
                    if (chroniclesResult.status === 'rejected' && !chroniclesAborted) {
                        console.warn('[SearchEngine] /api/chronicles failed:', chroniclesResult.reason);
                    }

                    // Both failed → show error
                    if (searchResult.status === 'rejected' && chroniclesResult.status === 'rejected') {
                        if (typeof cb.onError === 'function') {
                            cb.onError('Search unavailable. Please try again.');
                        }
                        return;
                    }

                    if (typeof cb.onResults === 'function') {
                        cb.onResults(siteResults, chroniclesResults);
                    }
                }).catch(function (err) {
                    // Catch-all safety net — should not normally fire with allSettled
                    if (err && err.name === 'AbortError') return;
                    console.error('[SearchEngine] Unexpected error:', err);
                    if (typeof cb.onError === 'function') {
                        cb.onError('Search unavailable. Please try again.');
                    }
                });
            }

        }, debounceMs);
    }

    // ── Public API ─────────────────────────────────────────────────────
    window.SearchEngine = {
        query:            query,
        highlight:        highlight,
        correctTypo:      correctTypo,
        normalizeResults: normalizeResults,
    };

})();
