from flask import Flask, request, jsonify
from flask_cors import CORS
from downloader.service import download_audio
from stt.service import transcribe_audio
from nlp.analyser import analyse_sentiments
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import numpy as np
from pydub import AudioSegment
import traceback

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "videosent"),
        user=os.getenv("DB_USER", "videosent"),
        password=os.getenv("DB_PASSWORD", "videosent"),
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
    )

def save_video_analysis(
        *,
        title: str,
        video_url: str,
        video_length_seconds: float,
        device: str,
        camera_score: float,
        battery_score: float,
        screen_score: float,
        performance_score: float,
        general_score: float,
        video_language: str,
        download_time_seconds: float,
        transcription_time_seconds: float,
        analysis_time_seconds: float,
        ) -> int:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO videosent.video_analysis (
                title,
                video_url,
                video_length_seconds,
                device,
                camera_score,
                battery_score,
                screen_score,
                performance_score,
                general_score,
                video_language,
                download_time_seconds,
                transcription_time_seconds,
                analysis_time_seconds
                )
                VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
                )
                RETURNING id
                """,
                (
                    title,
                    video_url,
                    video_length_seconds,
                    device,
                    camera_score,
                    battery_score,
                    screen_score,
                    performance_score,
                    general_score,
                    video_language,
                    download_time_seconds,
                    transcription_time_seconds,
                    analysis_time_seconds,
                ),
            )
            new_id = cur.fetchone()[0]
    return new_id

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}

    link = data.get("link")
    if not link:
        return jsonify({"error": "Missing 'link' field"}), 400

    language = data.get("language")
    if not language:
        return jsonify({"error": "Missing 'language' field"}), 400

    if language not in ("pl", "en"):
        return jsonify({"error": "Invalid 'language', expected 'pl' or 'en'"}), 400

    try:
        start_download = time.time()
        audio_path = download_audio(link)
        download_time_seconds = round(time.time() - start_download, 3)

        start_transcription = time.time()
        transcript = transcribe_audio(audio_path, language)
        transcription_time_seconds = round(time.time() - start_transcription, 3)

        start_analysis = time.time()
        sentiment = analyse_sentiments(transcript, language)
        analysis_time_seconds = round(time.time() - start_analysis, 3)

        camera_score = sentiment.get("aparat", sentiment.get("camera", {})).get("rating")
        battery_score = sentiment.get("bateria", sentiment.get("battery", {})).get("rating")
        screen_score = sentiment.get("ekran", sentiment.get("screen", {})).get("rating")
        performance_score = sentiment.get("wydajność", sentiment.get("efficiency", {})).get("rating")

        scores = [camera_score, battery_score, screen_score, performance_score]
        valid_scores = [s for s in scores if s is not None]

        if valid_scores:
            general_score = sum(valid_scores) / len(valid_scores)
        else:
            general_score = None

        audio = AudioSegment.from_file(audio_path)
        video_length_seconds = round(audio.duration_seconds, 3)

        base_name = os.path.basename(audio_path)
        title, _ = os.path.splitext(base_name)

        analysis_id = save_video_analysis(
            title=title,
            video_url=link,
            video_length_seconds=video_length_seconds,
            device=None,
            camera_score=camera_score,
            battery_score=battery_score,
            screen_score=screen_score,
            performance_score=performance_score,
            general_score=general_score,
            video_language=language,
            download_time_seconds=download_time_seconds,
            transcription_time_seconds=transcription_time_seconds,
            analysis_time_seconds=analysis_time_seconds,
        )

        return jsonify({
            "link": link,
            "transcript": transcript,
            "sentiment": sentiment,
            "analysis_id": analysis_id
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


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
