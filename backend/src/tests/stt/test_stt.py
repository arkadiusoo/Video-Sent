# python -m pytest -v -s

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
AUDIO_ENG = "stt/eng.wav"
AUDIO_PL = "stt/pl.wav"

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
    """Test wydajności — nie powinien trwać dłużej niż połowa długości nagrania"""
    audio = AudioSegment.from_file(audio_path)
    duration_seconds = audio.duration_seconds

    start = time.time()
    _ = transcribe_audio(audio_path, lang)
    duration = round(time.time() - start, 2)
    assert duration < duration_seconds/2, f"Transkrypcja trwała zbyt długo: {duration}s, powinna max: {duration_seconds/2}s"

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
'''LINK_ENG = "https://www.youtube.com/watch?v=KUaQgRiJukA"
LINK_PL = "https://www.youtube.com/watch?v=sOGEyuIttXY"

REFERENCE_ENG_integration = """Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference."""
REFERENCE_PL_integration = """Nic dwa razy się nie zdarza
i nie zdarzy. Z tej przyczyny
zrodziliśmy się bez wprawy
i pomrzemy bez rutyny.

Choćbyśmy uczniami byli
najlepszymi w szkole świata,
nie będziemy repetować
żadnej zimy ani lata.

Żaden dzień się nie powtórzy,
nie ma dwóch podobnych nocy,
dwóch tych samych pocałunków,
dwóch jednakich spojrzeń w oczy.

Wczoraj, kiedy twoje imię
ktoś wymówił przez mnie głośno,
tak mi było, jakby róża
przez otwarte wpadła okno.

Dziś, kiedy jesteśmy razem,
odwróciłam twarz ku ścianie.
Róża? Jak wygląda róża?
Czy to kwiat? A może kamień?

Czemu ty się, zła godzino,
z niepotrzebnym mieszasz lękiem?
Jesteś – a więc musisz minąć.
Miniesz – a więc to jest piękne.

Uśmiechnięci, wpółobjęci
spróbujemy szukać zgody,
choć różnimy się od siebie
jak dwie krople czystej wody.
"""

@pytest.mark.parametrize(
    "audio_path,lang,reference",
    [
        (LINK_ENG, "en", REFERENCE_ENG_integration),
        (LINK_PL,  "pl", REFERENCE_PL_integration),
    ],
    ids=["en", "pl"],
)
def integration_test_downloader_stt(link, lang, reference):
    """Test integracyjny: pobieranie i transkrypcja audio."""
    audio_path = download_audio(link)
    result = transcribe_audio(audio_path, lang)

    acc = similarity(result, reference)
    assert acc >= 90, f"Zbyt niska dokładność: {acc}% (< 90%)"'''