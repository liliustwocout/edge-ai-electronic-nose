// Alarm & Risk Decision Manager (4 Risk Levels)

export class AlarmManager {
  constructor() {
    this.currentLevel = 'Normal';
    this.alarmHistory = [];
    this.isAudioMuted = false;
    this.audioContext = null;
    this.isAcknowledged = false;
  }

  evaluateRisk(data) {
    const ppm = data.estimatedPpm;
    let level = 'Normal';
    let riskTheme = {
      level: 'Normal',
      color: '#10b981',
      bgLight: 'rgba(16, 185, 129, 0.22)',
      label: 'NORMAL'
    };

    // Tiêu chuẩn nồng độ an toàn H2S theo OSHA/NIOSH
    if (ppm >= 50.0) {
      level = 'Emergency';
      riskTheme = {
        level: 'Emergency',
        color: '#ef4444',
        bgLight: 'rgba(239, 68, 68, 0.35)',
        label: 'EMERGENCY'
      };
    } else if (ppm >= 10.0) {
      level = 'Hazardous';
      riskTheme = {
        level: 'Hazardous',
        color: '#f97316',
        bgLight: 'rgba(249, 115, 22, 0.3)',
        label: 'HAZARDOUS'
      };
    } else if (ppm >= 2.5) {
      level = 'Warning';
      riskTheme = {
        level: 'Warning',
        color: '#f59e0b',
        bgLight: 'rgba(245, 158, 11, 0.25)',
        label: 'WARNING'
      };
    }

    // Nếu trạng thái thay đổi hoặc có cảnh báo mới thì ghi log
    if (level !== this.currentLevel) {
      this.handleStateChange(this.currentLevel, level, data);
      this.currentLevel = level;
      this.isAcknowledged = false;
    }

    return { level, riskTheme };
  }

  handleStateChange(oldLevel, newLevel, data) {
    const timestamp = data.timestamp;
    const gas = data.gasName;
    const ppm = data.estimatedPpm;

    let message = '';
    if (newLevel === 'Emergency') {
      message = `CẢNH BÁO KHẨN CẤP: Phát hiện rò rỉ ${gas} nồng độ cao (${ppm} ppm)!`;
      this.playAlertTone(880, 0.5);
    } else if (newLevel === 'Hazardous') {
      message = `NGUY HẠI: Nồng độ ${gas} vượt ngưỡng an toàn (${ppm} ppm).`;
      this.playAlertTone(660, 0.3);
    } else if (newLevel === 'Warning') {
      message = `CẢNH BÁO SỚM: Xuất hiện dấu hiệu phát tán khí ${gas} (${ppm} ppm).`;
    } else {
      message = `Môi trường an toàn trở lại bình thường (${ppm} ppm).`;
    }

    const logEntry = {
      id: 'EVT-' + Math.floor(1000 + Math.random() * 9000),
      time: timestamp,
      level: newLevel,
      gas: gas,
      ppm: ppm,
      message: message,
      node: 'Node 1 (Compressor Area)'
    };

    this.alarmHistory.unshift(logEntry);
    if (this.alarmHistory.length > 20) {
      this.alarmHistory.pop();
    }

    this.updateLogTableUI();
  }

  playAlertTone(frequency, duration) {
    if (this.isAudioMuted) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!this.audioContext) {
        this.audioContext = new AudioCtx();
      }
      if (this.audioContext.state === 'suspended') {
        this.audioContext.resume();
      }

      const osc = this.audioContext.createOscillator();
      const gain = this.audioContext.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(frequency, this.audioContext.currentTime);

      gain.gain.setValueAtTime(0.12, this.audioContext.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);

      osc.connect(gain);
      gain.connect(this.audioContext.destination);

      osc.start();
      osc.stop(this.audioContext.currentTime + duration);
    } catch (e) {
      console.warn('Web Audio Playback muted or blocked by browser:', e);
    }
  }

  acknowledge() {
    this.isAcknowledged = true;
    const bar = document.getElementById('emergencyBar');
    if (bar) {
      bar.classList.remove('visible');
    }
  }

  updateLogTableUI() {
    const tbody = document.getElementById('alarmLogTableBody');
    if (!tbody) return;

    tbody.innerHTML = this.alarmHistory.map(entry => `
      <tr>
        <td><strong>${entry.time}</strong></td>
        <td><span class="log-badge ${entry.level.toLowerCase()}">${entry.level}</span></td>
        <td>${entry.node}</td>
        <td><strong>${entry.ppm}</strong> ppm</td>
        <td>${entry.message}</td>
      </tr>
    `).join('');
  }
}
