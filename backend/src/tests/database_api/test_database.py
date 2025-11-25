import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app import app, save_video_analysis


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class DummyCursor:
    def __init__(self, row=None, should_raise=False):
        self.row = row
        self.should_raise = should_raise
        self.executed_query = None
        self.executed_params = None

    def execute(self, query, params):
        self.executed_query = query
        self.executed_params = params
        if self.should_raise:
            raise Exception("DB error")

    def fetchone(self):
        return self.row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


class DummyConnection:
    def __init__(self, row=None, should_raise=False):
        self.cursor_obj = DummyCursor(row=row, should_raise=should_raise)

    def cursor(self, cursor_factory=None):
        return self.cursor_obj

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


def test_video_stats_by_link_success(client, monkeypatch):
    row = {
        "video_url": "https://example.com/video",
        "analyses_count": 3,
        "avg_camera_score": 8.5,
        "avg_battery_score": 7.0,
        "avg_screen_score": 9.0,
        "avg_performance_score": 8.0,
        "avg_general_score": 8.125,
        "avg_download_time_seconds": 1.23,
        "avg_transcription_time_seconds": 4.56,
        "avg_analysis_time_seconds": 0.78,
        "first_analysis_timestamp": "2025-01-01T12:00:00",
        "last_analysis_timestamp": "2025-01-02T15:30:00",
    }

    conn = DummyConnection(row=row)

    def fake_get_db_connection():
        return conn

    monkeypatch.setattr("app.get_db_connection", fake_get_db_connection)

    link = row["video_url"]
    resp = client.get(f"/video-stats/by-link?link={link}")

    assert resp.status_code == 200
    data = resp.get_json()

    for key, value in row.items():
        assert data[key] == value

    assert conn.cursor_obj.executed_params == (link,)


def test_save_video_analysis_inserts_and_returns_id(monkeypatch):
    row = (123,)  # id nowego rekordu
    conn = DummyConnection(row=row)

    def fake_get_db_connection():
        return conn

    monkeypatch.setattr("app.get_db_connection", fake_get_db_connection)

    kwargs = dict(
        title="Test title",
        video_url="https://example.com/video",
        video_length_seconds=123.456,
        device="Test device",
        camera_score=8.0,
        battery_score=7.0,
        screen_score=9.0,
        performance_score=6.5,
        general_score=7.625,
        video_language="pl",
        download_time_seconds=1.23,
        transcription_time_seconds=4.56,
        analysis_time_seconds=0.78,
    )

    new_id = save_video_analysis(**kwargs)

    assert new_id == 123

    executed_query = conn.cursor_obj.executed_query
    executed_params = conn.cursor_obj.executed_params

    assert "INSERT INTO videosent.video_analysis" in executed_query

    assert executed_params == (
        kwargs["title"],
        kwargs["video_url"],
        kwargs["video_length_seconds"],
        kwargs["device"],
        kwargs["camera_score"],
        kwargs["battery_score"],
        kwargs["screen_score"],
        kwargs["performance_score"],
        kwargs["general_score"],
        kwargs["video_language"],
        kwargs["download_time_seconds"],
        kwargs["transcription_time_seconds"],
        kwargs["analysis_time_seconds"],
    )
