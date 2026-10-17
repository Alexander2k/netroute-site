#!/usr/bin/env python3
"""
WebP copies of the popup renders in screenshots/guides/<lang>/: the pages reference the .webp
(every current browser decodes it) and the .png captures stay in the repository as the source.

    python3 tools/convert_shots_webp.py        # converts what is missing or older than its PNG

Requires Pillow. Lossless would keep every pixel but roughly match the PNG size; quality 88 keeps
the UI text crisp at a fraction of the weight (checked by eye on the 2x captures).
"""

import glob
import os
import sys

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
QUALITY = 88


def main() -> int:
    done = skipped = 0
    before = after = 0
    for png in sorted(glob.glob(os.path.join(ROOT, 'screenshots', 'guides', '*', '*.png'))):
        webp = png[:-4] + '.webp'
        if os.path.exists(webp) and os.path.getmtime(webp) >= os.path.getmtime(png):
            skipped += 1
            continue
        with Image.open(png) as im:
            im.save(webp, 'WEBP', quality=QUALITY, method=6)
        before += os.path.getsize(png)
        after += os.path.getsize(webp)
        done += 1
    if done:
        print(f'converted {done} files: {before // 1024} KB PNG -> {after // 1024} KB WebP ({100 * after // max(before, 1)}%)')
    print(f'up to date: {skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
