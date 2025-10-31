import { useState } from "react";
import PageLayout from "../widgets/Layout/PageLayout";
import UrlForm from "../features/submit/UrlForm";
import CookieHistory from "../features/history/CookieHistory";
import ResultsPanel from "../features/results/ResultsPanel";
import ChartsModal from "../features/charts/ChartsModal";
import { useTranslation } from "react-i18next";
import { apiStartAnalyze, pollResult } from "../shared/lib/api";
import { pushHistory } from "../shared/lib/cookies";

export default function App() {
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState(null);
    const [result, setResult] = useState(null);
    const [prefill, setPrefill] = useState(null);
    const [chartsOpen, setChartsOpen] = useState(false);
    const { t } = useTranslation();

    const runAnalyze = async ({ url, lang, device }) => {
        setErr(null); setLoading(true); setResult(null);
        try {
            const { jobId } = await apiStartAnalyze({ url, lang, device });
            const res = await pollResult(jobId, { intervalMs: 1200, timeoutMs: 20000 });

            if (res.backend?.status === "success") {
            setErr(null);
            alert("Video successfully downloaded!");
            }
            else if (res.backend?.status === "error") {
            alert ("Failed to download video: " + res.backend?.message);
            }

            setResult(res);
            pushHistory({ url, lang, createdAt: res.createdAt, device: device || null });
        } catch (e) {
            setErr(e.message || "Error");
        } finally {
            setLoading(false);
        }
    };

    const rerun = (url, lang, device) => setPrefill({ url, lang, device: device || "" });

    return (
      <PageLayout historyContent={<CookieHistory onRerun={rerun} />}>
        {err && (
          <div className="alert alert-danger" role="alert">
            {err}
          </div>
        )}

        <div className="row justify-content-center g-4">
          <div className="col-12 col-lg-8">
            <UrlForm onSubmit={runAnalyze} loading={loading} prefill={prefill} />
          </div>
        </div>

          <div className="row justify-content-center g-4">
              <div className="col-12 col-lg-8">
                  <ResultsPanel result={result} />

                  <div className="mt-3 d-grid">
                      <button
                          type="button"
                          className="btn btn-brand"
                          disabled={!result}
                          onClick={() => setChartsOpen(true)}
                      >
                          {result ? t("charts.open") : t("charts.openDisabled")}
                      </button>
                  </div>

                  <ChartsModal show={chartsOpen} onClose={() => setChartsOpen(false)} />
              </div>
          </div>
      </PageLayout>
    );
}