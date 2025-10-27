import { useTranslation } from "react-i18next";
import classNames from "classnames";

function Badge({ score }) {
    const color = score === "positive" ? "bg-green-600"
        : score === "negative" ? "bg-red-600"
            : "bg-gray-500";
    return <span className={classNames("text-white text-xs px-2 py-0.5 rounded", color)}>{score}</span>;
}

export default function ResultsPanel({ result }) {
    const { t } = useTranslation();

    if (!result) {
        return (
            <div className="rounded border p-4 h-full">
                <h3 className="font-semibold mb-2">{t("results.title")}</h3>
                <p className="opacity-70">{t("results.placeholder")}</p>
            </div>
        );
    }

    return (
        <div className="rounded border p-4">
            <div className="mb-4">
                <h3 className="font-semibold">{t("results.title")}</h3>
                <div className="mt-1 flex items-center gap-2">
                    <span className="opacity-80">{t("results.global")}:</span>
                    <Badge score={result.summary} />
                </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {result.aspects.map(a => (
                    <div key={a.key} className="rounded border p-3">
                        <div className="flex items-center justify-between mb-2">
                            <span className="font-medium">{t(`results.aspects.${a.key}`)}</span>
                            <Badge score={a.score} />
                        </div>
                        <p className="text-sm opacity-80" aria-label={t("results.quotes")}>“{a.quote}”</p>
                    </div>
                ))}
            </div>
        </div>
    );
}