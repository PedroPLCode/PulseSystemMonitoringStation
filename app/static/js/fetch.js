import ChartCreator from './charts.js';

function calculateAverage(dataArray, timestamps) {
    const now = Date.now();
    const tenMinutesAgo = now - (10 * 60 * 1000);

    const recentValues = dataArray.filter((value, index) => {
        const timestamp = new Date(timestamps[index]).getTime();
        return timestamp >= tenMinutesAgo;
    });

    if (recentValues.length === 0) return 0;

    const sum = recentValues.reduce((a, b) => a + b, 0);
    return (sum / recentValues.length);
}

function fetchData() {
    fetch("/api/data")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            const { timestamps } = data;
            const chartData = [
                { id: 'cpuChart', label: 'CPU Usage (%)', color: 'rgba(255, 99, 132, 1)', key: 'cpu_usage' },
                { id: 'ramChart', label: 'RAM Usage (%)', color: 'rgba(54, 162, 235, 1)', key: 'ram' },
                { id: 'diskChart', label: 'Disk Usage (%)', color: 'rgba(75, 192, 192, 1)', key: 'disk' },
                { id: 'netSentChart', label: 'Network Sent (MB)', color: 'rgba(153, 102, 255, 1)', key: 'net_sent' },
                { id: 'netRecvChart', label: 'Network Received (MB)', color: 'rgba(255, 159, 64, 1)', key: 'net_recv' },
                { id: 'temperatureChart', label: 'Temperature (°C)', color: 'rgba(255, 205, 86, 1)', key: 'temperature' }
            ];

            chartData.forEach(({ id, label, color, key }) => {
                const chart = new ChartCreator(id, label, color, key);
                chart.createChart();
                chart.updateChart(timestamps, data[key]);
            });

            // Aktualizacja wartości
            const currentTemp = data.temperature[data.temperature.length - 1];
            const avgTemp = calculateAverage(data.temperature, timestamps);

            document.getElementById('cpuUsageValue').textContent = `${data.cpu_usage[data.cpu_usage.length - 1].toFixed(2)}%`;
            document.getElementById('ramUsageValue').textContent = `${data.ram[data.ram.length - 1].toFixed(2)}%`;
            document.getElementById('diskUsageValue').textContent = `${data.disk[data.disk.length - 1].toFixed(2)}%`;
            document.getElementById('netSentValue').textContent = `${data.net_sent[data.net_sent.length - 1].toFixed(2)} MB`;
            document.getElementById('netRecvValue').textContent = `${data.net_recv[data.net_recv.length - 1].toFixed(2)} MB`;

            const temperatureValueEl = document.getElementById('temperatureValue');
            const temperatureAverageValueEl = document.getElementById('temperatureAverageValue');

            temperatureValueEl.textContent = `${currentTemp}°C`;
            temperatureAverageValueEl.textContent = `${avgTemp.toFixed(2)}°C`;

            temperatureValueEl.className = currentTemp > 75 ? 'text-danger' : 'text-success';
            temperatureAverageValueEl.className = avgTemp > 75 ? 'text-danger' : 'text-success';

            document.getElementById('cpuAverageValue').textContent = `${calculateAverage(data.cpu_usage, timestamps).toFixed(2)}%`;
            document.getElementById('ramAverageValue').textContent = `${calculateAverage(data.ram, timestamps).toFixed(2)}%`;

        })
        .catch(() => {
            console.error("Error fetching data");
        });
}

export default fetchData;
