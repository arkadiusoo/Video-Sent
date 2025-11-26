import React from "react";
// Import the component wrapper for ApexCharts
import Chart from 'react-apexcharts';
import { useTranslation } from "react-i18next";

// You no longer need useEffect or the direct 'apexcharts' import
// The Chart component handles the configuration and rendering lifecycle
export default function TimeChart(data) {
    const { t } = useTranslation();
    const download=parseFloat(data.data.avg_download_time_seconds)
    const transcription=parseFloat(data.data.avg_transcription_time_seconds)
    const analysis=parseFloat(data.data.avg_analysis_time_seconds)

    // 1. Chart Configuration (Remains the same, but passed directly to the <Chart/> component)
    const chartConfig = {
        series: [download, transcription, analysis],
        options: {
            chart: {
                type: "pie",
                width: 280,
                height: 280,
                toolbar: {
                    show: false,
                },
            },
            title: {
                show: false,
            },
            dataLabels: {
                enabled: false,
            },
            colors: ["#ff8f00", "#00897b", "#1e88e5"],
            legend: {
                show: false,
            },
            labels: ['download', 'transcription', 'analysis'],
        },
    };

    return (
        <div className="relative flex flex-col rounded-xl bg-transparent bg-clip-border text-gray-700 shadow-md">
            <div className="py-6 mt-4 grid place-items-center px-2">
                {/* 2. Use the dedicated Chart component */}
                <Chart
                    options={chartConfig.options}
                    series={chartConfig.series}
                    type="pie"
                    width={280}
                    height={280}
                />
            </div>
        </div>
    );
}