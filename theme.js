/*
 * Theme switch for the NetRoute site.
 * Loaded synchronously in <head> so a saved choice applies before the first paint
 * (no light flash on a dark page). Without a saved choice the system preference
 * (prefers-color-scheme) decides, as before. The toggle button is added to the top bar.
 */
(function () {
    'use strict';

    var KEY = 'netroute-theme';
    var root = document.documentElement;
    var media = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

    function saved() {
        try {
            var value = localStorage.getItem(KEY);
            return value === 'light' || value === 'dark' ? value : null;
        } catch (e) {
            return null;
        }
    }

    function current() {
        return saved() || (media && media.matches ? 'dark' : 'light');
    }

    var BAR = { light: '#f8fafd', dark: '#131314' };

    function applyTheme(theme) {
        root.setAttribute('data-theme', theme);
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.setAttribute('content', BAR[theme]);
    }

    // Before the first paint: only a stored choice forces a theme
    if (saved()) applyTheme(saved());

    var LABELS = {
        en: ['Switch to dark theme', 'Switch to light theme'],
        ru: ['Включить тёмную тему', 'Включить светлую тему'],
        es: ['Cambiar al tema oscuro', 'Cambiar al tema claro'],
        zh: ['切换到深色主题', '切换到浅色主题']
    };

    function label(theme) {
        var lang = (root.getAttribute('lang') || 'en').slice(0, 2);
        var pair = LABELS[lang] || LABELS.en;
        return theme === 'dark' ? pair[1] : pair[0];
    }

    var SVG = '<svg class="theme-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/>' +
        '<path d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8 6 18M18 6l1.8-1.8"/></svg>' +
        '<svg class="theme-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7z"/></svg>';

    function syncButton(button) {
        var theme = current();
        button.setAttribute('aria-label', label(theme));
        button.setAttribute('title', label(theme));
        button.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    }

    function toggle(event, button) {
        var next = current() === 'dark' ? 'light' : 'dark';
        var commit = function () {
            try { localStorage.setItem(KEY, next); } catch (e) { /* private mode: still switch */ }
            applyTheme(next);
            syncButton(button);
        };
        var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (!document.startViewTransition || reduce) {
            commit();
            return;
        }
        // Material Expressive: the new theme spreads as a circle from the button
        var rect = button.getBoundingClientRect();
        var x = event && event.clientX ? event.clientX : rect.left + rect.width / 2;
        var y = event && event.clientY ? event.clientY : rect.top + rect.height / 2;
        var radius = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
        var transition = document.startViewTransition(commit);
        transition.ready.then(function () {
            root.animate(
                { clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + radius + 'px at ' + x + 'px ' + y + 'px)'] },
                { duration: 560, easing: 'cubic-bezier(.2, 0, 0, 1)', pseudoElement: '::view-transition-new(root)' }
            );
        }).catch(function () { /* transition skipped: the theme is already applied */ });
    }

    function mount() {
        var bar = document.querySelector('.topbar-inner');
        if (!bar || bar.querySelector('.theme-toggle')) return;
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'theme-toggle';
        button.innerHTML = SVG;
        syncButton(button);
        button.addEventListener('click', function (event) { toggle(event, button); });

        var nav = bar.querySelector('.nav-links');
        var lang = nav && nav.querySelector('.lang-switch');
        if (lang) nav.insertBefore(button, lang);
        else if (nav) nav.appendChild(button);
        else bar.appendChild(button);

        // Follow the system while the user has not chosen
        if (media && media.addEventListener) {
            media.addEventListener('change', function () { if (!saved()) syncButton(button); });
        }
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
    else mount();
})();
