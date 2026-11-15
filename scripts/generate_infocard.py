"""
Generate Neofetch-style terminal info card SVG for GitHub profile README.
Outputs assets/info-card.svg with animated terminal details.
"""

import html
import os
import sys

OUTPUT_SVG_PATH = "assets/info-card.svg"

def escape_xml(text: str) -> str:
    return html.escape(text, quote=True)

def generate_infocard_svg(output_path: str = OUTPUT_SVG_PATH):
    svg_width = 430
    svg_height = 450

    # Fields list: (label, value, color)
    fields = [
        ("OS", "Arch Linux / macOS Darwin", "#58a6ff"),
        ("Host", "Sai Vidya Institute of Technology (SVIT)", "#f0883e"),
        ("Name", "Charan Gowda M D", "#58a6ff"),
        ("Role", "Computer Science Engineering Student", "#bc8cff"),
        ("Interests", "Software Eng • Backend Dev • AI/ML", "#39d353"),
        ("Open Source", "Apache Maven Contributor", "#79c0ff"),
        ("Focus", "Building systems &amp; contributing to OSS", "#56d364"),
        ("Languages", "Python • Java • C • Go • SQL", "#d2a8ff"),
        ("Tools", "Git • Docker • Linux • Maven • GH Actions", "#7ee787"),
    ]

    projects = [
        ("Salamander", "Coding challenge &amp; interview prep platform"),
        ("BEL Blockchain", "Defense Blockchain Secure Platform MVP"),
        ("Apache Maven", "Core pull requests &amp; community contribution"),
        ("OSS Club SVIT", "Official platform &amp; developer community"),
    ]

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&amp;display=swap');

      .window {{
        fill: #0d1117;
        stroke: #30363d;
        stroke-width: 1px;
        rx: 10px;
      }}

      .header {{
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
      }}

      .footer {{
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
      }}

      .mono {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      }}

      .header-title {{
        fill: #8b949e;
        font-size: 11.5px;
        font-weight: 600;
      }}

      .shell-badge {{
        fill: #58a6ff;
        font-size: 10px;
        font-weight: 600;
      }}

      .user-host {{
        fill: #39d353;
        font-size: 13px;
        font-weight: 700;
      }}

      .hr-line {{
        stroke: #30363d;
        stroke-width: 1px;
      }}

      .field-key {{
        font-size: 10.5px;
        font-weight: 700;
        fill: #39d353;
      }}

      .field-val {{
        font-size: 10px;
        font-weight: 400;
        fill: #c9d1d9;
      }}

      .section-title {{
        font-size: 11px;
        font-weight: 700;
        fill: #58a6ff;
        letter-spacing: 0.5px;
      }}

      .proj-name {{
        font-size: 10px;
        font-weight: 600;
        fill: #79c0ff;
      }}

      .proj-desc {{
        font-size: 9.5px;
        font-weight: 400;
        fill: #8b949e;
      }}

      @keyframes reveal {{
        0% {{
          opacity: 0;
          transform: translateY(-2px);
        }}
        100% {{
          opacity: 1;
          transform: translateY(0);
        }}
      }}

      .anim-row {{
        opacity: 0;
        animation: reveal 0.15s ease-out forwards;
      }}

      @keyframes blinkCursor {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}

      .cursor {{
        animation: blinkCursor 1.1s infinite;
        fill: #39d353;
      }}
    </style>

    <clipPath id="infoCardHeaderClip">
      <rect x="0" y="0" width="{svg_width}" height="32" rx="10" />
    </clipPath>
    <clipPath id="infoCardFooterClip">
      <rect x="0" y="{svg_height - 24}" width="{svg_width}" height="24" rx="10" />
    </clipPath>
  </defs>

  <!-- Terminal Window Background -->
  <rect class="window" x="0.5" y="0.5" width="{svg_width - 1}" height="{svg_height - 1}" />

  <!-- Header Bar -->
  <g clip-path="url(#infoCardHeaderClip)">
    <rect class="header" x="0" y="0" width="{svg_width}" height="32" />
    <line x1="0" y1="32" x2="{svg_width}" y2="32" stroke="#30363d" stroke-width="1" />
  </g>

  <!-- Window Buttons -->
  <circle cx="18" cy="16" r="5" fill="#ff5f56" />
  <circle cx="34" cy="16" r="5" fill="#ffbd2e" />
  <circle cx="50" cy="16" r="5" fill="#27c93f" />

  <!-- Window Title -->
  <text class="mono header-title" x="{svg_width // 2}" y="20" text-anchor="middle">charan@svit: ~ (neofetch)</text>
  <text class="mono shell-badge" x="{svg_width - 16}" y="20" text-anchor="end">zsh 5.9</text>

  <!-- Neofetch Content Body -->
  <g transform="translate(22, 48)">
    <!-- User @ Host Banner -->
    <g class="anim-row" style="animation-delay: 0.05s;">
      <text class="mono user-host" x="0" y="10">charan<tspan fill="#8b949e">@</tspan><tspan fill="#58a6ff">svit</tspan></text>
      <line class="hr-line" x1="0" y1="16" x2="160" y2="16" />
    </g>''')

    # Fields (System & Developer Info)
    start_y = 32
    row_height = 16.5
    for i, (k, v, val_color) in enumerate(fields):
        y = start_y + i * row_height
        delay = 0.08 + i * 0.03
        svg.append(f'''    <g class="anim-row" style="animation-delay: {delay:.3f}s;">
      <text class="mono field-key" x="0" y="{y}">{k}:</text>
      <text class="mono field-val" x="84" y="{y}" fill="{val_color}">{v}</text>
    </g>''')

    # Projects & Achievements Section
    proj_header_y = start_y + len(fields) * row_height + 10
    svg.append(f'''
    <!-- Projects Section -->
    <g class="anim-row" style="animation-delay: 0.38s;">
      <text class="mono section-title" x="0" y="{proj_header_y}">PROJECTS &amp; ACHIEVEMENTS</text>
      <line class="hr-line" x1="0" y1="{proj_header_y + 6}" x2="{svg_width - 44}" y2="{proj_header_y + 6}" />
    </g>''')

    proj_start_y = proj_header_y + 20
    proj_row_height = 17
    for j, (pname, pdesc) in enumerate(projects):
        y = proj_start_y + j * proj_row_height
        delay = 0.40 + j * 0.03
        svg.append(f'''    <g class="anim-row" style="animation-delay: {delay:.3f}s;">
      <circle cx="4" cy="{y - 3.5}" r="2" fill="#39d353" />
      <text class="mono proj-name" x="12" y="{y}">{pname}:</text>
      <text class="mono proj-desc" x="110" y="{y}">{pdesc}</text>
    </g>''')

    # Terminal Color Blocks (Classic Neofetch ANSI colors)
    palette_y = proj_start_y + len(projects) * proj_row_height + 14
    ansi_colors = [
        "#484f58",  # Black
        "#ff7b72",  # Red
        "#3fb950",  # Green
        "#d29922",  # Yellow
        "#58a6ff",  # Blue
        "#bc8cff",  # Magenta
        "#39c5cf",  # Cyan
        "#b1bac4",  # White
    ]
    block_w = 22
    block_h = 10
    block_rx = 3
    block_gap = 6

    svg.append(f'''
    <!-- ANSI Terminal Color Blocks -->
    <g class="anim-row" style="animation-delay: 0.55s;" transform="translate(0, {palette_y})">''')
    for idx, col in enumerate(ansi_colors):
        bx = idx * (block_w + block_gap)
        svg.append(f'      <rect x="{bx}" y="0" width="{block_w}" height="{block_h}" rx="{block_rx}" fill="{col}" />')
    svg.append('    </g>')

    svg.append(f'''  </g>

  <!-- Terminal Status Footer -->
  <g clip-path="url(#infoCardFooterClip)">
    <rect class="footer" x="0" y="{svg_height - 24}" width="{svg_width}" height="24" />
    <line x1="0" y1="{svg_height - 24}" x2="{svg_width}" y2="{svg_height - 24}" stroke="#30363d" stroke-width="1" />
  </g>

  <g transform="translate(14, {svg_height - 8})">
    <text class="mono" x="0" y="0" font-size="9.5px" fill="#8b949e">
      <tspan fill="#39d353">charan@svit:~$</tspan> echo $ENGINEER_GOALS <tspan class="cursor">█</tspan>
    </text>
  </g>
</svg>''')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated Neofetch info card SVG at {output_path}")

if __name__ == "__main__":
    generate_infocard_svg()
