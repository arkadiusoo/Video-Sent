from faster_whisper import WhisperModel
import torch

# Wybór urządzenia (CPU / GPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

WHISPER_MODELS = {
    "en": WhisperModel("base", device=DEVICE),   # Szybszy, wystarczająco dokładny dla EN
    "pl": WhisperModel("small", device=DEVICE)    # Dokładniejszy dla polskiego
}

def transcribe_audio(audio_path: str, language: str) -> str:
    """
    Transkrybuje audio do tekstu
    Używa odpowiedniego modelu Whisper w zależności od języka (pl/en).

    Args:
        audio (str): ścieżka do pliku audio (wav/mp3)
        language (str): 'pl' lub 'eng'

    Returns:
        str: tekst transkrypcji
    """
    # Wybór modelu
    model = WHISPER_MODELS[language]

    # Transkrypcja
    segments, _ = model.transcribe(audio_path, language=language)
    text = " ".join([seg.text.strip() for seg in segments])

    return text
