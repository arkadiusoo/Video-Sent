def analyze_sentiment(text: str) -> str:
    """
    Analizuje sentyment tekstu
    (MVP: prosta reguła keywordowa)
    """
    lower = text.lower()
    if "good" in lower or "great" in lower:
        return "positive"
    elif "bad" in lower or "terrible" in lower:
        return "negative"
    return "neutral"
