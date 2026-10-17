#!/usr/bin/env python3
"""
Links from the hand-written guides to the generated ones: every classic guide's "related" list
(<h2 id="related">) gets one <li> per new guide that exists in the same language, with the title
and one-line description from tools/guide_content/<slug>_<lang>.py. Idempotent: a link that is
already there is not added again; nothing is removed.

    python3 tools/add_related_links.py
"""

import importlib.util
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONTENT = os.path.join(ROOT, 'tools', 'guide_content')
LANG_DIRS = {'en': '', 'ru': 'ru/', 'es': 'es/', 'zh': 'zh/'}
CLASSIC = ['keenetic', 'mikrotik', 'wireguard', 'linux', 'openvpn']
NEW = ['singbox', 'clash', 'xray', 'happ', 'shadowrocket', 'pac', 'amnezia', 'openwrt']


def load_page(slug: str, lang: str):
    path = os.path.join(CONTENT, f'{slug}_{lang}.py')
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location(f'gc.{slug}_{lang}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.PAGE


def main() -> int:
    changed = 0
    for lang, prefix in LANG_DIRS.items():
        pages = [(slug, load_page(slug, lang)) for slug in NEW]
        pages = [(slug, p) for slug, p in pages if p]
        if not pages:
            continue
        for guide in CLASSIC:
            path = os.path.join(ROOT, prefix, 'guides', f'{guide}.html')
            if not os.path.exists(path):
                continue
            with open(path, encoding='utf-8') as f:
                html = f.read()
            m = re.search(r'<h2 id="related">.*?<ul>\n(.*?)(\s*</ul>)', html, re.DOTALL)
            if not m:
                print(f'{os.path.relpath(path, ROOT)}: no related list', file=sys.stderr)
                continue
            items = ''
            for slug, page in pages:
                if f'href="./{slug}.html"' in m.group(0):
                    continue
                items += f'        <li><a href="./{slug}.html">{page["card"]["title"]}</a> &mdash; {page["related_desc"]}</li>\n'
            if not items:
                continue
            html = html[:m.end(1)] + items + html[m.end(1):]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            changed += 1
            print(f'updated: {os.path.relpath(path, ROOT)} (+{items.count("<li>")})')
    print(f'Done. Updated: {changed}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
