"""
Fetch public GitHub contributions for a user and calculate statistics.
Saves data into assets/data/contributions.json.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

DEFAULT_USERNAME = "charangowdamd-cmd"

def parse_tooltip_text(text: str) -> int:
    """Extract number of contributions from tooltip text."""
    if not text or "No contributions" in text:
        return 0
    # Match patterns like '11 contributions on...' or '1 contribution on...'
    match = re.search(r"(\d+)\s+contribution", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0

def fetch_contributions_html(username: str) -> str:
    """Fetch the contributions calendar HTML snippet from GitHub."""
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text

def calculate_streaks(days: list[dict]) -> tuple[int, int]:
    """
    Calculate (current_streak, longest_streak) from an ordered list of days.
    Days are sorted chronologically by date.
    """
    if not days:
        return 0, 0

    sorted_days = sorted(days, key=lambda d: d["date"])
    
    longest_streak = 0
    current_streak = 0
    temp_streak = 0

    for d in sorted_days:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Calculate current streak ending today / latest recorded day
    # Check if latest day or previous day has contributions
    current_streak = 0
    # Traverse backwards from the end
    for d in reversed(sorted_days):
        if d["count"] > 0:
            current_streak += 1
        else:
            # If the very last day (e.g. today) has 0 so far, we might still count yesterday's active streak
            if current_streak == 0 and d == sorted_days[-1]:
                continue
            break

    return current_streak, longest_streak

def extract_contributions_data(html: str, username: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract total contributions from header if available
    h2 = soup.find("h2", class_=lambda c: c and "f4" in c and "text-normal" in c)
    header_total = None
    if h2:
        m = re.search(r"([\d,]+)\s+contribution", h2.text, re.IGNORECASE)
        if m:
            header_total = int(m.group(1).replace(",", ""))

    # Map tooltips by id
    tooltips = {}
    for tt in soup.find_all("tool-tip"):
        target_id = tt.get("for")
        if target_id:
            tooltips[target_id] = tt.text.strip()

    # Find calendar days (GitHub uses td with class ContributionCalendar-day)
    td_days = soup.find_all("td", class_="ContributionCalendar-day")
    if not td_days:
        # Fallback to rect tags if older layout
        td_days = soup.find_all("rect", class_="ContributionCalendar-day")

    raw_days = []
    for el in td_days:
        date_str = el.get("data-date")
        if not date_str:
            continue
        level = int(el.get("data-level", 0))
        el_id = el.get("id", "")
        tt_text = tooltips.get(el_id, "")
        count = parse_tooltip_text(tt_text)
        
        # If count was 0 but level > 0 (fallback in case tooltip wasn't matched)
        if count == 0 and level > 0:
            count = level  # conservative lower bound

        raw_days.append({
            "date": date_str,
            "level": level,
            "count": count,
            "tooltip": tt_text,
        })

    # Sort days chronologically
    raw_days.sort(key=lambda d: d["date"])

    # If we have days, compute total
    calc_total = sum(d["count"] for d in raw_days)
    total_contributions = header_total if (header_total is not None and header_total >= calc_total) else calc_total

    # Streaks
    current_streak, longest_streak = calculate_streaks(raw_days)

    # Active days & peak day
    active_days = sum(1 for d in raw_days if d["count"] > 0)
    peak_day = max(raw_days, key=lambda d: d["count"]) if raw_days else {"date": "", "count": 0}

    # Group into weeks (each week has 7 days: Sun=0 to Sat=6)
    # Align by day of week
    weeks = []
    current_week = []
    
    # To format nicely into 53 columns x 7 rows, we can align days by weekday
    for day in raw_days:
        dt = datetime.strptime(day["date"], "%Y-%m-%d")
        # Python weekday: Monday is 0, Sunday is 6.
        # GitHub calendar starts week on Sunday (weekday 6 -> 0)
        gh_weekday = (dt.weekday() + 1) % 7
        day["weekday"] = gh_weekday
        day["month"] = dt.strftime("%b")

    # Group raw_days into columns of 7 days
    # Fill any leading empty days in the first week
    if raw_days:
        first_day_w = raw_days[0]["weekday"]
        current_week = [None] * first_day_w
        for d in raw_days:
            current_week.append(d)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
        if current_week:
            # Pad with None until Sunday-Saturday is complete
            while len(current_week) < 7:
                current_week.append(None)
            weeks.append(current_week)

    return {
        "username": username,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "active_days": active_days,
        "peak_day": {
            "date": peak_day.get("date"),
            "count": peak_day.get("count", 0),
        },
        "days_count": len(raw_days),
        "weeks_count": len(weeks),
        "weeks": weeks,
    }

def fetch_and_save(username: str = DEFAULT_USERNAME, output_path: str = "assets/data/contributions.json") -> dict:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        print(f"Fetching contribution data for {username}...")
        html = fetch_contributions_html(username)
        data = extract_contributions_data(html, username)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Successfully saved contributions to {output_path}")
        print(f"  Total contributions: {data['total_contributions']}")
        print(f"  Current streak:      {data['current_streak']} days")
        print(f"  Longest streak:      {data['longest_streak']} days")
        print(f"  Active days:         {data['active_days']} days")
        print(f"  Peak day:            {data['peak_day']['date']} ({data['peak_day']['count']} contribs)")
        return data
    except Exception as e:
        print(f"Warning: Failed to fetch live contributions: {e}", file=sys.stderr)
        if os.path.exists(output_path):
            print(f"Loading existing data from {output_path}", file=sys.stderr)
            with open(output_path, "r", encoding="utf-8") as f:
                return json.load(f)
        raise

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USERNAME
    fetch_and_save(user)
