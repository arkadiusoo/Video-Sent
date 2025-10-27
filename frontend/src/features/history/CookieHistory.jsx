import { readHistory, HISTORY_EVENT } from "../../shared/lib/cookies";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

export default function CookieHistory({ onRerun }) {
    const { t } = useTranslation();
    const [items, setItems] = useState(() => readHistory());
    useEffect(() => {
        const onHist = () => setItems(readHistory());
        window.addEventListener(HISTORY_EVENT, onHist);
        return () => window.removeEventListener(HISTORY_EVENT, onHist);
    }, []);

    return (
        <div className="card border-brand">
            <div className="card-body">
                <h3 className="card-title fs-6 mb-3">{t("history.title")}</h3>

                {!items.length ? (
                    <p className="text-body-secondary mb-0">{t("history.empty")}</p>
                ) : (
                    <ul className="list-group">
                        {items.map((it, idx) => (
                            <li key={idx} className="list-group-item d-flex align-items-center justify-content-between">
                                <div className="me-2 text-truncate" style={{ maxWidth: "70%" }}>
                                    <div className="text-truncate">{it.device || t("device.empty")}</div>
                                    <div className="text-truncate">{it.url}</div>
                                    <small className="text-body-secondary">
                                        {new Date(it.createdAt).toLocaleString()} • {it.lang.toUpperCase()}
                                    </small>
                                </div>
                                <button className="btn btn-outline-secondary btn-sm" onClick={() => onRerun(it.url, it.lang, it.device)}>
                                    {t("history.rerun")}
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}