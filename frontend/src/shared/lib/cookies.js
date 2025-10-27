import Cookies from "js-cookie";

const HISTORY_KEY = "vs_history"; // JSON array of {url, lang, createdAt}
export const HISTORY_EVENT = "vs:history-changed";

export function readHistory() {
    const raw = Cookies.get(HISTORY_KEY);
    if (!raw) return [];
    try {
        const arr = JSON.parse(raw);
        return Array.isArray(arr) ? arr.slice(0, 10) : [];
    } catch {
        return [];
    }
}

export function pushHistory(item) {
    const current = readHistory();
    const next = [
        item,...current.filter(i => !(i.url === item.url && i.lang === item.lang && (i.device || null) === (item.device || null)))
    ].slice(0, 10);
    Cookies.set(HISTORY_KEY, JSON.stringify(next), { expires: 30 });
    try {
      window.dispatchEvent(new CustomEvent(HISTORY_EVENT, { detail: { items: next } }));
    } catch (_) {
    }
}