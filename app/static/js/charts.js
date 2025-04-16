class ChartCreator {
    constructor(canvasId, label, color, key) {
        this.canvasId = canvasId;
        this.label = label;
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
                    label: this.label,
                    data: [],
                    borderColor: this.color,
                    fill: false,
                }]
            },
            options: {
                scales: {
                    x: { display: false }
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
