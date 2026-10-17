#!/usr/bin/env python3
"""
Twitter Card meta tags for every content page that has Open Graph tags but no twitter:card:
summary_large_image with the og:title, og:description and og:image of the page. Inserted right
after the og:locale (or the last og:) tag. Idempotent.

    python3 tools/add_twitter_cards.py
"""

import os
import re
import sys
from glob import glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKIP = re.compile(r'^(yandex_|google[0-9a-f]+\.html$|404\.html$)')


def og(content: str, prop: str):
    m = re.search(rf'<meta\s+property="{re.escape(prop)}"\s+content="([^"]*)"', content)
    return m.group(1) if m else None


def main() -> int:
    added = skipped = 0
    for path in sorted(glob(f'{ROOT}/**/*.html', recursive=True)):
        if SKIP.match(os.path.basename(path)):
            continue
        with open(path, encoding='utf-8') as f:
            html = f.read()
        if 'name="twitter:card"' in html:
            skipped += 1
            continue
        title, desc, image = og(html, 'og:title'), og(html, 'og:description'), og(html, 'og:image')
        if not (title and desc and image):
            print(f'no Open Graph tags, skipped: {os.path.relpath(path, ROOT)}', file=sys.stderr)
            continue
        anchor = re.search(r'    <meta property="og:locale" content="[^"]*">\n', html) or \
            list(re.finditer(r'    <meta property="og:[^"]+" content="[^"]*">\n', html))[-1]
        block = (f'    <meta name="twitter:card" content="summary_large_image">\n'
                 f'    <meta name="twitter:title" content="{title}">\n'
                 f'    <meta name="twitter:description" content="{desc}">\n'
                 f'    <meta name="twitter:image" content="{image}">\n')
        html = html[:anchor.end()] + block + html[anchor.end():]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        added += 1
        print(f'added: {os.path.relpath(path, ROOT)}')
    print(f'Done. Added: {added}, already present: {skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
