from flask import Flask, request, jsonify
from flask_cors import CORS
from downloader.service import download_audio
from stt.service import transcribe_audio
from nlp.service import analyze_sentiment

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:51731"]}})

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

# Temporary, for testing download module
@app.route("/download", methods=["POST"])
def download_only():
    data = request.get_json()
    link = data.get("link")

    if not link:
        return jsonify({"status": "error", "message": "Missing 'link' field"}), 400

    try:
        file_path = download_audio(link)
        return jsonify({
            "status": "success",
            "message": f"Video successfully downloaded.",
            "file_path": file_path
        })
    except Exception as e:
        print("[Downloader] Error:", e)
        return jsonify({
            "status": "error",
            "message": f"Failed to download video: {str(e)}"
        }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
