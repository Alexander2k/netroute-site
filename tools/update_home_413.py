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
                        '            "Список сайтов AmneziaVPN для split tunneling",\n'
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
            ('guides/amnezia.html', 'AmneziaVPN &mdash; список сайтов', 'Хосты с адресами и подсети для split tunneling, импорт через меню ⋮.'),
        ],
        'guides_anchor_href': 'guides/openvpn.html',
        'footer_links': [('guides/singbox.html', 'sing-box'), ('guides/happ.html', 'Happ'), ('guides/xray.html', 'Xray'), ('guides/amnezia.html', 'AmneziaVPN')],
    },
    'en': {
        'version_old': '4.1.2', 'version_new': '4.1.3', 'generated_old': 'generated 2026-10-13', 'generated_new': f'generated {TODAY}',
        'hero_old': 'Generate optimized routing commands for <strong>9 platforms</strong> instantly.',
        'hero_new': 'Generate routes and rules for <strong>21 formats</strong> instantly: routers, operating systems, VPN and proxy clients.',
        'feature_old': '"Export as .bat, .sh, .rsc, .conf, .ovpn and Keenetic .bat"',
        'feature_new': ('"Export as .bat, .sh, .rsc, .conf, .ovpn, .json, .yaml, .list, .pac and Keenetic .bat",\n'
                        '            "Rules for proxy clients: sing-box, Clash/mihomo, Xray, v2rayN, Happ, Shadowrocket/Surge, Quantumult X, PAC",\n'
                        '            "AmneziaVPN site list for split tunneling",\n'
                        '            "MikroTik address-list, Keenetic DNS routes (KeeneticOS 5), OpenWrt routes (uci)"'),
        'faq1_old': 'NetRoute generates routing commands for 9 platforms: Windows, Linux, macOS, MikroTik, Cisco, Juniper, WireGuard (AllowedIPs), OpenVPN, and Keenetic, plus your own custom template. Both IPv4 and IPv6 are supported (the Keenetic format is IPv4 only).',
        'faq1_new': 'NetRoute outputs 21 formats. Route commands for operating systems and routers: Windows, Linux, macOS, OpenWrt, MikroTik, Cisco, Juniper, Keenetic; rules for VPN and proxy clients: WireGuard (AllowedIPs), OpenVPN, AmneziaVPN, sing-box, Clash/mihomo, Xray, v2rayN, Happ, Shadowrocket/Surge, Quantumult X and PAC; lists for routers: MikroTik address-list and Keenetic DNS routes (KeeneticOS 5). Plus your own template. IPv4 and IPv6 are supported; the Keenetic .bat, AmneziaVPN and PAC formats are IPv4 only.',
        'faq_new_q': 'Does NetRoute work with proxy clients such as Hiddify, Happ or v2rayN?',
        'faq_new_a': 'Yes. Pick the client’s format under “Target OS” and NetRoute outputs rules with the site’s domains and networks instead of route commands: a rule-set for sing-box (Hiddify, NekoBox), a rule-provider for Clash/mihomo, routing.rules for Xray and the 3X-UI panel, a rule import file for v2rayN, a Happ routing profile, a rule list for Shadowrocket/Surge and Quantumult X, a PAC file and a site list for AmneziaVPN. Domains are folded to suffixes; the networks are the same as in the routes.',
        'faq_anchor_q': 'Can I use NetRoute for VPN split tunneling?',
        'card_rules_h3': 'Rules for proxy clients',
        'card_rules_p': 'The same domains and networks as rules: sing-box (Hiddify), Clash/mihomo, Xray and 3X-UI, v2rayN, Happ, Shadowrocket/Surge, Quantumult X, PAC &mdash; and a site list for AmneziaVPN.',
        'card_lists_h3': 'Lists for routers',
        'card_lists_p': 'MikroTik address-list and Keenetic DNS routes (KeeneticOS 5) instead of hundreds of routes; persistent OpenWrt routes via uci.',
        'cards_anchor': '<h3>Keenetic Export</h3>',
        'platforms_h2_old': '<h2>9 Platform Formats</h2>',
        'platforms_h2_new': '<h2>21 Output Formats</h2>',
        'platforms_p_old': '<p>Native command syntax for every major OS and network equipment vendor.</p>',
        'platforms_p_new': '<p>Route commands for operating systems and routers, rules for VPN and proxy clients &mdash; each in its native syntax.</p>',
        'ipv4_only': 'IPv4 only',
        'stat_formats_old': '<span class="stat-value">9</span>\n        <span class="stat-label">Platform Formats</span>',
        'stat_formats_new': '<span class="stat-value">21</span>\n        <span class="stat-label">Output Formats</span>',
        'stat_export_old': '<span class="stat-value">7</span>\n        <span class="stat-label">Export Formats</span>',
        'stat_export_new': '<span class="stat-value">12</span>\n        <span class="stat-label">File Types</span>',
        'guides': [
            ('guides/singbox.html', 'sing-box &mdash; rule-set', 'The site’s domains and networks as a rule-set for sing-box and Hiddify: <code>route.rule_set</code>, compiling to <code>.srs</code>.'),
            ('guides/happ.html', 'Happ &mdash; routing profile', 'A JSON profile with the <code>ProxySites</code> and <code>ProxyIp</code> lists; into the app as a <code>happ://routing/onadd</code> link.'),
            ('guides/xray.html', 'Xray &mdash; routing.rules', 'Rules for an Xray-core config, the 3X-UI panel and import into v2rayN.'),
            ('guides/amnezia.html', 'AmneziaVPN &mdash; site list', 'Hosts with addresses and subnets for split tunneling, import via the ⋮ menu.'),
        ],
        'guides_anchor_href': 'guides/openvpn.html',
        'footer_links': [('guides/singbox.html', 'sing-box'), ('guides/happ.html', 'Happ'), ('guides/xray.html', 'Xray'), ('guides/amnezia.html', 'AmneziaVPN')],
    },
    'es': {
        'version_old': '4.1.2', 'version_new': '4.1.3', 'generated_old': 'generated 2026-10-13', 'generated_new': f'generated {TODAY}',
        'hero_old': 'Genera comandos de enrutamiento optimizados para <strong>9 plataformas</strong> al instante.',
        'hero_new': 'Genera rutas y reglas para <strong>21 formatos</strong> al instante: routers, sistemas operativos, clientes VPN y proxy.',
        'feature_old': '"Exportar como .bat, .sh, .rsc, .conf, .ovpn y .bat para Keenetic"',
        'feature_new': ('"Exportar como .bat, .sh, .rsc, .conf, .ovpn, .json, .yaml, .list, .pac y .bat para Keenetic",\n'
                        '            "Reglas para clientes proxy: sing-box, Clash/mihomo, Xray, v2rayN, Happ, Shadowrocket/Surge, Quantumult X, PAC",\n'
                        '            "Lista de sitios de AmneziaVPN para split tunneling",\n'
                        '            "MikroTik address-list, rutas DNS de Keenetic (KeeneticOS 5), rutas de OpenWrt (uci)"'),
        'faq1_old': 'NetRoute genera comandos de enrutamiento para 9 plataformas: Windows, Linux, macOS, MikroTik, Cisco, Juniper, WireGuard (AllowedIPs), OpenVPN y Keenetic, además de tu propia plantilla. Compatible con IPv4 e IPv6 (el formato Keenetic es solo IPv4).',
        'faq1_new': 'NetRoute genera 21 formatos. Comandos de rutas para sistemas operativos y routers: Windows, Linux, macOS, OpenWrt, MikroTik, Cisco, Juniper, Keenetic; reglas para clientes VPN y proxy: WireGuard (AllowedIPs), OpenVPN, AmneziaVPN, sing-box, Clash/mihomo, Xray, v2rayN, Happ, Shadowrocket/Surge, Quantumult X y PAC; listas para routers: MikroTik address-list y rutas DNS de Keenetic (KeeneticOS 5). Además de tu propia plantilla. Compatible con IPv4 e IPv6; los formatos Keenetic .bat, AmneziaVPN y PAC son solo IPv4.',
        'faq_new_q': '¿Funciona NetRoute con clientes proxy como Hiddify, Happ o v2rayN?',
        'faq_new_a': 'Sí. Elige el formato del cliente en «SO de destino» y NetRoute genera reglas con los dominios y redes del sitio en lugar de comandos de rutas: un rule-set para sing-box (Hiddify, NekoBox), un rule-provider para Clash/mihomo, routing.rules para Xray y el panel 3X-UI, un archivo de importación de reglas para v2rayN, un perfil de enrutamiento de Happ, una lista de reglas para Shadowrocket/Surge y Quantumult X, un archivo PAC y una lista de sitios para AmneziaVPN. Los dominios se agrupan por sufijo; las redes son las mismas que en las rutas.',
        'faq_anchor_q': '¿Se puede usar para VPN split tunneling?',
        'card_rules_h3': 'Reglas para clientes proxy',
        'card_rules_p': 'Los mismos dominios y redes como reglas: sing-box (Hiddify), Clash/mihomo, Xray y 3X-UI, v2rayN, Happ, Shadowrocket/Surge, Quantumult X, PAC &mdash; y una lista de sitios para AmneziaVPN.',
        'card_lists_h3': 'Listas para routers',
        'card_lists_p': 'MikroTik address-list y rutas DNS de Keenetic (KeeneticOS 5) en lugar de cientos de rutas; rutas persistentes de OpenWrt mediante uci.',
        'cards_anchor': '<h3>Exportación Keenetic</h3>',
        'platforms_h2_old': '<h2>9 formatos de plataforma</h2>',
        'platforms_h2_new': '<h2>21 formatos de salida</h2>',
        'platforms_p_old': '<p>Sintaxis nativa de comandos para cada SO principal y proveedor de equipos de red.</p>',
        'platforms_p_new': '<p>Comandos de rutas para sistemas operativos y routers, reglas para clientes VPN y proxy &mdash; cada uno en su sintaxis nativa.</p>',
        'ipv4_only': 'solo IPv4',
        'stat_formats_old': '<span class="stat-value">9</span>\n        <span class="stat-label">Formatos de plataforma</span>',
        'stat_formats_new': '<span class="stat-value">21</span>\n        <span class="stat-label">Formatos de salida</span>',
        'stat_export_old': '<span class="stat-value">7</span>\n        <span class="stat-label">Formatos de exportación</span>',
        'stat_export_new': '<span class="stat-value">12</span>\n        <span class="stat-label">Tipos de archivo</span>',
        'guides': [
            ('guides/singbox.html', 'sing-box &mdash; rule-set', 'Dominios y redes del sitio como rule-set para sing-box y Hiddify: <code>route.rule_set</code>, compilación a <code>.srs</code>.'),
            ('guides/happ.html', 'Happ &mdash; perfil de enrutamiento', 'Perfil JSON con las listas <code>ProxySites</code> y <code>ProxyIp</code>; a la app mediante un enlace <code>happ://routing/onadd</code>.'),
            ('guides/xray.html', 'Xray &mdash; routing.rules', 'Reglas para una configuración Xray-core, el panel 3X-UI y la importación en v2rayN.'),
            ('guides/amnezia.html', 'AmneziaVPN &mdash; lista de sitios', 'Hosts con direcciones y subredes para split tunneling, importación mediante el menú ⋮.'),
        ],
        'guides_anchor_href': 'guides/openvpn.html',
        'footer_links': [('guides/singbox.html', 'sing-box'), ('guides/happ.html', 'Happ'), ('guides/xray.html', 'Xray'), ('guides/amnezia.html', 'AmneziaVPN')],
    },
    'zh': {
        'version_old': '4.1.2', 'version_new': '4.1.3', 'generated_old': 'generated 2026-10-13', 'generated_new': f'generated {TODAY}',
        'hero_old': '为<strong>9个平台</strong>即时生成优化的路由命令。',
        'hero_new': '即时生成 <strong>21 种格式</strong>的路由和规则：路由器、操作系统、VPN 和代理客户端。',
        'feature_old': '"导出为 .bat、.sh、.rsc、.conf、.ovpn 和 Keenetic .bat"',
        'feature_new': ('"导出为 .bat、.sh、.rsc、.conf、.ovpn、.json、.yaml、.list、.pac 和 Keenetic .bat",\n'
                        '            "代理客户端规则：sing-box、Clash/mihomo、Xray、v2rayN、Happ、Shadowrocket/Surge、Quantumult X、PAC",\n'
                        '            "AmneziaVPN 分流站点列表",\n'
                        '            "MikroTik address-list、Keenetic DNS 路由（KeeneticOS 5）、OpenWrt 路由（uci）"'),
        'faq1_old': 'NetRoute 为 9 个平台生成路由命令：Windows、Linux、macOS、MikroTik、Cisco、Juniper、WireGuard（AllowedIPs）、OpenVPN 和 Keenetic，并支持自定义模板。支持 IPv4 和 IPv6（Keenetic 格式仅支持 IPv4）。',
        'faq1_new': 'NetRoute 输出 21 种格式。操作系统和路由器的路由命令：Windows、Linux、macOS、OpenWrt、MikroTik、Cisco、Juniper、Keenetic；VPN 和代理客户端的规则：WireGuard（AllowedIPs）、OpenVPN、AmneziaVPN、sing-box、Clash/mihomo、Xray、v2rayN、Happ、Shadowrocket/Surge、Quantumult X 和 PAC；路由器列表：MikroTik address-list 和 Keenetic DNS 路由（KeeneticOS 5）。另支持自定义模板。支持 IPv4 和 IPv6；Keenetic .bat、AmneziaVPN 和 PAC 格式仅支持 IPv4。',
        'faq_new_q': 'NetRoute 能用于 Hiddify、Happ、v2rayN 等代理客户端吗？',
        'faq_new_a': '可以。在「目标系统」中选择客户端的格式，NetRoute 会输出包含网站域名和网段的规则，而不是路由命令：sing-box（Hiddify、NekoBox）的 rule-set、Clash/mihomo 的 rule-provider、Xray 和 3X-UI 面板的 routing.rules、v2rayN 的规则导入文件、Happ 路由配置文件、Shadowrocket/Surge 和 Quantumult X 的规则列表、PAC 文件以及 AmneziaVPN 的站点列表。域名按后缀合并；网段与路由中的相同。',
        'faq_anchor_q': '可以用于 VPN 分流吗？',
        'card_rules_h3': '代理客户端规则',
        'card_rules_p': '同样的域名和网段以规则形式输出：sing-box（Hiddify）、Clash/mihomo、Xray 和 3X-UI、v2rayN、Happ、Shadowrocket/Surge、Quantumult X、PAC，以及 AmneziaVPN 的站点列表。',
        'card_lists_h3': '路由器列表',
        'card_lists_p': '用 MikroTik address-list 和 Keenetic DNS 路由（KeeneticOS 5）代替数百条路由；通过 uci 写入 OpenWrt 的持久路由。',
        'cards_anchor': '<h3>Keenetic导出</h3>',
        'platforms_h2_old': '<h2>9种平台格式</h2>',
        'platforms_h2_new': '<h2>21 种输出格式</h2>',
        'platforms_p_old': '<p>支持所有主要操作系统和网络设备厂商的原生命令语法。</p>',
        'platforms_p_new': '<p>操作系统和路由器的路由命令、VPN 和代理客户端的规则——均采用各自的原生语法。</p>',
        'ipv4_only': '仅 IPv4',
        'stat_formats_old': '<span class="stat-value">9</span>\n        <span class="stat-label">平台格式</span>',
        'stat_formats_new': '<span class="stat-value">21</span>\n        <span class="stat-label">种输出格式</span>',
        'stat_export_old': '<span class="stat-value">7</span>\n        <span class="stat-label">种导出格式</span>',
        'stat_export_new': '<span class="stat-value">12</span>\n        <span class="stat-label">种文件类型</span>',
        'guides': [
            ('guides/singbox.html', 'sing-box &mdash; rule-set', '网站的域名和网段生成 sing-box 与 Hiddify 的 rule-set：<code>route.rule_set</code>，编译为 <code>.srs</code>。'),
            ('guides/happ.html', 'Happ &mdash; 路由配置文件', '包含 <code>ProxySites</code> 和 <code>ProxyIp</code> 列表的 JSON 配置；通过 <code>happ://routing/onadd</code> 链接导入应用。'),
            ('guides/xray.html', 'Xray &mdash; routing.rules', '用于 Xray-core 配置、3X-UI 面板以及导入 v2rayN 的规则。'),
            ('guides/amnezia.html', 'AmneziaVPN &mdash; 站点列表', '带地址的主机和子网，用于分流；通过 ⋮ 菜单导入。'),
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
