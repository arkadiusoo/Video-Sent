CREATE TABLE IF NOT EXISTS results (
  id SERIAL PRIMARY KEY,
  video_url TEXT,
  transcript TEXT,
  sentiment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
