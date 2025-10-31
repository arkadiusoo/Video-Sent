import os
import tempfile
import yt_dlp

# --- create a temporary folder for this server run ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION_TEMP_DIR = tempfile.mkdtemp(prefix="downloaded_audio_", dir=PROJECT_ROOT)

print(f"[Downloader] Session temporary folder: {SESSION_TEMP_DIR}")

def download_audio(link: str) -> str:
    """
    Downloads audio from a video link, saves it as .wav inside
    a temporary folder valid only for this server run, and
    returns the full path to the saved .wav file.
    """

    print(f"[Downloader] Received link: {link}")
    print(f"[Downloader] Saving to: {SESSION_TEMP_DIR}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(SESSION_TEMP_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    wav_files = [
        os.path.join(SESSION_TEMP_DIR, f)
        for f in os.listdir(SESSION_TEMP_DIR)
        if f.endswith(".wav")
    ]

    if not wav_files:
        raise FileNotFoundError("No .wav file found after download.")

    latest_file = max(wav_files, key=os.path.getctime)
    print(f"[Downloader] File saved: {latest_file}")
    return latest_file
