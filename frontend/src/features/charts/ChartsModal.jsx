import {Modal} from "react-bootstrap";
import {useTranslation} from "react-i18next";
import TimeChart from "../../charts/timeChart"
import BarChart from "../../charts/barChart.jsx";
import {requestData} from "../../shared/lib/api.js";
import {useEffect, useState} from "react";

export default function ChartsModal({show, onClose, url}) {
    console.log(url)
    const [data, setData] = useState(null);
    const {t} = useTranslation();

    useEffect(() => {
        const fetchData = async () => {
            if (!url) return;
            const localdata = await requestData(url);
            setData(localdata);
        };
        fetchData();
    }, [url]);

    function ChartOfChoice(number) {
        const n = number.number
        if (n === 0) {
            return (
                <div>
                    <h2>{t(`final_charts.times`)}</h2>
                    <TimeChart
                        data={data}
                    />
                </div>
            );
        }
        if (n === 1) {
            return (
                <div>
                    <h2>{t(`final_charts.values`)}</h2><BarChart
                    data={data}></BarChart></div>
            );
        }
        return null
    }

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
                <Modal.Title
                    id="charts-modal-title">{t("charts.title")}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="container-fluid">
                    <div className="row g-3">
                        {[0, 1].map((idx) => (
                            <div key={idx} className="col-12 col-md-6">
                                <div className="card h-100 border-brand">
                                    <div
                                        className="card-body d-flex align-items-center justify-content-center text-center">
                                        <div>
                                            <div className="fw-medium mb-2">
                                                <ChartOfChoice
                                                    number={idx}></ChartOfChoice>
                                            </div>
                                            <div
                                                className="text-body-secondary small">
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