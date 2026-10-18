#!/usr/bin/env python3
"""
Generate the guide pages for the rule formats added in NetRoute 4.1.3 (proxy clients, VPN
clients, OpenWrt) in all four languages from the content files in tools/guide_content/.

Source of truth: tools/guide_content/<slug>_<lang>.py (PAGE dict with the page content) and
                 tools/guide_content/_ui_<lang>.py (UI dict with the shared strings)
                 Python modules rather than JSON so the HTML can be written in triple-quoted
                 strings without escaping.
Generated:       guides/<slug>.html, ru/guides/<slug>.html, es/..., zh/...
                 hub cards in */guides/index.html (inserted once, idempotent)
                 sitemap.xml entries (appended once, idempotent)

Run after editing content:
    python3 tools/gen_client_guides.py
    python3 tools/embed_examples.py      # fills the inline example block
    python3 tests/test_seo.py

The pages follow the hand-written guides (same head, CSS, nav, JSON-LD and section anchors), so
every check in tests/test_seo.py applies to them unchanged.
"""

import datetime
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONTENT = os.path.join(ROOT, 'tools', 'guide_content')
SITE_BASE = 'https://alexander2k.github.io/netroute-site'
STORE_URL = 'https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla'

LANGS = {
    # code: (dir prefix, html lang, og:locale, dropdown label, short label)
    'en': ('', 'en', 'en_US', 'English', 'EN'),
    'ru': ('ru/', 'ru', 'ru_RU', 'Русский', 'RU'),
    'es': ('es/', 'es', 'es_ES', 'Español', 'ES'),
    'zh': ('zh/', 'zh', 'zh_CN', '中文', 'ZH'),
}

# Order of the new guides: hub cards and "related" lists follow it
SLUGS = ['singbox', 'clash', 'xray', 'happ', 'shadowrocket', 'pac', 'amnezia', 'openwrt']
CLASSIC = ['keenetic', 'mikrotik', 'wireguard', 'linux', 'openvpn']

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' "
       "https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; "
       "connect-src 'self'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests")
FONTS = 'https://fonts.googleapis.com/css2?family=Google+Sans+Code:wght@300..800&family=Google+Sans+Flex:wght,ROND@400..800,0..100&display=swap'

GUIDE_CSS = """        .guide { max-width: 820px; margin: 0 auto; padding: 120px 32px 80px; position: relative; z-index: 1; }
        .guide h1 { font-size: 36px; margin-bottom: 12px; letter-spacing: -0.02em; }
        .guide .lead { font-size: 17px; color: var(--text-dim); line-height: 1.7; margin-bottom: 40px; }
        .guide .guide-date { font-family: var(--font-mono); font-size: 13px; color: var(--text-dim); margin: 0 0 20px; }
        .guide h2 { font-size: 24px; margin: 48px 0 16px; color: var(--text); letter-spacing: -0.01em; }
        .guide h3 { font-size: 18px; margin: 24px 0 8px; color: var(--text); font-family: var(--font-mono); }
        .guide p, .guide li { font-size: 15px; color: var(--text-dim); line-height: 1.8; }
        .guide ul, .guide ol { padding-left: 24px; margin: 12px 0; }
        .guide li { margin-bottom: 8px; }
        .guide a:not(.btn) { color: var(--accent); }
        .guide a.btn-primary { color: #fff; }
        .guide strong { color: var(--text); }
        .guide code { font-size: 13px; }
        .guide pre { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 16px 20px; overflow-x: auto; margin: 16px 0; }
        .guide pre code { background: none; padding: 0; font-family: var(--font-mono); font-size: 13px; color: var(--text-dim); line-height: 1.7; }
        .guide .callout { background: var(--bg-card); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 6px; padding: 16px 20px; margin: 20px 0; font-size: 14px; color: var(--text-dim); }
        .back { display: inline-block; margin-bottom: 32px; font-family: var(--font-mono); font-size: 13px; color: var(--text-dim); }
        .back:hover { color: var(--text); }
        .cta-block { background: linear-gradient(135deg, rgba(26,115,232,0.08), rgba(57,213,255,0.05)); border: 1px solid var(--border); border-radius: 12px; padding: 28px; margin: 40px 0; text-align: center; }
        .cta-block h3 { margin: 0 0 8px; font-family: var(--font-body); font-size: 20px; }
        .cta-block p { margin-bottom: 20px; }"""


def load(name: str, attr: str) -> dict:
    """Import tools/guide_content/<name>.py and return its PAGE or UI dict."""
    import importlib.util
    path = os.path.join(CONTENT, f'{name}.py')
    spec = importlib.util.spec_from_file_location(f'guide_content.{name}', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, attr)


def url_of(lang: str, slug: str) -> str:
    return f'{SITE_BASE}/{LANGS[lang][0]}guides/{slug}.html'


def jsonld(obj: dict) -> str:
    text = json.dumps(obj, ensure_ascii=False, indent=4)
    # indent the block like the hand-written pages
    return '\n'.join('    ' + line for line in text.split('\n'))


def png_size(path: str):
    """(width, height) of a PNG from its IHDR chunk, or None when the file is missing."""
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return int.from_bytes(head[16:20], 'big'), int.from_bytes(head[20:24], 'big')


def shot_paths(page: dict, lang: str):
    """(relative-from-page prefix, light path, dark path, shots_lang) of the page's render, or None."""
    fmt = page.get('shot_format')
    if not fmt:
        return None
    shots_lang = 'ru' if lang == 'ru' else 'en'
    ext = 'webp' if os.path.exists(os.path.join(ROOT, 'screenshots', 'guides', shots_lang, f'{fmt}-light.webp')) else 'png'
    light = os.path.join(ROOT, 'screenshots', 'guides', shots_lang, f'{fmt}-light.{ext}')
    dark = os.path.join(ROOT, 'screenshots', 'guides', shots_lang, f'{fmt}-dark.{ext}')
    if not os.path.exists(light) or not os.path.exists(dark):
        return None
    return fmt, shots_lang, ext, light, dark


def shot_image_url(page: dict, lang: str):
    """Absolute URL of the light render for schema/og, or None."""
    p = shot_paths(page, lang)
    if not p:
        return None
    fmt, shots_lang, ext, _, _ = p
    return f'{SITE_BASE}/screenshots/guides/{shots_lang}/{fmt}-light.{ext}'


def shot_figure(page: dict, ui: dict, lang: str) -> str:
    """<figure> with the light and dark popup renders of the page's format
    (screenshots/guides/<ru|en>/<format>-*.png, Russian popup for the Russian pages), or '' when the
    renders are not there yet. Captured at 2x, so the intrinsic size is halved for layout."""
    p = shot_paths(page, lang)
    if not p:
        return ''
    fmt, shots_lang, ext, light, _ = p
    up = '../' if lang == 'en' else '../../'
    rel = f'{up}screenshots/guides/{shots_lang}/{fmt}'
    # dimensions come from the PNG capture (the WebP is a conversion of the same image)
    size = png_size(os.path.join(ROOT, 'screenshots', 'guides', shots_lang, f'{fmt}-light.png'))
    if not size:
        return ''
    w, h = size[0] // 2, size[1] // 2
    alt = page.get('shot_alt') or ui['shot_alt_default']
    caption = page.get('shot_caption') or ui['shot_caption_default']
    return (f'    <figure class="shot">\n'
            f'        <img class="shot-light" src="{rel}-light.{ext}" width="{w}" height="{h}" loading="lazy" alt="{alt}">\n'
            f'        <img class="shot-dark" src="{rel}-dark.{ext}" width="{w}" height="{h}" loading="lazy" alt="{alt}">\n'
            f'        <figcaption>{caption}</figcaption>\n'
            f'    </figure>\n')


def extension_version() -> str:
    """Version of the extension the guides describe: manifest.json of the sibling net-route
    checkout when present, otherwise the highest x.y.z in the home pages' footers."""
    manifest = os.path.join(ROOT, '..', 'net-route', 'manifest.json')
    if os.path.exists(manifest):
        with open(manifest, encoding='utf-8') as f:
            return json.load(f).get('version', '')
    versions = []
    for prefix in ('', 'ru/', 'es/', 'zh/'):
        path = os.path.join(ROOT, prefix, 'index.html')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                versions += re.findall(r'<span>NetRoute v(\d+\.\d+\.\d+)</span>', f.read())
    return max(versions, key=lambda v: tuple(int(x) for x in v.split('.'))) if versions else ''


def render_page(lang: str, slug: str, page: dict, ui: dict, all_pages: dict, today: str) -> str:
    prefix, html_lang, locale, _, short = LANGS[lang]
    canonical = url_of(lang, slug)
    version = extension_version()
    # Only the language versions that exist are linked (the guides are written one language at a
    # time); rerunning the generator adds the links once a version appears
    present = [code for code in LANGS if (code, slug) in all_pages]
    x_default = 'en' if 'en' in present else lang
    hreflangs = ''.join(
        f'    <link rel="alternate" hreflang="{code}" href="{url_of(code, slug)}">\n' for code in present
    ) + f'    <link rel="alternate" hreflang="x-default" href="{url_of(x_default, slug)}">\n'

    # English pages live in guides/ (one level below the root), the others in <lang>/guides/
    up = '../' if lang == 'en' else '../../'
    dropdown = ''
    for code, (p, _, _, label, _) in LANGS.items():
        if code not in present:
            continue
        href = f'./{slug}.html' if code == lang else f'{up}{p}guides/{slug}.html'
        cls = ' class="lang-active"' if code == lang else ''
        dropdown += f'                    <a href="{href}"{cls}>{label}</a>\n'

    home_url = f'{SITE_BASE}/{prefix}'
    breadcrumbs = jsonld({
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': ui['home'], 'item': home_url},
            {'@type': 'ListItem', 'position': 2, 'name': ui['guides'], 'item': f'{home_url}guides/'},
            {'@type': 'ListItem', 'position': 3, 'name': page['breadcrumb']},
        ],
    })
    howto = jsonld({
        '@context': 'https://schema.org',
        '@type': 'HowTo',
        'name': page['howto']['name'],
        'description': page['howto']['description'],
        'inLanguage': html_lang,
        'totalTime': page['howto'].get('total_time', 'PT5M'),
        'step': [{'@type': 'HowToStep', 'name': s['name'], 'text': s['text']} for s in page['howto']['steps']],
    })
    # the article image list: the site banner plus this page's own popup render when it exists
    images = [f'{SITE_BASE}/screenshots/promo-large.png']
    shot_url = shot_image_url(page, lang)
    if shot_url:
        images.append(shot_url)
    article = jsonld({
        '@context': 'https://schema.org',
        '@type': 'TechArticle',
        'headline': page['title'].split(' | ')[0],
        'description': page['description'],
        'image': images,
        'inLanguage': html_lang,
        'datePublished': page.get('date_published', today),
        'dateModified': today,
        'author': {'@type': 'Organization', 'name': 'NetRoute', 'url': f'{SITE_BASE}/'},
        'publisher': {
            '@type': 'Organization', 'name': 'NetRoute', 'url': f'{SITE_BASE}/',
            'logo': {'@type': 'ImageObject', 'url': f'{SITE_BASE}/icon.png'},
        },
        'mainEntityOfPage': {'@type': 'WebPage', '@id': canonical},
    })

    body_sections = ''
    figure = shot_figure(page, ui, lang)
    for i, sec in enumerate(page['sections']):
        sid = f' id="{sec["id"]}"' if sec.get('id') else ''
        body_sections += f'\n    <h2{sid}>{sec["h2"]}</h2>\n{sec["html"].rstrip()}\n'
        # the popup render goes right after the first section ("what is inside the file")
        if i == 0 and figure:
            body_sections += '\n' + figure

    # Related: the five classic guides (required by the tests) plus the other new guides
    related = ''
    for other in CLASSIC:
        related += f'        <li><a href="./{other}.html">{ui["classic_names"][other]}</a> &mdash; {ui["classic_related"][other]}</li>\n'
    for other in SLUGS:
        if other == slug or (lang, other) not in all_pages:
            continue
        op = all_pages[(lang, other)]
        related += f'        <li><a href="./{other}.html">{op["card"]["title"]}</a> &mdash; {op["related_desc"]}</li>\n'

    docs = ''.join(
        f'        <li><a href="{d["url"]}" target="_blank" rel="noopener">{d["label"]}</a></li>\n'
        for d in page['official_docs']
    )
    example = page['example_file']

    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="{CSP}">
    <script>try{{var t=localStorage.getItem('netroute-theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
    <script src="{up}theme.js" defer></script>
    <title>{page['title']}</title>
    <meta name="description" content="{page['description']}">
    <meta name="keywords" content="{page['keywords']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
{hreflangs}
    <meta property="og:type" content="article">
    <meta property="og:title" content="{page['og_title']}">
    <meta property="og:description" content="{page['og_description']}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{SITE_BASE}/screenshots/promo-large.png">
    <meta property="og:image:width" content="1400">
    <meta property="og:image:height" content="560">
    <meta property="og:locale" content="{locale}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page['og_title']}">
    <meta name="twitter:description" content="{page['og_description']}">
    <meta name="twitter:image" content="{SITE_BASE}/screenshots/promo-large.png">
    <meta name="theme-color" content="#0e1117">

    <link rel="icon" type="image/svg+xml" href="{up}favicon.svg">
    <link rel="stylesheet" href="{up}style.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="{FONTS}"></noscript>

    <script type="application/ld+json">
{breadcrumbs}
    </script>

    <script type="application/ld+json">
{howto}
    </script>

    <script type="application/ld+json">
{article}
    </script>

    <style>
{GUIDE_CSS}
    </style>
</head>
<body>

<div class="grid-bg" aria-hidden="true"></div>

<nav class="topbar">
    <div class="topbar-inner">
        <a href="../" class="logo">
            <span class="logo-icon">&#9678;</span>
            <span class="logo-text">NetRoute</span>
        </a>
        <div class="nav-links">
            <a href="../">{ui['home']}</a>
            <div class="lang-switch">
                <span class="lang-current">{short}</span>
                <div class="lang-dropdown">
{dropdown}                </div>
            </div>
        </div>
    </div>
</nav>

<article class="guide">
    <a href="../" class="back">{ui['back']}</a>
    <h1>{page['h1']}</h1>
    <p class="guide-date">{ui['updated']} <time datetime="{today}">{today}</time> &middot; NetRoute {ui['version_word']} {version}</p>
    <p class="lead">{page['lead']}</p>
{body_sections}
    <h2 id="dns-leak">{page['dns_leak']['h2']}</h2>
{page['dns_leak']['html'].rstrip()}

    <h2 id="examples">{ui['examples_h2']}</h2>
    <p>{ui['examples_p']}</p>
    <ul>
        <li><a href="https://github.com/Alexander2k/netroute-site/blob/main/examples/{example}" target="_blank" rel="noopener"><code>{example}</code></a> &mdash; {page['example_desc']}</li>
    </ul>
    <p class="callout">{ui['comments_hint']}</p>

    <p><a href="https://github.com/Alexander2k/netroute-site/tree/main/examples" target="_blank" rel="noopener">{ui['all_examples']}</a></p>

    <h2 id="official-docs">{ui['official_docs']}</h2>
    <ul>
{docs}    </ul>

    <h2 id="related">{ui['related']}</h2>
    <ul>
{related}    </ul>

    <div class="cta-block">
        <h3>{ui['cta_h3']}</h3>
        <p>{ui['cta_p']}</p>
        <a href="{STORE_URL}" class="btn btn-primary" target="_blank" rel="noopener">{ui['cta_btn']}</a>
    </div>

</article>

</body>
</html>
'''


def hub_card(slug: str, page: dict) -> str:
    card = page['card']
    return (f'        <a class="hub-card" href="{slug}.html">\n'
            f'            <span class="hub-card-badge {card["badge"]}">{card["badge_label"]}</span>\n'
            f'            <h3>{card["title"]}</h3>\n'
            f'            <p>{card["text"]}</p>\n'
            f'        </a>\n')


def update_hub(lang: str, pages: dict) -> str:
    """Insert the new cards into the hub grid once: proxy/VPN cards after the OpenVPN card, the
    OpenWrt card replaces its 'coming soon' placeholder."""
    path = os.path.join(ROOT, LANGS[lang][0], 'guides', 'index.html')
    with open(path, encoding='utf-8') as f:
        html = f.read()
    original = html
    # OpenWrt: the placeholder <div class="hub-card coming-soon"> ... <h3>OpenWrt</h3> ... </div>
    placeholder = re.compile(r'        <div class="hub-card coming-soon">\s*<span class="hub-card-badge soon">[^<]*</span>\s*<h3>OpenWrt</h3>.*?</div>\n', re.DOTALL)
    if (lang, 'openwrt') in pages and 'href="openwrt.html"' not in html and placeholder.search(html):
        html = placeholder.sub(lambda _: hub_card('openwrt', pages[(lang, 'openwrt')]), html, count=1)
    # The client cards go right after the OpenVPN card
    cards = ''.join(hub_card(s, pages[(lang, s)]) for s in SLUGS
                    if s != 'openwrt' and (lang, s) in pages and f'href="{s}.html"' not in html)
    if cards:
        anchor = re.compile(r'(        <a class="hub-card" href="openvpn\.html">.*?</a>\n)', re.DOTALL)
        m = anchor.search(html)
        if not m:
            raise SystemExit(f'{path}: OpenVPN card not found, cannot insert new cards')
        html = html[:m.end()] + cards + html[m.end():]
    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return 'updated'
    return 'unchanged'


def update_sitemap(today: str, pages: dict) -> int:
    path = os.path.join(ROOT, 'sitemap.xml')
    with open(path, encoding='utf-8') as f:
        xml = f.read()
    added = 0
    blocks = ''
    for slug in SLUGS:
        for lang in LANGS:
            if (lang, slug) not in pages:
                continue
            loc = url_of(lang, slug)
            present = [code for code in LANGS if (code, slug) in pages]
            x_default = 'en' if 'en' in present else lang
            alts = ''.join(
                f'        <xhtml:link rel="alternate" hreflang="{code}" href="{url_of(code, slug)}"/>\n' for code in present
            ) + f'        <xhtml:link rel="alternate" hreflang="x-default" href="{url_of(x_default, slug)}"/>\n'
            marker = f'    <!-- {slug} guide ({lang.upper()}) -->\n'
            existing = re.compile(re.escape(marker) + r'    <url>\n(.*?)        <lastmod>(\d{4}-\d{2}-\d{2})</lastmod>\n(.*?)    </url>\n\n', re.DOTALL)
            m = existing.search(xml)
            lastmod = m.group(2) if m else today
            block = (marker +
                     f'    <url>\n'
                     f'        <loc>{loc}</loc>\n'
                     f'{alts}'
                     f'        <lastmod>{lastmod}</lastmod>\n'
                     f'        <changefreq>monthly</changefreq>\n'
                     f'        <priority>0.8</priority>\n'
                     f'    </url>\n\n')
            if m:
                # the alternates of an existing block follow the languages present today
                xml = xml[:m.start()] + block + xml[m.end():]
            else:
                blocks += block
                added += 1
    xml = xml.replace('</urlset>', blocks + '</urlset>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(xml)
    return added


def main() -> int:
    today = datetime.date.today().isoformat()
    # Only the pages whose content exists are generated: the guides are written language by
    # language, and a page is never published before its text is ready
    uis = {lang: load(f'_ui_{lang}', 'UI') for lang in LANGS if os.path.exists(os.path.join(CONTENT, f'_ui_{lang}.py'))}
    pages = {}
    for lang in uis:
        for slug in SLUGS:
            name = f'{slug}_{lang}'
            if os.path.exists(os.path.join(CONTENT, f'{name}.py')):
                pages[(lang, slug)] = load(name, 'PAGE')
    if not pages:
        print('no content yet (tools/guide_content/<slug>_<lang>.py)', file=sys.stderr)
        return 1

    written = 0
    for (lang, slug), page in pages.items():
        out = os.path.join(ROOT, LANGS[lang][0], 'guides', f'{slug}.html')
        html = render_page(lang, slug, page, uis[lang], pages, today)
        existing = None
        if os.path.exists(out):
            with open(out, encoding='utf-8') as f:
                existing = f.read()
            # keep the inline example block filled in by embed_examples.py
            m = re.search(r'<pre><code><!--\s*EMBED:.*?<!--\s*/EMBED\s*--></code></pre>\n\n    ', existing, re.DOTALL)
            if m:
                html = html.replace('    <p class="callout">', '    ' + m.group(0) + '<p class="callout">', 1)
            # keep the original publication date
            d = re.search(r'"datePublished": "(\d{4}-\d{2}-\d{2})"', existing)
            if d:
                html = html.replace(f'"datePublished": "{today}"', f'"datePublished": "{d.group(1)}"')
        if html != existing:
            with open(out, 'w', encoding='utf-8') as f:
                f.write(html)
            written += 1
    print(f'guide pages written: {written} / {len(pages)}')

    for lang in uis:
        print(f'hub {LANGS[lang][0] or "./"}guides/index.html: {update_hub(lang, pages)}')
    print(f'sitemap entries added: {update_sitemap(today, pages)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
