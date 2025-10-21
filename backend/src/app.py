from flask import Flask, request, jsonify
from downloader.service import download_audio
from stt.service import transcribe_audio
from nlp.service import analyze_sentiment

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    link = data.get("link")
    if not link:
        return jsonify({"error": "Missing 'link' field"}), 400

    audio_path = download_audio(link)
    transcript = transcribe_audio(audio_path)
    sentiment = analyze_sentiment(transcript)

    return jsonify({
        "link": link,
        "transcript": transcript,
        "sentiment": sentiment
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
