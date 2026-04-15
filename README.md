# Auto-Redbook-Skills

Markdown to image rendering tool for social media (Xiaohongshu, etc). Uses headless Chrome (Playwright) to render styled HTML into 9:16 vertical images.

## New Style System (`render.py`)

Each style is a self-contained Python module — fully controls layout, colors, fonts, and decorations. No shared HTML skeleton, no template limitations.

### Usage

```bash
python scripts/render.py input.md --style paper -o ./output
```

### Input Format

Markdown with YAML frontmatter. Use `---` to separate pages.

```markdown
---
title: "Article Title"
subtitle: "Optional subtitle"
---

First section (becomes cover page with large title).

---

Second section (page 2).

---

More sections...
```

- Page 1 (cover): title + subtitle + first section content
- Page 2+: one section per page
- Content height is dynamic — pages grow to fit, capped at `--max-height`

### Available Styles

| Style | Description |
|-------|-------------|
| `paper` | 笔记纸 — ruled lines + red margin line, warm paper background |
| `mono` / `stamp` / `canvas` / `blueprint` / `kraft` / `block` | earlier variants, kept for compatibility |
| `slab` / `slab-a` / `slab-b` / `slab-c` | Slab series — heavy color bands; A=indigo+amber, B=teal+terracotta, C=smoke+bronze |
| `verdict` | 裁定书 — parchment, serif clauses, red stamp |
| `roadmap` | 路线图 — light bg + 3-color route system, station markers, highlighter bold |
| `strata` | 技术地层 — aged parchment + indigo/rust/ochre era bands + § Ⅰ-Ⅶ numerals + ledger tables |

### Parameters

| Param | Short | Default | Description |
|-------|-------|---------|-------------|
| `--style` | `-s` | required | Style name |
| `--output-dir` | `-o` | cwd | Output directory |
| `--width` | `-w` | 1080 | Image width (px) |
| `--height` | | 1440 | Min image height / content page height (px) |
| `--cover-height` | | same as `--height` | Cover page height when it differs from content |
| `--max-height` | | 4320 | Max image height (px) |
| `--dpr` | | 2 | Device pixel ratio |

### Rendering Workflow (for long-form articles)

The canonical workflow for taking a long blog/reference markdown and producing an N-page redbook note:

1. **Copy, don't transform.** `cp source.md output/{slug}/input.md`. All edits happen inside `input.md`; source is never touched. This preserves diff-ability.
2. **Minimal header rewrite.** Replace the top `# Title` / `*subtitle*` / `Last Updated` block with YAML frontmatter (`title`, `subtitle`). Leave everything else verbatim.
3. **Preserve original text.** Do not compress, paraphrase, or drop sections unless explicitly requested. User has usually already compressed the source.
4. **Highlights only.** Authorized modifications to body content: wrap key phrases in `**bold**` so the style's highlighter kicks in.
5. **Verify with diff.** Before claiming done, `diff source input.md`. Every hunk must map to an explicit user approval. This catches accidental drops (e.g. missing words in a title).

### Page-count tuning

- `auto_split` uses `height * 0.92` as the per-page budget. Every ±1px of body font-size ≈ ±1 page on an ~18-page article.
- To hit a specific page count: start at default, get baseline, then adjust body `font-size` and `line-height` in 1px / 0.02 steps. Reduce paragraph/list margins next.
- **Chapter bands flow inline.** `render.py` does not force a new page on `##`. H2 renders mid-card with a generous top margin (`margin-top: ~36px`) and a full-width banner. This saves 1-2 pages compared to forced H2 breaks.
- **Tables → lists for density.** A 3-col table takes ~1.5-2× the vertical space of the equivalent `- **title** rating — description` list. Convert tables to lists when you need to compress without shrinking font.

### Canonical dimensions (user preference)

- **Cover:** 1080×1440 (3:4 portrait) or 1080×1520 when the cover has bottom decorations (timelines, badges) that risk overlapping the last line of body text.
- **Content:** 1080×1920 (9:16).
- **Command:** `--style <name> --cover-height 1440 --height 1920`.

### Multi-line title sizing

When a title uses `<br>` to split into multiple lines, compute the font-size from the **longest line's em-width**, not character count. A good CJK+Latin approximation:

```
em_width(ch) = 1.0   for CJK / full-width punctuation
             = 0.56  for Latin
             = 0.28  for space
font_size = (page_width - 2 * pad_x) * 0.95 / max_line_em_width
```

This fills the available width without wrapping, regardless of mixed scripts.

### Preview Styles

Generate an HTML page to visually compare all available styles:

```bash
python scripts/preview_styles.py          # opens in browser
python scripts/preview_styles.py -o preview.html  # save to file
```

### Adding a New Style

Create `scripts/styles/mystyle.py`:

```python
STYLE_NAME = "mystyle"
STYLE_DESCRIPTION = "My custom style"

def generate_cover(title, subtitle, first_section_html, width, height) -> str:
    """Return complete HTML for the cover page."""

def generate_card(content_html, page_number, total_pages, width, height) -> str:
    """Return complete HTML for content pages."""
```

Register in `scripts/styles/__init__.py`.

### Dependencies

```bash
pip install markdown pyyaml playwright
playwright install chromium
```

## Legacy Theme System (`render_xhs.py`)

The old rendering system with 11 CSS themes sharing a fixed HTML layout. Still works, documented in `README.old.md`.
