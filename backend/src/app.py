from flask import Flask, request, jsonify
from flask_cors import CORS
from downloader.service import download_audio
from stt.service import transcribe_audio
from nlp.service import analyze_sentiment

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost:51731",
        "http://127.0.0.1:51731"
    ]}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"],
    supports_credentials=False
)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    link = data.get("link")
    if not link:
        return jsonify({"error": "Missing 'link' field"}), 400
    language = data.get("language")
    if not language:
        return jsonify({"error": "Missing 'language' field"}), 400

    audio_path = download_audio(link)
    transcript = transcribe_audio(audio_path, language)
    sentiment = analyze_sentiment(transcript)

    return jsonify({
        "link": link,
        "transcript": transcript,
        "sentiment": sentiment
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
