import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { z } from "zod";

const urlSchema = z.string().url();

export default function UrlForm({ onSubmit, loading, prefill }) {
    const { t } = useTranslation();
    const [url, setUrl] = useState("");
    const [lang, setLang] = useState("pl");
    const [device, setDevice] = useState("");
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!prefill) return;
        if (typeof prefill.url !== "undefined") setUrl(prefill.url || "");
        if (typeof prefill.lang !== "undefined") setLang(prefill.lang || "pl");
        if (typeof prefill.device !== "undefined") setDevice(prefill.device || "");
        setError(null);
    }, [prefill]);

    const validate = () => {
        if (!url.trim()) return t("form.errors.required");
        const ok = urlSchema.safeParse(url).success;
        return ok ? null : t("form.errors.invalid");
    };

    const handleBlur = () => setError(validate());

    const handleSubmit = async (e) => {
        e.preventDefault();
        const err = validate();
        setError(err);
        if (!err) await onSubmit({ url, lang, device });
    };

    return (
        <form onSubmit={handleSubmit} aria-label="Analyze form" className="mb-3">
            <div className="mb-3">
                <label htmlFor="url" className="form-label fw-medium">{t("form.urlLabel")}</label>
                <input
                    id="url"
                    name="url"
                    aria-invalid={!!error}
                    aria-describedby={error ? "url-err" : undefined}
                    className={`form-control ${error ? "is-invalid" : ""}`}
                    placeholder={t("form.placeholder")}
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    onBlur={handleBlur}
                />
                {error && <div id="url-err" className="invalid-feedback">{error}</div>}
            </div>

            <div className="mb-3">
                <label htmlFor="device" className="form-label fw-medium">{t("form.deviceLabel")}</label>
                <input
                    id="device"
                    name="device"
                    className="form-control"
                    placeholder={t("form.devicePlaceholder")}
                    value={device}
                    onChange={(e) => setDevice(e.target.value)}
                />
                <div className="form-text">{t("form.deviceHelp")}</div>
            </div>

            <div className="row g-2 align-items-center">
                <div className="col-auto">
                    <span id="lang-label" className="col-form-label fw-medium">{t("form.langLabel")}</span>
                </div>
                <div className="col-auto">
                    <div role="group" aria-labelledby="lang-label">
                        <div className="form-check form-check-inline">
                            <input
                                className="form-check-input"
                                type="radio"
                                name="lang"
                                id="lang-pl"
                                value="pl"
                                checked={lang === "pl"}
                                onChange={(e) => setLang(e.target.value)}
                            />
                            <label className="form-check-label" htmlFor="lang-pl">
                                {t("lang.pl")}
                            </label>
                        </div>
                        <div className="form-check form-check-inline">
                            <input
                                className="form-check-input"
                                type="radio"
                                name="lang"
                                id="lang-en"
                                value="en"
                                checked={lang === "en"}
                                onChange={(e) => setLang(e.target.value)}
                            />
                            <label className="form-check-label" htmlFor="lang-en">
                                {t("lang.en")}
                            </label>
                        </div>
                    </div>
                </div>

            </div>
            <div className="col ms-auto">
                <button type="submit" disabled={loading} className="btn btn-brand w-100">
                    {t("form.analyze")}
                </button>
            </div>

            <div aria-live="polite" className="form-text mt-2">
                {loading ? t("state.loading") : null}
            </div>
        </form>
    );
}