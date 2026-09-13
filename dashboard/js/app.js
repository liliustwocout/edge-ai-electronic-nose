// Main App Controller: Tailored to WISE-IoT / WISE-PaaS Layout

import { DataStreamEngine } from './data-stream.js';
import { ChartManager } from './charts.js';
import { AlarmManager } from './alarm.js';
import { PAPER_INFO } from './paper-data.js';

class App {
  constructor() {
    this.chartManager = new ChartManager();
    this.alarmManager = new AlarmManager();
    this.streamEngine = new DataStreamEngine((data) => this.onTelemetryReceived(data));
  }

  async init() {
    console.log('Initializing Advantech WISE-IoT Style Dashboard...');
    this.chartManager.init();
    this.setupEventListeners();
    this.initClock();

    const loaded = await this.streamEngine.init();
    if (!loaded) {
      console.warn('Failed to load sample dataset.');
    }
  }

  initClock() {
    const clockEl = document.getElementById('wiseClock');
    if (!clockEl) return;
    setInterval(() => {
      const now = new Date();
      const pad = (n) => String(n).padStart(2, '0');
      const timeStr = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())} UTC`;
      clockEl.innerText = timeStr;
    }, 1000);
  }

  setupEventListeners() {
    // Gas Selector Tabs
    const gasTabs = document.querySelectorAll('.gas-tab');
    gasTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        gasTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const selectedGas = tab.getAttribute('data-gas');
        this.switchGas(selectedGas);
      });
    });

    // Play/Pause Stream
    const btnPlayPause = document.getElementById('btnPlayPause');
    if (btnPlayPause) {
      btnPlayPause.addEventListener('click', () => {
        const isPlaying = this.streamEngine.togglePlay();
        btnPlayPause.innerText = isPlaying ? 'PAUSE' : 'RESUME';
      });
    }

    // Speed Multipliers
    const btnSpeed1x = document.getElementById('speed1x');
    const btnSpeed2x = document.getElementById('speed2x');
    if (btnSpeed1x && btnSpeed2x) {
      btnSpeed1x.addEventListener('click', () => {
        btnSpeed1x.classList.add('active');
        btnSpeed2x.classList.remove('active');
        this.streamEngine.setSpeed(1);
      });
      btnSpeed2x.addEventListener('click', () => {
        btnSpeed2x.classList.add('active');
        btnSpeed1x.classList.remove('active');
        this.streamEngine.setSpeed(2.5);
      });
    }

    // Acknowledge Alarm
    const btnAck = document.getElementById('btnAcknowledge');
    if (btnAck) {
      btnAck.addEventListener('click', () => {
        this.alarmManager.acknowledge();
        const banner = document.getElementById('wiseAlertBanner');
        if (banner) banner.classList.remove('visible');
      });
    }
  }

  switchGas(gasName) {
    this.chartManager.resetHistory();
    this.streamEngine.setGas(gasName);

    const gasTitle = document.getElementById('currentGasTitle');
    if (gasTitle) gasTitle.innerText = gasName;

    const paperInfo = PAPER_INFO.gasPerformance[gasName];
    if (paperInfo) {
      const rangeEl = document.getElementById('kpiRangeVal');
      if (rangeEl) rangeEl.innerText = paperInfo.range;
      const mapeEl = document.getElementById('kpiMapeVal');
      if (mapeEl) mapeEl.innerText = paperInfo.mape;
    }
  }

  onTelemetryReceived(data) {
    const { level, riskTheme } = this.alarmManager.evaluateRisk(data);

    // 1. Cập nhật 6 thẻ KPI rực rỡ chuẩn WISE-PaaS
    this.updateKpiRow(data, level);

    // 2. Cập nhật các biểu đồ
    this.chartManager.updateCharts(data, riskTheme);

    // 3. Cập nhật thanh trạng thái Server/Edge Gateway
    this.updateServerBars(data);

    // 4. Cập nhật bảng System Transaction List
    this.updateTransactionTable(data, level);

    // 5. Cảnh báo khẩn cấp
    const banner = document.getElementById('wiseAlertBanner');
    if (banner && !this.alarmManager.isAcknowledged) {
      if (level === 'Emergency') {
        banner.classList.add('visible');
        document.getElementById('alertGasName').innerText = data.gasName;
        document.getElementById('alertPpm').innerText = data.estimatedPpm;
      } else {
        banner.classList.remove('visible');
      }
    }
  }

  updateKpiRow(data, level) {
    // Card 1 (Green): Estimated Concentration
    const ppmVal = document.getElementById('kpiPpmVal');
    if (ppmVal) ppmVal.innerText = `${data.estimatedPpm} ppm`;

    // Card 2 (Orange): Peak Reactive Channel
    const peakVal = document.getElementById('kpiPeakSensorVal');
    if (peakVal) peakVal.innerText = `${data.mostReactiveSensor} (Peak)`;

    // Card 3 (Purple): Frame Index
    const frameVal = document.getElementById('kpiTotalSampleVal');
    if (frameVal) frameVal.innerText = `${data.frameIndex + 1} / 60`;

    // Card 4 (Blue): Target Range
    const info = PAPER_INFO.gasPerformance[data.gasName];
    if (info) {
      const rangeVal = document.getElementById('kpiRangeVal');
      if (rangeVal) rangeVal.innerText = info.range;
      const mapeVal = document.getElementById('kpiMapeVal');
      if (mapeVal) mapeVal.innerText = info.mape;
    }

    // Card 5 (Red): Risk Level
    const riskVal = document.getElementById('kpiRiskVal');
    if (riskVal) riskVal.innerText = level.toUpperCase();
  }

  updateServerBars(data) {
    // Giả lập tải tính toán Edge AI Cortex-A76 & Modbus Bus Load
    const cpuLoad = Math.min(95, Math.floor(35 + data.maxDelta * 1200));
    const memLoad = 38.5;
    const busLoad = Math.min(98, Math.floor(60 + (data.frameIndex % 15)));

    const cpuEl = document.getElementById('barCpuFill');
    const cpuTxt = document.getElementById('barCpuTxt');
    if (cpuEl && cpuTxt) {
      cpuEl.style.width = `${cpuLoad}%`;
      cpuTxt.innerText = `${cpuLoad}%`;
    }

    const busEl = document.getElementById('barBusFill');
    const busTxt = document.getElementById('barBusTxt');
    if (busEl && busTxt) {
      busEl.style.width = `${busLoad}%`;
      busTxt.innerText = `${busLoad}%`;
    }
  }

  updateTransactionTable(data, level) {
    const tbody = document.getElementById('wiseTxTableBody');
    if (!tbody) return;

    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${new Date().toISOString().slice(0,19).replace('T', ' ')}</td>
      <td>Node 1 (Compressor)</td>
      <td>Telemetry Ingestion</td>
      <td><span class="status-tag ${level.toLowerCase()}">${level}</span></td>
    `;

    tbody.insertBefore(row, tbody.firstChild);
    while (tbody.children.length > 8) {
      tbody.removeChild(tbody.lastChild);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new App();
  app.init();
});
