from pathlib import Path
import json
import app

def test_log_writes_to_json(tmp_path, monkeypatch):
    # redirect the data path into a temp folder so tests don't touch real files
    monkeypatch.setattr(app, "DATA_PATH", tmp_path / "streak_data.json")

    day = app.log("calculus")

    # file created?
    assert app.DATA_PATH.exists()

    data = json.loads(Path(app.DATA_PATH).read_text())
    assert data["logs"][0]["subject"] == "calculus"
    assert data["logs"][0]["date"] == day
