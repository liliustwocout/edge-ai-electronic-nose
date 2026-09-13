// Chart Manager: Tailored for Advantech WISE-IoT / WISE-PaaS Layout

export class ChartManager {
  constructor() {
    this.barChart = null;
    this.lineTrendChart = null;
    this.areaNetworkChart = null;
    this.donutBrowserChart = null;
    this.radarFingerprintChart = null;
    this.gaugeChart = null;
    this.timeLabels = [];
    this.maxPoints = 12;
  }

  init() {
    this.initBarChart();
    this.initLineTrendChart();
    this.initAreaNetworkChart();
    this.initDonutChart();
    this.initGaugeChart();
  }

  // 1. Cột Real-time activity (như hình mẫu: Bar Chart màu Cyan với đường target vàng)
  initBarChart() {
    const ctx = document.getElementById('barActivityChart').getContext('2d');
    const sampleLabels = ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'];
    const sampleData = [450, 720, 950, 840, 1120, 980, 1420, 890];

    this.barChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sampleLabels,
        datasets: [{
          label: 'Gas Intensity Level',
          data: sampleData,
          backgroundColor: '#00d2ff',
          barPercentage: 0.55
        }, {
          type: 'line',
          label: 'Threshold PEL (Target)',
          data: [600, 600, 600, 600, 600, 600, 600, 600],
          borderColor: '#facc15',
          borderDash: [5, 5],
          borderWidth: 2,
          pointRadius: 0,
          fill: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#8fa3bf', boxWidth: 10, font: { size: 10 } }
          }
        },
        scales: {
          x: {
            grid: { color: '#132238' },
            ticks: { color: '#64748b', font: { size: 9 } }
          },
          y: {
            grid: { color: '#132238' },
            ticks: { color: '#64748b', font: { size: 9 } }
          }
        }
      }
    });
  }

  // 2. Page view / Multi-sensor trend (Line chart nhiều màu như hình A, B, C, D)
  initLineTrendChart() {
    const ctx = document.getElementById('lineTrendChart').getContext('2d');
    const sensors = ['S1', 'S2', 'S6', 'S8'];
    const colors = ['#34d399', '#facc15', '#38bdf8', '#818cf8'];

    const datasets = sensors.map((s, idx) => ({
      label: s,
      data: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
      borderColor: colors[idx],
      backgroundColor: 'transparent',
      borderWidth: 1.8,
      pointRadius: 3,
      tension: 0.3
    }));

    this.lineTrendChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#8fa3bf', boxWidth: 8, font: { size: 10 } }
          }
        },
        scales: {
          x: {
            grid: { color: '#132238' },
            ticks: { color: '#64748b', font: { size: 9 } }
          },
          y: {
            grid: { color: '#132238' },
            ticks: { color: '#64748b', font: { size: 9 } },
            suggestedMin: 0.98,
            suggestedMax: 1.02
          }
        }
      }
    });
  }

  // 3. Area Chart: Upload and download / Dynamic Gas Flow & Ratio
  initAreaNetworkChart() {
    const ctx = document.getElementById('areaNetworkChart').getContext('2d');

    this.areaNetworkChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'],
        datasets: [{
          label: 'Sensor Signal (Rg)',
          data: [9.8, 8.5, 10.2, 10.5, 11.2, 12.8, 14.5],
          borderColor: '#06b6d4',
          backgroundColor: 'rgba(6, 182, 212, 0.35)',
          fill: true,
          tension: 0.4,
          pointRadius: 2
        }, {
          label: 'Baseline Clean Air (Ra)',
          data: [7.2, 9.4, 7.8, 8.2, 9.0, 9.5, 10.0],
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.2)',
          fill: true,
          tension: 0.4,
          pointRadius: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#8fa3bf', boxWidth: 8, font: { size: 10 } }
          }
        },
        scales: {
          x: {
            grid: { color: '#132238' },
            ticks: { color: '#64748b', font: { size: 9 } }
          },
          y: {
            grid: { color: '#132238' },
            ticks: { color: '#64748b', font: { size: 9 } }
          }
        }
      }
    });
  }

  // 4. Donut Chart: Ma trận tỷ lệ phản ứng 8 kênh (Using browser statistics phong cách)
  initDonutChart() {
    const ctx = document.getElementById('donutArrayChart').getContext('2d');

    this.donutBrowserChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['S1-S2 (H2S Target)', 'S3-S4', 'S5-S6 (Reducing)', 'S7-S8 (Oxidizing)'],
        datasets: [{
          data: [46, 28, 18, 8],
          backgroundColor: ['#38bdf8', '#60a5fa', '#93c5fd', '#bfdbfe'],
          borderWidth: 2,
          borderColor: '#0d1829'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#8fa3bf', boxWidth: 8, font: { size: 9 } }
          }
        }
      }
    });
  }

  // 5. Gauge Chart: Đồng hồ bán nguyệt phong cách WISE-PaaS
  initGaugeChart() {
    const ctx = document.getElementById('gaugeProcessChart').getContext('2d');

    this.gaugeChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Score', 'Remaining'],
        datasets: [{
          data: [91, 9],
          backgroundColor: ['#10b981', '#1e293b'],
          circumference: 180,
          rotation: 270,
          borderWidth: 0,
          cutout: '78%'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        }
      }
    });
  }

  updateCharts(data, riskTheme) {
    if (!this.lineTrendChart || !this.areaNetworkChart) return;

    // 1. Cập nhật Line Trend Chart với các kênh cảm biến
    if (this.timeLabels.length >= this.maxPoints) {
      this.timeLabels.shift();
      this.lineTrendChart.data.datasets.forEach(ds => ds.data.shift());
    }

    this.timeLabels.push(data.timestamp);
    this.lineTrendChart.data.labels = this.timeLabels;

    const sensorKeys = ['S1', 'S2', 'S6', 'S8'];
    sensorKeys.forEach((key, idx) => {
      if (this.lineTrendChart.data.datasets[idx]) {
        this.lineTrendChart.data.datasets[idx].data.push(data.sensors[key]);
      }
    });
    this.lineTrendChart.update();

    // 2. Cập nhật Area Chart
    if (this.areaNetworkChart.data.datasets[0].data.length >= this.maxPoints) {
      this.areaNetworkChart.data.datasets[0].data.shift();
      this.areaNetworkChart.data.datasets[1].data.shift();
      this.areaNetworkChart.data.labels.shift();
    }
    this.areaNetworkChart.data.labels.push(data.timestamp);
    this.areaNetworkChart.data.datasets[0].data.push(Number((data.estimatedPpm * 1.2).toFixed(1)));
    this.areaNetworkChart.data.datasets[1].data.push(Number((10.0).toFixed(1)));
    this.areaNetworkChart.update();

    // 3. Cập nhật Donut Chart tỷ trọng
    if (this.donutBrowserChart) {
      const s1_s2 = (Math.abs(data.sensors.S1 - 1) + Math.abs(data.sensors.S2 - 1)) * 1000 + 10;
      const s3_s4 = (Math.abs(data.sensors.S3 - 1) + Math.abs(data.sensors.S4 - 1)) * 1000 + 8;
      const s5_s6 = (Math.abs(data.sensors.S5 - 1) + Math.abs(data.sensors.S6 - 1)) * 1000 + 6;
      const s7_s8 = (Math.abs(data.sensors.S7 - 1) + Math.abs(data.sensors.S8 - 1)) * 1000 + 4;
      this.donutBrowserChart.data.datasets[0].data = [s1_s2, s3_s4, s5_s6, s7_s8];
      this.donutBrowserChart.update();
    }

    // 4. Cập nhật Gauge Chart (AI Confidence)
    if (this.gaugeChart) {
      const score = Math.min(99, Math.floor(88 + data.maxDelta * 700));
      this.gaugeChart.data.datasets[0].data = [score, 100 - score];
      
      let gaugeColor = '#10b981';
      if (score > 95) gaugeColor = '#ef4444';
      else if (score > 90) gaugeColor = '#f59e0b';
      this.gaugeChart.data.datasets[0].backgroundColor[0] = gaugeColor;
      this.gaugeChart.update();

      const gaugeNum = document.getElementById('gaugeDisplayNumber');
      if (gaugeNum) gaugeNum.innerText = score;
    }
  }

  resetHistory() {
    this.timeLabels = [];
    if (this.lineTrendChart) {
      this.lineTrendChart.data.labels = [];
      this.lineTrendChart.data.datasets.forEach(ds => ds.data = []);
      this.lineTrendChart.update();
    }
  }
}
