"""Slab-C style — 厚板风变体: slate + copper editorial."""

from styles.slab_base import PALETTE_C, slab_generate_cover, slab_generate_card

STYLE_NAME = "slab-c"
STYLE_DESCRIPTION = "厚板 C — 烟墨+赭铜，冷暖杂志感"
COVER_HEIGHT = 1440

_PALETTE = PALETTE_C


def generate_cover(title, subtitle, first_section_html, width, height):
    return slab_generate_cover(_PALETTE, title, subtitle, first_section_html, width, height)


def generate_card(content_html, page_number, total_pages, width, height):
    return slab_generate_card(_PALETTE, content_html, page_number, total_pages, width, height)
