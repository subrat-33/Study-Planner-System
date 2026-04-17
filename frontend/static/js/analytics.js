// Analytics and Charts Script

document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    loadAnalyticsData();
});

async function loadAnalyticsData() {
    try {
        const data = await api.get('/progress/analytics');
        updateStatCards(data);
        renderCharts(data);
    } catch (error) {
        console.error('Failed to load analytics:', error);
        // Fallback with dummy data for demo if API not fully ready
        renderCharts(getDummyData());
    }
}

function updateStatCards(data) {
    if (data.total_hours) document.getElementById('total-hours').innerText = data.total_hours;
    if (data.avg_hours) document.getElementById('avg-hours').innerText = data.avg_hours;
    if (data.streak) document.getElementById('streak').innerText = data.streak;
    if (data.completion_rate) document.getElementById('completion-rate').innerText = data.completion_rate + '%';
}

function initCharts() {
    // Chart configurations
}

function renderCharts(data) {
    // 1. Hours Trend Chart
    const trendCtx = document.getElementById('hoursTrendChart').getContext('2d');
    new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: data.trend_labels || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Hours Studied',
                data: data.trend_data || [2, 4, 3, 5, 2, 6, 4],
                borderColor: '#4F46E5',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(79, 70, 229, 0.1)'
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    // 2. Subject Distribution
    const pieCtx = document.getElementById('subjectPieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'doughnut',
        data: {
            labels: data.subj_labels || ['DAA', 'CN', 'DBMS', 'OS'],
            datasets: [{
                data: data.subj_data || [30, 25, 20, 25],
                backgroundColor: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    // 3. Topic Completion
    const barCtx = document.getElementById('topicBarChart').getContext('2d');
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: data.subj_labels || ['DAA', 'CN', 'DBMS', 'OS'],
            datasets: [
                {
                    label: 'Completed',
                    data: data.completed_topics || [5, 3, 8, 2],
                    backgroundColor: '#10B981'
                },
                {
                    label: 'Remaining',
                    data: data.remaining_topics || [3, 4, 2, 5],
                    backgroundColor: '#E5E7EB'
                }
            ]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            scales: { x: { stacked: true }, y: { stacked: true } }
        }
    });
    // 4. Study Consistency (Radar/Polar chart)
    const consistencyCtx = document.getElementById('consistencyChart').getContext('2d');
    new Chart(consistencyCtx, {
        type: 'polarArea',
        data: {
            labels: data.subj_labels || ['DAA', 'CN', 'DBMS', 'OS'],
            datasets: [{
                label: 'Consistency Score',
                data: data.consistency_data || [85, 70, 90, 65],
                backgroundColor: [
                    'rgba(79, 70, 229, 0.5)',
                    'rgba(16, 185, 129, 0.5)',
                    'rgba(245, 158, 11, 0.5)',
                    'rgba(239, 68, 68, 0.5)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: { display: false }
                }
            }
        }
    });
}

function getDummyData() {
    return {
        total_hours: 42,
        avg_hours: 3.5,
        streak: 5,
        completion_rate: 65,
        trend_labels: ['Apr 1', 'Apr 2', 'Apr 3', 'Apr 4', 'Apr 5', 'Apr 6', 'Apr 7'],
        trend_data: [3, 4, 2, 5, 4, 6, 3],
        subj_labels: ['DAA', 'CN', 'DBMS', 'OS'],
        subj_data: [12, 10, 15, 5],
        completed_topics: [6, 4, 10, 2],
        remaining_topics: [4, 6, 2, 3],
        consistency_data: [80, 65, 95, 40]
    };
}
