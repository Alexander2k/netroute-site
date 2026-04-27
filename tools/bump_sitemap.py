#!/usr/bin/env python3
"""
Refresh <lastmod> dates in sitemap.xml from each file's last git commit date.

For every <loc> URL, finds the corresponding local HTML file, reads its
last commit date via `git log -1 --format=%cs`, and updates the matching
<lastmod> to that date. Falls back to today for untracked files.

Run before commit when content changes:
    python3 tools/bump_sitemap.py

Companion test (tests/test_seo.py :: check_sitemap) verifies sitemap dates
are not older than the file's last commit.
"""

import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE_BASE = 'https://alexander2k.github.io/netroute-site'
SITEMAP = os.path.join(ROOT, 'sitemap.xml')

URL_BLOCK_RE = re.compile(
    r'(<url>\s*<loc>([^<]+)</loc>.*?<lastmod>)(\d{4}-\d{2}-\d{2})(</lastmod>)',
    re.DOTALL,
)


def url_to_file(url: str) -> str:
    if not url.startswith(SITE_BASE):
        return ''
    rel = url[len(SITE_BASE):].lstrip('/')
    if rel == '' or rel.endswith('/'):
        rel += 'index.html'
    return os.path.join(ROOT, rel)


def git_last_commit_date(rel_path: str) -> str:
    try:
        out = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cs', '--', rel_path],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
        ).strip()
        return out
    except subprocess.CalledProcessError:
        return ''


def main() -> int:
    if not os.path.exists(SITEMAP):
        print(f'sitemap not found: {SITEMAP}', file=sys.stderr)
        return 1

    with open(SITEMAP) as f:
        content = f.read()

    today = datetime.date.today().isoformat()
    updates = 0
    skipped = 0
    missing = []

    def replace(m: re.Match) -> str:
        nonlocal updates, skipped, missing
        prefix, loc, current, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
        target = url_to_file(loc)
        if not target or not os.path.exists(target):
            missing.append(loc)
            return m.group(0)
        rel = os.path.relpath(target, ROOT)
        date = git_last_commit_date(rel) or today
        if date <= current:
            skipped += 1
            return m.group(0)
        updates += 1
        print(f'  {loc}: {current} → {date}')
        return f'{prefix}{date}{suffix}'

    new_content = URL_BLOCK_RE.sub(replace, content)

    if new_content != content:
        with open(SITEMAP, 'w') as f:
            f.write(new_content)
        print(f'\nUpdated {updates} entries, skipped {skipped} (already current)')
    else:
        print(f'No changes — all {skipped} entries already current')

    if missing:
        print(f'\nWARN: {len(missing)} URL(s) had no local file:')
        for m in missing:
            print(f'  - {m}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
