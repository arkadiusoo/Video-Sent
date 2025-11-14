import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

ASPECTS = {"pl": ["aparat", "bateria", "ekran", "wydajność"], "en": ["camera", "battery", "screen", "efficiency"]}
NLP = {"pl": spacy.load("pl_core_news_sm"), "en": spacy.load("en_core_web_sm")}

### Metoda do przetwarzania transkrypcji

def preprocess_data(content: str, lang: str) -> dict:
    # Wybór modelu spacy do wyszukania słów kluczowych w tekście
    nlp = NLP[lang] 
    # Lista aspektów do śledzenia
    aspects = ASPECTS[lang]

    # Tokenizacja tekstu
    doc = nlp(content) 

    # Tworzenie słownika aspektów i odpowiadających im zdań
    aspect_sentences = {}
    for sent in doc.sents:
        for aspect in aspects:
            if aspect.lower() in sent.text.lower():
                aspect_sentences.setdefault(aspect, []).append(sent.text)

    return aspect_sentences

### Metoda do oceny sentyment na poziomie zdania

def sentiment_of_sentence(sentence, tokenizer, model) -> int:
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1) # Ocena prawdopodobieństwa każdej z możliwych ocen
    rating = torch.argmax(probs).item() + 1  # ocena w skali 1-5
    return rating

### Metoda do przetwarzania zdań dla każdego aspektu i uzyskania sentymentu
### Output: słownik z ocenami sentymentu dla każdego aspektu w formacie {aspekt: {"rating": średnia_ocena}}

def process_aspect_sentences(aspect_sentences: dict) -> dict:
    # Model do analizy sentymentu
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    aspect_sentiments = {}
    # Iteracja przez aspekty i ich zdania
    for aspect, sentences in aspect_sentences.items():
        ratings = [sentiment_of_sentence(s, tokenizer, model) for s in sentences]
        # Uzupełnianie średniej oceny dla aspektu
        aspect_sentiments[aspect] = {
            "rating": float(np.mean(ratings))
        }
    print(f"Sentiments: {aspect_sentiments}")
    return aspect_sentiments

### Główna metoda do analizy sentymentu z transkrypcji

def analyze_sentiments(content: str, lang: str) -> dict:
    aspect_sentences = preprocess_data(content, lang)
    print(f"Aspect Sentences: {aspect_sentences}")
    sentiment_list = process_aspect_sentences(aspect_sentences)
    return sentiment_list

'''
file = open("./transcribe_2025-11-14 19_38_05.924528.txt", "r", encoding="utf-8")

# Read the entire content of the file
content = file.read()

sentiments = analyze_sentiments(content, "pl")

'''