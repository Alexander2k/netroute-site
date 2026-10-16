#!/usr/bin/env python3
"""
Insert (or refresh) the popup render into the hand-written guides: a <figure class="shot"> with
the light and dark captures of the extension for the guide's format, placed right after the lead
paragraph. The generated guides get theirs from tools/gen_client_guides.py.

Renders come from the extension repository:
    node scripts/render_guide_shots.cjs <site>/screenshots/guides/en en
    node scripts/render_guide_shots.cjs <site>/screenshots/guides/ru ru

Run:
    python3 tools/add_guide_shots.py            # all languages whose renders exist
Idempotent: an existing figure is replaced, nothing else on the page changes.
"""

import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# guide stem -> format key of the extension (the file name of the render)
GUIDE_FORMAT = {
    'keenetic': 'keenetic',
    'mikrotik': 'mikrotik',
    'wireguard': 'wireguard',
    'linux': 'linux',
    'openvpn': 'openvpn',
}

LANG_DIRS = {'en': '', 'ru': 'ru/', 'es': 'es/', 'zh': 'zh/'}

TEXT = {
    'en': {
        'alt': 'NetRoute popup after scanning github.com: the {name} format is selected and the result is shown on the Routes tab',
        'caption': 'What the result looks like in NetRoute: the <strong>{name}</strong> format is selected under “Target OS”, the output is on the Routes tab. Scan data: a github.com page.',
    },
    'ru': {
        'alt': 'Попап NetRoute после сканирования github.com: выбран формат {name}, результат на вкладке «Маршруты»',
        'caption': 'Так выглядит результат в NetRoute: формат <strong>{name}</strong> выбран в списке «Целевая ОС», вывод &mdash; на вкладке «Маршруты». Данные скана &mdash; страница github.com.',
    },
    'es': {
        'alt': 'Popup de NetRoute tras escanear github.com: formato {name} seleccionado y resultado en la pestaña Rutas',
        'caption': 'Así se ve el resultado en NetRoute: el formato <strong>{name}</strong> elegido en «SO de destino», la salida en la pestaña Rutas. Datos del escaneo: una página de github.com.',
    },
    'zh': {
        'alt': '扫描 github.com 后的 NetRoute 弹窗：已选择 {name} 格式，结果显示在「路由」标签页',
        'caption': 'NetRoute 中的结果：在「目标系统」中选择 <strong>{name}</strong> 格式，输出显示在「路由」标签页。扫描数据：github.com 页面。',
    },
}

# display name of the format, as the selector shows it
NAMES = {'keenetic': 'Keenetic', 'mikrotik': 'MikroTik', 'wireguard': 'WireGuard', 'linux': 'Linux', 'openvpn': 'OpenVPN'}

FIGURE_RE = re.compile(r'    <figure class="shot">.*?</figure>\n', re.DOTALL)
LEAD_RE = re.compile(r'(    <p class="lead">.*?</p>\n)', re.DOTALL)


def png_size(path: str):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    return int.from_bytes(head[16:20], 'big'), int.from_bytes(head[20:24], 'big')


def figure(lang: str, fmt: str) -> str:
    shots_lang = 'ru' if lang == 'ru' else 'en'
    light = os.path.join(ROOT, 'screenshots', 'guides', shots_lang, f'{fmt}-light.png')
    dark = os.path.join(ROOT, 'screenshots', 'guides', shots_lang, f'{fmt}-dark.png')
    size = png_size(light)
    if not size or not os.path.exists(dark):
        return ''
    w, h = size[0] // 2, size[1] // 2
    # English guides live in guides/ (one level below the root), the others in <lang>/guides/
    up = '../' if lang == 'en' else '../../'
    rel = f'{up}screenshots/guides/{shots_lang}/{fmt}'
    alt = TEXT[lang]['alt'].format(name=NAMES[fmt])
    caption = TEXT[lang]['caption'].format(name=NAMES[fmt])
    return (f'    <figure class="shot">\n'
            f'        <img class="shot-light" src="{rel}-light.png" width="{w}" height="{h}" loading="lazy" alt="{alt}">\n'
            f'        <img class="shot-dark" src="{rel}-dark.png" width="{w}" height="{h}" loading="lazy" alt="{alt}">\n'
            f'        <figcaption>{caption}</figcaption>\n'
            f'    </figure>\n')


def main() -> int:
    only = sys.argv[1:]  # optional language codes
    changed = skipped = 0
    for lang, prefix in LANG_DIRS.items():
        if only and lang not in only:
            continue
        for guide, fmt in GUIDE_FORMAT.items():
            path = os.path.join(ROOT, prefix, 'guides', f'{guide}.html')
            if not os.path.exists(path):
                continue
            fig = figure(lang, fmt)
            if not fig:
                skipped += 1
                continue
            with open(path, encoding='utf-8') as f:
                html = f.read()
            new = FIGURE_RE.sub('', html)
            m = LEAD_RE.search(new)
            if not m:
                print(f'{os.path.relpath(path, ROOT)}: no lead paragraph, skipped', file=sys.stderr)
                skipped += 1
                continue
            new = new[:m.end()] + '\n' + fig + new[m.end():]
            if new != html:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new)
                changed += 1
                print(f'updated: {os.path.relpath(path, ROOT)}')
    print(f'Done. Updated: {changed}, skipped (no renders yet): {skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
