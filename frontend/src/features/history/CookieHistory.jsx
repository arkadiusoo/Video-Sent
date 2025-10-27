import { readHistory } from "../../shared/lib/cookies";
import { useMemo } from "react";
import { useTranslation } from "react-i18next";

export default function CookieHistory({ onRerun }) {
    const { t } = useTranslation();
    const items = useMemo(() => readHistory(), []);

    if (!items.length) return (
        <div className="rounded border p-3">
            <h3 className="font-semibold mb-2">{t("history.title")}</h3>
            <p className="opacity-70">{t("history.empty")}</p>
        </div>
    );

    return (
        <div className="rounded border p-3">
            <h3 className="font-semibold mb-2">{t("history.title")}</h3>
            <ul className="space-y-2">
                {items.map((it, idx) => (
                    <li key={idx} className="flex items-center gap-2 justify-between">
                        <div className="min-w-0">
                            <p className="truncate">{it.url}</p>
                            <p className="text-xs opacity-70">{new Date(it.createdAt).toLocaleString()} • {it.lang.toUpperCase()}</p>
                        </div>
                        <button
                            className="rounded border px-2 py-1 hover:bg-brand-purple/10"
                            onClick={() => onRerun(it.url, it.lang)}
                        >
                            {t("history.rerun")}
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}