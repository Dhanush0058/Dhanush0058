import xml.etree.ElementTree as ET
import re

def enhance_dark_mode():
    with open('dark_mode.svg', 'r', encoding='utf-8') as f:
        svg = f.read()

    # Avoid double-enhancing if already enhanced
    if 'portraitClipDark' in svg:
        return

    defs_and_styles = """  <defs>
    <clipPath id="portraitClipDark">
      <rect x="0" y="0" width="530" height="476">
        <animate attributeName="height" from="0" to="476" dur="2.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1" />
      </rect>
    </clipPath>
    <linearGradient id="scannerGlowDark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#58a6ff" stop-opacity="0" />
      <stop offset="85%" stop-color="#58a6ff" stop-opacity="0.15" />
      <stop offset="100%" stop-color="#79c0ff" stop-opacity="0.4" />
    </linearGradient>
  </defs>
  <style>
    @keyframes scanSweepDark {
      0% { transform: translateY(15px); opacity: 0; }
      8% { opacity: 1; }
      88% { opacity: 1; }
      98% { transform: translateY(438px); opacity: 0; }
      100% { transform: translateY(15px); opacity: 0; }
    }
    .scanner-beam-dark {
      animation: scanSweepDark 3.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }
    @keyframes portraitPulse {
      0%, 100% { opacity: 0.95; }
      50% { opacity: 1; }
    }
    #portrait-group-dark {
      animation: portraitPulse 4s ease-in-out infinite;
    }
  </style>"""

    scanner_element = """  <g class="scanner-beam-dark">
    <rect x="30" y="0" width="480" height="26" fill="url(#scannerGlowDark)" />
    <line x1="30" y1="26" x2="510" y2="26" stroke="#58a6ff" stroke-width="2" opacity="0.95" />
    <line x1="30" y1="26" x2="510" y2="26" stroke="#ffffff" stroke-width="0.7" opacity="0.7" />
  </g>"""

    bg_rect_pattern = r'(<rect x="0\.5" y="0\.5"[^>]+/>)'
    svg = re.sub(bg_rect_pattern, r'\1\n' + defs_and_styles, svg, count=1)

    first_ascii = '<text x="28"'
    last_ascii_end = "</text>\n  <text x=\"540\" y=\"43\""
    if first_ascii in svg and last_ascii_end in svg:
        start_idx = svg.find(first_ascii)
        split_idx = svg.find(last_ascii_end)
        split_point = split_idx + len("</text>")

        ascii_block = svg[start_idx:split_point]
        wrapped_ascii = f'  <g id="portrait-group-dark" transform="translate(14, -14) scale(1.18, 1.08)" clip-path="url(#portraitClipDark)">\n{ascii_block}\n  </g>\n{scanner_element}'
        svg = svg[:start_idx] + wrapped_ascii + svg[split_point:]

    with open('dark_mode.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    ET.fromstring(svg)

def enhance_light_mode():
    with open('light_mode.svg', 'r', encoding='utf-8') as f:
        svg = f.read()

    if 'portraitClipLight' in svg:
        return

    defs_and_styles = """  <defs>
    <clipPath id="portraitClipLight">
      <rect x="0" y="0" width="530" height="517">
        <animate attributeName="height" from="0" to="517" dur="2.2s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1" />
      </rect>
    </clipPath>
    <linearGradient id="scannerGlowLight" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0969da" stop-opacity="0" />
      <stop offset="85%" stop-color="#0969da" stop-opacity="0.12" />
      <stop offset="100%" stop-color="#54aeff" stop-opacity="0.35" />
    </linearGradient>
  </defs>
  <style>
    @keyframes scanSweepLight {
      0% { transform: translateY(15px); opacity: 0; }
      8% { opacity: 1; }
      88% { opacity: 1; }
      98% { transform: translateY(480px); opacity: 0; }
      100% { transform: translateY(15px); opacity: 0; }
    }
    .scanner-beam-light {
      animation: scanSweepLight 3.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }
    @keyframes portraitPulseLight {
      0%, 100% { opacity: 0.95; }
      50% { opacity: 1; }
    }
    #portrait-group-light {
      animation: portraitPulseLight 4s ease-in-out infinite;
    }
  </style>"""

    scanner_element = """  <g class="scanner-beam-light">
    <rect x="30" y="0" width="480" height="26" fill="url(#scannerGlowLight)" />
    <line x1="30" y1="26" x2="510" y2="26" stroke="#0969da" stroke-width="2" opacity="0.9" />
    <line x1="30" y1="26" x2="510" y2="26" stroke="#ffffff" stroke-width="0.7" opacity="0.8" />
  </g>"""

    bg_rect_pattern = r'(<rect x="0\.5" y="0\.5"[^>]+/>)'
    svg = re.sub(bg_rect_pattern, r'\1\n' + defs_and_styles, svg, count=1)

    first_ascii = '<text x="28"'
    last_ascii_end = "</text>\n  <text x=\"540\" y=\"63.39999999999998\""
    if first_ascii in svg and last_ascii_end in svg:
        start_idx = svg.find(first_ascii)
        split_idx = svg.find(last_ascii_end)
        split_point = split_idx + len("</text>")

        ascii_block = svg[start_idx:split_point]
        wrapped_ascii = f'  <g id="portrait-group-light" transform="translate(14, -14) scale(1.18, 1.08)" clip-path="url(#portraitClipLight)">\n{ascii_block}\n  </g>\n{scanner_element}'
        svg = svg[:start_idx] + wrapped_ascii + svg[split_point:]

    with open('light_mode.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    ET.fromstring(svg)

if __name__ == '__main__':
    enhance_dark_mode()
    enhance_light_mode()
    print("Enhanced SVGs successfully")
