import { Navbar, Container } from "react-bootstrap";
import ThemeToggle from "../../shared/ui/ThemeToggle";
import { useTranslation } from "react-i18next";

export default function PageLayout({ children }) {
    const { t } = useTranslation();
    return (
        <div className="min-vh-100 d-flex flex-column">
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