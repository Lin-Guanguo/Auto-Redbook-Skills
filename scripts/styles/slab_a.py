"""Slab-A style — 厚板风变体: indigo + amber editorial."""

from styles.slab_base import PALETTE_A, slab_generate_cover, slab_generate_card

STYLE_NAME = "slab-a"
STYLE_DESCRIPTION = "厚板 A — 靛蓝+琥珀，海洋暖金"
COVER_HEIGHT = 1440

_PALETTE = PALETTE_A


def generate_cover(title, subtitle, first_section_html, width, height):
    return slab_generate_cover(_PALETTE, title, subtitle, first_section_html, width, height)


def generate_card(content_html, page_number, total_pages, width, height):
    return slab_generate_card(_PALETTE, content_html, page_number, total_pages, width, height)
