async function fetchStats() {
    const res = await fetch('/api/stats');
    const data = await res.json();
    
    document.getElementById('countEvents').innerText = data.total_events;
    document.getElementById('countHigh').innerText = data.severity_counts.HIGH;
    document.getElementById('countMed').innerText = data.severity_counts.MEDIUM;

    const topIpContainer = document.getElementById('topIpList');
    topIpContainer.innerHTML = data.top_ips.map(item => `
        <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--glass-border)">
            <span>${item.ip}</span>
            <span style="color: var(--primary); font-weight: 700">${item.count} events</span>
        </div>
    `).join('') || '<p style="color: #64748b">No data yet</p>';

    updateCharts(data);
}

async function fetchAlerts() {
    const res = await fetch('/api/alerts');
    const data = await res.json();
    const container = document.getElementById('alertContainer');
    container.innerHTML = data.map(alert => `
        <div class="item">
            <div>
                <span class="severity-pill ${alert.severity}">${alert.severity}</span>
                <span style="font-weight: 600; margin-left:1rem">${alert.rule}</span>
                <p style="color: #94a3b8; margin-top: 0.25rem">${alert.message}</p>
            </div>
            <div style="color: #64748b; font-family: monospace">${alert.timestamp.split('T')[1].split('.')[0]}</div>
        </div>
    `).join('');
}

async function fetchEvents() {
    const res = await fetch('/api/events');
    const data = await res.json();
    const container = document.getElementById('eventContainer');
    container.innerHTML = data.map(event => `
        <div class="item">
            <div style="display: flex; gap: 1rem">
                <span style="color: var(--primary)">[${event.type}]</span>
                <span>${event.ip}</span>
                <span style="color: #94a3b8">${event.message}</span>
            </div>
            <div style="color: #64748b; font-family: monospace">${event.timestamp.split('T')[1].split('.')[0]}</div>
        </div>
    `).join('');
}

let severityChart, activityChart;

function updateCharts(data) {
    const sevCtx = document.getElementById('severityChart').getContext('2d');
    if (severityChart) severityChart.destroy();
    severityChart = new Chart(sevCtx, {
        type: 'doughnut',
        data: {
            labels: ['High', 'Medium'],
            datasets: [{
                data: [data.severity_counts.HIGH, data.severity_counts.MEDIUM],
                backgroundColor: ['#ef4444', '#f59e0b'],
                borderWidth: 0
            }]
        },
        options: { plugins: { legend: { position: 'bottom', labels: { color: '#f8fafc' } } } }
    });
}

// Initial fetch and poll
setInterval(() => {
    fetchStats();
    fetchAlerts();
    fetchEvents();
}, 2000);

fetchStats();
fetchAlerts();
fetchEvents();
