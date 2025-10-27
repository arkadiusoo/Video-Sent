/** @type {import('tailwindcss').Config} */
export default {
    darkMode: "class",
    content: ["./index.html", "./src/**/*.{js,jsx}"],
    theme: {
        extend: {
            colors: {
                brand: { purple: "#7c3aed" },
                ink: { black: "#111111" }
            }
        }
    },
    plugins: []
};