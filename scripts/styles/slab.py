"""Slab style — 厚板风: warm color blocks, forest green + terracotta editorial."""

from styles.slab_base import PALETTE_ORIGINAL, slab_generate_cover, slab_generate_card

STYLE_NAME = "slab"
STYLE_DESCRIPTION = "厚板 — 暖色大色块，森绿+赤陶，杂志编辑感"
COVER_HEIGHT = 1440

_PALETTE = PALETTE_ORIGINAL


def generate_cover(title, subtitle, first_section_html, width, height):
    return slab_generate_cover(
        _PALETTE, title, subtitle, first_section_html, width, height,
        series_text="LLM Agent 研究系列 · 第二篇",
    )


def generate_card(content_html, page_number, total_pages, width, height):
    return slab_generate_card(_PALETTE, content_html, page_number, total_pages, width, height)
