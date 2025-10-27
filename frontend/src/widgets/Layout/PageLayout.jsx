import { useState } from "react";
import { Navbar, Container } from "react-bootstrap";
import ThemeToggle from "../../shared/ui/ThemeToggle";
import { useTranslation } from "react-i18next";

export default function PageLayout({ children, historyContent }) {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    return (
        <div className="min-vh-100 d-flex flex-column">
            {/* Slide-out history panel */}
            <button
              type="button"
              className="btn btn-light position-fixed"
              style={{
                left: 0,
                top: "50%",
                transform: "translate(-50%, -50%)",
                zIndex: 1051,
                borderRadius: "0 4px 4px 0",
                boxShadow: "0 0 6px rgba(0,0,0,.15)"
              }}
              aria-label="Toggle history"
              aria-controls="history-panel"
              aria-expanded={open}
              onClick={() => setOpen(o => !o)}
            >
              {open ? "‹" : "›"}
            </button>

            <div
              id="history-panel"
              className="bg-body border-end"
              style={{
                position: "fixed",
                top: 0,
                left: 0,
                height: "100vh",
                width: 320,
                transform: open ? "translateX(0)" : "translateX(-100%)",
                transition: "transform .25s ease",
                zIndex: 1050,
                overflowY: "auto"
              }}
            >
              <div className="p-3">
                {historyContent}
              </div>
            </div>

            <Navbar bg="body" data-bs-theme="auto" className="border-bottom border-brand">
                <Container>
                    <div>
                        <h1 className="fs-4 mb-0">Video-Sent</h1>
                        <p className="text-body-secondary mb-0">{t("app.subtitle")}</p>
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