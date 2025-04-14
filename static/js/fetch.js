import ChartCreator from './charts.js';

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

            document.getElementById('cpuUsageValue').textContent = `${data.cpu_usage[data.cpu_usage.length - 1]}%`;
            document.getElementById('ramUsageValue').textContent = `${data.ram[data.ram.length - 1]}%`;
            document.getElementById('diskUsageValue').textContent = `${data.disk[data.disk.length - 1]}%`;
            document.getElementById('netSentValue').textContent = `${data.net_sent[data.net_sent.length - 1]} MB`;
            document.getElementById('netRecvValue').textContent = `${data.net_recv[data.net_recv.length - 1]} MB`;
            document.getElementById('temperatureValue').textContent = `${data.temperature[data.temperature.length - 1]}°C`;
            
        })
        .catch(() => {
            console.error("Error fetching data");
        });
}

export default fetchData;
