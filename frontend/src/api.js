import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

export async function analyzeVideo(link) {
  const res = await axios.post(`${API_URL}/analyze`, { link });
  return res.data;
}
