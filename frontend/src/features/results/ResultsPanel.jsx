import { useTranslation } from "react-i18next";

function Badge({ score }) {
    const map = {
        positive: "bg-success",
        neutral: "bg-secondary",
        negative: "bg-danger"
    };
    return <span className={`badge ${map[score] || "bg-secondary"}`}>{score}</span>;
}

export default function ResultsPanel({ result }) {
    const { t } = useTranslation();

    if (!result) {
        return (
            <div className="card border-brand h-100">
                <div className="card-body">
                    <h3 className="card-title fs-6 mb-2">{t("results.title")}</h3>
                    <p className="text-body-secondary mb-0">{t("results.placeholder")}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card border-brand">
            <div className="card-body">
                <div className="d-flex align-items-center gap-2 mb-3">
                    <h3 className="card-title fs-6 mb-0">{t("results.title")}</h3>
                    <div className="ms-2">
                        <span className="me-2">{t("results.global")}:</span>
                        <Badge score={result.summary} />
                    </div>
                </div>

                <div className="row g-3">
                    {result.aspects.map((a) => (
                        <div className="col-12 col-sm-6 col-lg-4" key={a.key}>
                            <div className="card h-100">
                                <div className="card-body">
                                    <div className="d-flex justify-content-between align-items-center mb-2">
                                        <span className="fw-medium">{t(`results.aspects.${a.key}`)}</span>
                                        <Badge score={a.score} />
                                    </div>
                                    <p className="small text-body-secondary mb-0" aria-label={t("results.quotes")}>
                                        “{a.quote}”
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

            </div>
        </div>
    );
}