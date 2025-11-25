from flask import Flask, request, jsonify
from flask_cors import CORS
from downloader.service import download_audio
from stt.service import transcribe_audio
from nlp.service import analyze_sentiment
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "videosent"),
        user=os.getenv("DB_USER", "videosent"),
        password=os.getenv("DB_PASSWORD", "videosent"),
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
    )

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

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


@app.route("/video-stats/<int:analysis_id>", methods=["GET"])
def get_video_stats(analysis_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM videosent.video_analysis
                    WHERE id = %s
                    """,
                    (analysis_id,),
                )
                row = cur.fetchone()

        if row is None:
            return jsonify({
                "error": "Analysis not found",
                "id": analysis_id
            }), 404

        return jsonify(row), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/video-stats/by-link", methods=["GET"])
def get_video_stats_by_link():
    link = request.args.get("link")
    if not link:
        return jsonify({"error": "Missing 'link' query parameter"}), 400

    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT
                        video_url,
                        COUNT(*)           AS analyses_count,

                        AVG(camera_score)      AS avg_camera_score,
                        AVG(battery_score)     AS avg_battery_score,
                        AVG(screen_score)      AS avg_screen_score,
                        AVG(performance_score) AS avg_performance_score,
                        AVG(general_score)     AS avg_general_score,

                        AVG(download_time_seconds)      AS avg_download_time_seconds,
                        AVG(transcription_time_seconds) AS avg_transcription_time_seconds,
                        AVG(analysis_time_seconds)      AS avg_analysis_time_seconds,

                        MIN(analysis_creation_timestamp) AS first_analysis_timestamp,
                        MAX(analysis_creation_timestamp) AS last_analysis_timestamp
                    FROM videosent.video_analysis
                    WHERE video_url = %s
                    GROUP BY video_url
                    """,
                    (link,),
                )
                row = cur.fetchone()

        if row is None:
            return jsonify({
                "error": "No analyses found for given link",
                "link": link
            }), 404

        return jsonify(row), 200

    except Exception:
        return jsonify({"error": "Internal server error"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
