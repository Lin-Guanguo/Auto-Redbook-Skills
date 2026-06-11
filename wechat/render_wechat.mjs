#!/usr/bin/env node
/**
 * Markdown -> WeChat MP (公众号) ready HTML.
 *
 * Headless port of the md.doocs.org "copy" pipeline (doocs/md, WTFPL):
 *   marked render -> theme CSS -> resolve CSS vars -> juice inline styles
 *   -> WeChat editor fixups -> preview html + rich-text clipboard.
 *
 * The WeChat editor strips <style>/class/id on paste and only keeps inline
 * styles, so everything here exists to survive that sanitizer.
 *
 * Usage:
 *   node wechat/render_wechat.mjs <input.md> [options]
 *
 * Options:
 *   --theme <name>          theme file in wechat/themes/ (default: default)
 *   --primary-color <hex>   accent color (default: #0F4C81)
 *   --font-size <px>        base font size in px (default: 16)
 *   --no-cite               keep external <a> links instead of footnotes
 *   --copy                  put rich text on the macOS clipboard (paste into editor)
 *   --open                  open the preview html in browser
 *   --out <dir>             output dir (default: alongside input)
 */
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import { createRequire } from 'node:module'
import path from 'node:path'
import process from 'node:process'
import * as cheerio from 'cheerio'
import hljs from 'highlight.js'
import yaml from 'js-yaml'
import juice from 'juice'
import { marked } from 'marked'

const require = createRequire(import.meta.url)
const SCRIPT_DIR = path.dirname(new URL(import.meta.url).pathname)

// ---------------------------------------------------------------- args

function parseArgs(argv) {
  const opts = {
    input: null,
    theme: 'default',
    primaryColor: '#0F4C81',
    fontSize: 16,
    cite: true,
    copy: false,
    open: false,
    out: null,
  }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--theme') opts.theme = argv[++i]
    else if (a === '--primary-color') opts.primaryColor = argv[++i]
    else if (a === '--font-size') opts.fontSize = parseFloat(argv[++i])
    else if (a === '--no-cite') opts.cite = false
    else if (a === '--copy') opts.copy = true
    else if (a === '--open') opts.open = true
    else if (a === '--out') opts.out = argv[++i]
    else if (!a.startsWith('--') && !opts.input) opts.input = a
    else {
      console.error(`Unknown option: ${a}`)
      process.exit(1)
    }
  }
  if (!opts.input) {
    console.error('Usage: node wechat/render_wechat.mjs <input.md> [--theme x] [--copy] [--open]')
    process.exit(1)
  }
  return opts
}

// ---------------------------------------------------------------- front matter

function stripFrontMatter(src) {
  const m = src.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/)
  if (!m) return { meta: {}, body: src }
  let meta = {}
  try {
    meta = yaml.load(m[1]) || {}
  }
  catch {
    // tolerate broken front matter, treat as content
    return { meta: {}, body: src }
  }
  return { meta, body: src.slice(m[0].length) }
}

// ---------------------------------------------------------------- code highlight

const FONT_FAMILY = `-apple-system-font, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei UI', 'Microsoft YaHei', Arial, sans-serif`

/**
 * Port of doocs/md formatHighlightedCode (preserveNewlines=true):
 * WeChat collapses whitespace in pasted <pre>, so newlines become <br/>
 * and spaces in text nodes become &nbsp;.
 */
function formatHighlightedCode(html) {
  let formatted = html
  formatted = formatted.replace(
    /(<span[^>]*>[^<]*<\/span>)(\s+)(<span[^>]*>[^<]*<\/span>)/g,
    (_, span1, spaces, span2) => span1 + span2.replace(/^(<span[^>]*>)/, `$1${spaces}`),
  )
  formatted = formatted.replace(/(\s+)(<span[^>]*>)/g, (_, spaces, span) =>
    span.replace(/^(<span[^>]*>)/, `$1${spaces}`))
  formatted = formatted.replace(/\t/g, '    ')
  formatted = formatted
    .replace(/\r\n/g, '<br/>')
    .replace(/\n/g, '<br/>')
    .replace(/(>[^<]+)|(^[^<]+)/g, str => str.replace(/\s/g, '&nbsp;'))
  return formatted
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

// ---------------------------------------------------------------- renderer

function createRenderer(opts, state) {
  const renderer = new marked.Renderer()

  renderer.code = (code, infostring) => {
    const lang = (infostring || '').split(' ')[0]
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    const highlighted = hljs.highlight(code, { language }).value
    return `<pre class="hljs code__pre"><code class="language-${lang}">${formatHighlightedCode(highlighted)}</code></pre>`
  }

  renderer.codespan = text => `<code class="codespan">${text}</code>`

  renderer.link = (href, title, text) => {
    if (href.startsWith('#')) return text // in-page anchors break MP save
    if (href.startsWith('mailto:')) return text
    if (href.includes('mp.weixin.qq.com')) {
      return `<a href="${href}" title="${title || text}">${text}</a>`
    }
    if (!opts.cite || text === href) {
      // bare URLs stay visible; --no-cite keeps <a> (MP turns it into plain text)
      return `<a href="${href}" title="${title || text}">${text}</a>`
    }
    const existing = state.footnotes.find(f => f.href === href)
    const n = existing ? existing.n : state.footnotes.push({ n: state.footnotes.length + 1, title: title || text, href }) && state.footnotes.length
    return `${text}<sup>[${n}]</sup>`
  }

  renderer.image = (href, title, text) => {
    if (!/^https?:\/\//.test(href)) state.localImages.push(href)
    const caption = text ? `<figcaption class="md-figcaption">${escapeHtml(text)}</figcaption>` : ''
    return `<figure><img src="${href}" alt="${escapeHtml(text || '')}"${title ? ` title="${escapeHtml(title)}"` : ''}>${caption}</figure>`
  }

  return renderer
}

function buildFootnotes(footnotes) {
  if (!footnotes.length) return ''
  const items = footnotes
    .map(f => `<code class="codespan" style="font-size: 90%; opacity: 0.6;">[${f.n}]</code>: <i style="word-break: break-all">${escapeHtml(f.title)}: ${escapeHtml(f.href)}</i>`)
    .join('<br/>')
  return `<h4>引用链接</h4><p class="footnotes">${items}</p>`
}

// ---------------------------------------------------------------- css

function resolveCssVars(css, opts) {
  let out = css
    .replace(/hsl\(var\(--foreground\)\)/g, '#3f3f3f')
    .replace(/var\(--blockquote-background\)/g, '#f7f7f7')
    .replace(/var\(--md-primary-color\)/g, opts.primaryColor)
    .replace(/var\(--md-font-size\)/g, `${opts.fontSize}px`)
    .replace(/var\(--md-font-family\)/g, FONT_FAMILY)
  // WeChat inline styles reject calc(); precompute "calc(NNpx * K)"
  out = out.replace(/calc\((\d+(?:\.\d+)?)px\s*\*\s*([\d.]+)\)/g, (_, px, k) =>
    `${Math.round(parseFloat(px) * parseFloat(k) * 100) / 100}px`)
  const leftover = out.match(/var\(--[\w-]+(?:,[^)]*)?\)/g)
  if (leftover) {
    console.warn(`[warn] unresolved CSS vars (left as-is): ${[...new Set(leftover)].join(', ')}`)
  }
  return out
}

function loadCss(opts) {
  const themePath = path.join(SCRIPT_DIR, 'themes', `${opts.theme}.css`)
  if (!fs.existsSync(themePath)) {
    console.error(`Theme not found: ${themePath}`)
    process.exit(1)
  }
  const parts = [fs.readFileSync(themePath, 'utf-8')]
  parts.push(fs.readFileSync(require.resolve('highlight.js/styles/github.css'), 'utf-8'))
  const customPath = path.join(SCRIPT_DIR, 'themes', 'custom.css')
  if (opts.theme !== 'custom' && fs.existsSync(customPath)) {
    parts.push(fs.readFileSync(customPath, 'utf-8')) // personal overrides, highest priority
  }
  return resolveCssVars(parts.join('\n\n'), opts)
}

// ---------------------------------------------------------------- wechat fixups

/** Port of doocs/md processClipboardContent DOM fixups. */
function applyWeChatFixups(juicedHtml) {
  const $ = cheerio.load(juicedHtml)

  // WeChat renders nested lists wrongly inside <li>; move them after it
  $('li > ul, li > ol').each((_, el) => {
    const $el = $(el)
    $el.parent().after($el)
  })

  // page-internal anchors make MP saving fail
  $('a[href^="#"]').removeAttr('href')

  // width/height attributes -> inline style
  $('img').each((_, el) => {
    const $el = $(el)
    for (const attr of ['width', 'height']) {
      const v = $el.attr(attr)
      if (v) {
        $el.removeAttr(attr)
        $el.css(attr, /^\d+$/.test(v) ? `${v}px` : v)
      }
    }
  })

  let fragment = $.html($('#output'))
  // MP drops "top:" positioning (used by sup/sub); emulate via transform
  fragment = fragment.replace(/([^-])top:(.*?)em/g, '$1transform: translateY($2em)')
  return fragment
}

// ---------------------------------------------------------------- clipboard / preview

function copyToClipboard(fragmentPath) {
  execFileSync('osascript', [
    '-e',
    `set the clipboard to (read (POSIX file "${fragmentPath}") as «class HTML»)`,
  ])
}

function buildPreviewPage(fragment, title) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)} · 公众号预览</title>
<style>
  body { margin: 0; background: #ededed; }
  .bar { max-width: 578px; margin: 16px auto 0; font: 12px/1.6 ${FONT_FAMILY}; color: #888; padding: 0 8px; }
  .phone { max-width: 578px; margin: 8px auto 40px; background: #fff; padding: 24px 18px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }
</style>
</head>
<body>
<div class="bar">预览宽度 578px ≈ 公众号正文。粘贴用 --copy 写入剪贴板后到 mp.weixin.qq.com 编辑器 Cmd+V。</div>
<div class="phone">${fragment}</div>
</body>
</html>`
}

// ---------------------------------------------------------------- main

function main() {
  const opts = parseArgs(process.argv.slice(2))
  const inputPath = path.resolve(opts.input)
  if (!fs.existsSync(inputPath)) {
    console.error(`Input not found: ${inputPath}`)
    process.exit(1)
  }

  const { meta, body } = stripFrontMatter(fs.readFileSync(inputPath, 'utf-8'))
  const state = { footnotes: [], localImages: [] }

  marked.setOptions({ renderer: createRenderer(opts, state), gfm: true, breaks: false })
  const bodyHtml = marked.parse(body) + buildFootnotes(state.footnotes)

  const doc = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>${loadCss(opts)}</style></head><body><section id="output">${bodyHtml}</section></body></html>`
  const juiced = juice(doc, {
    inlinePseudoElements: true,
    preserveImportant: true,
    resolveCSSVariables: false,
  })
  const fragment = applyWeChatFixups(juiced)

  const outDir = opts.out ? path.resolve(opts.out) : path.dirname(inputPath)
  fs.mkdirSync(outDir, { recursive: true })
  const base = path.basename(inputPath).replace(/\.md$/, '')
  const previewPath = path.join(outDir, `${base}.wechat.html`)
  const fragmentPath = path.join(outDir, `${base}.wechat.fragment.html`)

  const title = meta.title || (body.match(/^#\s+(.+)$/m) || [])[1] || base
  fs.writeFileSync(previewPath, buildPreviewPage(fragment, title))
  fs.writeFileSync(fragmentPath, fragment)

  console.log(`preview:   ${previewPath}`)
  console.log(`fragment:  ${fragmentPath}`)
  console.log(`footnotes: ${state.footnotes.length}`)
  if (state.localImages.length) {
    console.log(`[warn] ${state.localImages.length} 张本地图片粘贴后不会显示，需要图床 URL 或在编辑器里手动上传：`)
    state.localImages.forEach(p => console.log(`       - ${p}`))
  }

  if (opts.copy) {
    copyToClipboard(fragmentPath)
    console.log('已写入剪贴板（富文本），到公众号编辑器直接 Cmd+V')
  }
  if (opts.open) execFileSync('open', [previewPath])
}

main()
