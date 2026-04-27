#!/usr/bin/env python3
"""
Sync example config files from examples/ into inline <pre><code> blocks
inside each guide HTML page.

Source of truth: examples/<file>
Generated copies: inline blocks between <!-- EMBED:<file> --> and <!-- /EMBED -->

Run before commit when examples/ changes:
    python3 tools/embed_examples.py

The companion test (tests/test_seo.py :: check_guide_inline_example) verifies
that inline content stays in sync with the source files.
"""

import html as html_lib
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# guide stem  ->  examples/<file>
GUIDE_TO_FILE = {
    'keenetic':  'keenetic-routes.bat',
    'mikrotik':  'mikrotik-routes.rsc',
    'wireguard': 'wireguard-split-tunnel.conf',
    'linux':     'linux-routes.sh',
    'openvpn':   'openvpn-routes.ovpn',
}

LANG_PREFIXES = ['', 'ru/', 'es/', 'zh/']

CTA_SENTINEL = '<p><a href="https://github.com/Alexander2k/netroute-site/tree/main/examples"'


def make_block(filename: str, escaped_content: str) -> str:
    """Build the inline <pre><code> block with EMBED markers."""
    return (
        f'<pre><code><!-- EMBED:{filename} -->\n'
        f'{escaped_content}\n'
        f'<!-- /EMBED --></code></pre>\n\n    '
    )


def sync_one(html_content: str, filename: str, escaped_content: str) -> tuple[str, str]:
    """Update or insert the embed block for `filename` in `html_content`.
    Returns (new_html, action) where action in {'updated', 'inserted', 'skipped'}.
    """
    # Existing markers — replace inner content (idempotent re-sync)
    existing = re.compile(
        r'<pre><code><!--\s*EMBED:' + re.escape(filename) + r'\s*-->.*?<!--\s*/EMBED\s*--></code></pre>',
        re.DOTALL,
    )
    new_block_no_trailing_indent = (
        f'<pre><code><!-- EMBED:{filename} -->\n'
        f'{escaped_content}\n'
        f'<!-- /EMBED --></code></pre>'
    )
    if existing.search(html_content):
        return existing.sub(lambda _: new_block_no_trailing_indent, html_content), 'updated'

    # No markers yet — insert just before the CTA sentinel inside the examples section
    if CTA_SENTINEL not in html_content:
        return html_content, 'skipped'
    block = make_block(filename, escaped_content)
    return html_content.replace(CTA_SENTINEL, block + CTA_SENTINEL, 1), 'inserted'


def main() -> int:
    updated = inserted = skipped = 0
    errors: list[str] = []

    for prefix in LANG_PREFIXES:
        for guide, filename in GUIDE_TO_FILE.items():
            guide_path = os.path.join(ROOT, prefix, 'guides', f'{guide}.html')
            src_path = os.path.join(ROOT, 'examples', filename)

            if not os.path.exists(guide_path):
                errors.append(f'guide not found: {guide_path}')
                continue
            if not os.path.exists(src_path):
                errors.append(f'source not found: {src_path}')
                continue

            with open(src_path) as f:
                src = f.read().rstrip('\n')
            escaped = html_lib.escape(src, quote=False)

            with open(guide_path) as f:
                content = f.read()

            new_content, action = sync_one(content, filename, escaped)
            rel = os.path.relpath(guide_path, ROOT)
            if action == 'skipped':
                errors.append(f'{rel}: no insertion point (CTA sentinel not found) and no existing markers')
                continue
            if new_content != content:
                with open(guide_path, 'w') as f:
                    f.write(new_content)
            if action == 'updated':
                updated += 1
                print(f'updated:  {rel} ({filename})')
            elif action == 'inserted':
                inserted += 1
                print(f'inserted: {rel} ({filename})')

    print(f'\nDone. Updated: {updated}, Inserted: {inserted}, Skipped: {skipped}')
    if errors:
        print('\nERRORS:')
        for e in errors:
            print(' -', e)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
