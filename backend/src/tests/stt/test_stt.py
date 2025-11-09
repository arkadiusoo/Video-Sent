# python -m pytest -v -s

#docker exec -it video-sent-backend-1 bash
#pytest -v tests
#pytest -v -s tests

import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from stt.service import transcribe_audio
from downloader.service import download_audio
from difflib import SequenceMatcher
import time
from pydub import AudioSegment

# 🔹 PRZYKŁADOWE PLIKI TESTOWE
AUDIO_ENG = "tests/stt/eng.wav"
AUDIO_PL = "tests/stt/pl.wav"

REFERENCE_ENG = (
    "There’s something magical about the way the seasons change. Spring arrives first, bringing fresh air and the scent of flowers after months of grey. Trees come alive again, and everything feels new and full of promise. Then comes summer — warm, bright, and full of energy. People spend more time outside, the days seem endless, and the sunsets paint the sky in gold. When autumn follows, the world slows down. Leaves turn red and orange, the air feels crisp, and the rhythm of life becomes calmer. Finally, winter wraps the earth in quiet. It’s a time for reflection, warm drinks, and cozy evenings indoors. Each season has its own beauty, its own rhythm — a reminder that change is natural, and every moment in time has something special to offer."
)
REFERENCE_PL = (
    "Jest coś niezwykłego w tym, jak zmieniają się pory roku. Najpierw przychodzi wiosna — świeże powietrze, zapach kwiatów i pierwsze promienie słońca po długich, szarych miesiącach. Drzewa budzą się do życia, a świat nabiera kolorów i nadziei. Potem nadchodzi lato — ciepłe, pełne światła i energii. Dni są długie, ludzie spędzają więcej czasu na zewnątrz, a zachody słońca zamieniają niebo w złoty obraz. Jesienią tempo życia zwalnia. Liście stają się czerwone i pomarańczowe, powietrze jest chłodniejsze, a wokół panuje spokojniejszy nastrój. W końcu nadchodzi zima — cicha, pełna refleksji i domowego ciepła. Każda pora roku ma swój rytm i swoje piękno — przypomnienie, że zmiany są naturalne, a każda chwila warta jest zauważenia."
)

def similarity(a: str, b: str) -> float:
    """Prosty współczynnik podobieństwa (0–100%)."""
    return round(SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100, 2)


# =====================================================
# TESTY FUNKCJI transcribe_audio
# =====================================================

@pytest.mark.parametrize(
    "audio_path,lang,reference,min_acc",
    [
        (AUDIO_ENG, "en", REFERENCE_ENG, 90),
        (AUDIO_PL,  "pl", REFERENCE_PL,  90),
    ],
    ids=["en", "pl"],
)
def test_whisper_transcription(audio_path, lang, reference, min_acc):
    """Test działania Whispera dla angielskiego i polskiego."""
    start = time.time()
    result = transcribe_audio(audio_path, lang)
    elapsed = round(time.time() - start, 2)

    assert isinstance(result, str)
    assert len(result.strip()) > 0

    acc = similarity(result, reference)
    print(f"\n[{lang.upper()}] Accuracy: {acc}% | Time: {elapsed}s")
    assert acc >= min_acc, f"Zbyt niska dokładność: {acc}% (< {min_acc}%)"

def test_whisper_returns_text_without_newlines():
    """Transkrypt nie powinien zawierać \n ani \t."""
    result = transcribe_audio(AUDIO_ENG, "en")
    assert "\n" not in result
    assert "\t" not in result

@pytest.mark.parametrize(
    "audio_path,lang",
    [
        (AUDIO_ENG, "en"),
        (AUDIO_PL,  "pl"),
    ],
    ids=["en", "pl"],
)
def test_whisper_speed_benchmark(audio_path, lang):
    """Test wydajności — nie powinien trwać dłużej niż długość nagrania"""
    audio = AudioSegment.from_file(audio_path)
    duration_seconds = audio.duration_seconds

    start = time.time()
    _ = transcribe_audio(audio_path, lang)
    duration = round(time.time() - start, 2)
    assert duration < duration_seconds, f"Transkrypcja trwała zbyt długo: {duration}s, powinna max: {duration_seconds/2}s"

def test_transcribe_audio_invalid_language_real():
    """Nieobsługiwany język powinien powodować błąd."""
    with pytest.raises(KeyError):
        transcribe_audio(AUDIO_ENG, "de")

def test_transcribe_audio_missing_file():
    """Brak pliku powinien zwracać błąd FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        transcribe_audio("nonexistent.wav", "en")

def test_transcribe_audio_text_is_sentence_like():
    """Transkrypt powinien wyglądać jak zdania (min. 5 słów)."""
    result = transcribe_audio(AUDIO_PL, "pl")
    words = result.split()
    assert len(words) >= 5
    assert result[0].isupper()

@pytest.mark.parametrize(
    "audio_path,lang",
    [
        (AUDIO_ENG, "en"),
        (AUDIO_PL,  "pl"),
    ],
    ids=["en", "pl"],
)
def test_transcribe_audio_consistency_between_runs(audio_path,lang):
    """Powinien dawać podobne wyniki dla tego samego audio."""
    res1 = transcribe_audio(audio_path, lang)
    res2 = transcribe_audio(audio_path, lang)
    acc = similarity(res1, res2)
    assert acc > 90, f"Niestabilna transkrypcja ({acc}%)"

# =====================================================
# TESTY INTEGRACYJNE downloader stt
# =====================================================
LINK_ENG = "https://www.youtube.com/shorts/0SaQjC7o7iA"
LINK_PL = "https://www.youtube.com/shorts/2naDMd6VlyE"

REFERENCE_ENG_integration = """So here it is. The brand new Galaxy S25. Not a big difference compared to the previous model. It is 6 grams lighter and you can kind of feel it if you're holding both. You have a faster processor inside. The same battery size, same cameras that displays kind of equal, but it could do better upscaling. And look, I'm going to review it, but do you want me to compare it to any other phones?"""
REFERENCE_PL_integration = """Trzy miesiące temu zadebiutował Samsung S24. Czy warto było czekać na ten telefon? Nowy flagowiec ma odrobinę większy ekran i nową, aluminiową ramkę o bardziej płaskim profilu i matowym wykończeniu. Wyniki wydajnościowe potwierdziły, że w codziennym użytkowaniu praktycznie nie zobaczycie wyraźnej różnicy względem poprzednika, również w kwestii osiąganych temperatur. Ekran doczekał się wsparcia technologią LTPO i oferuje nominalnie większą jasność w szczycie, ale jest to różnica trudna do zarejestrowania ludzkim okiem. Tutejsze aparaty są praktycznie te samo od lat. Trzeci rok z rzędu dostajemy ten sam zestaw z 10-megapixelowym tele i 12-megapixelowym szerokim kontem. Plusem natomiast jest wsparcie siedmioma latami aktualizacji systemu. Jeśli S24 stanieje, a ty będziesz rozważać przesiadkę na przykład Samsunga S10e, to będzie to dobra decyzja. Ale zakup S23 da ci praktycznie te same wrażenia, no i będzie tańszy. Nawet jak S24 stanieje, a ty będziesz mieć w tym czasie nadal S23, to lepiej odłóż te pieniądze na gorsze czasy."""

@pytest.mark.parametrize(
    "link,lang,reference",
    [
        (LINK_ENG, "en", REFERENCE_ENG_integration),
        (LINK_PL,  "pl", REFERENCE_PL_integration),
    ],
    ids=["en", "pl"],
)
def test_integration_test_downloader_stt(link, lang, reference):
    """Test integracyjny: pobieranie i transkrypcja audio."""
    audio_path = download_audio(link)
    result = transcribe_audio(audio_path, lang)

    acc = similarity(result, reference)
    assert acc >= 90, f"Zbyt niska dokładność: {acc}% (< 90%)"