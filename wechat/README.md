# WeChat MP Renderer (公众号排版)

Markdown → 公众号编辑器可直接粘贴的富文本。md.doocs.org「复制」按钮的本地化复刻（doocs/md, WTFPL），主题 CSS 归本仓库维护，方便调整格式。

## Usage

```bash
npm run wechat -- <input.md> [options]
# or: node wechat/render_wechat.mjs <input.md> [options]
```

| Option | Default | 说明 |
|---|---|---|
| `--copy` | off | 渲染结果以富文本写入 macOS 剪贴板，去 mp.weixin.qq.com 编辑器 Cmd+V 即可 |
| `--open` | off | 在浏览器打开预览页（578px 正文宽度模拟） |
| `--theme <name>` | `default` | 对应 `wechat/themes/<name>.css` |
| `--primary-color <hex>` | `#0F4C81` | 主题色（标题、加粗、强调） |
| `--font-size <px>` | `16` | 正文字号 |
| `--no-cite` | off | 不把外链转成文末「引用链接」脚注，保留 `<a>`（公众号会变纯文本） |
| `--out <dir>` | 输入文件所在目录 | 输出目录 |

输出两个文件（与输入同目录）：

- `<name>.wechat.html` — 浏览器预览页
- `<name>.wechat.fragment.html` — 剪贴板实际内容（内联样式 HTML 片段）

## 典型流程

```bash
node wechat/render_wechat.mjs output/<topic>/source.md --copy --open
# 浏览器确认效果 → 公众号编辑器 Cmd+V → 填标题/封面/摘要 → 群发
```

## 为什么要这套处理（背景）

公众号编辑器粘贴时会清洗 HTML：丢掉 `<style>`/class/id，只保留内联 style。脚本因此做了：

1. marked 渲染 + highlight.js 代码高亮（换行转 `<br/>`、空格转 `&nbsp;`，防编辑器折叠）
2. 主题 CSS 变量求值（含 `calc()` 预计算，公众号内联样式不支持 calc）
3. juice 把所有 CSS 内联到元素 style 上
4. 微信特化修正：嵌套列表移出 `<li>`、页内锚点去 href（不去会保存报错）、img 宽高属性转 style、外链转文末脚注

## 图片

- 正文图片需要**公网 URL**（粘贴时微信会自动转存到自己 CDN；带防盗链的图床会失败，GitHub raw / OSS 可用）
- 本地路径图片粘贴后不显示，脚本会列出警告，去编辑器里手动上传替换
- 标题、封面、摘要属于编辑器表单字段，不在正文粘贴范围内，手动填

## 调整格式

- 长期改动：直接编辑 `themes/default.css`（元素选择器 + 少量 class：`.hljs.code__pre`、`.codespan`、`p.footnotes`、`.md-figcaption`）
- 个人覆盖：新建 `themes/custom.css`，自动追加在主题之后（优先级最高）
- 新主题：复制 `default.css` 为 `themes/<name>.css`，用 `--theme <name>` 调用
