import { useState } from "react";
import { useTranslation } from "react-i18next";
import { z } from "zod";

const urlSchema = z.string().url();

export default function UrlForm({ onSubmit, loading }) {
    const { t } = useTranslation();
    const [url, setUrl] = useState("");
    const [lang, setLang] = useState("pl");
    const [error, setError] = useState(null);

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
        if (!err) await onSubmit({ url, lang });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-3" aria-label="Analyze form">
            <div className="flex flex-col gap-2">
                <label htmlFor="url" className="font-medium">{t("form.urlLabel")}</label>
                <input
                    id="url"
                    name="url"
                    aria-invalid={!!error}
                    aria-describedby={error ? "url-err" : undefined}
                    className="rounded border px-3 py-2 bg-white text-ink-black dark:bg-ink-black dark:text-white"
                    placeholder={t("form.placeholder")}
                    value={url}
                    onChange={e => setUrl(e.target.value)}
                    onBlur={handleBlur}
                />
                {error && <p id="url-err" className="text-red-600 text-sm">{error}</p>}
            </div>

            <div className="flex items-center gap-3">
                <label htmlFor="lang" className="font-medium">{t("form.langLabel")}</label>
                <select
                    id="lang"
                    className="rounded border px-2 py-2 bg-white text-ink-black dark:bg-ink-black dark:text-white"
                    value={lang}
                    onChange={(e) => setLang(e.target.value)}
                >
                    <option value="pl">{t("lang.pl")}</option>
                    <option value="en">{t("lang.en")}</option>
                </select>

                <button
                    type="submit"
                    disabled={loading}
                    className="ml-auto rounded-lg bg-brand-purple px-4 py-2 text-white hover:opacity-90 disabled:opacity-50"
                >
                    {t("form.analyze")}
                </button>
            </div>
            <div aria-live="polite" className="text-sm opacity-80">
                {loading ? t("state.loading") : null}
            </div>
        </form>
    );
}