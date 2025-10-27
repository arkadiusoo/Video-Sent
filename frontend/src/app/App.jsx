import { useState } from "react";
import PageLayout from "../widgets/Layout/PageLayout";
import UrlForm from "../features/submit/UrlForm";
import CookieHistory from "../features/history/CookieHistory";
import ResultsPanel from "../features/results/ResultsPanel";
import { apiStartAnalyze, pollResult } from "../shared/lib/api";
import { pushHistory } from "../shared/lib/cookies";

export default function App() {
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState(null);
    const [result, setResult] = useState(null);

    const runAnalyze = async ({ url, lang, device }) => {
        setErr(null); setLoading(true); setResult(null);
        try {
            const { jobId } = await apiStartAnalyze({ url, lang, device });
            const res = await pollResult(jobId, { intervalMs: 1200, timeoutMs: 20000 });
            setResult(res);
            pushHistory({ url, lang, createdAt: res.createdAt, device: device || null });
        } catch (e) {
            setErr(e.message || "Error");
        } finally {
            setLoading(false);
        }
    };

    const rerun = (url, lang) => runAnalyze({ url, lang });

    return (
      <PageLayout historyContent={<CookieHistory onRerun={rerun} />}>
        {err && (
          <div className="alert alert-danger" role="alert">
            {err}
          </div>
        )}

        <div className="row justify-content-center g-4">
          <div className="col-12 col-lg-8">
            <UrlForm onSubmit={runAnalyze} loading={loading} />
          </div>
        </div>

        <div className="row justify-content-center g-4">
          <div className="col-12 col-lg-8">
            <ResultsPanel result={result} />
          </div>
        </div>
      </PageLayout>
    );
}