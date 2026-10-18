#!/usr/bin/env python3
"""
style.css -> style.min.css. style.css stays the source you edit; the pages load style.min.css.

    python3 tools/minify_css.py

Conservative on purpose: removes comments, collapses whitespace and drops spaces only next to
{ } ; and after , — never around ':' (a space before ':' changes a selector: `a :hover` is not
`a:hover`) and never inside calc() (`a + b` needs its spaces). Strings and url() are kept as they are.
"""

import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'style.css')
OUT = os.path.join(ROOT, 'style.min.css')

TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|url\([^)]*\)|/\*.*?\*/', re.DOTALL)


def minify(css: str) -> str:
    # protect strings and url(); drop comments
    kept = []

    def stash(m):
        s = m.group(0)
        if s.startswith('/*'):
            return ' '
        kept.append(s)
        return f'\x00{len(kept) - 1}\x00'

    css = TOKEN.sub(stash, css)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};])\s*', r'\1', css)
    css = re.sub(r',\s+', ',', css)
    css = css.replace(';}', '}').strip()
    return re.sub(r'\x00(\d+)\x00', lambda m: kept[int(m.group(1))], css)


def main() -> int:
    with open(SRC, encoding='utf-8') as f:
        src = f.read()
    out = minify(src)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out + '\n')
    print(f'style.css {len(src.encode())} B -> style.min.css {len(out.encode())} B')
    # sanity: same number of rule blocks
    if src.count('{') != out.count('{') or src.count('}') != out.count('}'):
        print('brace count changed — check the output', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
