Last Updated: 2026-04-21

# `essay` Style Design

## Background

Adding a new style for the article `shortcut-vs-friction` (捷径与摩擦：AI 时代重新理解人类的学习). The existing `paper` style was rejected for this article because (a) the left red margin line plus 14% left padding wastes horizontal space on the cover, and (b) blockquotes (marked as 金句 / "golden lines" in the source) receive no visual emphasis.

The new style targets long-form reflective essays with:
- A mix of personal narrative, first-hand research citations, and policy overview
- Frequent `**bold**` inline emphasis
- 8+ blockquotes used as narrative punctuation (金句)

Visual reference: the bookish register of 三联 / 单读 / 企鹅经典 long-form editorial — "a book that has been read twice, marked up with a highlighter."

## Design Decisions

1. **Aesthetic register**: classic essay / 二次阅读的书本. Rejected alternatives: handwritten notes (too casual), magazine columns (too cold).

2. **Palette P1 — cream + navy + yellow highlighter**. Rejected P2 (warm rust — too nostalgic for AI topic) and P3 (dark forest — too literary, misfit with research/policy content).

3. **Pullquote as primary 金句 treatment (Q2)**. Blockquotes become oversized italic navy serif pulled between two navy rules across the content area. Rejected Q1 (book-edge quote — too quiet) and Q3 (sticky-note card — clashes with yellow highlighter).

4. **Balanced left/right padding (7%/7%)**. Eliminates `paper` style's notebook-margin asymmetry and recovers ~7% horizontal width for body content.

5. **Highlighter is a CSS gradient**, not a fancy irregular skew effect. Print-press feel beats hand-drawn feel for the "second-read book" register.

6. **Blockquotes disable the inline highlighter**. Yellow on navy blockquote bg reads dirty; inside a pullquote, bold stays bold (font weight) without yellow wash.

## Palette

| Role | Hex | Usage |
|---|---|---|
| page-bg | `#f5efe4` | Cream page background |
| text | `#1a1a1a` | Body text (near-black, not pure black) |
| text-muted | `#5a5a5a` | Subtitle, page number secondary |
| highlight | `#ffe066` | `**bold**` highlighter wash |
| accent | `#2b3a5c` | Navy — blockquote rules, ornaments, Act fleuron, links |
| divider | `rgba(0,0,0,0.08)` | Subtle rules (hr, etc.) |

## Typography

- **Body (CJK)**: `Noto Serif SC` weights 400/700
- **Latin mix**: `EB Garamond` fallback to `Noto Serif`
- **Code**: `SF Mono`, `Monaco`, `Consolas` fallback chain
- **Body size**: 42px, `line-height: 1.85`
- **H2 (Act titles)**: 64px, weight 700, serif, with navy `❧` fleuron centered above (36px, margin-bottom 12px)
- **H3**: 48px, weight 600
- **Paragraph margin**: 35px bottom (matching `paper`'s density)

## Layout

- **Cover page**: 1080 × 1440 baseline (3:4). `min-height` not `height` — may grow when the opening section is long (e.g. the 封面概要 hook runs ~6 paragraphs). Growth is acceptable; hard clipping is not.
- **Content page**: 1080 × 1920 baseline (9:16), `min-height` — may grow to cleanly end on a paragraph boundary.
- **Inner padding**: 76px left + 76px right (7% each, balanced). Eliminates `paper`'s asymmetric notebook margin.
- **Top/bottom padding**: `0.05 * height` (72px on cover, 96px on content)
- **Content width**: 928px
- **Page number**: bottom-right, navy `#2b3a5c`, 32px, `{current}/{total}`. Cover has no page number.

## Highlighter Bold

```css
.content strong {
  background: linear-gradient(
    transparent 55%,
    #ffe066 55%,
    #ffe066 92%,
    transparent 92%
  );
  color: #1a1a1a;
  padding: 0 2px;
  font-weight: 700;
}
```

- Yellow covers the bottom ~37% of the text line with small gaps above and below the highlight band — simulates a highlighter pass.
- Text color stays near-black for contrast. No color shift on hover (static rendering).

## Blockquote / Pullquote (Q2)

```css
.content blockquote {
  border-top: 2px solid #2b3a5c;
  border-bottom: 2px solid #2b3a5c;
  padding: 60px 40px;
  margin: 60px 0;
  position: relative;
  text-align: center;
}

.content blockquote::before {
  content: '◆';
  position: absolute;
  top: -18px;
  left: 50%;
  transform: translateX(-50%);
  background: #f5efe4;
  color: #2b3a5c;
  font-size: 36px;
  padding: 0 12px;
  line-height: 1;
}

.content blockquote p {
  font-family: 'Noto Serif SC', serif;
  font-style: italic;
  font-size: 60px;
  line-height: 1.5;
  color: #2b3a5c;
  margin: 0;
}

.content blockquote strong {
  /* Override: no highlighter inside pullquote */
  background: none;
  color: #2b3a5c;
  font-weight: 700;
  padding: 0;
}

.content blockquote h1,
.content blockquote h2,
.content blockquote h3 {
  font-size: 60px;
  color: #2b3a5c;
  font-style: italic;
  margin: 0;
}
```

- `◆` marker sits on the top rule, with cream padding to break the rule visually (inline notch).
- Nested `### **heading**` blockquotes (like the article's finale line) render at the same 60px italic navy — no size hierarchy inside pullquote.

## Cover

```
[7% top padding]

[Title — Noto Serif SC 900, title_font_size() auto, color #1a1a1a]

[Subtitle — EB Garamond italic + Noto Serif SC, 38px, color #5a5a5a]

[Divider: 60px navy line · ❧ · 60px navy line, centered]

[First-section body — same 42px serif as content pages]
```

- No left-margin notch, no red stripe.
- `title_font_size()` helper from `base.py` handles the 22-char title; natural CSS wrap at mid-sentence is acceptable.
- `❧` serves as the cover's signature ornament, echoed on Act H2s.

## Ornaments — final inventory

| Glyph | Where | Purpose |
|---|---|---|
| `❧` | Cover divider center, above every H2 Act title | Chapter/section fleuron |
| `◆` | Pullquote top notch | Quote anchor |
| `1/N` | Content page bottom-right | Page number |

Nothing else. No borders, no background textures, no gradients beyond the highlighter.

## Implementation notes

- Module path: `scripts/styles/essay.py`
- Register in `scripts/styles/__init__.py` alongside existing styles
- Reuse helpers from `base.py`: `css_reset`, `font_imports`, `html_document`, `title_font_size`, `page_number_html`
- Add `'EB Garamond'` to the font import list alongside `'Noto Serif SC'`
- Follow the same two-function contract as other styles: `generate_cover(title, subtitle, first_section_html, width, height)` and `generate_card(content_html, page_number, total_pages, width, height)`

## Non-goals

- No dark-mode variant.
- No A/B/C color variants (unlike `slab`). Single canonical palette.
- No decorative page frames or corner ornaments.
- No automatic H2 page breaks (inherits the existing inline H2 behavior from `render.py`).

## Success criteria

- Renders `output/shortcut-vs-friction/input.md` to ~18-20 content pages
- Cover allowed to grow beyond 1440 for the full 封面概要; target range 1440-2200px
- Every blockquote in the article is visually dominant — large italic navy across navy rules, inline `◆` marker
- Every `**bold**` phrase outside blockquotes has the yellow highlighter wash
- No horizontal space wasted on a notebook-style left margin; content area ≥ 920px wide
- All 8+ blockquotes render distinctly from surrounding paragraphs at first glance
