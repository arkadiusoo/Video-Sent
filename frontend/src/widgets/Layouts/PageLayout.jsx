import ThemeToggle from "../../shared/ui/ThemeToggle";
import { useTranslation } from "react-i18next";

export default function PageLayout({ children }) {
    const { t } = useTranslation();
    return (
        <div className="min-h-screen">
            <header className="flex items-center justify-between px-4 py-3 border-b">
                <div>
                    <h1 className="text-xl font-semibold">Video-Sent</h1>
                    <p className="text-sm opacity-80">{t("app.subtitle")}</p>
                </div>
                <ThemeToggle />
            </header>
            <main className="mx-auto w-full max-w-6xl px-4 py-6">{children}</main>
            <footer className="px-4 py-6 text-center opacity-60">© {new Date().getFullYear()} Video-Sent MVP</footer>
        </div>
    );
}