let timestamps = [];
let cpuUsage = [];
let ram = [];
let disk = [];
let netSent = [];
let netRecv = [];
let temperature = [];

const commonOptions = {
    scales: {
        x: {
            display: false
        }
    }
};

const cpuChart = new Chart(document.getElementById('cpuChart'), {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'CPU Usage (%)',
            data: cpuUsage,
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false,
        }]
    },
    options: commonOptions
});

const ramChart = new Chart(document.getElementById('ramChart'), {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'RAM Usage (%)',
            data: ram,
            borderColor: 'rgba(54, 162, 235, 1)',
            fill: false,
        }]
    },
    options: commonOptions
});

const diskChart = new Chart(document.getElementById('diskChart'), {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Disk Usage (%)',
            data: disk,
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false,
        }]
    },
    options: commonOptions
});

const netSentChart = new Chart(document.getElementById('netSentChart'), {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Network Sent (MB)',
            data: netSent,
            borderColor: 'rgba(153, 102, 255, 1)',
            fill: false,
        }]
    },
    options: commonOptions
});

const netRecvChart = new Chart(document.getElementById('netRecvChart'), {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Network Received (MB)',
            data: netRecv,
            borderColor: 'rgba(255, 159, 64, 1)',
            fill: false,
        }]
    },
    options: commonOptions
});

const temperatureChart = new Chart(document.getElementById('temperatureChart'), {
    type: 'line',
    data: {
        labels: timestamps,
        datasets: [{
            label: 'Temperature (°C)',
            data: temperature,
            borderColor: 'rgba(255, 205, 86, 1)',
            fill: false,
        }]
    },
    options: commonOptions
});

function fetchData() {
    fetch("/api/data")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            timestamps = data.timestamps;
            cpuUsage = data.cpu_usage;
            ram = data.ram;
            disk = data.disk;
            netSent = data.net_sent;
            netRecv = data.net_recv;
            temperature = data.temperature;

            cpuChart.data.labels = timestamps;
            cpuChart.data.datasets[0].data = cpuUsage;
            cpuChart.update();

            ramChart.data.labels = timestamps;
            ramChart.data.datasets[0].data = ram;
            ramChart.update();

            diskChart.data.labels = timestamps;
            diskChart.data.datasets[0].data = disk;
            diskChart.update();

            netSentChart.data.labels = timestamps;
            netSentChart.data.datasets[0].data = netSent;
            netSentChart.update();

            netRecvChart.data.labels = timestamps;
            netRecvChart.data.datasets[0].data = netRecv;
            netRecvChart.update();

            temperatureChart.data.labels = timestamps;
            temperatureChart.data.datasets[0].data = temperature;
            temperatureChart.update();

        })
        .catch(() => {
            console.error("Error fetching data");
        });
}

fetchData();
setInterval(fetchData, 60000);
