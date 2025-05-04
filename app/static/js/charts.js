class ChartCreator {
    constructor(canvasId, color, key) {
        this.canvasId = canvasId;
        this.color = color;
        this.key = key;
        this.chart = null;
    }

    createChart() {
        this.chart = new Chart(document.getElementById(this.canvasId), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    borderColor: this.color,
                    fill: false,
                }]
            },
            options: {
                scales: {
                    x: { display: false }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    updateChart(timestamps, data) {
        this.chart.data.labels = timestamps;
        this.chart.data.datasets[0].data = data;
        this.chart.update();
    }
}

export default ChartCreator;
