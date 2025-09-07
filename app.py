from datetime import date
from pathlib import Path
import json
import argparse

# Where we store logs
DATA_PATH = Path("streak_data.json")

def _load():
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text())
    return {"logs": []}

def _save(data):
    DATA_PATH.write_text(json.dumps(data, indent=2))

def log(subject: str) -> str:
    """Append today's {date, subject} to the log and return the date string."""
    data = _load()
    today = str(date.today())
    data["logs"].append({"date": today, "subject": subject})
    _save(data)
    return today

def stats():
    """Return a dict with total unique study days and longest consecutive streak."""
    data = _load()
    by_day = {}

    # Count study sessions per day
    for entry in data["logs"]:
        by_day.setdefault(entry["date"], 0)
        by_day[entry["date"]] += 1

    if not by_day:
        return {"days": 0, "streak": 0}

    # Sort days in ascending order
    all_days = sorted(by_day.keys())

    from datetime import datetime, timedelta

    def to_dt(s): 
        return datetime.fromisoformat(s).date()

    streak = best = 1
    for i in range(1, len(all_days)):
        if to_dt(all_days[i]) == to_dt(all_days[i-1]) + timedelta(days=1):
            streak += 1
            best = max(best, streak)
        else:
            streak = 1

    return {"days": len(by_day), "streak": best}


def main():
    parser = argparse.ArgumentParser(description="Study Streak Tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # log <subject>
    p_log = sub.add_parser("log", help="Log today's study subject")
    p_log.add_argument("subject", help="What you studied (e.g., 'calculus')")

    # stats
    sub.add_parser("stats", help="Show total days studied and longest streak")

    args = parser.parse_args()

    if args.cmd == "log":
        d = log(args.subject)
        print(f"Logged {args.subject!r} for {d}")
    elif args.cmd == "stats":
        s = stats()
        print(f"Days logged: {s['days']} | Best streak: {s['streak']}")

    


if __name__ == "__main__":
    main()
