import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from nlp.analyser import preprocess_data, analyze_sentiments, ASPECTS, NLP

def test_preprocess_detects_aspects():
    text = "Aparat jest świetny. Bateria jest słaba."
    result = preprocess_data(text, "pl")
    
    assert "aparat" in result
    assert "bateria" in result
    assert len(result["aparat"]) == 1
    assert len(result["bateria"]) == 1


def test_preprocess_ignores_missing_aspects():
    text = "Ten telefon jest bardzo dobry, polecam."
    result = preprocess_data(text, "pl")
    
    assert result == {}  # brak aspektów → pusty słownik


def test_preprocess_multiple_sentences_one_aspect():
    text = "Aparat jest super. Kocham aparat w tym telefonie."
    result = preprocess_data(text, "pl")
    
    assert "aparat" in result
    assert len(result["aparat"]) == 2


def test_preprocess_empty_text():
    result = preprocess_data("", "pl")
    assert result == {}

def test_preprocess_correctly_chooses_language():
    text_pl = "Aparat działa dobrze."
    text_en = "The camera works well."
    
    result_pl = preprocess_data(text_pl, "pl")
    result_en = preprocess_data(text_en, "en")
    
    assert "aparat" in result_pl
    assert "camera" in result_en

def test_preprocess_does_not_return_aspect_sentences_for_wrong_language():
    text = "Aparat działa dobrze."
    result = preprocess_data(text, "en")
    
    assert result == {}

    text = "Camera works fine."
    result = preprocess_data(text, "pl")

    assert result == {}

def test_analyze_sentiment_does_not_return_rating_for_unmentioned_aspects():
    text = "Aparat jest świetny. Bateria jest słaba. Ekran jest jasny i wyraźny."
    result = analyze_sentiments(text, "pl")
    assert "aparat" in result
    assert "bateria" in result
    assert "ekran" in result
    assert "wydajność" not in result

