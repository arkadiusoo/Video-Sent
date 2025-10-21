import os

def download_audio(link: str) -> str:
    """
    Pobiera audio z linku i zwraca ścieżkę do pliku .wav
    (MVP: zwraca ścieżkę mockową)
    """
    print(f"[Downloader] Pretend downloading audio from: {link}")
    dummy_path = "/tmp/audio.wav"
    open(dummy_path, "wb").close()
    return dummy_path
