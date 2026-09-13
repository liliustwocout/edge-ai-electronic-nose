// Data Stream Engine: Load and Stream Multi-gas E-Nose Samples

export class DataStreamEngine {
  constructor(onDataCallback) {
    this.onDataCallback = onDataCallback;
    this.datasets = null;
    this.activeGas = 'H2S';
    this.currentIndex = 0;
    this.isPlaying = true;
    this.speedMs = 1200; // Tốc độ cập nhật (mỗi tick 1.2s)
    this.timer = null;
    this.historyLength = 20;
    this.history = [];
  }

  async init() {
    try {
      const response = await fetch('./data/gases_sample.json');
      this.datasets = await response.json();
      console.log('Loaded gases datasets:', Object.keys(this.datasets));
      this.start();
      return true;
    } catch (err) {
      console.error('Failed to load gases sample dataset:', err);
      return false;
    }
  }

  setGas(gasName) {
    if (this.datasets && this.datasets[gasName]) {
      this.activeGas = gasName;
      this.currentIndex = 0;
      this.history = []; // Reset lịch sử đồ thị khi chuyển loại khí
      this.emitCurrentTick();
    }
  }

  start() {
    if (this.timer) clearInterval(this.timer);
    this.isPlaying = true;
    this.timer = setInterval(() => {
      this.tick();
    }, this.speedMs);
    this.emitCurrentTick();
  }

  pause() {
    this.isPlaying = false;
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.start();
    }
    return this.isPlaying;
  }

  setSpeed(multiplier) {
    this.speedMs = 1200 / multiplier;
    if (this.isPlaying) {
      this.start();
    }
  }

  tick() {
    if (!this.datasets || !this.datasets[this.activeGas]) return;

    const gasData = this.datasets[this.activeGas];
    const totalRows = gasData.rows.length;

    this.currentIndex = (this.currentIndex + 1) % totalRows;
    this.emitCurrentTick();
  }

  emitCurrentTick() {
    if (!this.datasets || !this.datasets[this.activeGas]) return;

    const gasData = this.datasets[this.activeGas];
    const rawRow = gasData.rows[this.currentIndex];
    const sensors = gasData.sensors; // ['S1', 'S2', ..., 'S8']

    // Chuẩn bị vector cảm biến
    const sensorValues = {};
    sensors.forEach((name, idx) => {
      sensorValues[name] = rawRow[idx];
    });

    // Tính toán độ lệch tương đối so với baseline 1.0
    // Khí H2S thường kích thích phản ứng S2 giảm mạnh hoặc S5/S4 tăng
    let maxDelta = 0;
    let mostReactiveSensor = 'S1';
    sensors.forEach(s => {
      const delta = Math.abs(sensorValues[s] - 1.0);
      if (delta > maxDelta) {
        maxDelta = delta;
        mostReactiveSensor = s;
      }
    });

    // Quy đổi nồng độ ppm ước lượng theo phản ứng cảm biến
    let estimatedPpm = 0;
    if (this.activeGas === 'H2S') {
      // Dựa trên mức độ nhạy của ma trận khí với H2S
      estimatedPpm = Math.max(0.2, (maxDelta * 1250) + (Math.sin(this.currentIndex / 5) * 0.4));
    } else {
      estimatedPpm = Math.max(0.5, (maxDelta * 950) + 1.2);
    }

    const payload = {
      gasName: this.activeGas,
      frameIndex: this.currentIndex,
      totalFrames: gasData.rows.length,
      timestamp: new Date().toLocaleTimeString(),
      sensors: sensorValues,
      rawRow: rawRow,
      mostReactiveSensor: mostReactiveSensor,
      maxDelta: maxDelta,
      estimatedPpm: Number(estimatedPpm.toFixed(2)),
      // Giả lập thông số môi trường DHT22 (28-31°C, 65-72% RH)
      temperature: Number((29.5 + Math.sin(this.currentIndex / 8) * 1.5).toFixed(1)),
      humidity: Number((68.0 + Math.cos(this.currentIndex / 8) * 3.0).toFixed(1))
    };

    if (this.onDataCallback) {
      this.onDataCallback(payload);
    }
  }
}
