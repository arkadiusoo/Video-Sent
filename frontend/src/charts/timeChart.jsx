import React from "react";
// Import the component wrapper for ApexCharts
import Chart from 'react-apexcharts';
import { useTranslation } from "react-i18next";

// You no longer need useEffect or the direct 'apexcharts' import
// The Chart component handles the configuration and rendering lifecycle
export default function TimeChart() {
    const { t } = useTranslation();

    // 1. Chart Configuration (Remains the same, but passed directly to the <Chart/> component)
    const chartConfig = {
        series: [44, 55, 13, 43, 22],
        options: { // All chart settings go under the 'options' property
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
            colors: ["#020617", "#ff8f00", "#00897b", "#1e88e5", "#d81b60"],
            legend: {
                show: false,
            },
            labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
        },
    };

    return (
        <div className="relative flex flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
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