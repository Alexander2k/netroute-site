#!/usr/bin/env python3
"""
Home pages for NetRoute 4.1.3: the rule formats for proxy/VPN clients and the router lists.

Per language a set of exact replacements and insertions on <lang>/index.html: version strings,
hero line, SoftwareApplication featureList, FAQ (JSON-LD + HTML), two feature cards, the platform
table (12 new rows), the stats bar, popular guides and the footer links. Facts come from the
extension (modules/RuleFormats.js, popup.html): 9 classic formats + 12 rule formats = 21.

    python3 tools/update_home_413.py [lang ...]     default: every language that has texts below

Idempotent: a replacement whose new text is already present is skipped; insertions check for
their own marker. Nothing is removed — old sentences are replaced by their updated versions.
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LANG_DIRS = {'en': '', 'ru': 'ru/', 'es': 'es/', 'zh': 'zh/'}
TODAY = '2026-10-17'

STORE = 'https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla'


def row(badge, name, v4, v6):
    return (f'                <tr>\n'
            f'                    <td><span class="platform-badge {badge}">{name}</span></td>\n'
            f'                    <td>{v4}</td>\n'
            f'                    <td>{v6}</td>\n'
            f'                </tr>\n')


# The 12 new rows of the platform table; the "IPv6" cell text for IPv4-only formats is per language
def table_rows(ipv4_only: str):
    return ''.join([
        row('badge-os', 'OpenWrt', '<code>uci add network route</code>', '<code>uci add network route6</code>'),
        row('badge-hw', 'MikroTik address-list', '<code>/ip firewall address-list add</code>', '<code>/ipv6 firewall address-list add</code>'),
        row('badge-hw', 'Keenetic DNS routes', '<code>object-group fqdn … include</code>', '<code>include {cidr}</code>'),
        row('badge-vpn', 'AmneziaVPN', '<code>{"hostname", "ips", "ip"}</code>', ipv4_only),
        row('badge-proxy', 'sing-box', '<code>domain_suffix</code>, <code>ip_cidr</code>', '<code>ip_cidr</code>'),
        row('badge-proxy', 'Clash / mihomo', '<code>DOMAIN-SUFFIX</code>, <code>IP-CIDR</code>', '<code>IP-CIDR6</code>'),
        row('badge-proxy', 'Xray / 3X-UI', '<code>domain:</code>, <code>ip</code>', '<code>ip</code>'),
        row('badge-proxy', 'v2rayN', '<code>domain[]</code>, <code>ip[]</code>', '<code>ip[]</code>'),
        row('badge-proxy', 'Happ', '<code>ProxySites</code>, <code>ProxyIp</code>', '<code>ProxyIp</code>'),
        row('badge-proxy', 'Shadowrocket / Surge', '<code>DOMAIN-SUFFIX</code>, <code>IP-CIDR</code>', '<code>IP-CIDR6</code>'),
        row('badge-proxy', 'Quantumult X', '<code>host-suffix</code>, <code>ip-cidr</code>', '<code>ip6-cidr</code>'),
        row('badge-proxy', 'PAC', '<code>dnsDomainIs</code>, <code>isInNet</code>', ipv4_only),
    ])


def guide_card(href, title, text):
    return (f'        <a class="feature-card" href="{href}" style="text-decoration:none;display:block;">\n'
            f'            <h3>{title}</h3>\n'
            f'            <p>{text}</p>\n'
            f'        </a>\n')


ICON_RULES = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="1.5"><path d="M4 6h16M4 12h9M4 18h6"/><circle cx="17.5" cy="16.5" r="3.5"/><path d="M20 19l2 2"/></svg>'
ICON_LISTS = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="1.5"><rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01M11 7h6M11 17h6"/></svg>'


def feature_cards(t):
    return (f'        <div class="feature-card">\n'
            f'            <div class="feature-icon">\n                {ICON_RULES}\n            </div>\n'
            f'            <h3>{t["card_rules_h3"]}</h3>\n'
            f'            <p>{t["card_rules_p"]}</p>\n'
            f'        </div>\n'
            f'        <div class="feature-card">\n'
            f'            <div class="feature-icon">\n                {ICON_LISTS}\n            </div>\n'
            f'            <h3>{t["card_lists_h3"]}</h3>\n'
            f'            <p>{t["card_lists_p"]}</p>\n'
            f'        </div>\n')


TEXTS = {
    'ru': {
        'version_old': '4.1.2', 'version_new': '4.1.3', 'generated_old': 'generated 2026-10-13', 'generated_new': f'generated {TODAY}',
        'hero_old': 'Генерирует оптимизированные команды маршрутизации для <strong>9 платформ</strong> мгновенно.',
        'hero_new': 'Генерирует маршруты и правила для <strong>21 формата</strong> мгновенно: роутеры, ОС, VPN- и прокси-клиенты.',
        'feature_old': '"Экспорт в .bat, .sh, .rsc, .conf, .ovpn и .bat для Keenetic"',
        'feature_new': ('"Экспорт в .bat, .sh, .rsc, .conf, .ovpn, .json, .yaml, .list, .pac и .bat для Keenetic",\n'
                        '            "Правила для прокси-клиентов: sing-box, Clash/mihomo, Xray, v2rayN, Happ, Shadowrocket/Surge, Quantumult X, PAC",\n'
                        '            "Список сайтов AmneziaVPN для раздельного туннелирования",\n'
                        '            "MikroTik address-list, DNS-маршруты Keenetic (KeeneticOS 5), маршруты OpenWrt (uci)"'),
        'faq1_old': 'NetRoute генерирует команды маршрутизации для 9 платформ: Windows, Linux, macOS, MikroTik, Cisco, Juniper, WireGuard (AllowedIPs), OpenVPN и Keenetic, а также по вашему собственному шаблону. Поддерживаются IPv4 и IPv6 (формат Keenetic — только IPv4).',
        'faq1_new': 'NetRoute выдаёт 21 формат. Команды маршрутов для систем и роутеров: Windows, Linux, macOS, OpenWrt, MikroTik, Cisco, Juniper, Keenetic; правила для VPN- и прокси-клиентов: WireGuard (AllowedIPs), OpenVPN, AmneziaVPN, sing-box, Clash/mihomo, Xray, v2rayN, Happ, Shadowrocket/Surge, Quantumult X и PAC; списки для роутеров: MikroTik address-list и DNS-маршруты Keenetic (KeeneticOS 5). Плюс свой шаблон. Поддерживаются IPv4 и IPv6; форматы Keenetic .bat, AmneziaVPN и PAC — только IPv4.',
        'faq_new_q': 'Подходит ли NetRoute для прокси-клиентов — Hiddify, Happ, v2rayN?',
        'faq_new_a': 'Да. Выберите формат клиента в списке «Целевая ОС», и вместо команд маршрутов NetRoute выдаст правила с доменами и сетями сайта: rule-set для sing-box (Hiddify, NekoBox), rule-provider для Clash/mihomo, routing.rules для Xray и панели 3X-UI, файл импорта правил для v2rayN, профиль маршрутизации Happ, список правил для Shadowrocket/Surge и Quantumult X, PAC-файл и список сайтов для AmneziaVPN. Домены сворачиваются по суффиксам, сети — те же, что в маршрутах.',
        'faq_anchor_q': 'Можно ли использовать для VPN split tunneling?',
        'card_rules_h3': 'Правила для прокси-клиентов',
        'card_rules_p': 'Те же домены и сети как правила: sing-box (Hiddify), Clash/mihomo, Xray и 3X-UI, v2rayN, Happ, Shadowrocket/Surge, Quantumult X, PAC — и список сайтов для AmneziaVPN.',
        'card_lists_h3': 'Списки для роутеров',
        'card_lists_p': 'MikroTik address-list и DNS-маршруты Keenetic (KeeneticOS 5) вместо сотен маршрутов; постоянные маршруты OpenWrt через uci.',
        'cards_anchor': '<h3>Экспорт для Keenetic</h3>',
        'platforms_h2_old': '<h2>9 форматов платформ</h2>',
        'platforms_h2_new': '<h2>21 формат вывода</h2>',
        'platforms_p_old': '<p>Нативный синтаксис команд для всех основных ОС и сетевого оборудования.</p>',
        'platforms_p_new': '<p>Команды маршрутов для ОС и роутеров, правила для VPN- и прокси-клиентов &mdash; в родном синтаксисе каждого.</p>',
        'ipv4_only': 'только IPv4',
        'stat_formats_old': '<span class="stat-value">9</span>\n        <span class="stat-label">Форматов платформ</span>',
        'stat_formats_new': '<span class="stat-value">21</span>\n        <span class="stat-label">Формат вывода</span>',
        'stat_export_old': '<span class="stat-value">7</span>\n        <span class="stat-label">Форматов экспорта</span>',
        'stat_export_new': '<span class="stat-value">12</span>\n        <span class="stat-label">Расширений файлов</span>',
        'guides': [
            ('guides/singbox.html', 'sing-box &mdash; rule-set', 'Домены и сети сайта как rule-set для sing-box и Hiddify: <code>route.rule_set</code>, компиляция в <code>.srs</code>.'),
            ('guides/happ.html', 'Happ &mdash; профиль маршрутизации', 'JSON-профиль со списками <code>ProxySites</code> и <code>ProxyIp</code>; в приложение &mdash; ссылкой <code>happ://routing/onadd</code>.'),
            ('guides/xray.html', 'Xray &mdash; routing.rules', 'Правила для конфига Xray-core, панели 3X-UI и импорта в v2rayN.'),
            ('guides/amnezia.html', 'AmneziaVPN &mdash; список сайтов', 'Хосты с адресами и подсети для раздельного туннелирования, импорт через меню ⋮.'),
        ],
        'guides_anchor_href': 'guides/openvpn.html',
        'footer_links': [('guides/singbox.html', 'sing-box'), ('guides/happ.html', 'Happ'), ('guides/xray.html', 'Xray'), ('guides/amnezia.html', 'AmneziaVPN')],
    },
}


def replace_once(html, old, new, label, report):
    if new in html:
        report.append(f'  = {label}')
        return html
    if old not in html:
        report.append(f'  ! {label}: anchor not found')
        return html
    report.append(f'  + {label}')
    return html.replace(old, new)


def update(lang: str) -> list:
    t = TEXTS[lang]
    path = os.path.join(ROOT, LANG_DIRS[lang], 'index.html')
    with open(path, encoding='utf-8') as f:
        html = f.read()
    original = html
    report = [f'{LANG_DIRS[lang] or "./"}index.html']

    # version strings
    html = replace_once(html, f'"softwareVersion": "{t["version_old"]}"', f'"softwareVersion": "{t["version_new"]}"', 'softwareVersion', report)
    html = replace_once(html, f'<span class="logo-ver">v{t["version_old"]}</span>', f'<span class="logo-ver">v{t["version_new"]}</span>', 'logo version', report)
    html = replace_once(html, f'# NetRoute v{t["version_old"]} — {t["generated_old"]}', f'# NetRoute v{t["version_new"]} — {t["generated_new"]}', 'terminal comment', report)
    html = replace_once(html, f'<span>NetRoute v{t["version_old"]}</span>', f'<span>NetRoute v{t["version_new"]}</span>', 'footer version', report)

    html = replace_once(html, t['hero_old'], t['hero_new'], 'hero line', report)
    html = replace_once(html, t['feature_old'], t['feature_new'], 'featureList', report)
    html = replace_once(html, t['faq1_old'], t['faq1_new'], 'FAQ platforms answer (JSON-LD + HTML)', report)

    # new FAQ entry: JSON-LD (before the split tunneling question) and HTML (before the same question)
    jsonld_anchor = f'            {{\n                "@type": "Question",\n                "name": "{t["faq_anchor_q"]}",'
    jsonld_new = (f'            {{\n                "@type": "Question",\n                "name": "{t["faq_new_q"]}",\n'
                  f'                "acceptedAnswer": {{\n                    "@type": "Answer",\n'
                  f'                    "text": "{t["faq_new_a"]}"\n                }}\n            }},\n')
    html = replace_once(html, jsonld_anchor, jsonld_new + jsonld_anchor, 'FAQ JSON-LD: proxy clients', report)
    html_anchor = f'        <details class="faq-item">\n            <summary>{t["faq_anchor_q"]}</summary>'
    html_new = (f'        <details class="faq-item">\n            <summary>{t["faq_new_q"]}</summary>\n'
                f'            <div class="faq-answer">{t["faq_new_a"]}</div>\n        </details>\n')
    html = replace_once(html, html_anchor, html_new + html_anchor, 'FAQ HTML: proxy clients', report)

    # feature cards after the Keenetic card
    if f'<h3>{t["card_rules_h3"]}</h3>' not in html:
        i = html.find(t['cards_anchor'])
        if i == -1:
            report.append('  ! feature cards: Keenetic card not found')
        else:
            end = html.find('        </div>\n', i) + len('        </div>\n')
            html = html[:end] + feature_cards(t) + html[end:]
            report.append('  + feature cards')
    else:
        report.append('  = feature cards')
    # (the FAQ answer and featureList mention the same words; only the <h3> counts as "present")

    # platform table
    html = replace_once(html, t['platforms_h2_old'], t['platforms_h2_new'], 'platforms heading', report)
    html = replace_once(html, t['platforms_p_old'], t['platforms_p_new'], 'platforms text', report)
    if 'Keenetic DNS routes</span>' not in html:
        i = html.find('<table class="platform-table">')
        j = html.find('            </tbody>', i)
        if i == -1 or j == -1:
            report.append('  ! platform table not found')
        else:
            html = html[:j] + table_rows(t['ipv4_only']) + html[j:]
            report.append('  + platform table rows')
    else:
        report.append('  = platform table rows')

    html = replace_once(html, t['stat_formats_old'], t['stat_formats_new'], 'stat formats', report)
    html = replace_once(html, t['stat_export_old'], t['stat_export_new'], 'stat file types', report)

    # popular guides: after the OpenVPN card
    if f'href="{t["guides"][0][0]}"' not in html.split('id="popular-guides"', 1)[-1].split('</section>', 1)[0]:
        sec_start = html.find('id="popular-guides"')
        anchor = html.find(f'<a class="feature-card" href="{t["guides_anchor_href"]}"', sec_start)
        if anchor == -1:
            report.append('  ! popular guides: OpenVPN card not found')
        else:
            end = html.find('        </a>\n', anchor) + len('        </a>\n')
            cards = ''.join(guide_card(h, title, text) for h, title, text in t['guides'])
            html = html[:end] + cards + html[end:]
            report.append('  + popular guide cards')
    else:
        report.append('  = popular guide cards')

    # footer guide links after the OpenVPN link
    footer_anchor = f'                <a href="{t["guides_anchor_href"]}">OpenVPN</a>\n'
    footer_new = ''.join(f'                <a href="{h}">{name}</a>\n' for h, name in t['footer_links'])
    if f'<a href="{t["footer_links"][0][0]}">' in html.split('<footer', 1)[-1]:
        report.append('  = footer links')
    elif footer_anchor not in html:
        report.append('  ! footer: OpenVPN link not found')
    else:
        html = html.replace(footer_anchor, footer_anchor + footer_new, 1)
        report.append('  + footer links')

    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return report


def main() -> int:
    langs = sys.argv[1:] or [lang for lang in LANG_DIRS if lang in TEXTS]
    for lang in langs:
        if lang not in TEXTS:
            print(f'{lang}: no texts yet, skipped')
            continue
        for line in update(lang):
            print(line)
    return 0


if __name__ == '__main__':
    sys.exit(main())
