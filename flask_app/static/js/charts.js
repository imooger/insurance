// static/js/loss_ratio_chart.js


var GREEN_1 = '#c8dcd6'
var GREEN_2 = '#689f8f'
var GREEN_3 = '#487165'
var GREEN_3_T = 'rgba(2,113,101,0.2)'
var GREEN_4 = '#3D645A'

var GREY_1 = '#f2f2f2'
var GREY_2 = '#e5e5e5'
var GREY_3= '#d8d8d8'

var RED_Line = 'rgba(255, 80, 80, 1)'
var RED_Line_T = 'rgba(255, 80, 80, 0.2)'
var RED_Bar = '#EF6351'
var RED_Pie = '#ff5050'
var RED_Pie_light = '#ffa0a0'
var RED_Pie_very_light = '#ffe0e0'

document.addEventListener('DOMContentLoaded', function () {
    

    var canvas = document.getElementById('premiumVsClaimsChart');
    if (canvas) {
        // Read data from data attributes
        var totalPremium = parseFloat(canvas.getAttribute('data-total-premium'));
        var totalClaimAmount = parseFloat(canvas.getAttribute('data-total-claim-amount'));
        
        var ctx = canvas.getContext('2d');
        var premiumVsClaimsChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Total Premiums', 'Total Claims'],
                datasets: [{
                    data: [
                        totalPremium,
                        totalClaimAmount
                    ],
                    backgroundColor: [GREEN_3, GREY_2],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            boxWidth: 20
                        }
                    }
                }
            }
        });
    }
});

// HORIZONTAL premiumVsClaimsChart
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('lossRatioBarChart');
    if (canvas) {
        // Reading data from data attributes
        var totalPremium = parseFloat(canvas.getAttribute('data-total-premium'));
        var totalClaimAmount = parseFloat(canvas.getAttribute('data-total-claim-amount'));
        
        var ctx = canvas.getContext('2d');
        var lossRatioBarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Total Premiums', 'Total Claims'],
                datasets: [{
                    data: [
                        totalPremium,
                        totalClaimAmount
                    ],
                    backgroundColor: [GREEN_3, GREY_2],
                    hoverOffset: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: false,
                plugins: {
                    legend: {
                        display:false
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            beginAtZero: true,
                            callback: function(value) {
                                return value >= 1000 ? (value / 1000) + 'k' : value;
                            }
                        }
                    }
                }
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('claimsCountChart');
    if (canvas) {
        // Reading data from data attributes
        var newClaimCount = parseFloat(canvas.getAttribute('data-new-claim-count'));
        var pendingClaimCount = parseFloat(canvas.getAttribute('data-pending-claim-count'));
        var paidClaimCount = parseFloat(canvas.getAttribute('data-paid-claim-count'));
        var deniedClaimCount = parseFloat(canvas.getAttribute('data-denied-claim-count'));

        var ctx3 = canvas.getContext('2d');
        var claimsCountChart = new Chart(ctx3, {
            type: 'pie',
            data: {
                labels: ['New', 'Pending', 'Paid', 'Denied'],
                datasets: [{
                    data: [
                        newClaimCount,
                        pendingClaimCount,
                        paidClaimCount,
                        deniedClaimCount
                    ],
                    backgroundColor: [RED_Pie, RED_Pie_very_light, RED_Pie_light, GREY_1],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            boxWidth: 15
                        }
                    }
                }
            }
        });
    }
});

// Barchart claim status
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('claimsCountChartBAR');
    if (canvas) {
        // Reading data from data attributes
        var newClaimCount_bar = parseFloat(canvas.getAttribute('data_bar_new_claim_count'));
        var pendingClaimCount_bar = parseFloat(canvas.getAttribute('data_bar_pending_claim_count'));
        var paidClaimCount_bar = parseFloat(canvas.getAttribute('data_bar_paid_claim_count'));
        var deniedClaimCount_bar = parseFloat(canvas.getAttribute('data_bar_denied_claim_count'));

        var ctx3 = canvas.getContext('2d');
        var claimsCountChartBAR = new Chart(ctx3, {
            type: 'bar',
            data: {
                labels: ['New', 'Pending', 'Paid', 'Denied'],
                datasets: [{
                    data: [
                        newClaimCount_bar,
                        pendingClaimCount_bar,
                        paidClaimCount_bar,
                        deniedClaimCount_bar
                    ],
                    backgroundColor: [RED_Bar,  GREY_3, GREY_2, GREY_1],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: {
                        display:false
                    }
                }
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('activeVsExpiredPoliciesBar');
    if (canvas) {
        // Reading data from data attributes
        var houseActivePremiums = parseFloat(canvas.getAttribute('data-house-active-premiums'));
        var autoActivePremiums = parseFloat(canvas.getAttribute('data-auto-active-premiums'));
        var lifeActivePremiums = parseFloat(canvas.getAttribute('data-life-active-premiums'));
        var healthActivePremiums = parseFloat(canvas.getAttribute('data-health-active-premiums'));
        
        var houseExpiredPremiums = parseFloat(canvas.getAttribute('data-house-expired-premiums'));
        var autoExpiredPremiums = parseFloat(canvas.getAttribute('data-auto-expired-premiums'));
        var lifeExpiredPremiums = parseFloat(canvas.getAttribute('data-life-expired-premiums'));
        var healthExpiredPremiums = parseFloat(canvas.getAttribute('data-health-expired-premiums'));

        var ctx6 = canvas.getContext('2d');
        var activeVsExpiredPoliciesBar = new Chart(ctx6, {
            type: 'bar',
            data: {
                labels: ['House', 'Car', 'Life', 'Health'],
                datasets: [
                    {
                        label: 'Active Policies',
                        data: [
                            houseActivePremiums,
                            autoActivePremiums,
                            lifeActivePremiums,
                            healthActivePremiums
                        ],
                        backgroundColor: GREEN_2,
                        hoverOffset: 4
                    },
                    {
                        label: 'Expired Policies',
                        data: [
                            houseExpiredPremiums,
                            autoExpiredPremiums,
                            lifeExpiredPremiums,
                            healthExpiredPremiums
                        ],
                        backgroundColor: GREY_2,
                        hoverOffset: 4
                    }
                ]
            },
            options: {
                responsive: false,
                scales: {
                    x: {
                        beginAtZero: true
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('activeVsExpiredStacked');
    if (canvas) {
        // Reading data from data attributes
        var houseActivePremiums = parseFloat(canvas.getAttribute('data-house-active-premiums'));
        var autoActivePremiums = parseFloat(canvas.getAttribute('data-auto-active-premiums'));
        var lifeActivePremiums = parseFloat(canvas.getAttribute('data-life-active-premiums'));
        var healthActivePremiums = parseFloat(canvas.getAttribute('data-health-active-premiums'));
        
        var houseExpiredPremiums = parseFloat(canvas.getAttribute('data-house-expired-premiums'));
        var autoExpiredPremiums = parseFloat(canvas.getAttribute('data-auto-expired-premiums'));
        var lifeExpiredPremiums = parseFloat(canvas.getAttribute('data-life-expired-premiums'));
        var healthExpiredPremiums = parseFloat(canvas.getAttribute('data-health-expired-premiums'));

        var ctx6 = canvas.getContext('2d');
        var activeVsExpiredStacked = new Chart(ctx6, {
            type: 'bar',
            data: {
                labels: ['House', 'Car', 'Life', 'Health'],
                datasets: [
                    {
                        label: 'Active Policies',
                        data: [
                            houseActivePremiums,
                            autoActivePremiums,
                            lifeActivePremiums,
                            healthActivePremiums
                        ],
                        backgroundColor: GREEN_2,
                        hoverOffset: 4
                    },
                    {
                        label: 'Expired Policies',
                        data: [
                            houseExpiredPremiums,
                            autoExpiredPremiums,
                            lifeExpiredPremiums,
                            healthExpiredPremiums
                        ],
                        backgroundColor: GREY_2,
                        hoverOffset: 4
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        beginAtZero: true
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('lossRatioStacked');
    if (canvas) {
        // Reading data from data attributes
        var data_paid_house_claim_by_type = parseFloat(canvas.getAttribute('data_paid_house_claim_by_type'));
        var data_paid_auto_claim_by_type = parseFloat(canvas.getAttribute('data_paid_auto_claim_by_type'));
        var data_paid_life_claim_by_type = parseFloat(canvas.getAttribute('data_paid_life_claim_by_type'));
        var data_paid_health_claim_by_type = parseFloat(canvas.getAttribute('data_paid_health_claim_by_type'));
        
        var data_sum_of_house_by_type = parseFloat(canvas.getAttribute('data_sum_of_house_by_type'));
        var data_sum_of_auto_by_type = parseFloat(canvas.getAttribute('data_sum_of_auto_by_type'));
        var data_sum_of_life_by_type = parseFloat(canvas.getAttribute('data_sum_of_life_by_type'));
        var data_sum_of_health_by_type = parseFloat(canvas.getAttribute('data_sum_of_health_by_type'));

        var ctx30 = canvas.getContext('2d');
        var lossRatioStacked = new Chart(ctx30, {
            type: 'bar',
            data: {
                labels: ['House', 'Car', 'Life', 'Health'],
                datasets: [
                    {
                        label: 'Paid Claims',
                        data: [
                            data_paid_house_claim_by_type,
                            data_paid_auto_claim_by_type,
                            data_paid_life_claim_by_type,
                            data_paid_health_claim_by_type
                        ],
                        backgroundColor: RED_Pie,
                        hoverOffset: 4
                    },
                    {
                        label: 'Sum of Premiums',
                        data: [
                            data_sum_of_house_by_type,
                            data_sum_of_auto_by_type,
                            data_sum_of_life_by_type,
                            data_sum_of_health_by_type
                        ],
                        backgroundColor: GREY_2,
                        hoverOffset: 4
                    }
                ]
            },
            options: {
                scales: {
                    x: {
                        beginAtZero: true
                    },
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('policyCountsByType');
    if (canvas) {
        // Reading data from data attributes
        var data_house_policy_count = parseFloat(canvas.getAttribute('data_house_policy_count'));
        var data_auto_policy_count = parseFloat(canvas.getAttribute('data_auto_policy_count'));
        var data_life_policy_count = parseFloat(canvas.getAttribute('data_life_policy_count'));
        var data_health_policy_count = parseFloat(canvas.getAttribute('data_health_policy_count'));

        var ctx2 = canvas.getContext('2d');
        var policyCountsByType = new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: ['House', 'Auto', 'Life', 'Health'],
                datasets: [{
                    data: [
                        data_house_policy_count,
                        data_auto_policy_count,
                        data_life_policy_count,
                        data_health_policy_count

                    ],
                
                    backgroundColor: [GREEN_1, GREEN_2, GREEN_3, GREEN_4],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            boxWidth: 20
                        }
                    },
                }
            }
        });
    }
});

// BAR policyCountsByType

document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('policyCountsByTypeBAR');
    if (canvas) {
        // Reading data from data attributes
        var data_house_policy_count = parseFloat(canvas.getAttribute('data_house_policy_count'));
        var data_auto_policy_count = parseFloat(canvas.getAttribute('data_auto_policy_count'));
        var data_life_policy_count = parseFloat(canvas.getAttribute('data_life_policy_count'));
        var data_health_policy_count = parseFloat(canvas.getAttribute('data_health_policy_count'));

        var ctx2 = canvas.getContext('2d');
        var policyCountsByTypeBAR = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: ['House', 'Car', 'Life', 'Health',],
                datasets: [{
                    data: [
                        data_house_policy_count,
                        data_auto_policy_count,
                        data_life_policy_count,
                        data_health_policy_count

                    ],
                
                    backgroundColor: [GREEN_1, GREEN_2, GREEN_3, GREEN_4],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: {
                        display:false
                    }
                }
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('claimsByPolicyTypeChart');
    if (canvas) {
        // Reading data from data attributes
        var data_house_claim_count = parseFloat(canvas.getAttribute('data_house_claim_count'));
        var data_auto_claim_count = parseFloat(canvas.getAttribute('data_auto_claim_count'));
        var data_life_claim_count = parseFloat(canvas.getAttribute('data_life_claim_count'));
        var data_health_claim_count = parseFloat(canvas.getAttribute('data_health_claim_count'));
        
        var ctx5 = canvas.getContext('2d');
        var claimsByPolicyTypeChart = new Chart(ctx5, {
            type: 'pie',
            data: {
                labels: ['House', 'Auto', 'Life', 'Health',],
                datasets: [{
                    data: [
                        data_house_claim_count,
                        data_auto_claim_count,
                        data_life_claim_count,
                        data_health_claim_count
                        
                    ],
                    backgroundColor: [GREEN_1, GREEN_2, GREEN_3, GREEN_4],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            boxWidth: 15
                        }
                    },
                }
            }

        });
    }
});

// BAR claims by policy type

document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('claimsByPolicyTypeChartBAR');
    if (canvas) {
        // Reading data from data attributes
        var data_house_claim_count = parseFloat(canvas.getAttribute('data_bar_house_claim_count'));
        var data_auto_claim_count = parseFloat(canvas.getAttribute('data_bar_auto_claim_count'));
        var data_life_claim_count = parseFloat(canvas.getAttribute('data_bar_life_claim_count'));
        var data_health_claim_count = parseFloat(canvas.getAttribute('data_bar_health_claim_count'));
        
        var ctx5 = canvas.getContext('2d');
        var claimsByPolicyTypeChartBAR = new Chart(ctx5, {
            type: 'bar',
            data: {
                labels: ['House', 'Auto', 'Life', 'Health',],
                datasets: [{
                    data: [
                        data_house_claim_count,
                        data_auto_claim_count,
                        data_life_claim_count,
                        data_health_claim_count
                        
                    ],
                    backgroundColor: [GREEN_1, GREEN_2, GREEN_3, GREEN_4],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: {
                        display:false
                    }
                }
            }

        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('clientsPoliciesChart');
    if (canvas) {
        // Reading data from data attributes
        var data_paid_claim_count = parseFloat(canvas.getAttribute('data_paid_claim_count'));
        var data_denied_claim_count = parseFloat(canvas.getAttribute('data_denied_claim_count'));

        var ctx1 = canvas.getContext('2d');
        var clientsPoliciesChart = new Chart(ctx1, {
            type: 'pie',
            data: {
                labels: ['Paid', 'Denied'],
                datasets: [{
                    data: [
                        data_paid_claim_count,
                        data_denied_claim_count
                    ],
                    backgroundColor: [RED_Pie, GREY_2],
                    hoverOffset: 4
                }]
            }
        });
    }
});
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('lossRatioChartos');
    
    if (canvas) {
        // Reading data from data attributes
        var data_house_claims_to_premiums_ratio = parseFloat(canvas.getAttribute('data_house_claims_to_premiums_ratio'));
        var data_auto_claims_to_premiums_ratio = parseFloat(canvas.getAttribute('data_auto_claims_to_premiums_ratio'));
        var data_life_claims_to_premiums_ratio = parseFloat(canvas.getAttribute('data_life_claims_to_premiums_ratio'));
        var data_health_claims_to_premiums_ratio = parseFloat(canvas.getAttribute('data_health_claims_to_premiums_ratio'));


        var ctx = canvas.getContext('2d');
        var lossRatioChartos = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['House', 'Auto', 'Life', 'Health'],
                datasets: [{
                    label: 'Loss Ratio',
                    data: [
                        data_house_claims_to_premiums_ratio,
                        data_auto_claims_to_premiums_ratio,
                        data_life_claims_to_premiums_ratio,
                        data_health_claims_to_premiums_ratio
                    ],
                    backgroundColor: [
                        GREY_2,
                        GREY_2,
                        GREY_2,
                        GREY_2,
                    ],
                    borderColor: [
                        GREY_1,
                        GREY_1,
                        GREY_1,
                        GREY_1
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('combinedChart');
    if (!canvas) return;

    const policiesDataStr = canvas.getAttribute('data-new-policies-count-by-month');
    const claimsDataStr = canvas.getAttribute('data-new-claim-count-by-month');
    const policiesData = JSON.parse(policiesDataStr) || [];
    const claimsData = JSON.parse(claimsDataStr) || [];
    
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];
    
    const newPoliciesData = Array(12).fill(0);
    const newClaimsData = Array(12).fill(0);

    policiesData.forEach(([month, count]) => {
        newPoliciesData[month - 1] = count;
    });

    claimsData.forEach(([month, count]) => {
        newClaimsData[month - 1] = count;
    });

    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'New Policies Count',
                    data: newPoliciesData,
                    backgroundColor: GREEN_3_T,
                    borderColor: GREEN_3,
                    borderWidth: 1,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'New Claims Count',
                    data: newClaimsData,
                    backgroundColor: RED_Line_T,
                    borderColor: RED_Line,
                    borderWidth: 1,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            scales: {
                x: {
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: { display: true }
            }
        }
    });
});   

document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('combinedChartAllTime');
    if (!canvas) return;

    const policiesDataStr = canvas.getAttribute('data-all-policies-count-by-month');
    const claimsDataStr = canvas.getAttribute('data-all-claims-count-by-month');
    const policiesData = JSON.parse(policiesDataStr) || [];
    const claimsData = JSON.parse(claimsDataStr) || [];
    
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];
    
    const newPoliciesData = Array(12).fill(0);
    const newClaimsData = Array(12).fill(0);

    policiesData.forEach(([month, count]) => {
        newPoliciesData[month - 1] = count;
    });

    claimsData.forEach(([month, count]) => {
        newClaimsData[month - 1] = count;
    });

    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'New Policies Count',
                    data: newPoliciesData,
                    backgroundColor: GREEN_3_T,
                    borderColor: GREEN_3,
                    borderWidth: 1,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'New Claims Count',
                    data: newClaimsData,
                    backgroundColor: RED_Line_T,
                    borderColor: RED_Line,
                    borderWidth: 1,
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            scales: {
                x: {
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: { display: true }
            }
        }
    });
});   

// POLICIES
    
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('policyStatusChart');

    if (canvas) {
       
        var data_active_policy_count = canvas.getAttribute('data_active_policy_count');
        var data_expired_policy_count = canvas.getAttribute('data_expired_policy_count');

        var ctxStatus1 = canvas.getContext('2d');
        var policyStatusChart = new Chart(ctxStatus1, {
            type: 'bar',
            data: {
                labels: ['Active', 'Expired'],
                datasets: [{
                    label: 'Policy Status',
                    data: [
                        data_active_policy_count,
                        data_expired_policy_count
                    ],
                    backgroundColor: [GREEN_3, GREY_2],
                    hoverOffset: 4
                }]
            },
            options: {
                indexAxis: 'y',
                aspectRatio: 2, // Aspect ratio to make the pie chart a perfect circle
                responsive: false, // Ensuring the chart resizes within its container
                plugins: {
                    legend: {
                        display:false
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            beginAtZero: true,
                            callback: function(value) {
                                return value >= 1000 ? (value / 1000) + 'k' : value;
                            }
                        }
                    }
                }
            }
        });
    }
});

// New Policies by Month Chart

document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('newPoliciesByMonthChart');
    if (!canvas) return;

    const dataStr = canvas.getAttribute('data-new-policies-count-by-month');
    const data = JSON.parse(dataStr) || [];
    const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    const newPoliciesData = Array(12).fill(0);

    data.forEach(([month, count]) => {
        newPoliciesData[month - 1] = count;
    });

    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'New Policies Count',
                data: newPoliciesData,
                backgroundColor: GREEN_3_T,
                borderColor: GREEN_3,
                borderWidth: 1,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: false,
            scales: {
                x: {
                    grid: { display: false }
                },
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
});

// CLAIMS

document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('claimsByMonthChart');
    if (!canvas) return;

    
    const dataStr = canvas.getAttribute('data-new-claim-count-by-month');
    const data = JSON.parse(dataStr) || [];
    const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    const newClaimData = Array(12).fill(0);

    data.forEach(([month, count]) => {
        newClaimData[month - 1] = count;
    });

    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Claims Count',
                data: newClaimData,
                backgroundColor: RED_Line_T,
                borderColor: RED_Line,
                borderWidth: 1,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: false,
            scales: {
                x: { grid: { display: false } },
                y: { beginAtZero: true }
            },
            plugins: { legend: { display: false } }
        }
    });
});

