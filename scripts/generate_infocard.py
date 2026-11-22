"""
Generate improved Neofetch-style terminal info card SVG.
Full-width layout (870px), improved animations:
- Each row slides in from left with staggered delay
- Blinking cursor at the shell prompt
- Tech stack pills with colored backgrounds
- Gradient header accent line
- Animated skill progress bars
"""

import html as html_module
import os

OUTPUT_SVG_PATH = "assets/info-card.svg"


def generate_infocard_svg(output_path: str = OUTPUT_SVG_PATH):
    W = 870
    H = 310

    fields = [
        ("OS",          "Linux (Ubuntu 22.04 LTS) · macOS Sonoma",  "#58a6ff"),
        ("Host",        "Sai Vidya Institute of Technology — Bengaluru", "#f0883e"),
        ("Name",        "Charan Gowda M D",                         "#c9d1d9"),
        ("Role",        "Computer Science Engineering Student",      "#bc8cff"),
        ("Interests",   "Backend Dev · AI/ML · Systems Engineering","#39d353"),
        ("Open Source", "Apache Maven Core Contributor (ASF)",       "#79c0ff"),
        ("Current",     "Building production systems · OSS",         "#56d364"),
        ("Languages",   "Python · Java · C · Go · SQL",             "#d2a8ff"),
        ("Tools",       "Git · Docker · Linux · Maven · GH Actions", "#7ee787"),
    ]

    # Skill bars: (name, pct, color)
    skills = [
        ("Python",   88, "#3572A5"),
        ("Java",     80, "#b07219"),
        ("C",        70, "#555555"),
        ("SQL",      72, "#e38c00"),
        ("Linux",    82, "#39d353"),
    ]

    projects = [
        ("Salamander",        "Full-stack coding challenge &amp; interview prep platform"),
        ("BEL Blockchain",    "Defense Blockchain Secure Platform MVP (Bharat Electronics Ltd.)"),
        ("Apache Maven",      "Core pull requests, bug fixes &amp; community contributions to ASF"),
        ("OSS Club SVIT",     "Founded &amp; led the SVIT Open-Source developer community"),
    ]

    svg = []

    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <style>
    .mono  {{ font-family:'JetBrains Mono','Fira Code','Courier New',monospace; }}
    .title {{ fill:#8b949e; font-size:11.5px; font-weight:600; }}
    .badge {{ fill:#58a6ff; font-size:9.5px; font-weight:700; }}
    .uhost {{ fill:#39d353; font-size:14px; font-weight:800; }}
    .fkey  {{ fill:#39d353; font-size:10px; font-weight:700; }}
    .fval  {{ fill:#c9d1d9; font-size:10px; font-weight:400; }}
    .sectitle {{ fill:#58a6ff; font-size:10.5px; font-weight:800; letter-spacing:0.6px; }}
    .pname {{ fill:#79c0ff; font-size:9.5px; font-weight:700; }}
    .pdesc {{ fill:#8b949e; font-size:9px; }}
    .sbar-label {{ fill:#8b949e; font-size:9px; }}

    /* Slide-in-left for each row */
    @keyframes slideIn {{
      from {{ opacity:0; transform:translateX(-18px); }}
      to   {{ opacity:1; transform:translateX(0);     }}
    }}
    .row {{ opacity:0; animation:slideIn 0.3s ease-out forwards; }}

    /* Progress bar fill */
    @keyframes barGrow {{
      from {{ width:0px; }}
    }}
    .bar-fill {{ animation:barGrow 0.8s ease-out forwards; }}

    /* Blinking cursor */
    @keyframes blink {{
      0%,49% {{ opacity:1; }}
      50%,100% {{ opacity:0; }}
    }}
    .cursor {{ animation:blink 1.1s step-end infinite; fill:#39d353; }}

    /* Pulsing dot */
    @keyframes pulse {{
      0%,100% {{ opacity:1; }}
      50% {{ opacity:0.3; }}
    }}
    .live {{ animation:pulse 1.8s ease-in-out infinite; }}
  </style>

  <linearGradient id="bgInfo" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="#0d1117"/>
    <stop offset="100%" stop-color="#0a1628"/>
  </linearGradient>
  <linearGradient id="accentLine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#39d353"/>
    <stop offset="50%"  stop-color="#58a6ff"/>
    <stop offset="100%" stop-color="#bc8cff"/>
  </linearGradient>

  <clipPath id="hClipInfo">
    <rect x="0" y="0" width="{W}" height="30" rx="10"/>
  </clipPath>
  <clipPath id="fClipInfo">
    <rect x="0" y="{H-26}" width="{W}" height="26" rx="10"/>
  </clipPath>
</defs>

<!-- BG -->
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10"
      fill="url(#bgInfo)" stroke="#30363d" stroke-width="1"/>

<!-- Header -->
<g clip-path="url(#hClipInfo)">
  <rect x="0" y="0" width="{W}" height="30" fill="#161b22"/>
  <line x1="0" y1="30" x2="{W}" y2="30" stroke="#30363d" stroke-width="1"/>
</g>
<circle cx="18" cy="15" r="5" fill="#ff5f56"/>
<circle cx="34" cy="15" r="5" fill="#ffbd2e"/>
<circle cx="50" cy="15" r="5" fill="#27c93f"/>
<text class="mono title" x="{W//2}" y="19" text-anchor="middle">charan@svit: ~ — neofetch</text>
<text class="mono badge" x="{W-16}" y="19" text-anchor="end">zsh 5.9</text>

<!-- Accent gradient line just below header -->
<rect x="0" y="30" width="{W}" height="2" fill="url(#accentLine)"/>
''')

    # ---- LEFT COLUMN: neofetch fields (x=24..440) ----
    col1_x = 24
    col2_x = col1_x + 100
    start_y = 52
    rh = 17.5  # row height

    svg.append(f'''<!-- === LEFT: neofetch identity === -->
<g class="row" style="animation-delay:0.05s">
  <text class="mono uhost" x="{col1_x}" y="{start_y}">charan<tspan fill="#8b949e">@</tspan><tspan fill="#58a6ff">svit</tspan></text>
  <line x1="{col1_x}" y1="{start_y+4}" x2="{col1_x+155}" y2="{start_y+4}" stroke="#30363d" stroke-width="1"/>
</g>''')

    for i, (k, v, vc) in enumerate(fields):
        y = start_y + (i + 1) * rh + 4
        delay = 0.08 + i * 0.04
        svg.append(f'''<g class="row mono" style="animation-delay:{delay:.2f}s">
  <text class="fkey" x="{col1_x}" y="{y}">{k}:</text>
  <text class="fval" x="{col2_x}" y="{y}" fill="{vc}">{v}</text>
</g>''')

    # ANSI color blocks
    ansi_y = start_y + (len(fields) + 1) * rh + 10
    ansi_colors = ["#484f58","#ff7b72","#3fb950","#d29922","#58a6ff","#bc8cff","#39c5cf","#b1bac4"]
    delay_ansi = 0.08 + len(fields) * 0.04 + 0.06
    svg.append(f'<g class="row" style="animation-delay:{delay_ansi:.2f}s">')
    for idx, c in enumerate(ansi_colors):
        bx = col1_x + idx * 26
        svg.append(f'  <rect x="{bx}" y="{ansi_y}" width="20" height="10" rx="3" fill="{c}"/>')
    svg.append('</g>')

    # ---- RIGHT COLUMN: skill bars (x=460..850) ----
    rc_x = 460
    rc_w = 190  # bar width
    svg.append(f'''<!-- === RIGHT: skills & projects === -->
<g class="row" style="animation-delay:0.08s">
  <text class="mono sectitle" x="{rc_x}" y="52">SKILLS</text>
  <line x1="{rc_x}" y1="56" x2="{W-24}" y2="56" stroke="#30363d" stroke-width="1"/>
</g>''')

    bar_start_y = 70
    bar_h = 8
    bar_rx = 4
    bar_gap = 20
    for bi, (sname, pct, scolor) in enumerate(skills):
        by = bar_start_y + bi * bar_gap
        bdelay = 0.14 + bi * 0.06
        fill_w = int(rc_w * pct / 100)
        anim_delay_bar = 0.14 + bi * 0.06 + 0.2  # bar fill starts a bit after label
        svg.append(f'''<g class="row mono" style="animation-delay:{bdelay:.2f}s">
  <text class="sbar-label" x="{rc_x}" y="{by}">{sname}</text>
  <text class="sbar-label" x="{rc_x + rc_w + 32}" y="{by}" fill="{scolor}">{pct}%</text>
  <!-- Track -->
  <rect x="{rc_x}" y="{by+3}" width="{rc_w}" height="{bar_h}" rx="{bar_rx}" fill="#21262d"/>
  <!-- Fill -->
  <rect class="bar-fill" x="{rc_x}" y="{by+3}" width="{fill_w}" height="{bar_h}" rx="{bar_rx}"
        fill="{scolor}" opacity="0.85"
        style="animation-delay:{anim_delay_bar:.2f}s; animation-duration:0.9s;"/>
</g>''')

    # Projects section
    proj_title_y = bar_start_y + len(skills) * bar_gap + 18
    delay_proj = 0.14 + len(skills) * 0.06 + 0.12
    svg.append(f'''<g class="row" style="animation-delay:{delay_proj:.2f}s">
  <text class="mono sectitle" x="{rc_x}" y="{proj_title_y}">PROJECTS</text>
  <line x1="{rc_x}" y1="{proj_title_y+4}" x2="{W-24}" y2="{proj_title_y+4}" stroke="#30363d" stroke-width="1"/>
</g>''')

    for pi, (pname, pdesc) in enumerate(projects):
        py = proj_title_y + 18 + pi * 16
        pdelay = delay_proj + 0.06 + pi * 0.05
        svg.append(f'''<g class="row mono" style="animation-delay:{pdelay:.2f}s">
  <circle cx="{rc_x + 4}" cy="{py - 4}" r="2" fill="#39d353"/>
  <text class="pname" x="{rc_x + 12}" y="{py}">{pname}</text>
  <text class="pdesc" x="{rc_x + 12}" y="{py + 11}">{pdesc}</text>
</g>''')

    # Vertical divider between columns
    svg.append(f'<line x1="445" y1="38" x2="445" y2="{H-30}" stroke="#21262d" stroke-width="1"/>')

    # Footer
    svg.append(f'''<g clip-path="url(#fClipInfo)">
  <rect x="0" y="{H-26}" width="{W}" height="26" fill="#161b22"/>
  <line x1="0" y1="{H-26}" x2="{W}" y2="{H-26}" stroke="#30363d" stroke-width="1"/>
</g>
<g class="mono" transform="translate(18,{H-9})">
  <text font-size="9.5px" fill="#8b949e">
    <tspan fill="#39d353">charan@svit:~$</tspan>
    <tspan> cat ~/goals.md</tspan>
    <tspan class="cursor"> █</tspan>
  </text>
  <circle class="live" cx="{W-32}" cy="-5" r="4" fill="#39d353"/>
  <text font-size="9px" fill="#39d353" x="{W-22}" y="-1">OK</text>
</g>
</svg>''')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Info card written to {output_path}")


if __name__ == "__main__":
    generate_infocard_svg()
