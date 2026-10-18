#!/usr/bin/env python3
"""
theme.js no longer blocks rendering: every page gets a one-line inline script in <head> that
applies a saved theme before the first paint (the only part that has to run that early), and
theme.js itself is loaded with `defer` (toggle button, labels, view transition). theme.js keeps
applying the saved theme too — doing it twice is harmless.

    python3 tools/defer_theme_script.py        # idempotent; also run after adding pages

CSP of the site allows 'unsafe-inline' scripts, so the inline line needs no hash.
"""

import os
import re
import sys
from glob import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Same key and values as theme.js
INLINE = ("<script>try{var t=localStorage.getItem('netroute-theme');"
          "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>")

SYNC = re.compile(r'(?m)^(\s*)<script src="([^"]*theme\.js)"></script>\n')


def main() -> int:
    changed = 0
    for path in sorted(glob(f'{ROOT}/**/*.html', recursive=True)):
        with open(path, encoding='utf-8') as f:
            html = f.read()
        m = SYNC.search(html)
        if not m:
            continue
        indent, src = m.group(1), m.group(2)
        repl = f'{indent}{INLINE}\n{indent}<script src="{src}" defer></script>\n'
        html = html[:m.start()] + repl + html[m.end():]
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(html)
        changed += 1
    print(f'pages updated: {changed}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
