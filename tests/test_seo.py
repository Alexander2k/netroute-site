#!/usr/bin/env python3
"""
SEO/structural test suite for NetRoute Pro static site.

Run: python3 tests/test_seo.py
Exit code: 0 = all pass, 1 = failures.

Covers:
  - HTML well-formedness
  - <title> / <meta description> presence and length
  - Canonical URL matches file path
  - hreflang alternates point to existing files
  - JSON-LD blocks parse and required fields are present per @type
  - BreadcrumbList: middle items have "item" field; positions sequential
  - HowTo: name, step[].name, step[].text
  - FAQPage: mainEntity[].name and .acceptedAnswer.text
  - SoftwareApplication: name, applicationCategory, operatingSystem, offers/aggregateRating
  - sitemap.xml: every <loc> exists as file; every content HTML appears in sitemap
"""

import os
import re
import sys
import json
from glob import glob
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE_BASE = 'https://alexander2k.github.io/netroute-site'

EXCLUDED_HTML_BASENAMES_RE = re.compile(r'^(yandex_|google[0-9a-f]+\.html$)')
NON_CONTENT_HTML = {'404.html'}


def is_content_html(path: str) -> bool:
    base = os.path.basename(path)
    if base in NON_CONTENT_HTML:
        return False
    if EXCLUDED_HTML_BASENAMES_RE.match(base):
        return False
    return True


def file_to_url(path: str) -> str:
    """Convert local file path to canonical URL."""
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if rel == 'index.html' or rel.endswith('/index.html'):
        rel = rel[:-len('index.html')]
    return f'{SITE_BASE}/{rel}'


def url_to_file(url: str) -> str:
    """Convert canonical URL to local file path."""
    if not url.startswith(SITE_BASE):
        return ''
    rel = url[len(SITE_BASE):].lstrip('/')
    if rel == '' or rel.endswith('/'):
        rel += 'index.html'
    return os.path.join(ROOT, rel)


class FailFastParser(HTMLParser):
    def error(self, msg):
        raise ValueError(msg)


# ────────────────────────────────────────────────────────────────────
# Test runner

class Failures(list):
    def add(self, file: str, msg: str):
        self.append(f'[{os.path.relpath(file, ROOT)}] {msg}')


def collect_html_files() -> list:
    files = sorted(glob(f'{ROOT}/**/*.html', recursive=True))
    return [f for f in files if is_content_html(f)]


def extract_meta(content: str, name_or_property: str, attr: str = 'name') -> str | None:
    m = re.search(
        rf'<meta\s+{attr}="{re.escape(name_or_property)}"\s+content="([^"]*)"',
        content,
    )
    return m.group(1) if m else None


def extract_title(content: str) -> str | None:
    m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    return m.group(1).strip() if m else None


def extract_canonical(content: str) -> str | None:
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    return m.group(1) if m else None


def extract_hreflangs(content: str) -> list:
    return re.findall(
        r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"',
        content,
    )


def extract_jsonld_blocks(content: str) -> list:
    return re.findall(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        content,
        re.DOTALL,
    )


# ────────────────────────────────────────────────────────────────────
# Individual checks

def check_html_wellformed(path: str, content: str, fails: Failures):
    try:
        FailFastParser().feed(content)
    except Exception as e:
        fails.add(path, f'HTML parse error: {e}')


def check_title(path: str, content: str, fails: Failures):
    t = extract_title(content)
    if not t:
        fails.add(path, 'missing <title>')
        return
    if len(t) < 10:
        fails.add(path, f'title too short ({len(t)} chars): "{t}"')
    if len(t) > 130:
        fails.add(path, f'title too long ({len(t)} chars): "{t[:60]}..."')


def check_meta_description(path: str, content: str, fails: Failures):
    d = extract_meta(content, 'description')
    if not d:
        fails.add(path, 'missing meta description')
        return
    if len(d) < 50:
        fails.add(path, f'description too short ({len(d)} chars)')
    if len(d) > 200:
        fails.add(path, f'description too long ({len(d)} chars)')


def check_canonical(path: str, content: str, fails: Failures):
    c = extract_canonical(content)
    if not c:
        fails.add(path, 'missing rel=canonical')
        return
    expected = file_to_url(path)
    if c != expected:
        fails.add(path, f'canonical mismatch: got "{c}", expected "{expected}"')


def check_hreflangs(path: str, content: str, fails: Failures):
    alts = extract_hreflangs(content)
    if not alts:
        return  # ok if not multilingual
    seen_langs = set()
    for lang, href in alts:
        if lang in seen_langs:
            fails.add(path, f'duplicate hreflang="{lang}"')
        seen_langs.add(lang)
        if href.startswith(SITE_BASE):
            target = url_to_file(href)
            if target and not os.path.exists(target):
                fails.add(path, f'hreflang="{lang}" points to missing file: {href}')
    if 'x-default' not in seen_langs:
        fails.add(path, 'missing hreflang="x-default"')


def check_jsonld(path: str, content: str, fails: Failures):
    for i, raw in enumerate(extract_jsonld_blocks(content)):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            fails.add(path, f'JSON-LD block {i} invalid JSON: {e}')
            continue
        t = data.get('@type', '?')

        if t == 'BreadcrumbList':
            items = data.get('itemListElement', [])
            for j, it in enumerate(items):
                pos = it.get('position')
                if pos != j + 1:
                    fails.add(path, f'BreadcrumbList item[{j}] position={pos}, expected {j+1}')
                if 'name' not in it:
                    fails.add(path, f'BreadcrumbList pos {pos} missing "name"')
                is_last = (j == len(items) - 1)
                if 'item' not in it and not is_last:
                    fails.add(path, f'BreadcrumbList pos {pos} ("{it.get("name","")}") missing "item"')

        elif t == 'HowTo':
            for fld in ['name', 'step']:
                if fld not in data:
                    fails.add(path, f'HowTo missing "{fld}"')
            for j, step in enumerate(data.get('step', [])):
                if step.get('@type') != 'HowToStep':
                    fails.add(path, f'HowTo step[{j}] @type wrong: {step.get("@type")}')
                if 'name' not in step:
                    fails.add(path, f'HowTo step[{j}] missing "name"')
                if 'text' not in step:
                    fails.add(path, f'HowTo step[{j}] missing "text"')

        elif t == 'FAQPage':
            qs = data.get('mainEntity', [])
            if not qs:
                fails.add(path, 'FAQPage has no mainEntity')
            for j, q in enumerate(qs):
                if q.get('@type') != 'Question':
                    fails.add(path, f'FAQPage q[{j}] not Question type')
                if 'name' not in q:
                    fails.add(path, f'FAQPage q[{j}] missing "name"')
                ans = q.get('acceptedAnswer', {})
                if ans.get('@type') != 'Answer':
                    fails.add(path, f'FAQPage q[{j}] acceptedAnswer not Answer')
                if 'text' not in ans:
                    fails.add(path, f'FAQPage q[{j}] Answer missing "text"')

        elif t in ('SoftwareApplication', 'WebApplication'):
            for fld in ['name', 'applicationCategory', 'operatingSystem']:
                if fld not in data:
                    fails.add(path, f'{t} missing "{fld}"')
            if 'offers' not in data and 'aggregateRating' not in data:
                fails.add(path, f'{t} missing both "offers" and "aggregateRating"')


def _is_guide_leaf(path: str) -> bool:
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    parts = rel.split('/')
    return 'guides' in parts and parts[-1] != 'index.html'


def check_guide_official_docs(path: str, content: str, fails: Failures):
    """Every guide leaf page must have an h2 with id=official-docs anchor.
    SEO target: ловит запросы '* official documentation/docs/quickstart'.
    """
    if not _is_guide_leaf(path):
        return
    if not re.search(r'<h2[^>]*\bid="official-docs"', content):
        fails.add(path, 'guide page missing <h2 id="official-docs"> anchor')


def _is_home_index(path: str) -> bool:
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    return rel == 'index.html' or re.match(r'^(ru|es|zh)/index\.html$', rel) is not None


def check_home_brand_signals(path: str, content: str, fails: Failures):
    """Home pages must carry brand signals in SoftwareApplication schema:
    alternateName (catches 'netroute' lowercase / variations) and sameAs
    (links to authoritative profiles: Chrome Web Store, GitHub).
    """
    if not _is_home_index(path):
        return
    apps = []
    for raw in extract_jsonld_blocks(content):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if data.get('@type') == 'SoftwareApplication':
            apps.append(data)
    if not apps:
        fails.add(path, 'home page missing SoftwareApplication schema')
        return
    app = apps[0]
    if 'alternateName' not in app:
        fails.add(path, 'SoftwareApplication missing "alternateName" (brand variants)')
    if 'sameAs' not in app:
        fails.add(path, 'SoftwareApplication missing "sameAs" (authority links)')


def check_guide_related_links(path: str, content: str, fails: Failures):
    """Each guide leaf should link to the other 4 guides in the same language
    (internal weight distribution + UX). Look for the section anchored as 'related'.
    """
    if not _is_guide_leaf(path):
        return
    if not re.search(r'<h2[^>]*\bid="related"', content):
        fails.add(path, 'guide page missing <h2 id="related"> section')
        return
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    own = rel.split('/')[-1].replace('.html', '')
    others = [g for g in ('keenetic', 'mikrotik', 'wireguard', 'linux', 'openvpn') if g != own]
    for o in others:
        # Must link to ./<other>.html (sibling in same language)
        if f'href="./{o}.html"' not in content and f'href="{o}.html"' not in content:
            fails.add(path, f'guide page missing related link to ./{o}.html')


def check_guide_examples(path: str, content: str, fails: Failures):
    """Every guide leaf page must have an examples section with a GitHub link.
    SEO target: ловит запросы 'free wireguard config', 'github openvpn config', etc.
    """
    if not _is_guide_leaf(path):
        return
    # find a section/h2 with id="examples" and a github.com link inside or following it
    if not re.search(r'<(?:section|h2)[^>]*\bid="examples"', content):
        fails.add(path, 'guide page missing id="examples" anchor')
        return
    # Check there is at least one github.com link on the page (in body section)
    if 'github.com' not in content:
        fails.add(path, 'guide page has examples anchor but no github.com link')


def check_sitemap(fails: Failures):
    sitemap_path = f'{ROOT}/sitemap.xml'
    if not os.path.exists(sitemap_path):
        fails.add(sitemap_path, 'sitemap.xml not found')
        return
    with open(sitemap_path) as f:
        sm = f.read()
    locs = re.findall(r'<loc>([^<]+)</loc>', sm)

    # every loc must exist as file
    for loc in locs:
        target = url_to_file(loc)
        if not target:
            fails.add(sitemap_path, f'sitemap loc outside site base: {loc}')
            continue
        if not os.path.exists(target):
            fails.add(sitemap_path, f'sitemap loc has no file: {loc} → {target}')

    # every content HTML must appear in sitemap
    locs_set = set(locs)
    for f_ in collect_html_files():
        url = file_to_url(f_)
        if url not in locs_set:
            fails.add(sitemap_path, f'content HTML missing from sitemap: {url}')

    # lastmod format
    for date_str in re.findall(r'<lastmod>([^<]+)</lastmod>', sm):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            fails.add(sitemap_path, f'lastmod not ISO date: {date_str}')


# ────────────────────────────────────────────────────────────────────
# Main

def main():
    fails = Failures()
    files = collect_html_files()
    print(f'Checking {len(files)} HTML files…')
    for path in files:
        with open(path) as f:
            content = f.read()
        check_html_wellformed(path, content, fails)
        check_title(path, content, fails)
        check_meta_description(path, content, fails)
        check_canonical(path, content, fails)
        check_hreflangs(path, content, fails)
        check_jsonld(path, content, fails)
        check_guide_official_docs(path, content, fails)
        check_guide_examples(path, content, fails)
        check_home_brand_signals(path, content, fails)
        check_guide_related_links(path, content, fails)
    check_sitemap(fails)

    if fails:
        print(f'\n❌ {len(fails)} failure(s):\n')
        for f in fails:
            print(' -', f)
        sys.exit(1)
    print(f'\n✅ All checks passed ({len(files)} HTML files + sitemap).')


if __name__ == '__main__':
    main()
