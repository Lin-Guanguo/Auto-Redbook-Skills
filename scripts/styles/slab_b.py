"""Slab-B style — 厚板风变体: dark teal + terracotta editorial."""

from styles.slab_base import PALETTE_B, slab_generate_cover, slab_generate_card

STYLE_NAME = "slab-b"
STYLE_DESCRIPTION = "厚板 B — 墨青+赤陶，青绿暖土"
COVER_HEIGHT = 1440

_PALETTE = PALETTE_B


def generate_cover(title, subtitle, first_section_html, width, height):
    return slab_generate_cover(_PALETTE, title, subtitle, first_section_html, width, height)


def generate_card(content_html, page_number, total_pages, width, height):
    return slab_generate_card(_PALETTE, content_html, page_number, total_pages, width, height)
