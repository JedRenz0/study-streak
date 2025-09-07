from pathlib import Path
import json
import app

def test_list_returns_logs_sorted_desc(tmp_path, monkeypatch):
    # use a temp data file
    monkeypatch.setattr(app, "DATA_PATH", tmp_path / "streak_data.json")

    # seed fake data (unsorted)
    fake = {
        "logs": [
            {"date": "2025-09-01", "subject": "calculus"},
            {"date": "2025-09-03", "subject": "physics"},
            {"date": "2025-09-02", "subject": "programming"},
        ]
    }
    Path(app.DATA_PATH).write_text(json.dumps(fake))

    items = app.list_logs()
    # should be newest first (desc by date)
    assert [i["date"] for i in items] == ["2025-09-03", "2025-09-02", "2025-09-01"]
    assert items[0]["subject"] == "physics"
