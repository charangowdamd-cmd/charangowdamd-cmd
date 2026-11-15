"""
Generate animated SVG contribution heatmap for GitHub profile README.
Reads data from assets/data/contributions.json and outputs assets/heatmap.svg.
"""

import json
import os
import sys

# Professional GitHub Dark theme green palette
PALETTE = {
    0: "#161b22",  # Empty / no contributions
    1: "#0e4429",  # Level 1
    2: "#006d32",  # Level 2
    3: "#26a641",  # Level 3
    4: "#39d353",  # Level 4
}

BORDER_COLOR = "#21262d"

def generate_heatmap_svg(data_path: str = "assets/data/contributions.json", output_path: str = "assets/heatmap.svg"):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    weeks = data.get("weeks", [])
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    active_days = data.get("active_days", 0)
    peak = data.get("peak_day", {})
    peak_count = peak.get("count", 0)
    peak_date = peak.get("date", "N/A")

    # Dimensions
    svg_width = 860
    svg_height = 230
    
    cell_size = 10
    cell_gap = 3.5
    cell_rx = 2.5
    
    grid_start_x = 48
    grid_start_y = 105

    # Month labels calculation
    month_labels = []
    last_month = ""
    for col_idx, week in enumerate(weeks):
        for day in week:
            if day and day.get("month"):
                m = day["month"]
                if m != last_month and (col_idx == 0 or (col_idx * (cell_size + cell_gap) > 30)):
                    # Check that it's at least 3 weeks away from previous month label
                    if not month_labels or (col_idx - month_labels[-1][1] >= 3):
                        month_labels.append((m, col_idx))
                        last_month = m
                break

    # Build SVG content
    svg_parts = []
    
    # Root SVG tag with dark terminal styles
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');
      
      .terminal-window {{
        fill: #0d1117;
        stroke: #30363d;
        stroke-width: 1px;
        rx: 10px;
      }}
      
      .terminal-header {{
        fill: #161b22;
        stroke: #30363d;
        stroke-width: 1px;
      }}
      
      .mono-text {{
        font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular, monospace;
      }}
      
      .title-text {{
        fill: #8b949e;
        font-size: 12px;
        font-weight: 600;
      }}
      
      .stat-label {{
        fill: #7d8590;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
      }}
      
      .stat-value {{
        fill: #58a6ff;
        font-size: 13px;
        font-weight: 700;
      }}
      
      .stat-green {{
        fill: #39d353;
      }}
      
      .axis-label {{
        fill: #6e7681;
        font-size: 9.5px;
        font-weight: 400;
      }}
      
      .legend-text {{
        fill: #6e7681;
        font-size: 10px;
      }}
      
      .live-badge {{
        animation: pulse 2s infinite ease-in-out;
      }}
      
      @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.92); }}
      }}

      @keyframes cellAnim {{
        0% {{
          opacity: 0;
          transform: scale(0.2);
        }}
        70% {{
          opacity: 1;
          transform: scale(1.15);
        }}
        100% {{
          opacity: 1;
          transform: scale(1);
        }}
      }}
      
      .cell {{
        transform-box: fill-box;
        transform-origin: center;
        opacity: 0;
        animation: cellAnim 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
      }}
      
      .cell:hover {{
        stroke: #58a6ff;
        stroke-width: 1.5px;
        cursor: pointer;
      }}
    </style>
    
    <clipPath id="headerClip">
      <rect x="0" y="0" width="{svg_width}" height="32" rx="10" />
    </clipPath>
  </defs>

  <!-- Terminal Window Background -->
  <rect class="terminal-window" x="0.5" y="0.5" width="{svg_width - 1}" height="{svg_height - 1}" />

  <!-- Header Bar -->
  <g clip-path="url(#headerClip)">
    <rect class="terminal-header" x="0" y="0" width="{svg_width}" height="32" />
    <line x1="0" y1="32" x2="{svg_width}" y2="32" stroke="#30363d" stroke-width="1" />
  </g>

  <!-- macOS / Terminal Window Buttons -->
  <circle cx="20" cy="16" r="5.5" fill="#ff5f56" />
  <circle cx="38" cy="16" r="5.5" fill="#ffbd2e" />
  <circle cx="56" cy="16" r="5.5" fill="#27c93f" />

  <!-- Window Title -->
  <text class="mono-text title-text" x="{svg_width // 2}" y="20" text-anchor="middle">charan@svit: ~/contributions (53 weeks heatmap)</text>

  <!-- Live Pulse Indicator -->
  <circle class="live-badge" cx="{svg_width - 78}" cy="16" r="3.5" fill="#39d353" />
  <text class="mono-text" x="{svg_width - 68}" y="20" fill="#39d353" font-size="10px" font-weight="600">LIVE</text>

  <!-- Stats Banner Bar -->
  <g transform="translate(48, 44)">
    <!-- Stat 1: Total -->
    <text class="mono-text stat-label" x="0" y="12">TOTAL CONTRIBUTIONS</text>
    <text class="mono-text stat-value stat-green" x="0" y="32">{total}</text>

    <!-- Divider -->
    <line x1="165" y1="4" x2="165" y2="34" stroke="#21262d" stroke-width="1" />

    <!-- Stat 2: Current Streak -->
    <text class="mono-text stat-label" x="185" y="12">CURRENT STREAK</text>
    <text class="mono-text stat-value" x="185" y="32">{current_streak} <tspan font-size="10px" font-weight="400" fill="#8b949e">days</tspan></text>

    <!-- Divider -->
    <line x1="315" y1="4" x2="315" y2="34" stroke="#21262d" stroke-width="1" />

    <!-- Stat 3: Longest Streak -->
    <text class="mono-text stat-label" x="335" y="12">LONGEST STREAK</text>
    <text class="mono-text stat-value" x="335" y="32">{longest_streak} <tspan font-size="10px" font-weight="400" fill="#8b949e">days</tspan></text>

    <!-- Divider -->
    <line x1="470" y1="4" x2="470" y2="34" stroke="#21262d" stroke-width="1" />

    <!-- Stat 4: Active Days -->
    <text class="mono-text stat-label" x="490" y="12">ACTIVE DAYS</text>
    <text class="mono-text stat-value" x="490" y="32">{active_days} <tspan font-size="10px" font-weight="400" fill="#8b949e">days</tspan></text>

    <!-- Divider -->
    <line x1="600" y1="4" x2="600" y2="34" stroke="#21262d" stroke-width="1" />

    <!-- Stat 5: Peak Day -->
    <text class="mono-text stat-label" x="620" y="12">PEAK ACTIVITY</text>
    <text class="mono-text stat-value" x="620" y="32">{peak_count} <tspan font-size="10px" font-weight="400" fill="#8b949e">({peak_date})</tspan></text>
  </g>

  <!-- Month Labels -->
  <g class="mono-text axis-label">''')

    for month_name, col_idx in month_labels:
        mx = grid_start_x + col_idx * (cell_size + cell_gap)
        svg_parts.append(f'    <text x="{mx:.1f}" y="{grid_start_y - 6}">{month_name}</text>')

    svg_parts.append('  </g>')

    # Day of week labels (Mon, Wed, Fri)
    svg_parts.append('''  <!-- Day of Week Labels -->
  <g class="mono-text axis-label">
    <text x="24" y="128">Mon</text>
    <text x="24" y="155">Wed</text>
    <text x="24" y="182">Fri</text>
  </g>''')

    # Calendar Cells Grid with staggered animation
    svg_parts.append('  <!-- Heatmap Calendar Cells -->\n  <g id="heatmap-cells">')

    for col_idx, week in enumerate(weeks):
        x = grid_start_x + col_idx * (cell_size + cell_gap)
        for row_idx, day in enumerate(week):
            if day is None:
                continue
            y = grid_start_y + row_idx * (cell_size + cell_gap)
            level = day.get("level", 0)
            fill_color = PALETTE.get(level, PALETTE[0])
            count = day.get("count", 0)
            date_str = day.get("date", "")
            
            # Staggered wave delay: ripples from left to right, slight vertical ripple
            anim_delay = col_idx * 0.016 + row_idx * 0.012
            
            tooltip_title = f"{count} contributions on {date_str}" if count > 0 else f"No contributions on {date_str}"
            
            svg_parts.append(
                f'    <rect class="cell" x="{x:.1f}" y="{y:.1f}" width="{cell_size}" height="{cell_size}" '
                f'rx="{cell_rx}" fill="{fill_color}" stroke="{BORDER_COLOR}" stroke-width="0.5" '
                f'style="animation-delay: {anim_delay:.3f}s;">\n'
                f'      <title>{tooltip_title}</title>\n'
                f'    </rect>'
            )

    svg_parts.append('  </g>')

    # Bottom Legend and Footer
    legend_x = svg_width - 175
    legend_y = grid_start_y + 7 * (cell_size + cell_gap) + 12

    svg_parts.append(f'''  <!-- Legend & Terminal Prompt -->
  <g transform="translate(48, {legend_y})">
    <text class="mono-text" x="0" y="9" fill="#8b949e" font-size="10px">
      <tspan fill="#39d353">$</tspan> git log --graph --all --decorate
    </text>
  </g>

  <g transform="translate({legend_x}, {legend_y - 2})">
    <text class="mono-text legend-text" x="0" y="10">Less</text>
    <rect x="32" y="1" width="10" height="10" rx="2" fill="{PALETTE[0]}" stroke="{BORDER_COLOR}" stroke-width="0.5" />
    <rect x="46" y="1" width="10" height="10" rx="2" fill="{PALETTE[1]}" stroke="{BORDER_COLOR}" stroke-width="0.5" />
    <rect x="60" y="1" width="10" height="10" rx="2" fill="{PALETTE[2]}" stroke="{BORDER_COLOR}" stroke-width="0.5" />
    <rect x="74" y="1" width="10" height="10" rx="2" fill="{PALETTE[3]}" stroke="{BORDER_COLOR}" stroke-width="0.5" />
    <rect x="88" y="1" width="10" height="10" rx="2" fill="{PALETTE[4]}" stroke="{BORDER_COLOR}" stroke-width="0.5" />
    <text class="mono-text legend-text" x="105" y="10">More</text>
  </g>
</svg>''')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"Generated animated contribution heatmap at {output_path}")

if __name__ == "__main__":
    generate_heatmap_svg()
