#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 README.md 渲染成本地预览页 preview.html（模拟 GitHub 的排版）。
改完 README 或 SVG 后重跑：python build_preview.py
"""
import os
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
md_text = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()

body = markdown.markdown(
    md_text,
    extensions=["tables", "sane_lists", "md_in_html", "attr_list", "fenced_code"],
)

HTML = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AstonKrss · README 预览</title>
<style>
  :root {
    --bg: #ffffff; --fg: #1f2328; --muted: #59636e; --border: #d1d9e0;
    --link: #0969da; --code-bg: #f6f8fa; --th-bg: #f6f8fa; --canvas: #f6f8fa;
  }
  [data-theme="dark"] {
    --bg: #0d1117; --fg: #e6edf3; --muted: #9198a1; --border: #3d444d;
    --link: #4493f8; --code-bg: #151b23; --th-bg: #151b23; --canvas: #010409;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--canvas); color: var(--fg);
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
          "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .page { max-width: 1012px; margin: 28px auto 60px; background: var(--bg);
          border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
  .bar { display: flex; align-items: center; justify-content: space-between;
         gap: 12px; padding: 12px 24px; border-bottom: 1px solid var(--border);
         font-size: 13px; color: var(--muted); }
  .bar b { color: var(--fg); font-weight: 600; }
  button { font: inherit; font-size: 12px; cursor: pointer; color: var(--fg);
           background: transparent; border: 1px solid var(--border);
           border-radius: 6px; padding: 4px 10px; }
  .markdown-body { padding: 32px 40px 48px; }
  .markdown-body h1, .markdown-body h2, .markdown-body h3 {
    font-weight: 600; line-height: 1.25; margin: 28px 0 16px; }
  .markdown-body h2 { font-size: 24px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
  .markdown-body h3 { font-size: 18px; }
  .markdown-body h1 { font-size: 30px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
  .markdown-body p, .markdown-body li { font-size: 15.5px; }
  .markdown-body p { margin: 0 0 16px; }
  .markdown-body a { color: var(--link); text-decoration: none; }
  .markdown-body a:hover { text-decoration: underline; }
  .markdown-body img { max-width: 100%; border: 0; }
  .markdown-body ul { padding-left: 2em; margin: 0 0 16px; }
  .markdown-body li { margin: 4px 0; }
  .markdown-body li > strong { color: var(--fg); }
  .markdown-body table { border-collapse: collapse; margin: 0 0 16px; font-size: 14.5px; }
  .markdown-body th, .markdown-body td { border: 1px solid var(--border); padding: 7px 12px; }
  .markdown-body th { background: var(--th-bg); font-weight: 600; text-align: left; }
  .markdown-body table td img { display: block; }
  .markdown-body code { background: var(--code-bg); padding: .2em .4em; border-radius: 6px;
                        font: 85% ui-monospace, SFMono-Regular, Consolas, monospace; }
  .markdown-body br { line-height: 1; }
  .spacer { height: 20px; }
  .footer { padding: 14px 24px; border-top: 1px solid var(--border);
            font-size: 12px; color: var(--muted); }
</style>
</head>
<body>
<div class="page">
  <div class="bar">
    <span><b>AstonKrss</b> / README.md · 本地预览（GitHub 渲染效果近似）</span>
    <button id="t">切换深/浅色</button>
  </div>
  <div class="markdown-body">
__BODY__
  </div>
  <div class="footer">提示：右上角切换深浅色，看两种主题下的实际观感。</div>
</div>
<script>
  const t = document.getElementById('t'), root = document.documentElement;
  t.onclick = () => {
    const d = root.getAttribute('data-theme') === 'dark';
    root.setAttribute('data-theme', d ? 'light' : 'dark');
  };
</script>
</body>
</html>
"""

body = body.replace("<p><br></p>", '<div class="spacer"></div>')
out = HTML.replace("__BODY__", body)
open(os.path.join(HERE, "preview.html"), "w", encoding="utf-8").write(out)
print("wrote preview.html  %.1f KB" % (len(out.encode()) / 1024))
