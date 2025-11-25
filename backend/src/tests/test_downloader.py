import os
from unittest.mock import MagicMock

from downloader.service import download_audio, SESSION_TEMP_DIR
import pytest


def test_download_youtube_audio():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    path = download_audio(url)
    assert os.path.exists(path)
    assert path.endswith(".wav")
def test_download_audio_valid(monkeypatch):
    """Test happy-path with mock download producing a .wav file"""

    # --- mock yt_dlp ---
    mock_dl = MagicMock()
    mock_dl.download.return_value = None

    # mocking YoutubeDL object
    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = mock_dl
    mock_ctx.__exit__.return_value = None

    monkeypatch.setattr("downloader.service.yt_dlp.YoutubeDL", lambda opts: mock_ctx)

    # Create fake wav file
    fname = os.path.join(SESSION_TEMP_DIR, "test.wav")
    with open(fname, "wb") as f:
        f.write(b"FAKE DATA")

    result = download_audio("https://youtube.com/watch?v=abc123")

    assert result.endswith(".wav")
    assert os.path.exists(result)


def test_download_audio_invalid_link(monkeypatch):
    """Test that invalid link triggers an exception."""
    mock_dl = MagicMock()
    mock_dl.download.side_effect = Exception("Bad URL")

    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = mock_dl
    monkeypatch.setattr("downloader.service.yt_dlp.YoutubeDL", lambda opts: mock_ctx)

    with pytest.raises(Exception):
        download_audio("https://youtube.com/watch?v=INVALID")


def test_download_audio_no_file(monkeypatch):
    """Test when yt_dlp succeeds but wav file is not created"""
    mock_dl = MagicMock()
    mock_dl.download.return_value = None

    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = mock_dl
    monkeypatch.setattr("downloader.service.yt_dlp.YoutubeDL", lambda opts: mock_ctx)

    # Ensure folder is empty
    for f in os.listdir(SESSION_TEMP_DIR):
        os.remove(os.path.join(SESSION_TEMP_DIR, f))

    with pytest.raises(FileNotFoundError):
        download_audio("https://youtube.com/watch?v=123")
