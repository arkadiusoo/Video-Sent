import warnings

# 🔇 Wyłącz wszystkie ostrzeżenia, które nie są istotne dla testów
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg")
warnings.filterwarnings("ignore", message=".*audioop.*")

# Możesz też dodać coś takiego, jeśli chcesz mieć 100% ciszę:
# import pytest
# @pytest.fixture(autouse=True)
# def silence_warnings():
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore")
#         yield
