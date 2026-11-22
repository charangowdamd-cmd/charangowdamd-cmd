"""
Generate improved animated SVG contribution heatmap for GitHub profile README.
Upgraded with:
- Gradient background
- Glowing active cells with drop-shadow filter
- Smoother diagonal wave animation
- Wider layout with better stat cards
- Animated counter effect on stats
"""

import json
import os

PALETTE = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}
GLOW = {
    0: "none",
    1: "url(#glow1)",
    2: "url(#glow2)",
    3: "url(#glow3)",
    4: "url(#glow4)",
}
BORDER_COLOR = "#21262d"


def generate_heatmap_svg(
    data_path: str = "assets/data/contributions.json",
    output_path: str = "assets/heatmap.svg",
):
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    weeks = data.get("weeks", [])
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    active_days = data.get("active_days", 0)
    peak = data.get("peak_day", {})
    peak_count = peak.get("count", 0)
    peak_date = peak.get("date", "N/A")

    svg_width = 870
    svg_height = 240
    cell_size = 11
    cell_gap = 3
    cell_rx = 3
    grid_start_x = 42
    grid_start_y = 108

    # Month labels
    month_labels = []
    last_month = ""
    for col_idx, week in enumerate(weeks):
        for day in week:
            if day and day.get("month"):
                m = day["month"]
                if m != last_month:
                    if not month_labels or (col_idx - month_labels[-1][1] >= 3):
                        month_labels.append((m, col_idx))
                        last_month = m
                break

    p = []  # SVG parts

    p.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 {svg_width} {svg_height}"
  width="{svg_width}" height="{svg_height}">
<defs>
  <style>
    .mono {{ font-family: 'JetBrains Mono','Fira Code',ui-monospace,monospace; }}
    .title  {{ fill:#8b949e; font-size:11.5px; font-weight:600; }}
    .slabel {{ fill:#484f58; font-size:9px; font-weight:700; letter-spacing:0.8px; text-transform:uppercase; }}
    .sval   {{ font-size:15px; font-weight:800; }}
    .green  {{ fill:#39d353; }}
    .blue   {{ fill:#58a6ff; }}
    .purple {{ fill:#bc8cff; }}
    .orange {{ fill:#f0883e; }}
    .axis   {{ fill:#484f58; font-size:9px; }}
    .legend {{ fill:#484f58; font-size:9px; }}

    /* Pulsing live dot */
    @keyframes livePulse {{
      0%,100% {{ opacity:1; r:3.5px; }}
      50%      {{ opacity:0.3; r:2px; }}
    }}
    .live-dot {{ animation: livePulse 1.8s ease-in-out infinite; }}

    /* Cell entrance: diagonal wave (col*20ms + row*12ms) */
    @keyframes cellIn {{
      0%   {{ opacity:0; transform:scale(0.1); }}
      65%  {{ opacity:1; transform:scale(1.2); }}
      100% {{ opacity:1; transform:scale(1);   }}
    }}
    .cell {{
      transform-box:fill-box;
      transform-origin:center;
      opacity:0;
      animation: cellIn 0.4s cubic-bezier(0.34,1.56,0.64,1) forwards;
    }}

    /* Stat row fade-up */
    @keyframes fadeUp {{
      from {{ opacity:0; transform:translateY(6px); }}
      to   {{ opacity:1; transform:translateY(0);   }}
    }}
    .stat-g {{ opacity:0; animation: fadeUp 0.5s ease-out forwards; }}
  </style>

  <!-- Glow filters per activity level -->
  <filter id="glow1" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="1.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glow2" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feFlood flood-color="#006d32" flood-opacity="0.5" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="d"/>
    <feMerge><feMergeNode in="d"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glow3" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="2.8" result="b"/>
    <feFlood flood-color="#26a641" flood-opacity="0.6" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="d"/>
    <feMerge><feMergeNode in="d"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glow4" x="-70%" y="-70%" width="240%" height="240%">
    <feGaussianBlur stdDeviation="3.5" result="b"/>
    <feFlood flood-color="#39d353" flood-opacity="0.7" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="d"/>
    <feMerge><feMergeNode in="d"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>

  <!-- Subtle gradient background -->
  <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="#0d1117"/>
    <stop offset="100%" stop-color="#0a1628"/>
  </linearGradient>

  <clipPath id="hClip">
    <rect x="0" y="0" width="{svg_width}" height="30" rx="10"/>
  </clipPath>
</defs>

<!-- Background -->
<rect x="0.5" y="0.5" width="{svg_width-1}" height="{svg_height-1}" rx="10"
      fill="url(#bgGrad)" stroke="#30363d" stroke-width="1"/>

<!-- Header -->
<g clip-path="url(#hClip)">
  <rect x="0" y="0" width="{svg_width}" height="30" fill="#161b22"/>
  <line x1="0" y1="30" x2="{svg_width}" y2="30" stroke="#30363d" stroke-width="1"/>
</g>

<!-- Window buttons -->
<circle cx="18" cy="15" r="5" fill="#ff5f56"/>
<circle cx="34" cy="15" r="5" fill="#ffbd2e"/>
<circle cx="50" cy="15" r="5" fill="#27c93f"/>

<!-- Window title -->
<text class="mono title" x="{svg_width//2}" y="19" text-anchor="middle">
  charan@svit: ~/contributions — 53-week heatmap
</text>

<!-- Live indicator -->
<circle class="live-dot" cx="{svg_width-72}" cy="15" r="3.5" fill="#39d353"/>
<text class="mono" x="{svg_width-62}" y="19" fill="#39d353" font-size="9px" font-weight="700">LIVE</text>
''')

    # Stats row (5 cards)
    stats = [
        ("TOTAL", str(total),    "#39d353", "green"),
        ("CURRENT STREAK", f"{current_streak} days", "#58a6ff", "blue"),
        ("LONGEST STREAK", f"{longest_streak} days", "#bc8cff", "purple"),
        ("ACTIVE DAYS",    f"{active_days} days",    "#f0883e", "orange"),
        ("PEAK / DAY",     str(peak_count),           "#39d353", "green"),
    ]

    stat_x_positions = [42, 220, 400, 575, 745]
    for i, ((label, value, color, cls), sx) in enumerate(zip(stats, stat_x_positions)):
        delay = 0.1 + i * 0.08
        p.append(f'''<g class="stat-g mono" style="animation-delay:{delay:.2f}s">
  <text class="slabel" x="{sx}" y="50">{label}</text>
  <text class="sval {cls}" x="{sx}" y="70">{value}</text>
</g>''')

    # Separator line
    p.append(f'<line x1="34" y1="82" x2="{svg_width-34}" y2="82" stroke="#21262d" stroke-width="1"/>')

    # Month labels
    p.append('<g class="mono axis">')
    for (mname, col_idx) in month_labels:
        mx = grid_start_x + col_idx * (cell_size + cell_gap)
        p.append(f'  <text x="{mx:.1f}" y="{grid_start_y - 5}">{mname}</text>')
    p.append('</g>')

    # DOW labels
    p.append(f'''<g class="mono axis">
  <text x="8" y="{grid_start_y + 1*(cell_size+cell_gap) + 9}">Mon</text>
  <text x="8" y="{grid_start_y + 3*(cell_size+cell_gap) + 9}">Wed</text>
  <text x="8" y="{grid_start_y + 5*(cell_size+cell_gap) + 9}">Fri</text>
</g>''')

    # Heatmap cells
    p.append('<g id="cells">')
    for col_idx, week in enumerate(weeks):
        x = grid_start_x + col_idx * (cell_size + cell_gap)
        for row_idx, day in enumerate(week):
            if day is None:
                continue
            y = grid_start_y + row_idx * (cell_size + cell_gap)
            level = day.get("level", 0)
            fill = PALETTE.get(level, PALETTE[0])
            count = day.get("count", 0)
            date_str = day.get("date", "")
            # diagonal wave: col drives primary delay, row adds ripple
            delay = col_idx * 0.020 + row_idx * 0.010
            glow_filter = GLOW.get(level, "none")
            tooltip = f"{count} contributions on {date_str}" if count else f"No contributions on {date_str}"
            filter_attr = f'filter="{glow_filter}"' if glow_filter != "none" else ""
            p.append(
                f'  <rect class="cell" x="{x:.1f}" y="{y:.1f}" '
                f'width="{cell_size}" height="{cell_size}" rx="{cell_rx}" '
                f'fill="{fill}" stroke="{BORDER_COLOR}" stroke-width="0.4" '
                f'{filter_attr} style="animation-delay:{delay:.3f}s">'
                f'<title>{tooltip}</title></rect>'
            )
    p.append('</g>')

    # Legend
    legend_x = svg_width - 160
    legend_y = grid_start_y + 7 * (cell_size + cell_gap) + 14
    p.append(f'''<g class="mono legend" transform="translate({legend_x},{legend_y})">
  <text x="0" y="9">Less</text>
  <rect x="28" y="0" width="11" height="11" rx="2.5" fill="{PALETTE[0]}" stroke="{BORDER_COLOR}" stroke-width="0.4"/>
  <rect x="43" y="0" width="11" height="11" rx="2.5" fill="{PALETTE[1]}" stroke="{BORDER_COLOR}" stroke-width="0.4"/>
  <rect x="58" y="0" width="11" height="11" rx="2.5" fill="{PALETTE[2]}" stroke="{BORDER_COLOR}" stroke-width="0.4"/>
  <rect x="73" y="0" width="11" height="11" rx="2.5" fill="{PALETTE[3]}" stroke="{BORDER_COLOR}" stroke-width="0.4"/>
  <rect x="88" y="0" width="11" height="11" rx="2.5" fill="{PALETTE[4]}" stroke="{BORDER_COLOR}" stroke-width="0.4"/>
  <text x="104" y="9">More</text>
</g>''')

    # Footer prompt
    p.append(f'''<text class="mono" x="42" y="{legend_y + 9}" font-size="9px" fill="#484f58">
  <tspan fill="#39d353">$</tspan> git log --oneline --graph
</text>''')

    p.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"Heatmap written to {output_path}")


if __name__ == "__main__":
    generate_heatmap_svg()
