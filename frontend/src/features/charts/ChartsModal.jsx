import { Modal } from "react-bootstrap";
import { useTranslation } from "react-i18next";

export default function ChartsModal({ show, onClose }) {
    const { t } = useTranslation();

    return (
        <Modal
            show={show}
            onHide={onClose}
            size="xl"
            centered
            backdrop="static"
            aria-labelledby="charts-modal-title"
        >
            <Modal.Header closeButton closeLabel={t("charts.close")}>
                <Modal.Title id="charts-modal-title">{t("charts.title")}</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <div className="container-fluid">
                    <div className="row g-3">
                        {[0, 1, 2, 3].map((idx) => (
                            <div key={idx} className="col-12 col-md-6">
                                <div className="card h-100 border-brand">
                                    <div className="card-body d-flex align-items-center justify-content-center text-center">
                                        <div>
                                            <div className="fw-medium mb-2">
                                                {t(`charts.slots.${idx + 1}.title`)}
                                            </div>
                                            <div className="text-body-secondary small">
                                                {t("charts.placeholder")}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </Modal.Body>

            <Modal.Footer>

            </Modal.Footer>
        </Modal>
    );
}