// =======================================================
// AEGISAI Autonomous Cyber Defense Platform
// Dashboard JavaScript
// =======================================================

console.log("========================================");
console.log("AEGISAI Dashboard Started");
console.log("========================================");

document.addEventListener("DOMContentLoaded", function () {

    //----------------------------------------------------
    // Read Risk Values from Flask
    //----------------------------------------------------

    let highRisk = 0;
    let mediumRisk = 0;
    let lowRisk = 0;

    if (typeof dashboardData !== "undefined") {

        highRisk = dashboardData.high;
        mediumRisk = dashboardData.medium;
        lowRisk = dashboardData.low;

    }

    //----------------------------------------------------
    // Doughnut Chart
    //----------------------------------------------------

    const chartCanvas = document.getElementById("riskChart");

    if (chartCanvas) {

        new Chart(chartCanvas, {

            type: "doughnut",

            data: {

                labels: [

                    "High Risk",
                    "Medium Risk",
                    "Low Risk"

                ],

                datasets: [

                    {

                        label: "Detected Risks",

                        data: [

                            highRisk,
                            mediumRisk,
                            lowRisk

                        ],

                        backgroundColor: [

                            "#ff4d4d",
                            "#ffae42",
                            "#3fb950"

                        ],

                        borderColor: [

                            "#ffffff",
                            "#ffffff",
                            "#ffffff"

                        ],

                        borderWidth: 2

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {

                    duration: 1800,

                    animateRotate: true,

                    animateScale: true

                },

                plugins: {

                    title: {

                        display: true,

                        text: "Risk Distribution",

                        color: "white",

                        font: {

                            size: 18

                        }

                    },

                    legend: {

                        position: "bottom",

                        labels: {

                            color: "white",

                            font: {

                                size: 13

                            }

                        }

                    }

                }

            }

        });

    }

    //----------------------------------------------------
    // Highlight Risk Column
    //----------------------------------------------------

    const rows = document.querySelectorAll("tbody tr");

    rows.forEach(function (row) {

        if (row.cells.length < 6)
            return;

        const risk = row.cells[5].innerText.trim();

        row.cells[5].classList.remove("high", "medium", "low");

        if (risk === "HIGH") {

            row.cells[5].classList.add("high");

        }

        else if (risk === "MEDIUM") {

            row.cells[5].classList.add("medium");

        }

        else {

            row.cells[5].classList.add("low");

        }

    });

    //----------------------------------------------------
    // Auto Refresh Dashboard
    //----------------------------------------------------

    setInterval(function () {

        location.reload();

    }, 30000);

    console.log("Dashboard Ready");

});