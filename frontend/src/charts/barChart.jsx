import React, {useEffect, useRef, useState} from 'react';



// Custom hook to load an external script dynamically
const useScript = (url) => {
    const [loaded, setLoaded] = useState(false);

    useEffect(() => {
        // 1. Check if the library is already loaded (e.g., if component re-renders)
        if (window.ApexCharts) {
            setLoaded(true);
            return;
        }

        // 2. Check if script element already exists to avoid duplication
        let script = document.querySelector(`script[src="${url}"]`);

        if (!script) {
            // Create script tag
            script = document.createElement('script');
            script.src = url;
            script.async = true;

            // Append it to the document body
            document.body.appendChild(script);
        }

        // 3. Event listeners for load and error
        const onScriptLoad = () => setLoaded(true);
        const onScriptError = () => console.error(`Failed to load script: ${url}`);

        script.addEventListener('load', onScriptLoad);
        script.addEventListener('error', onScriptError);

        // 4. Cleanup function
        return () => {
            script.removeEventListener('load', onScriptLoad);
            script.removeEventListener('error', onScriptError);
        };
    }, [url]);

    return loaded;
};


/**
 * Komponent do obsługi montowania i renderowania ApexChart.
 * Teraz czeka na załadowanie biblioteki.
 */


const BarChartComponent = ({isLibraryLoaded,data}) => {
    console.log("data")
    console.log(data)
    const chartRef = useRef(null);
    const chartConfig = {
        series: [
            {
                name: "score",
                data: [
                    data.data.avg_camera_score,
                    data.data.avg_battery_score,
                    data.data.avg_screen_score,
                    data.data.avg_performance_score,
                    data.data.avg_general_score],
            },
        ],
        chart: {
            type: "bar",
            height: 240,
            toolbar: {
                show: false,
            },
        },
        title: {
            show: "",
        },
        dataLabels: {
            enabled: false,
        },
        colors: ["#114fff"],
        plotOptions: {
            bar: {
                columnWidth: "40%",
                borderRadius: 4,
            },
        },
        xaxis: {
            axisTicks: {
                show: false,
            },
            axisBorder: {
                show: false,
            },
            labels: {
                style: {
                    colors: "#e4e4e4",
                    fontSize: "12px",
                    fontFamily: "Inter, sans-serif",
                    fontWeight: 400,
                },
            },
            categories: [
                "Camera",
                "Battery",
                "Screen",
                "Performance",
                "General"
            ],
        },
        yaxis: {
            labels: {
                style: {
                    colors: "#e4e4e4",
                    fontSize: "12px",
                    fontFamily: "Inter, sans-serif",
                    fontWeight: 400,
                },
            },
        },
        grid: {
            show: true,
            borderColor: "#000000",
            strokeDashArray: 5,
            xaxis: {
                lines: {
                    show: true,
                },
            },
            padding: {
                top: 5,
                right: 20,
            },
        },
        fill: {
            opacity: 0.9,
        },
        tooltip: {
            theme: "dark",
        },
    };

    useEffect(() => {
        let chartInstance;

        if (isLibraryLoaded && window.ApexCharts && chartRef.current) {
            chartInstance = new window.ApexCharts(chartRef.current, chartConfig);
            chartInstance.render();
        } else if (isLibraryLoaded && !window.ApexCharts) {
            // Should not happen if useScript works, but good for diagnostics
            console.error("ApexCharts failed to attach to window after loading.");
        }

        // Funkcja czyszcząca do zniszczenia wykresu po odmontowaniu komponentu
        return () => {
            if (chartInstance) {
                chartInstance.destroy();
            }
        };
    }, [isLibraryLoaded]); // Zależność od stanu załadowania

    // Stan ładowania
    if (!isLibraryLoaded) {
        return (
            <div
                className="h-60 w-full flex items-center justify-center bg-gray-100 rounded-lg">
                <svg className="animate-spin h-5 w-5 text-gray-500 mr-3"
                     viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10"
                            stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p className="text-gray-500">Ładowanie wykresu...</p>
            </div>
        );
    }

    return <div ref={chartRef} className="h-60 w-full"/>;
};

/**
 * Główny komponent aplikacji.
 */
const App = (data) => {
    if (!data)
        return null
    // Dynamicznie ładujemy skrypt biblioteki ApexCharts
    const isApexLoaded = useScript("https://cdn.jsdelivr.net/npm/apexcharts");
    return (
        <div
            className="min-h-screen bg-gray-50 p-4 md:p-8 flex justify-center items-start">
            <div
                className="relative flex w-full max-w-4xl flex-col rounded-xl bg-transparent bg-clip-border text-gray-700 shadow-xl">

                <div className="p-4 pt-0">
                    {/* Przekazujemy stan załadowania do komponentu wykresu */}
                    <BarChartComponent isLibraryLoaded={isApexLoaded} data={data}/>
                </div>

            </div>
        </div>
    );
};

export default App;