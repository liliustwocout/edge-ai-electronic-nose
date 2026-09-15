# Edge AI Model Design & Risk Alert Logic - Raspberry Pi 5

**Project:** Edge AI-Based Electronic Nose For Hydrogen Sulfide Leak Detection  
**Layer:** Edge AI Layer - Layer 3  
**Hardware:** Raspberry Pi 5 - Cortex-A76  

---

## 1. Edge Pipeline

```
Modbus RTU Master Polling Telemetry
       │
       ▼
Data Preprocessing
  ├── Digital Filtering Qua EMA Filter
  ├── Drift Compensation Cho Nhiệt Độ & Độ Ẩm
  └── Time-Series Feature Extraction: Mean, Δ, Slope, Statistical Features (Mean, Std, Max, Min, Quartiles)
       │
       ▼
Edge AI Inference JSON Runtime
  ├── Gas Fingerprint Pattern Recognition
  ├── Anomaly & Leak Detection
  └── Risk Classification 4 Level
       │
       ▼
Decision & Alert Logic
  ├── Multi-Criteria Threshold & AI Confidence Check
  ├── Local Event Logging Vào SQLite Trên SSD
  └── Instant Alert Dispatch Qua Siren Cục Bộ & MQTT Lên WISE-IoT Cloud
```

---

## 2. Data Preprocessing

### 2.1. Filtering & Normalization

- EMA Filter Khử Nhiễu Dao Động Điện Áp & Luồng Gió Với Hệ Số Alpha 0.2
- Drift Compensation Hiệu Chuẩn Sai Lệch Nhiệt Ẩm Cho Cảm Biến MQ136 & MQ135

### 2.2. Time-Series Feature Extraction

- Sliding Window 30s Trích Xuất 3 Nhóm Đặc Trưng:
  - Instantaneous Values: H2S ppm, MQ136 ADC, MQ135 ADC, Nhiệt Độ, Độ Ẩm
  - Gradient ΔC / Δt: Tốc Độ Tăng Nồng Độ Chỉ Báo Rò Rỉ Đột Biến
  - Sensor Array Statistical Features (Mean, Std, Max, Min, Quartiles): Phân Biệt H2S Thực Sự Với Khí Nền VOCs

---

## 3. Edge AI Inference

### 3.1. Model Architecture

- Random Forest Model Tối Ưu Hóa Sang Định Dạng JSON
- Input: Vector K Đặc Trưng Trong Sliding Window
- Output: Leak Probability 0.0 Đến 1.0 & Risk Class 4 Level

### 3.2. 4 Risk Levels Standard

- Tiêu Chuẩn An Toàn OSHA & NIOSH Cho Khí H2S:

| Level | Status | Color | Threshold | System Action |
|---|---|---|---|---|
| Level 1 | Normal | Green | Dưới 1.0 ppm | Safe Baseline, Truyền Telemetry Định Kỳ |
| Level 2 | Warning | Yellow | 1.0 Đến 9.9 ppm | Rò Rỉ Sớm, Cảnh Báo Ca Trực |
| Level 3 | Hazardous | Orange | 10.0 Đến 49.9 ppm | Vượt Ngưỡng OSHA PEL, Bật Siren & Strobe Light, Yêu Cầu Mặt Nạ |
| Level 4 | Emergency | Red | Từ 50.0 ppm | Nguy Hiểm IDLH, Kích Hoạt Auto Shutdown Valve & Sơ Tán Khẩn Cấp |

---

## 4. Local Storage & Fail-Safe

- Local Database: SQLite Lưu Trên Raspberry Pi 5
- Dữ Liệu Lưu Trữ: Raw Sensor Logs, Inference History, System Alarms
- Fail-Safe Offline Mode: Toàn Bộ Suy Luận & Còi Báo Động Chạy Độc Lập 100% Khi Mất Mạng
- Offline Message Buffer: Tự Động Đồng Bộ Dữ Liệu Lên WISE-IoT Cloud Khi Có Mạng Trở Lại
