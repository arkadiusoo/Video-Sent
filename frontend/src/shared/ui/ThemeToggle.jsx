import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

export default function ThemeToggle() {
    const { t, i18n } = useTranslation();
    const [dark, setDark] = useState(() => document.documentElement.classList.contains("dark"));

    useEffect(() => {
        const saved = localStorage.getItem("vs_theme");
        if (saved) document.documentElement.classList.toggle("dark", saved === "dark");
        setDark(document.documentElement.classList.contains("dark"));
    }, []);

    useEffect(() => {
        document.documentElement.classList.toggle("dark", dark);
        localStorage.setItem("vs_theme", dark ? "dark" : "light");
    }, [dark]);

    return (
        <div className="flex items-center gap-3">
            <select
                aria-label="Language"
                className="rounded border px-2 py-1 bg-white text-ink-black dark:bg-ink-black dark:text-white"
                value={i18n.language}
                onChange={(e) => i18n.changeLanguage(e.target.value)}
            >
                <option value="pl">{t("lang.pl")}</option>
                <option value="en">{t("lang.en")}</option>
            </select>
            <button
                aria-label={dark ? "Switch to light mode" : "Switch to dark mode"}
                className="rounded-lg border px-3 py-1 hover:bg-brand-purple/10"
                onClick={() => setDark(v => !v)}
            >
                {dark ? t("theme.light") : t("theme.dark")}
            </button>
        </div>
    );
}