import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

export default function ThemeToggle() {
    const { t, i18n } = useTranslation();
    const [theme, setTheme] = useState(() => {
        const saved = localStorage.getItem("vs_theme_bs");
        if (saved === "dark" || saved === "light") return saved;
        const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
        return prefersDark ? "dark" : "light";
    });

    useEffect(() => {
        document.documentElement.setAttribute("data-bs-theme", theme);
        localStorage.setItem("vs_theme_bs", theme);
    }, [theme]);

    return (
        <div className="d-flex align-items-center gap-2">
            <select
                aria-label="Language"
                className="form-select form-select-sm"
                style={{ width: 120 }}
                value={i18n.language}
                onChange={(e) => {
                    i18n.changeLanguage(e.target.value);
                    localStorage.setItem("vs_lang", e.target.value);
                }}
            >
                <option value="pl">{t("lang.pl")}</option>
                <option value="en">{t("lang.en")}</option>
            </select>

            <button
                type="button"
                className="btn btn-outline-secondary btn-sm"
                onClick={() => setTheme((v) => (v === "dark" ? "light" : "dark"))}
                aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            >
                {theme === "dark" ? t("theme.light") : t("theme.dark")}
            </button>
        </div>
    );
}