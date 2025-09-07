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

def main():
    parser = argparse.ArgumentParser(description="Study Streak Tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_log = sub.add_parser("log", help="Log today's study subject")
    p_log.add_argument("subject", help="What you studied (e.g., 'calculus')")

    args = parser.parse_args()

    if args.cmd == "log":
        d = log(args.subject)
        print(f"Logged {args.subject!r} for {d}")

if __name__ == "__main__":
    main()
