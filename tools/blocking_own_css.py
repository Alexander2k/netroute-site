#!/usr/bin/env python3
"""
The site's own stylesheet is loaded render-blocking (style.min.css) instead of the async
preload+onload pattern: with the async pattern the first frame was painted unstyled and the whole
body shifted when the CSS arrived — Lighthouse measured CLS 0.43 on desktop. Fonts stay async.

    python3 tools/blocking_own_css.py      # idempotent
"""

import os
import re
import sys
from glob import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAIR = re.compile(
    r'(?m)^(\s*)<link rel="preload" as="style" href="([^"]*)style\.css" onload="this\.onload=null;this\.rel=\'stylesheet\'">\n'
    r'\s*<noscript><link rel="stylesheet" href="\2style\.css"></noscript>\n')


def main() -> int:
    changed = 0
    for path in sorted(glob(f'{ROOT}/**/*.html', recursive=True)):
        with open(path, encoding='utf-8') as f:
            html = f.read()
        new = PAIR.sub(lambda m: f'{m.group(1)}<link rel="stylesheet" href="{m.group(2)}style.min.css">\n', html)
        if new != html:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(new)
            changed += 1
    print(f'pages updated: {changed}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
