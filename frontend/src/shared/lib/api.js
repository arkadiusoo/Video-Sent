const jobs = new Map();

const API_BASE = "http://127.0.0.1:8080";
const sleep = ms => new Promise(r => setTimeout(r, ms));

function fakeAspects() {
    return [
        { key: "camera", score: "positive"},
        { key: "battery", score: "neutral"},
        { key: "display", score: "negative"},
        { key: "performance", score: "positive"},
    ];
}


async function requestDownloadFromBackend(url) {
    try {
        const res = await fetch(`${API_BASE}/download`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ link: url }),
        });

        if (!res.ok) {
            throw new Error(`Backend responded with ${res.status}`);
        }

        const data = await res.json();
        console.log("[API] /download response:", data);

        if (data.status !== "success") {
            throw new Error(data.message || "Download failed");
        }

        return data; // { status, message, file_path }
    } catch (err) {
        console.error("[API] Download error:", err);
        throw new Error("Failed to download video via backend.");
    }
}


export async function apiStartAnalyze({ url, lang, device }) {

      const downloadResult = await requestDownloadFromBackend(url);
    // in the future: fetch('/api/analyze', { method:'POST', body: JSON.stringify({url, lang}) })
    const jobId = Math.random().toString(36).slice(2);
    (async () => {
        await sleep(1200);
        const aspects = fakeAspects();
        const positives = aspects.filter(a => a.score === "positive").length;
        const negatives = aspects.filter(a => a.score === "negative").length;
        const summary = positives >= negatives ? "positive" : "negative";
        jobs.set(jobId, {
            jobId, url, lang, device: device || null ,summary, aspects, createdAt: new Date().toISOString(), backend: downloadResult
        });
    })();
    return { jobId };
}

export async function apiGetAnalyze(jobId) {
    // in the future: fetch(`/api/analyze/${jobId}`)
    const hit = jobs.get(jobId);
    if (!hit) return { status: "pending" };
    return hit;
}

export async function pollResult(jobId, { intervalMs = 1200, timeoutMs = 15000 } = {}) {
    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
        const res = await apiGetAnalyze(jobId);
        if (res && res.status !== "pending") return res;
        await sleep(intervalMs);
    }
    throw new Error("Timeout");
}