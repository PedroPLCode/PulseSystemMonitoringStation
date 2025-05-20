import ChartCreator from "../src/ChartCreator";

describe("ChartCreator", () => {
  beforeEach(() => {
    document.body.innerHTML = `<canvas id="myChart"></canvas>`;

    global.Chart.mockClear();
  });

  test("createChart initializes Chart instance with correct parameters", () => {
    const chartCreator = new ChartCreator("myChart", "red", "someKey");

    chartCreator.createChart();

    expect(global.Chart).toHaveBeenCalledTimes(1);
    expect(global.Chart).toHaveBeenCalledWith(document.getElementById("myChart"), expect.objectContaining({
      type: "line",
      data: expect.any(Object),
      options: expect.any(Object),
    }));

    expect(chartCreator.chart).not.toBeNull();
  });

  test("updateChart updates data and calls chart.update", () => {
    const chartCreator = new ChartCreator("myChart", "red", "someKey");
    chartCreator.createChart();

    const timestamps = ["2025-05-01", "2025-05-02"];
    const data = [10, 20];

    chartCreator.updateChart(timestamps, data);

    expect(chartCreator.chart.data.labels).toEqual(timestamps);
    expect(chartCreator.chart.data.datasets[0].data).toEqual(data);
    expect(chartCreator.chart.update).toHaveBeenCalledTimes(1);
  });
});
