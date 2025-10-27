import { useState, useRef } from "react";
import { Navbar, Container } from "react-bootstrap";
import ThemeToggle from "../../shared/ui/ThemeToggle";
import { useTranslation } from "react-i18next";

export default function PageLayout({ children, historyContent }) {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    const [panelW, setPanelW] = useState(320);
    const resizingRef = useRef(false);
    const startXRef = useRef(0);
    const startWRef = useRef(320);

    const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

    const onMouseMove = (e) => {
      if (!resizingRef.current) return;
      const dx = e.clientX - startXRef.current;
      setPanelW(clamp(startWRef.current + dx, 260, 560));
    };

    const onMouseUp = () => {
      if (!resizingRef.current) return;
      resizingRef.current = false;
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
      document.body.style.userSelect = "";
    };

    const startResize = (e) => {
      resizingRef.current = true;
      startXRef.current = e.clientX;
      startWRef.current = panelW;
      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", onMouseUp);
      document.body.style.userSelect = "none";
    };
    return (
        <div className="min-vh-100 d-flex flex-column">

            <div
              id="history-panel"
              className="bg-body border-end"
              style={{
                position: "fixed",
                top: 0,
                left: 0,
                height: "100vh",
                width: panelW,
                transform: open ? "translateX(0)" : "translateX(-100%)",
                transition: "transform .25s ease",
                zIndex: 1050,
                overflowY: "auto"
              }}
            >
              <div className="p-3">
                {historyContent}
              </div>
              <div
                onMouseDown={startResize}
                role="separator"
                aria-orientation="vertical"
                aria-label="Resize history panel"
                style={{
                  position: "absolute",
                  right: 0,
                  top: 0,
                  width: 6,
                  height: "100%",
                  cursor: "ew-resize",
                  background: "transparent"
                }}
              />
            </div>

            <Navbar bg="body" data-bs-theme="auto" className="border-bottom border-brand">
              <Container className="d-flex align-items-center justify-content-between">
                <div className="d-flex align-items-center gap-2">
                  <button
                    type="button"
                    className="btn btn-outline-secondary btn-sm"
                    aria-label="Toggle history"
                    aria-controls="history-panel"
                    aria-expanded={open}
                    onClick={() => setOpen(o => !o)}
                  >
                    <span className="d-inline-block" aria-hidden="true" style={{ lineHeight: 0 }}>
                      <span style={{ display: "block", width: 16, height: 2, backgroundColor: "currentColor", margin: "3px 0" }} />
                      <span style={{ display: "block", width: 16, height: 2, backgroundColor: "currentColor", margin: "3px 0" }} />
                      <span style={{ display: "block", width: 16, height: 2, backgroundColor: "currentColor", margin: "3px 0" }} />
                    </span>
                  </button>
                  <div>
                    <h1 className="fs-4 mb-0">Video-Sent</h1>
                    <p className="text-body-secondary mb-0">{t("app.subtitle")}</p>
                  </div>
                </div>
                <ThemeToggle />
              </Container>
            </Navbar>

            <Container as="main" className="py-4 flex-grow-1">
                {children}
            </Container>

            <footer className="py-4 text-center text-body-secondary border-top border-brand">
                © {new Date().getFullYear()} Video-Sent MVP
            </footer>
        </div>
    );
}