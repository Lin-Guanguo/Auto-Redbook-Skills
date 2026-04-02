#!/usr/bin/env python3
"""
New rendering entry point for the style system.

Usage:
    python scripts/render.py input.md --style paper -o ./output
"""

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path
from typing import List

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


def split_into_blocks(md_text: str) -> List[str]:
    """Split markdown into logical blocks, preserving code blocks as single units."""
    blocks = []
    current: list[str] = []
    in_code = False

    for line in md_text.split("\n"):
        if line.startswith("```"):
            if not in_code:
                # Starting a code block — flush any pending text first
                if current and any(l.strip() for l in current):
                    blocks.append("\n".join(current))
                    current = []
                current.append(line)
                in_code = True
            else:
                # Ending a code block
                current.append(line)
                blocks.append("\n".join(current))
                current = []
                in_code = False
        elif in_code:
            current.append(line)
        elif line.strip() == "":
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            current.append(line)

    if current:
        blocks.append("\n".join(current))

    return [b for b in blocks if b.strip()]


async def auto_split_content(
    body_md: str, style, width: int, height: int, dpr: int
) -> List[str]:
    """Split markdown body into pages based on actual rendered height."""
    blocks = split_into_blocks(body_md)
    if not blocks:
        return []

    pages: list[str] = []
    current_blocks: list[str] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": width, "height": height * 3},
            device_scale_factor=dpr,
        )

        for block in blocks:
            # H2 headings force a new page
            is_h2 = block.strip().startswith("## ")
            if is_h2 and current_blocks:
                pages.append("\n\n".join(current_blocks))
                current_blocks = []

            test_blocks = current_blocks + [block]
            test_md = "\n\n".join(test_blocks)
            test_html = convert_markdown_to_html(test_md)
            card_html = style.generate_card(test_html, 1, 1, width, height)

            await page.set_content(card_html, wait_until="load")
            await page.evaluate("() => document.fonts.ready")

            content_height = await page.evaluate(
                """() => {
                const el = document.querySelector('.content');
                return el ? el.scrollHeight : document.body.scrollHeight;
            }"""
            )

            available = height * 0.92

            if content_height > available and current_blocks:
                pages.append("\n\n".join(current_blocks))
                current_blocks = [block]
            else:
                current_blocks = test_blocks

        if current_blocks:
            pages.append("\n\n".join(current_blocks))

        await page.close()
        await browser.close()

    return pages


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
    cover_height: int | None = None,
):
    style = get_style(style_name)
    ch = cover_height or height  # cover uses its own height if specified
    print(f"Rendering: {md_file}")
    print(f"Style: {style.STYLE_NAME} — {style.STYLE_DESCRIPTION}")
    if cover_height:
        print(f"  Cover: {width}x{ch}, Content: {width}x{height}")

    os.makedirs(output_dir, exist_ok=True)

    data = parse_markdown_file(md_file)
    metadata = data["metadata"]
    body = data["body"]

    title = metadata.get("title", "")
    subtitle = metadata.get("subtitle", "")

    # Split: first --- separates cover content from body
    parts = split_content_by_separator(body)
    if not parts:
        print("No content found.")
        return

    cover_md = parts[0]
    rest_md = "\n\n".join(parts[1:]) if len(parts) > 1 else ""

    # Auto-split the body into pages (uses content page height)
    print("  Analyzing content for auto-split...")
    if rest_md:
        card_pages = await auto_split_content(rest_md, style, width, height, dpr)
    else:
        card_pages = []

    total_pages = 1 + len(card_pages)
    print(f"  {total_pages} pages ({1} cover + {len(card_pages)} content)")

    # Render all pages
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": width, "height": max_height},
            device_scale_factor=dpr,
        )

        # Page 1: cover (uses cover height)
        cover_html_content = convert_markdown_to_html(cover_md)
        cover_html = style.generate_cover(
            title, subtitle, cover_html_content, width, ch
        )
        await render_html_to_image(
            cover_html,
            os.path.join(output_dir, "page_1.png"),
            width, ch, max_height, dpr, page,
        )

        # Page 2+: auto-split cards (uses content height)
        for i, card_md in enumerate(card_pages, start=2):
            card_html_content = convert_markdown_to_html(card_md)
            card_html = style.generate_card(
                card_html_content, i, total_pages, width, height
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
    parser.add_argument(
        "--cover-height", type=int, default=None,
        help="Cover page height (default: same as --height)",
    )

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
            cover_height=args.cover_height,
        )
    )


if __name__ == "__main__":
    main()
