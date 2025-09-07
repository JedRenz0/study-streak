from pathlib import Path
import json
import app

def test_stats_calculates_days_and_streak(tmp_path, monkeypatch):
    # Redirect to a temporary file for safety
    monkeypatch.setattr(app, "DATA_PATH", tmp_path / "streak_data.json")

    # Create fake data with gaps
    fake_data = {
        "logs": [
            {"date": "2025-09-01", "subject": "calculus"},
            {"date": "2025-09-02", "subject": "physics"},
            {"date": "2025-09-04", "subject": "programming"},
            {"date": "2025-09-05", "subject": "biology"},
        ]
    }

    # Save fake data
    Path(app.DATA_PATH).write_text(json.dumps(fake_data))

    # Run stats()
    result = app.stats()

    assert result["days"] == 4          # 4 unique days
    assert result["streak"] == 2        # Best streak = 2 consecutive days (Sep 1-2)
