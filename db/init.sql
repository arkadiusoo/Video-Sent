CREATE SCHEMA IF NOT EXISTS videosent;

CREATE TABLE IF NOT EXISTS videosent.video_analysis (
    id BIGSERIAL PRIMARY KEY,

    title TEXT NOT NULL,
    video_url TEXT NOT NULL CHECK (video_url ~ '^https?://'),
    video_length_seconds NUMERIC(10,3) NOT NULL CHECK (video_length_seconds > 0),
    device TEXT,

    camera_score NUMERIC(4,2) NOT NULL CHECK (camera_score BETWEEN 0 AND 10),
    battery_score NUMERIC(4,2) NOT NULL CHECK (battery_score BETWEEN 0 AND 10),
    screen_score NUMERIC(4,2) NOT NULL CHECK (screen_score BETWEEN 0 AND 10),
    performance_score NUMERIC(4,2) NOT NULL CHECK (performance_score BETWEEN 0 AND 10),
    general_score NUMERIC(4,2) NOT NULL CHECK (general_score BETWEEN 0 AND 10),

    video_language VARCHAR(2) NOT NULL CHECK (video_language IN ('pl', 'en')),

    analysis_creation_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    download_time_seconds NUMERIC(10,3) NOT NULL CHECK (download_time_seconds >= 0),
    transcription_time_seconds NUMERIC(10,3) NOT NULL CHECK (transcription_time_seconds >= 0),
    analysis_time_seconds NUMERIC(10,3) NOT NULL CHECK (analysis_time_seconds >= 0)
);

CREATE INDEX IF NOT EXISTS idx_video_analysis_device
    ON videosent.video_analysis (device);

CREATE INDEX IF NOT EXISTS idx_video_analysis_language
    ON videosent.video_analysis (video_language);

CREATE INDEX IF NOT EXISTS idx_video_analysis_created_at
    ON videosent.video_analysis (analysis_creation_timestamp DESC);

INSERT INTO videosent.video_analysis
(title, video_url, video_length_seconds, device, camera_score, battery_score, screen_score, performance_score, general_score,
 video_language, download_time_seconds, transcription_time_seconds, analysis_time_seconds)
VALUES
('Review: XYZ Phone', 'https://www.youtube.com/watch?v=abcd1234', 1023.45, 'XYZ Phone', 8.5, 7.0, 9.0, 8.0, 8.0, 'en', 4.210, 28.330, 3.950);
