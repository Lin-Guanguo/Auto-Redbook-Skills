"""Shared utilities for style modules."""

import re
from typing import List

import markdown
import yaml


def css_reset() -> str:
    return "* { margin: 0; padding: 0; box-sizing: border-box; }"


def font_imports(fonts: List[str]) -> str:
    urls = []
    for font in fonts:
        name = font.replace(" ", "+")
        urls.append(
            f"@import url('https://fonts.googleapis.com/css2?"
            f"family={name}:wght@300;400;500;700;900&display=swap');"
        )
    return "\n".join(urls)


def html_document(body: str, styles: str, width: int, scripts: str = "") -> str:
    script_tag = f"<script>{scripts}</script>" if scripts else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width={width}">
    <style>
{styles}
    </style>
</head>
<body>
{body}
{script_tag}
</body>
</html>"""


def convert_markdown_to_html(md_content: str) -> str:
    # Extract tags (lines like #tag at end)
    tags_pattern = r'((?:#[\w\u4e00-\u9fa5]+\s*)+)$'
    tags_match = re.search(tags_pattern, md_content, re.MULTILINE)
    tags_html = ""

    if tags_match:
        tags_str = tags_match.group(1)
        md_content = md_content[:tags_match.start()].strip()
        tags = re.findall(r'#([\w\u4e00-\u9fa5]+)', tags_str)
        if tags:
            tags_html = '<div class="tags-container">'
            for tag in tags:
                tags_html += f'<span class="tag">#{tag}</span>'
            tags_html += "</div>"

    html = markdown.markdown(
        md_content,
        extensions=["extra", "codehilite", "tables", "nl2br"],
    )
    return html + tags_html


def title_font_size(title: str, width: int) -> int:
    length = len(title)
    if length <= 6:
        return int(width * 0.14)
    elif length <= 10:
        return int(width * 0.12)
    elif length <= 18:
        return int(width * 0.09)
    elif length <= 30:
        return int(width * 0.07)
    else:
        return int(width * 0.055)


def page_number_html(current: int, total: int) -> str:
    if total <= 1:
        return ""
    return f'<div class="page-number">{current}/{total}</div>'


def parse_markdown_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    yaml_pattern = r"^---\s*\n(.*?)\n---\s*\n"
    yaml_match = re.match(yaml_pattern, content, re.DOTALL)

    metadata = {}
    body = content

    if yaml_match:
        try:
            metadata = yaml.safe_load(yaml_match.group(1)) or {}
        except yaml.YAMLError:
            metadata = {}
        body = content[yaml_match.end():]

    return {"metadata": metadata, "body": body.strip()}


def split_content_by_separator(body: str) -> List[str]:
    parts = re.split(r"\n---+\n", body)
    return [part.strip() for part in parts if part.strip()]
