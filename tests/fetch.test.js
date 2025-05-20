import fetchData from '../src/fetchData';
import ChartCreator from '../src/charts.js';

jest.mock('../src/charts.js');
describe('fetchData', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div id="cpuUsageValue"></div>
      <div id="ramUsageValue"></div>
      <div id="diskUsageValue"></div>
      <div id="netSentValue"></div>
      <div id="netRecvValue"></div>
      <div id="temperatureValue"></div>
      <div id="temperatureAverageValue"></div>
      <div id="cpuAverageValue"></div>
      <div id="ramAverageValue"></div>
      <canvas id="cpuChart"></canvas>
      <canvas id="ramChart"></canvas>
      <canvas id="diskChart"></canvas>
      <canvas id="netSentChart"></canvas>
      <canvas id="netRecvChart"></canvas>
      <canvas id="temperatureChart"></canvas>
    `;

    ChartCreator.mockClear();
    ChartCreator.prototype.createChart = jest.fn();
    ChartCreator.prototype.updateChart = jest.fn();

    global.fetch = jest.fn();
  });

  test('poprawnie przetwarza i wyświetla dane', async () => {
    const fakeData = {
      timestamps: [
        new Date(Date.now() - 5 * 60 * 1000).toISOString(),
        new Date().toISOString()
      ],
      cpu_usage: [10, 20],
      ram: [30, 40],
      disk: [50, 60],
      net_sent: [70, 80],
      net_recv: [90, 100],
      temperature: [60, 70],
      temperature_limit: 65,
    };

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve(fakeData),
    });

    await fetchData();

    expect(ChartCreator).toHaveBeenCalledTimes(6);

    expect(ChartCreator.prototype.createChart).toHaveBeenCalledTimes(6);
    expect(ChartCreator.prototype.updateChart).toHaveBeenCalledTimes(6);

    expect(document.getElementById('cpuUsageValue').textContent).toBe('20.00%');
    expect(document.getElementById('ramUsageValue').textContent).toBe('40.00%');
    expect(document.getElementById('diskUsageValue').textContent).toBe('60.00%');
    expect(document.getElementById('netSentValue').textContent).toBe('80.00 MB');
    expect(document.getElementById('netRecvValue').textContent).toBe('100.00 MB');
    expect(document.getElementById('temperatureValue').textContent).toBe('70°C');
    expect(document.getElementById('temperatureAverageValue').textContent).toBeCloseTo((65), 2); // average around 65

    expect(document.getElementById('temperatureValue').className).toBe('text-danger'); // 70 > 65
    expect(document.getElementById('temperatureAverageValue').className).toBe('text-success'); // avg < 65

    expect(document.getElementById('cpuAverageValue').textContent).toBe('15.00%');
    expect(document.getElementById('ramAverageValue').textContent).toBe('35.00%');
  });

  test('loguje błąd jeśli data.error istnieje', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ error: 'Some error' }),
    });

    await fetchData();

    expect(consoleErrorSpy).toHaveBeenCalledWith('Some error');

    consoleErrorSpy.mockRestore();
  });

  test('loguje błąd przy fetch rejection', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    fetch.mockRejectedValueOnce(new Error('Fetch failed'));

    await fetchData();

    expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching data');

    consoleErrorSpy.mockRestore();
  });
});
