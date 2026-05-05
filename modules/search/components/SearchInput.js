/**
 * SearchInput.js — Input row component for the search overlay
 */
(function () {
    'use strict';

    var _inputEl = null;

    function render(container, callbacks) {
        var cb = callbacks || {};

        var row = document.createElement('div');
        row.className = 'search-input-row';
        row.innerHTML = [
            '<i class="fas fa-search search-input-icon" aria-hidden="true"></i>',
            '<input type="text" id="mlrit-search-input" class="search-input"',
            '       placeholder="Search departments, admissions, placements…"',
            '       autocomplete="off" spellcheck="false" aria-label="Search MLRIT">',
            '<button class="search-close-btn" id="mlrit-search-close-btn"',
            '        aria-label="Close search" title="Close (Esc)">&#x2715;</button>',
        ].join('');

        container.insertBefore(row, container.firstChild);
        _inputEl = document.getElementById('mlrit-search-input');

        // Input event
        _inputEl.addEventListener('input', function () {
            if (typeof cb.onInput === 'function') cb.onInput(_inputEl.value);
        });

        // Enter key → submit
        _inputEl.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                var val = _inputEl.value.trim();
                if (val && typeof cb.onSubmit === 'function') cb.onSubmit(val);
            }
        });

        // Close button
        document.getElementById('mlrit-search-close-btn').addEventListener('click', function () {
            if (typeof cb.onClose === 'function') cb.onClose();
        });
    }

    function focus() {
        var el = document.getElementById('mlrit-search-input');
        if (el) el.focus();
    }

    function getValue() {
        var el = document.getElementById('mlrit-search-input');
        return el ? el.value : '';
    }

    function setValue(str) {
        var el = document.getElementById('mlrit-search-input');
        if (el) el.value = String(str || '');
    }

    function clear() {
        setValue('');
    }

    window.SearchInput = { render: render, focus: focus, getValue: getValue, setValue: setValue, clear: clear };

})();
