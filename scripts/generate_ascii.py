"""
Generate monochrome animated ASCII portrait SVG from source photo.
Saves pre-rendered ASCII to assets/data/portrait_ascii.txt and
compiles it into assets/ascii-portrait.svg.
Does not commit personal source photographs.
"""

import os
import sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

DEFAULT_PHOTO = "C:/Users/Charan Gowda/.gemini/antigravity/brain/68c725fd-7bd0-439f-a4d6-389a51a3fb0d/.user_uploaded/media_1794763228072_d603f337.jpg"
ASCII_DATA_PATH = "assets/data/portrait_ascii.txt"
OUTPUT_SVG_PATH = "assets/ascii-portrait.svg"

def is_in_silhouette(x, y, max_x=42, max_y=31):
    """
    Define the silhouette boundary of Charan's head, neck, and shoulders
    to eliminate background artifacts cleanly.
    """
    hx, hy = 21, 9
    rx, ry = 14, 10
    # Head oval
    if ((x - hx) / rx) ** 2 + ((y - hy) / ry) ** 2 <= 1.0:
        return True
    # Neck & jawline
    if 10 <= y <= 18 and 10 <= x <= 32:
        return True
    # Shoulders and chest (fans out naturally)
    if y >= 17:
        span = 13 + (y - 17) * 2.2
        if abs(x - 21) <= span:
            return True
    return False

def convert_photo_to_ascii(photo_path: str, target_w: int = 42) -> list[str]:
    """Convert photograph into high-definition monospace ASCII art."""
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Source photograph not found at {photo_path}")

    img = Image.open(photo_path)
    
    # Precise crop for Charan's face, glasses, neck, and shoulders
    # Coordinates calibrated from (768 x 1024)
    crop_box = (150, 210, 618, 850)
    cropped = img.crop(crop_box)
    w, h = cropped.size

    gray = ImageOps.grayscale(cropped)
    # Edge filter to crispen glasses, jaw, smile, hair
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(2.0)

    # Monospace aspect ratio compensation (height ~ 1.82x width)
    target_h = int(target_w * (h / w) * 0.55)

    r_gray = gray.resize((target_w, target_h), Image.Resampling.LANCZOS)
    r_edge = edges.resize((target_w, target_h), Image.Resampling.LANCZOS)

    palette = " .:-=+*#%@"

    lines = []
    for y in range(target_h):
        line = []
        for x in range(target_w):
            if not is_in_silhouette(x, y, target_w, target_h):
                line.append(" ")
                continue
            
            g = r_gray.getpixel((x, y))
            e = r_edge.getpixel((x, y))
            
            # Dark features (hair, glasses frames, pupils, flannel pattern)
            # get mapped to brighter characters in the green terminal
            val = int(255 - g)
            if e > 45:
                val = min(255, val + 65)
            
            idx = int((val / 255.0) * (len(palette) - 1))
            ch = palette[idx]
            if ch == " ":
                ch = "."
            line.append(ch)
        lines.append("".join(line))

    return lines

def save_ascii_text(lines: list[str], output_path: str = ASCII_DATA_PATH):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"Saved ASCII text to {output_path}")

def load_ascii_text(input_path: str = ASCII_DATA_PATH) -> list[str]:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"ASCII data not found at {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f]
    return lines

def generate_ascii_svg(lines: list[str], output_svg_path: str = OUTPUT_SVG_PATH):
    svg_width = 410
    svg_height = 450
    line_height = 11.2
    start_y = 60
    font_size = 9.8

    # Escape XML entities for characters like <, >, &
    def escape_xml(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    svg_lines = []
    svg_lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;display=swap');

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

      .status-bar {{
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

      .badge {{
        fill: #58a6ff;
        font-size: 10px;
        font-weight: 600;
      }}

      .status-text {{
        fill: #8b949e;
        font-size: 9.5px;
        font-weight: 500;
      }}

      .status-accent {{
        fill: #39d353;
        font-weight: 700;
      }}

      .ascii-text {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: {font_size}px;
        font-weight: 600;
        fill: #39d353;
        letter-spacing: 0.8px;
        filter: drop-shadow(0 0 1.5px rgba(57, 211, 83, 0.4));
        white-space: pre;
      }}

      @keyframes revealLine {{
        0% {{
          opacity: 0;
          transform: translateY(-2px);
        }}
        100% {{
          opacity: 1;
          transform: translateY(0);
        }}
      }}

      .term-line {{
        opacity: 0;
        animation: revealLine 0.15s ease-out forwards;
      }}

      @keyframes blinkCursor {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}

      .cursor {{
        animation: blinkCursor 1.1s infinite;
        fill: #39d353;
      }}

      .scanline {{
        background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0, 0, 0, 0.2) 50%, rgba(0, 0, 0, 0.2));
      }}
    </style>

    <clipPath id="asciiHeaderClip">
      <rect x="0" y="0" width="{svg_width}" height="32" rx="10" />
    </clipPath>
    <clipPath id="asciiFooterClip">
      <rect x="0" y="{svg_height - 24}" width="{svg_width}" height="24" rx="10" />
    </clipPath>
  </defs>

  <!-- Terminal Window Background -->
  <rect class="window" x="0.5" y="0.5" width="{svg_width - 1}" height="{svg_height - 1}" />

  <!-- Header Bar -->
  <g clip-path="url(#asciiHeaderClip)">
    <rect class="header" x="0" y="0" width="{svg_width}" height="32" />
    <line x1="0" y1="32" x2="{svg_width}" y2="32" stroke="#30363d" stroke-width="1" />
  </g>

  <!-- Window Buttons -->
  <circle cx="18" cy="16" r="5" fill="#ff5f56" />
  <circle cx="34" cy="16" r="5" fill="#ffbd2e" />
  <circle cx="50" cy="16" r="5" fill="#27c93f" />

  <!-- Window Title -->
  <text class="mono header-title" x="{svg_width // 2}" y="20" text-anchor="middle">charan@terminal: ~/portrait.asc</text>
  <text class="mono badge" x="{svg_width - 16}" y="20" text-anchor="end">UTF-8</text>

  <!-- ASCII Art Lines with Typing / Line-by-Line Staggered Animation -->
  <g class="ascii-text">''')

    # Center ASCII horizontally: approx character width is ~5.8px for 9.8px monospace font
    # target_w is 42 chars -> ~243px wide
    # offset_x = (svg_width - 243) / 2 = ~83px
    offset_x = 82

    for idx, line in enumerate(lines):
        y = start_y + idx * line_height
        delay = 0.08 + idx * 0.038
        escaped_line = escape_xml(line)
        svg_lines.append(
            f'    <text class="term-line" x="{offset_x}" y="{y:.1f}" '
            f'style="animation-delay: {delay:.3f}s;">{escaped_line}</text>'
        )

    # Status Bar at bottom (Vim style)
    footer_y = svg_height - 24
    total_lines = len(lines)
    svg_lines.append(f'''  </g>

  <!-- Terminal Status Bar -->
  <g clip-path="url(#asciiFooterClip)">
    <rect class="status-bar" x="0" y="{footer_y}" width="{svg_width}" height="24" />
    <line x1="0" y1="{footer_y}" x2="{svg_width}" y2="{footer_y}" stroke="#30363d" stroke-width="1" />
  </g>

  <g transform="translate(14, {footer_y + 16})">
    <text class="mono status-text" x="0" y="0">
      <tspan class="status-accent">[RENDERED]</tspan> portrait.asc
    </text>
    <text class="mono status-text" x="{svg_width - 28}" y="0" text-anchor="end">
      {total_lines}L, 100% <tspan class="cursor">█</tspan>
    </text>
  </g>
</svg>''')

    os.makedirs(os.path.dirname(output_svg_path), exist_ok=True)
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Generated animated ASCII portrait SVG at {output_svg_path}")

def build_ascii(photo_path: str = DEFAULT_PHOTO):
    # If photo exists locally, convert and save text
    if os.path.exists(photo_path):
        lines = convert_photo_to_ascii(photo_path)
        save_ascii_text(lines)
    elif os.path.exists(ASCII_DATA_PATH):
        print(f"Using existing ASCII text from {ASCII_DATA_PATH}")
        lines = load_ascii_text(ASCII_DATA_PATH)
    else:
        raise FileNotFoundError("Neither source photograph nor ASCII data file exists.")

    generate_ascii_svg(lines)

if __name__ == "__main__":
    photo = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PHOTO
    build_ascii(photo)
