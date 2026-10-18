import urllib.request
import re
import os

HANDLE = "Dhanush0058"

def fetch_upstream(theme):
    url = f"https://gh.crafter.run/{HANDLE}?theme={theme}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def extract_stats_lines(raw_svg):
    lines = raw_svg.splitlines()
    stats_lines = []
    for line in lines:
        if line.strip().startswith("<text") and any(k in line for k in [
            "Dhanush0058@github", "Uptime:", "Company:", "Languages:",
            "Contact", "Email:", "Website:", "GitHub:",
            "GitHub Stats", "Repos:", "Forks:", "Commits:", "PRs:", "Top repo:",
            "Last 12 Months", "Contributions:", "Private:", "▄▃"
        ]):
            stats_lines.append(line.strip())
    return stats_lines

def update_card(svg_path, upstream_stats, target_x):
    if not os.path.exists(svg_path):
        return
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find where the stats start in existing card
    # Existing stats start right after </g>\n  <g class="scanner-laser...
    # Up to </svg>
    laser_end_marker = re.search(r'</g>\s*(?=<text[^>]*x="[^"]*"[^>]*y="[^"]*".*?Dhanush0058@github)', content, re.DOTALL)
    if not laser_end_marker:
        return
    
    prefix = content[:laser_end_marker.end()]
    
    # Adjust target_x on upstream stats
    new_stats_formatted = []
    for line in upstream_stats:
        adj_line = re.sub(r'x="[^"]*"', f'x="{target_x}"', line)
        new_stats_formatted.append(f"  {adj_line}")
    
    new_content = f"{prefix}\n" + "\n".join(new_stats_formatted) + "\n</svg>\n"
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {svg_path} with {len(new_stats_formatted)} fresh stats lines.")

def main():
    try:
        dark_raw = fetch_upstream("dark")
        dark_stats = extract_stats_lines(dark_raw)
        if dark_stats:
            update_card("dark_mode.svg", dark_stats, 675)
    except Exception as e:
        print("Warning: failed to refresh dark stats:", e)

    try:
        light_raw = fetch_upstream("light")
        light_stats = extract_stats_lines(light_raw)
        if light_stats:
            update_card("light_mode.svg", light_stats, 580)
    except Exception as e:
        print("Warning: failed to refresh light stats:", e)

if __name__ == "__main__":
    main()
