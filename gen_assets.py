#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 GitHub Profile README 用的毛玻璃风 SVG 资产。
改完下面的配置重新跑一遍即可：python gen_assets.py
"""
import base64
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
FONT = ('-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",'
        '"Hiragino Sans GB","Microsoft YaHei",sans-serif')

# ---------------- 基础工具 ----------------

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def cw(ch):
    """粗略字符宽度系数：中日韩全角按 1em，其余按比例。"""
    o = ord(ch)
    if o > 0x2E80 or ch in "，。、：；？！（）《》“”…·—":
        return 1.0
    if ch in "ilj|!.,:;'` ":
        return 0.30
    if ch in "mwMW@#%&":
        return 0.86
    if ch.isupper() or ch.isdigit():
        return 0.60
    return 0.52


def tw(s, size, weight=400):
    k = 1.06 if weight >= 600 else 1.0
    return sum(cw(c) for c in s) * size * k


def tokenize(s):
    """把英文单词/数字/符号串当成不可分割的 token，中日韩字符逐字成 token。"""
    toks, cur = [], ""
    for ch in s:
        if ch.isascii() and (ch.isalnum() or ch in "_+-./~#@%&:="):
            cur += ch
        else:
            if cur:
                toks.append(cur)
                cur = ""
            toks.append(ch)
    if cur:
        toks.append(cur)
    return toks


def wrap(s, size, maxw, weight=400):
    """按 token 换行，避免把英文单词劈成两半。"""
    lines, cur = [], ""
    for tok in tokenize(s):
        if tw(cur + tok, size, weight) > maxw and cur.strip():
            lines.append(cur.rstrip())
            cur = tok.lstrip()
        else:
            cur += tok
    if cur.strip():
        lines.append(cur.rstrip())
    # 中文排版规矩：这些标点不能出现在行首，挪回上一行末尾
    NO_START = "。，、；：！？）」』】%"
    for i in range(1, len(lines)):
        while lines[i] and lines[i][0] in NO_START:
            lines[i - 1] += lines[i][0]
            lines[i] = lines[i][1:]
    return [ln for ln in lines if ln.strip()]


def base64img(path, mime):
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())


AVATAR = base64img(os.path.join(OUT, "avatar.jpg"), "image/jpeg")

# ---------------- 公共 defs ----------------

DEFS = """
  <defs>
    <linearGradient id="base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="0.45" stop-color="#141b2d"/>
      <stop offset="1" stop-color="#0b0f18"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.13"/>
      <stop offset="0.5" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.45"/>
      <stop offset="0.4" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.03"/>
    </linearGradient>
    <linearGradient id="topline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="0.5" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="blobA" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#8b5cf6" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blobB" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#22d3ee" stop-opacity="0.70"/>
      <stop offset="1" stop-color="#22d3ee" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blobC" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#f472b6" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#f472b6" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#a78bfa"/>
      <stop offset="0.55" stop-color="#22d3ee"/>
      <stop offset="1" stop-color="#f472b6"/>
    </linearGradient>
    <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="46"/>
    </filter>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="180%">
      <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#05070d" flood-opacity="0.55"/>
    </filter>
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
    <clipPath id="avatarClip"><circle cx="96" cy="116" r="46"/></clipPath>
  </defs>
"""


def glass_panel(w, h, r=22, x=0, y=0, extra=""):
    return f"""
  <g {extra}>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glass)"
          stroke="url(#edge)" stroke-width="1.2" filter="url(#shadow)"/>
    <rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="1.4" rx="0.7" fill="url(#topline)"/>
  </g>"""


def pill_width(label, size=12.5, pad=13, dot=None, weight=500):
    return tw(label, size, weight) + pad * 2 + (12 if dot else 0)


def pill(x, y, label, size=12.5, pad=13, dot=None, color="#c9d4ea", weight=500,
         opacity=1.0, pulse=False):
    """返回 (svg, 宽度)"""
    w = pill_width(label, size, pad, dot, weight)
    h = size + 13
    inner = ""
    if dot:
        if pulse:
            inner += (f'<circle cx="{x + pad + 3}" cy="{y + h / 2}" r="3" fill="{dot}">'
                      f'<animate attributeName="opacity" values="1;0.3;1" dur="2.2s" '
                      f'repeatCount="indefinite"/></circle>')
        else:
            inner += f'<circle cx="{x + pad + 3}" cy="{y + h / 2}" r="3" fill="{dot}"/>'
    tx = x + pad + (12 if dot else 0)
    inner += (f'<text x="{tx}" y="{y + h / 2 + size * 0.36:.1f}" font-size="{size}" '
              f'font-weight="{weight}" fill="{color}" opacity="{opacity}">{esc(label)}</text>')
    svg = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" '
           f'fill="#ffffff" fill-opacity="0.055" stroke="#ffffff" stroke-opacity="0.16" stroke-width="1"/>'
           + inner)
    return svg, w


def canvas(W, H, r):
    """圆角画布：所有内容裁剪在圆角矩形内。"""
    return (f'<defs><clipPath id="cc"><rect width="{W}" height="{H}" rx="{r}" ry="{r}"/>'
            f'</clipPath></defs><g clip-path="url(#cc)">')


def svg_open(w, h, extra_style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">'
            f'<style>text{{font-family:{FONT};}}</style>' + DEFS + extra_style)


def bg_blobs(w, h, glow=1.0, dim=0.42):
    return f"""
  <rect x="0" y="0" width="{w}" height="{h}" fill="url(#base)"/>
  <g filter="url(#soft)" opacity="{glow}">
    <ellipse cx="{w * 0.16:.0f}" cy="{h * 0.10:.0f}" rx="{w * 0.30:.0f}" ry="{h * 0.55:.0f}" fill="url(#blobA)"/>
    <ellipse cx="{w * 0.86:.0f}" cy="{h * 0.18:.0f}" rx="{w * 0.28:.0f}" ry="{h * 0.62:.0f}" fill="url(#blobB)"/>
    <ellipse cx="{w * 0.50:.0f}" cy="{h * 1.05:.0f}" rx="{w * 0.34:.0f}" ry="{h * 0.48:.0f}" fill="url(#blobC)"/>
  </g>
  <rect x="0" y="0" width="{w}" height="{h}" fill="url(#base)" opacity="{dim}"/>
  <rect x="0" y="0" width="{w}" height="{h}" filter="url(#grain)" opacity="0.05"/>"""


# ---------------- 1. Hero ----------------

def build_hero():
    W, H = 900, 300
    s = svg_open(W, H)
    s += canvas(W, H, 26)
    s += bg_blobs(W, H, glow=1.0, dim=0.40)
    s += glass_panel(W - 24, H - 24, r=22, x=12, y=12)

    # 头像
    s += f'''
  <circle cx="96" cy="116" r="50" fill="none" stroke="url(#ring)" stroke-width="2.4" opacity="0.9"/>
  <image x="50" y="70" width="92" height="92" clip-path="url(#avatarClip)"
         preserveAspectRatio="xMidYMid slice" href="{AVATAR}"/>
  <circle cx="96" cy="116" r="46" fill="none" stroke="#ffffff" stroke-opacity="0.22" stroke-width="1"/>'''

    # 文字
    s += f'''
  <text x="170" y="86" font-size="33" font-weight="700" fill="#f5f7ff" letter-spacing="0.4">AstonKrss</text>
  <text x="171" y="112" font-size="13" fill="#9aa7c2">@AstonKrss · github.com/AstonKrss</text>
  <text x="171" y="146" font-size="14.5" fill="#dbe3f5" opacity="0.92">系统底层性能 × 智能体工程 —— 从 epoll 与协议字节，到会自己规划下一步的 Agent。</text>
  <text x="171" y="170" font-size="14.5" fill="#dbe3f5" opacity="0.92">C++17 / 20 · Go · Java · Python ｜ 偏爱把边界、数字与取舍都写清楚的项目。</text>'''

    # 状态胶囊（带呼吸点）
    st, sw = pill(171, 186, "Focusing · 持续折腾中", size=12.5, dot="#34d399", pulse=True)
    s += st

    # 底部信息条
    chips = ["44 次贡献 · 近一年", "4 个主力项目", "上游 PR：WeKnora · opentelemetry-java"]
    x = 26
    y = H - 66
    out = ""
    for c in chips:
        svg, w = pill(x, y, c, size=12, dot="#7dd3fc", color="#cfd9ee")
        out += svg
        x += w + 14
    s += out
    s += "</g></svg>"
    return s


# ---------------- 2. 技术栈 ----------------

LANGS = [
    ("C", "#555555"), ("C++17 / 20", "#f34b7d"), ("Go", "#00ADD8"), ("Java", "#b07219"),
    ("Python", "#3572A5"), ("TypeScript", "#3178c6"), ("Linux", "#FCC624"),
    ("WebSocket", "#8b5cf6"), ("MySQL / PG", "#00758F"), ("OCR / NER", "#f472b6"),
    ("LangGraph", "#ff6b6b"), ("Git", "#F05032"),
]


def build_stack():
    W = 900
    rows = [LANGS[:6], LANGS[6:]]
    size, pad = 14, 15
    chip_h = size + 13
    gap_x, gap_y = 16, 16
    H = 24 + len(rows) * chip_h + (len(rows) - 1) * gap_y + 24
    s = svg_open(W, H)
    s += canvas(W, H, 20)
    s += bg_blobs(W, H, glow=0.72, dim=0.52)
    s += glass_panel(W - 16, H - 16, r=18, x=8, y=8)

    y = 24
    for row in rows:
        widths = [pill_width(n, size, pad, c) for n, c in row]
        # 间距随行内内容自适应：最多拉开到 40px，再整体居中
        g = min(40, (W - 52 - sum(widths)) / max(1, len(row) - 1))
        total = sum(widths) + g * (len(row) - 1)
        x = (W - total) / 2
        for (name, color), w in zip(row, widths):
            svg, _ = pill(x, y, name, size=size, pad=pad, dot=color, color="#e6ecfa")
            s += svg
            x += w + g
        y += chip_h + gap_y
    s += "</g></svg>"
    return s


# ---------------- 3. 项目卡片 ----------------

CARD_W, CARD_H = 424, 176

CARDS = [
    dict(file="card-chatserver.svg", name="ChatServer", lang="C++20", color="#f34b7d",
         tag="7.3k 行 · 手写协议栈",
         desc="从 socket 起步的 Reactor 通讯服务器。HTTP/1.1、WebSocket RFC6455、"
              "SMTP RFC5321 三套协议全部自己解析，JSON 与 JWT 也自带。",
         foot="epoll / kqueue ｜ 环形缓冲 ｜ ctest"),
    dict(file="card-travel-agent.svg", name="travel-agent", lang="Python", color="#3572A5",
         tag="8 节点编排",
         desc="企业差旅 Agent。LangGraph 编排意图识别、信息提取、政策 RAG 校验、行程规划与"
              "超预算审批中断，全流程状态可断点恢复、审批结果可回放。",
         foot="多模型路由 ｜ 人工审批 ｜ SSE 流式"),
    dict(file="card-heartbeatd.svg", name="heartbeatd", lang="C++17", color="#f34b7d",
         tag="116 万 pps · 零丢包",
         desc="Linux UDP 心跳检测服务。epoll + recvmmsg 批量收包、SO_REUSEPORT 多 reactor、"
              "host_id 分片 worker，纯 C++17 零第三方依赖。",
         foot="p99 < 500 µs ｜ 环形队列 + 延迟直方图"),
    dict(file="card-holodata.svg", name="HoloData-PII-Scanner", lang="Python", color="#3572A5",
         tag="6 类数据源 · 3 种识别",
         desc="数据库敏感信息识别系统。表字段、JSON/XML、Base64、非结构化文本、图片 OCR、"
              "存储过程全扫一遍，按 L2–L4 分级导出 CSV。",
         foot="CRF / BiLSTM ｜ RapidOCR ｜ 6.6k 行"),
]


def build_card(c):
    W, H = CARD_W, CARD_H
    s = svg_open(W, H)
    s += canvas(W, H, 20)
    s += f'''
  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#base)"/>
  <ellipse cx="60" cy="18" rx="150" ry="92" fill="url(#blobA)" opacity="0.42" filter="url(#soft)"/>
  <ellipse cx="382" cy="176" rx="140" ry="86" fill="url(#blobB)" opacity="0.34" filter="url(#soft)"/>
  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#base)" opacity="0.34"/>
  <rect x="0" y="0" width="{W}" height="{H}" filter="url(#grain)" opacity="0.05"/>'''
    s += glass_panel(W - 12, H - 12, r=18, x=6, y=6)

    # 顶部语言色条
    s += (f'<rect x="22" y="6.6" width="86" height="2.4" rx="1.2" fill="{c["color"]}" opacity="0.95"/>')

    # 仓库名
    s += (f'<text x="22" y="44" font-size="18.5" font-weight="700" fill="#f2f6ff">'
          f'{esc(c["name"])}</text>')

    # 亮点胶囊（右上）
    tw_ = pill_width(c["tag"], 11, 10, c["color"])
    tg, _ = pill(W - 22 - tw_, 22, c["tag"], size=11, pad=10, dot=c["color"], color="#dfe7f8")
    s += tg

    # 描述（去掉只剩标点的孤行，避免视觉上的空荡）
    lines = wrap(c["desc"], 13, W - 46)[:3]
    while len(lines) > 1 and not lines[-1].strip("。，、；：）. "):
        lines.pop()
    y = 70
    for line in lines:
        s += f'<text x="22" y="{y}" font-size="13" fill="#c2ccdf" opacity="0.92">{esc(line)}</text>'
        y += 21

    # 底部
    fy = H - 22
    s += f'<circle cx="26" cy="{fy - 4}" r="3.4" fill="{c["color"]}"/>'
    s += f'<text x="36" y="{fy}" font-size="12" fill="#9fadc7">{esc(c["lang"])}</text>'
    fw = tw(c["foot"], 11.5, 500)
    s += f'<text x="{W - 22 - fw:.0f}" y="{fy}" font-size="11.5" fill="#8e9cb6">{esc(c["foot"])}</text>'
    s += "</g></svg>"
    return s


# ---------------- 4. 尾注 ----------------

def build_quote():
    W, H = 900, 92
    s = svg_open(W, H)
    s += canvas(W, H, 20)
    s += bg_blobs(W, H, glow=0.6, dim=0.55)
    s += glass_panel(W - 16, H - 16, r=16, x=8, y=8)
    q = "数据不造假，边界写清楚 —— 所有数字都标注了机器、内核与配置。"
    s += f'<text x="{W / 2}" y="42" font-size="15.5" font-style="italic" fill="#e8eefb" text-anchor="middle">{esc(q)}</text>'
    s += f'<text x="{W / 2}" y="66" font-size="11.5" fill="#8b99b3" text-anchor="middle">—— heartbeatd README，也是我写项目的规矩</text>'
    s += "</g></svg>"
    return s


# ---------------- main ----------------

def main():
    os.makedirs(OUT, exist_ok=True)
    files = {"hero.svg": build_hero(), "techstack.svg": build_stack(),
             "quote.svg": build_quote()}
    for c in CARDS:
        files[c["file"]] = build_card(c)
    for name, content in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)
        print("wrote assets/%-24s %6.1f KB" % (name, len(content.encode()) / 1024))


if __name__ == "__main__":
    main()
