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
    const [successMsg, setSuccessMsg] = useState(null);
    const [prefill, setPrefill] = useState(null);
    const [chartsOpen, setChartsOpen] = useState(false);
    const { t } = useTranslation();

    const runAnalyze = async ({ url, lang, device }) => {
        setErr(null); setLoading(true); setResult(null);setSuccessMsg(null);
        try {
            const { jobId } = await apiStartAnalyze({ url, lang, device });
            const res = await pollResult(jobId, { intervalMs: 1200, timeoutMs: 20000 });

            if (res.backend?.status === "success") {
              setErr(null);
              setSuccessMsg("Video successfully downloaded!");
              setTimeout(() => setSuccessMsg(null), 5000); // auto-hide after 5s
            } else if (res.backend?.status === "error") {
              setErr("Failed to download video: " + res.backend?.message);
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
          <div
            className="p-3 mb-3 text-center rounded"
            style={{
              backgroundColor: "#4a1c1c",
              color: "#ffbdbd",
              fontWeight: "500",
            }}
          >
            {err}
          </div>
        )}

        {successMsg && (
          <div
            className="p-3 mb-3 text-center rounded"
            style={{
              backgroundColor: "#1c4a2a",
              color: "#baffc9",
              fontWeight: "500",
            }}
          >
            {successMsg}
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
                  <ChartsModal show={chartsOpen} url={url} onClose={() => setChartsOpen(false)} />
              </div>
          </div>
      </PageLayout>
    );
}