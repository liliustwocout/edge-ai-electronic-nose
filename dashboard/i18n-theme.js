/**
 * WISE-IoTSuite - Internationalization (i18n) & Theme (Light / Dark) Controller
 * Shared between index.html and experiment.html
 */

(function () {
  const translations = {
    vi: {
      // Common Navigation & Header
      navDashboard: "Dashboard Tổng Quan",
      navExperiment: "Thực Nghiệm Realtime",
      navBreadcrumb: "Cảm Biến Đơn MQ136 True Edge AI Gateway • TaskForce141",
      poweredBy: "Vận hành bởi",
      btnLangLabel: "VI",
      themeLight: "Sáng",
      themeDark: "Tối",
      backToDashboard: "Về Dashboard Tổng Quan",
      labTitle: "Phòng Thực Nghiệm",
      labSubtitle: "Cổng Nối Tiếp RS-485 (/dev/ttyUSB0)",
      rtdbConnected: "Đã Kết Nối RS-485",
      btnPause: "Tạm Dừng",
      btnResume: "Tiếp Tục",
      btnExportCsv: "Xuất CSV",
      btnDownloadCsv: "Tải Báo Cáo CSV",

      // Alarms & Status
      prognosticsSafe: "Dự Đoán AI: Baseline An Toàn",
      criticalAlarm: "Cảnh Báo Nguy Hiểm",
      hazardousWarning: "Cảnh Báo Độc Hại",
      detected: "Đã Phát Hiện",
      btnAcknowledge: "Xác Nhận Báo Động",
      normalStatus: "Bình Thường",
      warningStatus: "Cảnh Báo",
      hazardousStatus: "Nguy Hại",
      emergencyStatus: "Khẩn Cấp",

      // Modes & Filters
      modeLabel: "Kịch Bản:",
      modeFieldScenario: "Kịch Bản Thực Địa - Tự Động",
      modeH2SRun: "Rò Rỉ H2S Nguy Hiểm - 0 - 10 ppm",
      modeNH3Run: "Khí NH3 Công Nghiệp - 0 - 100 ppm",
      modeAirRun: "Không Khí Sạch Chuẩn",
      emaFilterOn: "Bộ Lọc EMA: Bật - α=0.2",
      emaFilterPipeline: "Bộ Lọc EMA: Luồng Edge AI",
      driftCompOn: "Bù Trôi (Drift): Bật",
      driftCompAuto: "Bù Trôi (Drift): Tự Động Edge AI",
      pause: "Tạm Dừng",
      resume: "Tiếp Tục",

      // KPI Cards
      kpiEstConcentration: "Nồng Độ Ước Tính",
      kpiSensorDvDt: "Cảm Biến MQ136 & dV/dt",
      kpiMlGas: "Khí Nhận Diện ML",
      kpiPredictedHorizon: "Dự Đoán Tương Lai - +20s",
      kpiSafetyStatus: "Trạng Thái An Toàn",
      kpiModelAccuracy: "Độ Chính Xác Mô Hình RF",
      kpiActiveScenario: "Kịch bản hoạt động:",
      kpiTteSafe: "TTE: Trạng Thái Ổn Định An Toàn",
      kpiRfDualMode: "RandomForest Song Song",
      kpiExtrapolated: "Quỹ Đạo Ngoại Suy",
      kpiThresholdOsha: "Kiểm Tra Ngưỡng OSHA PEL",
      kpiRfEdgeAi: "RandomForest • Edge AI",
      cleanAirSafe: "Không Khí Sạch - An Toàn",
      h2sToxicLeak: "Rò Rỉ H2S Độc Hại",
      nh3IrritantGas: "Khí Kích Thích NH3",

      // Chart Headers
      chartGasProb: "Xác Suất Khí",
      chartWaveCycle: "Dao Động Ký Chu Kỳ Sóng (250 Điểm / 60s)",
      chartCycleProgress: "Tiến trình chu kỳ:",
      chartClassification: "Phân Loại",
      chartHardwareStatus: "Trạng Thái Phần Cứng",
      chartLatency: "Độ Trễ Suy Luận RF",
      chartAuditLog: "Nhật Ký Sự Kiện",
      chartConfidence: "Độ Tin Cậy AI",
      chartScore: "Điểm",
      ghostTrace: "Chu kỳ trước (Ghost Trace)",
      sweepOverwrite: "Quét Đè (Sweep Overwrite)",

      // Hardware Status Items
      cpuUsage: "Tải CPU - RPi 5",
      memBuffer: "Bộ Nhớ - Edge Buffer",
      modelFootprint: "Kích Thước Mô Hình - RF",
      busLoad: "Tải Bus RS-485 Modbus RTU",
      mqttSync: "Đồng Bộ Đám Mây MQTT",

      // Audit Log Table
      tableTime: "Thời Gian",
      tableNode: "Nút Mạng",
      tableGas: "Khí Nhận Diện",
      tableStatus: "Trạng Thái",
      tableCycle: "Chu Kỳ",
      tableConcentration: "Nồng Độ (ppm)",
      tablePeakV1: "Đỉnh V1 (V)",
      tableMinV1: "Min V1 (V)",
      tableDeltaV: "Độ Lệch ΔV",
      tableAuc: "Diện Tích AUC",
      tableRisk: "Rủi Ro",
      waitingCycle: "Đang chờ hoàn thành chu kỳ sóng đầu tiên (WaveCycle #1)...",

      // Oscilloscope Controls (experiment.html)
      waveStyleContinuous: "Sóng: Liền Mạch",
      waveStyleSweep: "Sóng: Quét Đè",
      filterOn: "Lọc Nhiễu: Bật",
      filterOff: "Lọc Nhiễu: Tắt (Raw)",
      despikeOn: "Despike: Bật",
      despikeOff: "Despike: Tắt",
      ghostOn: "Ghost Trace: Bật",
      ghostOff: "Ghost Trace: Tắt",
      onlyV1: "Chỉ Xem Voltage 1 (MQ136)",
      showAllChannels: "Xem Cả 2 Kênh",
      perPointMode: "Theo Điểm (0-249)",
      perSecondMode: "Theo Giây (0-60s)",
      channelLabel: "Kênh:",
      telemetryLabel: "Dữ Liệu Đo:",
      v1Label: "Điện Áp 1 (MQ136)",
      v2Label: "Điện Áp 2 (Kênh Phụ)",
      ghostLegend: "V1 Chu Kỳ Trước",

      // Live Telemetry & Model Cards
      edgeAiModelCard: "Mô Hình Edge AI (Phân Loại Khí)",
      realtimeIdentifiedGas: "Khí Nhận Diện Thời Gian Thực",
      confidence: "Độ Tin Cậy",
      concentrationRisk: "Nồng Độ & Mức Độ Rủi Ro",
      cyclePeakWave: "Đỉnh Sóng Chu Kỳ (Max V1)",
      peakPoint: "Điểm đỉnh:",
      slidingFeatures: "Đặc Trưng Trượt (Sliding 20 pts)",
      safetyThresholds: "Ngưỡng an toàn: H2S < 1 ppm • NH3 < 25 ppm",
      hardwareTelemetry: "Dữ Liệu Mạch Thu (Telemetry)",
      targetGas: "Khí Mục Tiêu:",
      cycleHistoryLog: "Lịch Sử Các Chu Kỳ Sóng Đã Ghi (WaveCycle Log)",
      clearHistory: "Xóa Lịch Sử",
      cyclesCount: "chu kỳ",

      // Email Modal
      emailTitle: "Mô Phỏng Gửi Email Cảnh Báo WISE-IoT",
      emailTo: "Gửi đến:",
      emailSubject: "Tiêu đề:",
      emailTimestamp: "Thời gian:",
      emailLocation: "Vị trí:",
      emailAction: "Hành động yêu cầu:",
      emailSource: "Nguồn phát hiện:",

      // Tooltips & Descriptions
      tooltipWaveStyle: "Chế độ hiển thị: Sóng Liền Mạch theo chu kỳ hoặc Quét Đè Dao Động Ký",
      tooltipDespike: "Loại bỏ nhiễu gai phần cứng tại mốc ~điểm 125",
      tooltipGhost: "Hiển thị đường sóng chu kỳ trước để so sánh"
    },

    en: {
      // Common Navigation & Header
      navDashboard: "Overview Dashboard",
      navExperiment: "Realtime Experiment",
      navBreadcrumb: "Single-Sensor - MQ136 True Edge AI Gateway • TaskForce141",
      poweredBy: "Powered By",
      btnLangLabel: "EN",
      themeLight: "Light",
      themeDark: "Dark",
      backToDashboard: "Back to Dashboard",
      labTitle: "Experiment Lab",
      labSubtitle: "RS-485 Serial Port (/dev/ttyUSB0)",
      rtdbConnected: "RS-485 Connected",
      btnPause: "Pause",
      btnResume: "Resume",
      btnExportCsv: "Export CSV",
      btnDownloadCsv: "Download CSV Report",

      // Alarms & Status
      prognosticsSafe: "AI Prognostics: Safe Baseline",
      criticalAlarm: "Critical Alarm",
      hazardousWarning: "Hazardous Warning",
      detected: "Detected",
      btnAcknowledge: "Acknowledge Alarm",
      normalStatus: "Normal",
      warningStatus: "Warning",
      hazardousStatus: "Hazardous",
      emergencyStatus: "Emergency",

      // Modes & Filters
      modeLabel: "Mode:",
      modeFieldScenario: "Field Scenario - Auto",
      modeH2SRun: "H2S Lethal Leak - 0 - 10 ppm",
      modeNH3Run: "NH3 Industrial - 0 - 100 ppm",
      modeAirRun: "Clean Air Baseline",
      emaFilterOn: "EMA Filter: On - α=0.2",
      emaFilterPipeline: "EMA Filter: Edge AI Pipeline",
      driftCompOn: "Drift Comp: Active",
      driftCompAuto: "Drift Comp: Edge AI Auto",
      pause: "Pause",
      resume: "Resume",

      // KPI Cards
      kpiEstConcentration: "Estimated Concentration",
      kpiSensorDvDt: "Sensor MQ136 & dV/dt",
      kpiMlGas: "ML Predicted Gas",
      kpiPredictedHorizon: "Predicted Horizon - +20s",
      kpiSafetyStatus: "Safety Status",
      kpiModelAccuracy: "RF Model Accuracy",
      kpiActiveScenario: "Active Scenario:",
      kpiTteSafe: "TTE: Safe Stability",
      kpiRfDualMode: "RandomForest Dual-Mode",
      kpiExtrapolated: "Extrapolated Trajectory",
      kpiThresholdOsha: "Threshold Check OSHA PEL",
      kpiRfEdgeAi: "RandomForest • Edge AI",
      cleanAirSafe: "Clean Air - Safe",
      h2sToxicLeak: "H2S Toxic Leak",
      nh3IrritantGas: "NH3 Irritant Gas",

      // Chart Headers
      chartGasProb: "Gas Probability",
      chartWaveCycle: "WaveCycle Oscilloscope (250 Points / 60s)",
      chartCycleProgress: "Cycle Progress:",
      chartClassification: "Classification",
      chartHardwareStatus: "Hardware Status",
      chartLatency: "RF Inference Latency",
      chartAuditLog: "Event Audit Log",
      chartConfidence: "AI Confidence",
      chartScore: "Score",
      ghostTrace: "Previous Cycle (Ghost Trace)",
      sweepOverwrite: "Sweep Overwrite",

      // Hardware Status Items
      cpuUsage: "CPU Usage - RPi 5",
      memBuffer: "Memory - Edge Buffer",
      modelFootprint: "Model Footprint - RF",
      busLoad: "RS-485 Modbus RTU Load",
      mqttSync: "MQTT Cloud Sync",

      // Audit Log Table
      tableTime: "Time",
      tableNode: "Node",
      tableGas: "Identified Gas",
      tableStatus: "Status",
      tableCycle: "Cycle",
      tableConcentration: "Concentration (ppm)",
      tablePeakV1: "Peak V1 (V)",
      tableMinV1: "Min V1 (V)",
      tableDeltaV: "Delta ΔV",
      tableAuc: "AUC Area",
      tableRisk: "Risk",
      waitingCycle: "Waiting for the first wave cycle to complete (WaveCycle #1)...",

      // Oscilloscope Controls (experiment.html)
      waveStyleContinuous: "Wave: Continuous",
      waveStyleSweep: "Wave: Sweep Overwrite",
      filterOn: "Noise Filter: ON",
      filterOff: "Noise Filter: OFF (Raw)",
      despikeOn: "Despike: On",
      despikeOff: "Despike: Off",
      ghostOn: "Ghost Trace: On",
      ghostOff: "Ghost Trace: Off",
      onlyV1: "Only Voltage 1 (MQ136)",
      showAllChannels: "Show All Channels",
      perPointMode: "Per Point (0-249)",
      perSecondMode: "Per Second (0-60s)",
      channelLabel: "Channel:",
      telemetryLabel: "Telemetry:",
      v1Label: "Voltage 1 (MQ136)",
      v2Label: "Voltage 2 (Aux Channel)",
      ghostLegend: "Previous V1",

      // Live Telemetry & Model Cards
      edgeAiModelCard: "Edge AI Model (Gas Classification)",
      realtimeIdentifiedGas: "Realtime Identified Gas",
      confidence: "Confidence",
      concentrationRisk: "Concentration & Risk Level",
      cyclePeakWave: "Cycle Peak Wave (Max V1)",
      peakPoint: "Peak Point:",
      slidingFeatures: "Sliding Features (20 pts)",
      safetyThresholds: "Safety Thresholds: H2S < 1 ppm • NH3 < 25 ppm",
      hardwareTelemetry: "Hardware Telemetry Packet",
      targetGas: "Target Gas:",
      cycleHistoryLog: "Recorded WaveCycle History",
      clearHistory: "Clear History",
      cyclesCount: "cycles",

      // Email Modal
      emailTitle: "WISE-IoT Email Dispatch Simulation",
      emailTo: "To:",
      emailSubject: "Subject:",
      emailTimestamp: "Timestamp:",
      emailLocation: "Location:",
      emailAction: "Required Action:",
      emailSource: "Source:",

      // Tooltips & Descriptions
      tooltipWaveStyle: "Display Mode: Continuous Waveform or Oscilloscope Sweep Overwrite",
      tooltipDespike: "Filter out hardware spike anomaly at ~point 125",
      tooltipGhost: "Display previous cycle waveform for visual comparison"
    }
  };

  class I18nThemeManager {
    constructor() {
      this.currentLang = localStorage.getItem('wise_lang') || 'vi';
      this.currentTheme = localStorage.getItem('wise_theme') || 'dark';
    }

    init() {
      this.applyTheme(this.currentTheme, false);
      this.applyLanguage(this.currentLang);
      this.bindNavbarControls();
    }

    t(key) {
      const dict = translations[this.currentLang] || translations.vi;
      return dict[key] !== undefined ? dict[key] : key;
    }

    getLang() {
      return this.currentLang;
    }

    isLight() {
      return this.currentTheme === 'light';
    }

    setLanguage(lang) {
      if (lang !== 'vi' && lang !== 'en') lang = 'vi';
      this.currentLang = lang;
      localStorage.setItem('wise_lang', lang);
      this.applyLanguage(lang);
      window.dispatchEvent(new CustomEvent('appLanguageChanged', { detail: { lang } }));
    }

    toggleLanguage() {
      this.setLanguage(this.currentLang === 'vi' ? 'en' : 'vi');
    }

    applyLanguage(lang) {
      const dict = translations[lang] || translations.vi;

      // Update elements with data-i18n
      document.querySelectorAll('[data-i18n]').forEach((el) => {
        const key = el.getAttribute('data-i18n');
        if (dict[key] !== undefined) {
          el.textContent = dict[key];
        }
      });

      // Update elements with data-i18n-title
      document.querySelectorAll('[data-i18n-title]').forEach((el) => {
        const key = el.getAttribute('data-i18n-title');
        if (dict[key] !== undefined) {
          el.setAttribute('title', dict[key]);
        }
      });

      // Update elements with data-i18n-placeholder
      document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key] !== undefined) {
          el.setAttribute('placeholder', dict[key]);
        }
      });

      // Update Language Switcher UI if present
      const langBtn = document.getElementById('btnToggleLang');
      if (langBtn) {
        const flag = lang === 'vi' ? '🇻🇳' : '🇬🇧';
        const label = lang.toUpperCase();
        langBtn.innerHTML = `<span>${flag}</span> <span class="font-bold">${label}</span>`;
      }

      const langToggleText = document.getElementById('langToggleText');
      if (langToggleText) {
        langToggleText.textContent = lang === 'vi' ? 'VI' : 'EN';
      }
    }

    setTheme(theme) {
      if (theme !== 'light' && theme !== 'dark') theme = 'dark';
      this.currentTheme = theme;
      localStorage.setItem('wise_theme', theme);
      this.applyTheme(theme, true);
    }

    toggleTheme() {
      this.setTheme(this.currentTheme === 'dark' ? 'light' : 'dark');
    }

    applyTheme(theme, dispatch = true) {
      const root = document.documentElement;
      if (theme === 'light') {
        root.classList.add('light');
        root.classList.remove('dark');
        root.setAttribute('data-theme', 'light');
      } else {
        root.classList.add('dark');
        root.classList.remove('light');
        root.setAttribute('data-theme', 'dark');
      }

      // Update Theme button icon and tooltip
      const themeBtn = document.getElementById('btnToggleTheme');
      if (themeBtn) {
        const isL = theme === 'light';
        const iconName = isL ? 'sun' : 'moon';
        const titleText = isL ? (this.currentLang === 'vi' ? 'Giao diện Sáng' : 'Light Mode') : (this.currentLang === 'vi' ? 'Giao diện Tối' : 'Dark Mode');
        themeBtn.setAttribute('title', titleText);
        themeBtn.innerHTML = `<i data-lucide="${iconName}" class="w-4 h-4 ${isL ? 'text-amber-500' : 'text-sky-300'}"></i>`;
        if (window.lucide) {
          window.lucide.createIcons();
        }
      }

      if (dispatch) {
        window.dispatchEvent(
          new CustomEvent('appThemeChanged', {
            detail: { theme, isLight: theme === 'light' }
          })
        );
      }
    }

    bindNavbarControls() {
      const langBtn = document.getElementById('btnToggleLang');
      if (langBtn) {
        langBtn.addEventListener('click', () => this.toggleLanguage());
      }

      const themeBtn = document.getElementById('btnToggleTheme');
      if (themeBtn) {
        themeBtn.addEventListener('click', () => this.toggleTheme());
      }
    }
  }

  // Expose global singleton
  window.wiseApp = new I18nThemeManager();

  // Auto-init on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.wiseApp.init());
  } else {
    window.wiseApp.init();
  }
})();
