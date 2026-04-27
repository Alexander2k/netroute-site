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

import html
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


def check_home_organization_schema(path: str, content: str, fails: Failures):
    """Each home index must carry an Organization schema with name, url,
    logo, and sameAs links (Chrome Web Store + GitHub) — strengthens brand
    entity for Google's Knowledge Graph.
    """
    if not _is_home_index(path):
        return
    org = None
    for raw in extract_jsonld_blocks(content):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if data.get('@type') == 'Organization':
            org = data
            break
    if org is None:
        fails.add(path, 'home page missing Organization schema')
        return
    for fld in ('name', 'url', 'logo', 'sameAs'):
        if fld not in org:
            fails.add(path, f'Organization schema missing "{fld}"')


def check_home_popular_guides(path: str, content: str, fails: Failures):
    """Each home index must have a 'Popular Guides' section linking to all 5
    guide leaves (in the same language). Uses deep anchors to syntax/examples
    sections to surface long-tail keywords from inside the guides.
    """
    if not _is_home_index(path):
        return
    if not re.search(r'<(?:section|h2)[^>]*\bid="popular-guides"', content):
        fails.add(path, 'home page missing id="popular-guides" section')
        return
    # Each guide must be linked from the page (relative path inside same-lang area).
    for guide in ('keenetic', 'mikrotik', 'wireguard', 'linux', 'openvpn'):
        # Accept any href ending with guides/<guide>.html (with optional anchor)
        if not re.search(rf'href="[^"]*guides/{re.escape(guide)}\.html(?:#[^"]*)?"', content):
            fails.add(path, f'home page missing link to guides/{guide}.html')


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


EMBED_RE = re.compile(
    r'<!--\s*EMBED:(\S+?)\s*-->(.*?)<!--\s*/EMBED\s*-->',
    re.DOTALL,
)


CHECKBOX_LABELS = {
    'en': 'Include comments in exported files',
    'ru': 'Включать комментарии в экспортируемые файлы',
    'es': 'Incluir comentarios en archivos exportados',
    'zh': '在导出文件中包含注释',
}


def _guide_lang(path: str) -> str:
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    parts = rel.split('/')
    if parts[0] in ('ru', 'es', 'zh'):
        return parts[0]
    return 'en'


def check_guide_comments_toggle_note(path: str, content: str, fails: Failures):
    """Each guide leaf must reference the extension's 'Include comments...'
    checkbox so users know they can generate routes without inline comments
    (some routers like certain Keenetic firmwares don't tolerate them).
    """
    if not _is_guide_leaf(path):
        return
    lang = _guide_lang(path)
    label = CHECKBOX_LABELS[lang]
    if label not in content:
        fails.add(path, f'guide page missing reference to checkbox label "{label}" ({lang})')


def check_guide_article_schema(path: str, content: str, fails: Failures):
    """Each guide leaf should have an Article schema (in addition to HowTo)
    so Google can pick either as a rich snippet. Required: headline, author,
    datePublished, image.
    """
    if not _is_guide_leaf(path):
        return
    has_article = False
    for raw in extract_jsonld_blocks(content):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        t = data.get('@type')
        if t in ('Article', 'TechArticle'):
            has_article = True
            for fld in ('headline', 'author', 'datePublished', 'image'):
                if fld not in data:
                    fails.add(path, f'{t} schema missing "{fld}"')
            break
    if not has_article:
        fails.add(path, 'guide page missing Article/TechArticle schema')


def check_guide_inline_example(path: str, content: str, fails: Failures):
    """Each guide leaf must inline the corresponding examples/<file> contents
    between <!-- EMBED:<file> --> ... <!-- /EMBED --> markers, and the inlined
    content must stay in sync with the source file in examples/.
    """
    if not _is_guide_leaf(path):
        return
    m = EMBED_RE.search(content)
    if not m:
        fails.add(path, 'guide page missing inline example block (EMBED marker)')
        return
    filename = m.group(1).strip()
    embedded = m.group(2)
    src_path = os.path.join(ROOT, 'examples', filename)
    if not os.path.exists(src_path):
        fails.add(path, f'embed references non-existent file: examples/{filename}')
        return
    with open(src_path) as f:
        src = f.read().rstrip('\n')
    # strip leading/trailing blank lines around marker, un-escape HTML entities
    embedded_inner = embedded.strip('\n')
    embedded_inner = html.unescape(embedded_inner).rstrip('\n')
    if embedded_inner != src:
        fails.add(path, f'embed content drift: examples/{filename} differs from inline block')


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


def check_keenetic_guide_correct_cli(path: str, content: str, fails: Failures):
    """Keenetic guide must not present PowerShell `New-NetRoute -destinationprefix`
    syntax as Keenetic CLI — that's a Windows PowerShell cmdlet, not RouterOS-style
    Keenetic CLI. Real Keenetic CLI for routes is `ip route <CIDR> <interface>`.
    """
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if not rel.endswith('guides/keenetic.html'):
        return
    if 'new-netroute -destinationprefix' in content:
        fails.add(path, 'Keenetic guide presents PowerShell New-NetRoute as Keenetic CLI (it is a Windows PowerShell cmdlet)')


def check_openvpn_guide_correct_route_nopull(path: str, content: str, fails: Failures):
    """OpenVPN guide must not advise removing route-nopull as a fix for
    "route directives ignored" — route-nopull only filters server-pushed routes,
    it does NOT block locally-defined `route` directives. Removing it breaks
    split tunneling.
    """
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if not rel.endswith('guides/openvpn.html'):
        return
    # Anti-pattern: doc claims route-nopull causes local route directives to be ignored
    bad_phrases = [
        'route-nopull</code> or a <code>--pull-filter</code> that drops them',
        'contiene <code>route-nopull</code>',  # Spanish equivalent if added
    ]
    for phrase in bad_phrases:
        if phrase in content:
            fails.add(path, f'OpenVPN guide wrongly blames route-nopull for ignored local route directives')
            break


def check_wireguard_guide_dns_leak(path: str, content: str, fails: Failures):
    """WireGuard guide must explicitly cover DNS leak risk in split tunneling
    setups — DNS queries can bypass VPN if not configured.
    """
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if not rel.endswith('guides/wireguard.html'):
        return
    # Look for any DNS leak related discussion or DNS configuration recommendation
    if 'DNS' not in content:
        fails.add(path, 'WireGuard guide does not mention DNS configuration / leak risk')


def check_mikrotik_routeros_version(path: str, content: str, fails: Failures):
    """MikroTik guide must clarify RouterOS version differences — `/ip route rule`
    is v6, replaced by `/routing rule` in v7. Native WireGuard requires v7+.
    """
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if not rel.endswith('guides/mikrotik.html'):
        return
    if 'RouterOS 7' not in content:
        fails.add(path, 'MikroTik guide should clarify RouterOS 7 specifics (WireGuard, /routing rule)')


def check_linux_guide_persistence(path: str, content: str, fails: Failures):
    """The Linux guide must not recommend `@reboot cron` for VPN routes
    (race condition with VPN bring-up — routes fail silently when cron fires
    before tunnel is established). Use systemd oneshot service instead.
    """
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if not rel.endswith('guides/linux.html'):
        return
    # Check for the actual recommendation pattern, not just any mention of @reboot
    # (the systemd section's "Why not @reboot cron?" callout legitimately mentions it).
    if re.search(r'@reboot\s+/usr/local/bin/routes\.sh', content):
        fails.add(path, 'Linux guide actively recommends @reboot cron — race with VPN bring-up')
    if re.search(r'crontab\s+-e', content):
        fails.add(path, 'Linux guide tells user to edit crontab for VPN routes — use systemd oneshot service instead')
    if 'vpn-routes.service' not in content:
        fails.add(path, 'Linux guide must recommend a systemd oneshot service (vpn-routes.service) for persistence')


def check_csp_meta(path: str, content: str, fails: Failures):
    """Each HTML file must declare a Content-Security-Policy via <meta http-equiv>.
    Required directives: default-src, frame-ancestors (clickjacking defense),
    base-uri (prevents <base> injection). Static hosting can't set HTTP headers,
    so meta-CSP is our only knob.
    """
    m = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        content, re.IGNORECASE,
    )
    if not m:
        fails.add(path, 'missing <meta http-equiv="Content-Security-Policy">')
        return
    policy = m.group(1)
    for directive in ('default-src', 'frame-ancestors', 'base-uri'):
        if directive not in policy:
            fails.add(path, f'CSP missing directive "{directive}"')


def check_no_render_blocking_css(path: str, content: str, fails: Failures):
    """Stylesheets loaded synchronously block first paint and hurt LCP/FCP.
    Each <link rel="stylesheet"> should either (a) be inside <noscript> as a
    fallback, or (b) come from a <link rel="preload" as="style" onload=...>
    pair. Any sync <link rel="stylesheet"> outside <noscript> fails this check.
    """
    # Strip <noscript> blocks (sync stylesheets there are intentional fallbacks)
    stripped = re.sub(r'<noscript>.*?</noscript>', '', content, flags=re.DOTALL)
    blockers = re.findall(r'<link\s+[^>]*rel="stylesheet"[^>]*>', stripped)
    for b in blockers:
        fails.add(path, f'render-blocking stylesheet: {b}')


def check_404_navigation(fails: Failures):
    """404.html must offer navigation back to key destinations: home,
    guides hub, and ideally the 5 platform guides — so a wrong URL still
    leads users to useful content.
    """
    path = os.path.join(ROOT, '404.html')
    if not os.path.exists(path):
        fails.add(path, '404.html not found')
        return
    with open(path) as f:
        content = f.read()
    expected = [
        ('/', 'home'),
        ('guides/', 'guides hub'),
    ]
    for href_target, label in expected:
        if not re.search(rf'href="[^"]*{re.escape(href_target)}"', content):
            fails.add(path, f'404 page missing link to {label} ({href_target})')
    # Each platform guide should be linked
    for g in ('keenetic', 'mikrotik', 'wireguard', 'linux', 'openvpn'):
        if not re.search(rf'href="[^"]*guides/{re.escape(g)}\.html"', content):
            fails.add(path, f'404 page missing link to guides/{g}.html')


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

    # lastmod freshness: must be >= last git commit date for the file (so sitemap
    # signals real changes to crawlers).
    import subprocess
    url_block_re = re.compile(
        r'<url>\s*<loc>([^<]+)</loc>.*?<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>',
        re.DOTALL,
    )
    for loc, lastmod in url_block_re.findall(sm):
        target = url_to_file(loc)
        if not target or not os.path.exists(target):
            continue
        rel = os.path.relpath(target, ROOT)
        try:
            git_date = subprocess.check_output(
                ['git', 'log', '-1', '--format=%cs', '--', rel],
                cwd=ROOT, text=True,
            ).strip()
        except subprocess.CalledProcessError:
            continue
        if not git_date:
            continue
        if git_date > lastmod:
            fails.add(sitemap_path, f'sitemap lastmod stale for {loc}: file last committed {git_date}, sitemap says {lastmod}')


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
        check_home_popular_guides(path, content, fails)
        check_home_organization_schema(path, content, fails)
        check_guide_related_links(path, content, fails)
        check_guide_inline_example(path, content, fails)
        check_guide_comments_toggle_note(path, content, fails)
        check_guide_article_schema(path, content, fails)
        check_no_render_blocking_css(path, content, fails)
        check_csp_meta(path, content, fails)
        check_linux_guide_persistence(path, content, fails)
        check_keenetic_guide_correct_cli(path, content, fails)
        check_openvpn_guide_correct_route_nopull(path, content, fails)
        check_wireguard_guide_dns_leak(path, content, fails)
        check_mikrotik_routeros_version(path, content, fails)
    check_sitemap(fails)
    check_404_navigation(fails)

    if fails:
        print(f'\n❌ {len(fails)} failure(s):\n')
        for f in fails:
            print(' -', f)
        sys.exit(1)
    print(f'\n✅ All checks passed ({len(files)} HTML files + sitemap).')


if __name__ == '__main__':
    main()
