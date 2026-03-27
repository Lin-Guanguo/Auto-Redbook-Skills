#!/usr/bin/env python3
"""
New rendering entry point for the style system.

Usage:
    python scripts/render.py input.md --style paper -o ./output
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Ensure styles package is importable
sys.path.insert(0, str(Path(__file__).parent))

from styles import get_style, list_styles
from styles.base import (
    convert_markdown_to_html,
    parse_markdown_file,
    split_content_by_separator,
)

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Missing dependency: playwright")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)

DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1440
MAX_HEIGHT = 4320


async def render_html_to_image(
    html_content: str,
    output_path: str,
    width: int,
    height: int,
    max_height: int,
    dpr: int,
    page,
) -> int:
    """Render HTML to PNG using an existing Playwright page. Returns actual height."""
    await page.set_content(html_content, wait_until="load")
    await page.evaluate("() => document.fonts.ready")

    # Let content determine height (within bounds)
    content_height = await page.evaluate(
        """() => {
        const el = document.querySelector('.page');
        return el ? el.scrollHeight : document.body.scrollHeight;
    }"""
    )
    actual_height = max(height, min(content_height, max_height))

    await page.screenshot(
        path=output_path,
        clip={"x": 0, "y": 0, "width": width, "height": actual_height},
        type="png",
    )
    print(f"  -> {output_path} ({width}x{actual_height})")
    return actual_height


async def render(
    md_file: str,
    output_dir: str,
    style_name: str,
    width: int,
    height: int,
    max_height: int,
    dpr: int,
):
    style = get_style(style_name)
    print(f"Rendering: {md_file}")
    print(f"Style: {style.STYLE_NAME} — {style.STYLE_DESCRIPTION}")

    os.makedirs(output_dir, exist_ok=True)

    data = parse_markdown_file(md_file)
    metadata = data["metadata"]
    body = data["body"]

    sections = split_content_by_separator(body)
    if not sections:
        print("No content found.")
        return

    title = metadata.get("title", "")
    subtitle = metadata.get("subtitle", "")

    # First section → cover, rest → cards
    first_section_html = convert_markdown_to_html(sections[0])
    card_sections = sections[1:]
    total_pages = 1 + len(card_sections)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": width, "height": max_height},
            device_scale_factor=dpr,
        )

        # Page 1: cover
        cover_html = style.generate_cover(
            title, subtitle, first_section_html, width, height
        )
        await render_html_to_image(
            cover_html,
            os.path.join(output_dir, "page_1.png"),
            width, height, max_height, dpr, page,
        )

        # Page 2+: cards
        for i, section in enumerate(card_sections, start=2):
            section_html = convert_markdown_to_html(section)
            card_html = style.generate_card(
                section_html, i, total_pages, width, height
            )
            await render_html_to_image(
                card_html,
                os.path.join(output_dir, f"page_{i}.png"),
                width, height, max_height, dpr, page,
            )

        await page.close()
        await browser.close()

    print(f"\nDone! {total_pages} pages saved to {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Render markdown to styled image cards"
    )
    parser.add_argument("markdown_file", help="Markdown file path")
    parser.add_argument(
        "--style", "-s", required=True,
        choices=list_styles(),
        help="Visual style",
    )
    parser.add_argument(
        "--output-dir", "-o", default=os.getcwd(),
        help="Output directory (default: cwd)",
    )
    parser.add_argument("--width", "-w", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--max-height", type=int, default=MAX_HEIGHT)
    parser.add_argument("--dpr", type=int, default=2)

    args = parser.parse_args()

    if not os.path.exists(args.markdown_file):
        print(f"File not found: {args.markdown_file}")
        sys.exit(1)

    asyncio.run(
        render(
            args.markdown_file,
            args.output_dir,
            style_name=args.style,
            width=args.width,
            height=args.height,
            max_height=args.max_height,
            dpr=args.dpr,
        )
    )


if __name__ == "__main__":
    main()
