# Edge AI-Based Electronic Nose For Toxic Gas Detection In Industrial Plants

**Competition:** Advantech AIoT InnoWorks  
**Development Team:** TaskForce141  
**Academic Advisor:** Dr. Nguyen Dac Cu  
**Team Members:**  
1. Do Duc Khoi - Leader  
2. Le Pham Thanh Dat  
3. Vu Anh Kiet  

---

## Project Overview

Khí Độc H2S & NH3 Xuất Hiện Tại Các Mỏ Khí & Nhà Máy Lọc Hóa Dầu  
Đầu Báo Khí Cố Định Truyền Thống Thường Báo Động Muộn & Gây Báo Động Giả  
Hệ Thống E-Nose Kết Hợp Edge AI Xây Dựng Gas Fingerprint Của H2S & NH3  
Cảnh Báo Sớm Nguy Cơ Rò Rỉ Theo Động Học Time-Series  
Phân Cấp An Toàn 4 Cấp Độ: Normal, Warning, Hazardous, Emergency  
Truyền Thông Chống Nhiễu RS-485 Modbus RTU & Đồng Bộ WISE-IoT Cloud Qua MQTT  

---

## Detected Gases & Concentration Ranges

| Gas | Type | Concentrations | Risk Threshold |
|-----|------|---------------|----------------|
| **H2S** | Toxic (Lethal) | 1, 5, 10 ppm | ≥1 ppm Warning, ≥10 ppm Hazardous, ≥50 ppm Emergency |
| **NH3** | Irritant (Industrial) | 10, 50, 100 ppm | ≥25 ppm Warning, ≥50 ppm Hazardous, ≥100 ppm Emergency |
| **Clean Air** | Baseline | 0 ppm | Normal |

---

## Edge AI Model Performance

**Architecture:** RandomForest Dual-Mode (scikit-learn)  
**Validation:** Zero-Overlap Stratified Pulse Cross-Validation  

### Pulse-Level Model (Offline / High Accuracy)

Phân tích toàn bộ 250 điểm dữ liệu trong 60 giây mỗi pulse.

| Metric | Value |
|--------|-------|
| **Gas Classification Accuracy** | **95.76%** |
| **Concentration MAE** | 5.58 ppm |
| **Concentration R²** | 0.7947 |

### Window-Level Model (Real-Time Streaming)

Trích xuất feature từ sliding window 20 bước thời gian cho inference liên tục.

| Metric | Value |
|--------|-------|
| **Gas Classification Accuracy** | **94.97%** |
| **Concentration MAE** | 2.47 ppm |
| **Concentration R²** | 0.9333 |

### Per-Class Classification Report (Pulse Model)

| Gas | Precision | Recall | F1-Score | Support |
|-----|-----------|--------|----------|---------|
| Clean Air | 89.7% | 92.9% | 91.2% | 28 |
| H2S | 97.8% | 93.6% | 95.7% | 47 |
| NH3 | 97.8% | 100.0% | 98.9% | 44 |

### Top Feature Importance (RandomForest)

| Feature | Importance |
|---------|-----------|
| Std_V (Biến thiên tín hiệu) | 13.04% |
| Decay_Slope (Tốc độ suy giảm) | 11.70% |
| Rise_Slope (Tốc độ tăng) | 10.58% |
| Delta_V (Biên độ tín hiệu) | 9.43% |
| Peak_Time (Thời điểm đỉnh) | 7.52% |

---

## 5-Layer System Architecture

```
Application Layer: Web Dashboard - Operations Center (Dark Mode Industrial UI)
           ▲
           │ Internet MQTT / HTTPS
           ▼
Cloud Platform Layer: Advantech WISE-IoT Platform - Historical Storage, Analytics, Alarms
           ▲
           │ Internet MQTT Via Ethernet / Wi-Fi
           ▼
Edge AI Layer: Raspberry Pi 5 Gateway - Modbus Master, Filtering, RandomForest AI
           ▲
           │ RS-485 Bus Modbus RTU - STP Twisted Pair, 120 Ohm Termination
           ▼
Communication Layer: Daisy-Chain Bus: Node 1 ─── Node 2 ─── Node 3 ─── Node N
           ▲
           │
           ▼
Perception Layer: ESP32 Nodes + ZE03-H2S / MQ136, MQ135, DHT22 + IP65 Enclosure + 12V Power
```

---

## System Operating Workflow

Closed-Loop Operating Process Từ Hiện Trường Đến Operator:

```
Gas Leakage Tại Hiện Trường (H2S / NH3)
           │
           ▼
Node ESP32 Sampling ADC & Nhiệt Ẩm (250 samples / 60s per pulse)
           │
           ▼
Modbus RTU Slave Đóng Gói Khung Truyền Qua RS-485
           │
           ▼
Raspberry Pi 5 Gateway Modbus Master Thu Thập Dữ Liệu
           │
           ├── Lọc Số EMA Filter (α=0.2) & Bù Drift Nhiệt Ẩm
           ├── Trích Xuất Time-Series Feature Vector (20 statistical + anchor features)
           └── Chạy Edge AI RandomForest Model Nhận Dạng Gas Pattern & Classify Risk
           │
           ▼
Fail-Safe Decision Cảnh Báo Tại Biên Ngay Cả Khi Mất Network
           │
           ▼
Publish Telemetry & Event Qua MQTT Lên WISE-IoT Cloud → Display Trên Web Dashboard
```

### 1. Perception Layer - Field Data Acquisition

- Node Cảm Biến Bố Trí Tại Compressor Station, Throttle Valve, Storage Tank
- ESP32 Sampling Liên Tục Từ Sensor Array:
  - ZE03-H2S / MQ136: Đo Nồng Độ Target Gas H2S
  - MQ135: Đo Background Gas VOCs, Smoke, NH3 Nhận Diện Nền Khí Tạo Gas Fingerprint
  - DHT22: Bù Drift Nhiệt Ẩm Cho MOS Sensor
- ESP32 Lọc Tín Hiệu Sơ Cấp & Map Vào Modbus Holding Registers 16-Bit

### 2. Communication Layer - Industrial Anti-Interference Bus

- Tuyến Daisy-Chain Dọc Tuyến Ống Bằng Twisted Pair Shielded Cable RS-485
- Gắn 120 Ohm Termination Resistor Tại 2 Đầu Bus
- Modbus RTU Truyền Xa Hàng Trăm Mét, Chống EMI Noise Từ Động Cơ Lớn

### 3. Edge AI Layer - Edge Computing & AI Pattern Recognition

- Raspberry Pi 5 Làm Gateway Modbus Master Polling Chu Kỳ 1s → 2s
- Preprocessing Pipeline:
  - Digital Filtering Bằng EMA Filter (α=0.2)
  - Normalize Giá Trị Sensor So Với Clean Air Baseline
  - Temporal Sliding Window 20 Bước Thời Gian Cho Khảo Sát Động Học
- Edge AI Inference:
  - RandomForest Dual-Mode Model Chạy Trên 4 Nhân Cortex-A76
  - Pulse-Level: Phân Tích Toàn Bộ Pulse (250 points / 60s) → Gas Classification + ppm Estimation
  - Window-Level: Streaming Inference Từ 20-Step Sliding Window → Real-Time Detection
  - Phân Tích Gas Fingerprint Matrix Tách Biệt H2S / NH3 Leakage Với Clean Air
  - Real-Time Risk Classification 4 Level:
    - **Normal**: Safe Baseline - Dưới Ngưỡng Phát Hiện
    - **Warning**: Early Leakage - H2S ≥1 ppm Hoặc NH3 ≥25 ppm
    - **Hazardous**: Exceed OSHA PEL - H2S ≥10 ppm Hoặc NH3 ≥50 ppm
    - **Emergency**: IDLH Danger - H2S ≥50 ppm Hoặc NH3 ≥100 ppm
- Fail-Safe Offline Mode: Local SQLite Logging & Cảnh Báo Hoạt Động Độc Lập 100% Khi Mất Network

### 4. Cloud Platform Layer - Cloud Synchronization & Analytics

- Gateway Publish Telemetry & Alert Event Qua MQTT Lên WISE-IoT
- WISE-IoT Platform:
  - Time-Series DB Lưu Trữ Lịch Sử
  - Device Health & Heartbeat Management
  - Alert Dispatch Qua Email

### 5. Application Layer - Visual Monitoring & Operations

- Web Dashboard:
  - Real-Time Industrial Dark Mode UI (Tailwind CSS + Chart.js)
  - 6 KPI Cards: Concentration, Sensor S3, Predicted Gas, Horizon +20s, Safety Status, Model Accuracy
  - 4 Live Charts: Gas Probability Bar, S3 Waveform Line, Velocity/Kinetics Area, Classification Donut
  - RF Inference Latency Chart & AI Confidence Gauge
  - Hardware Status Monitoring: CPU, Memory, RS-485 Bus, MQTT Sync
  - 4 Scenario Modes: Field Scenario (Auto), H2S Lethal Leak, NH3 Industrial, Clean Air Baseline
  - Alarm System: Audio Tones, Alert Banners, Event Audit Log
  - CSV Export & Email Dispatch Simulation
- Operator Workflow: Định Vị Điểm Leak, Nhấn Acknowledge Để Log Response Time & Kích Hoạt Đội Safety Cô Lập Tuyến Ống

---

## Data Pipeline

### Raw Data Collection

Mỗi file CSV chứa dữ liệu cảm biến S3 (Rg/Ra) ghi trong 60 giây, mỗi pulse 250 điểm dữ liệu.

| File | Gas | Pulses |
|------|-----|--------|
| `data/h2s_sensor_1.csv` | H2S (1, 5, 10 ppm) | ~45 pulses |
| `data/nh3_sensor_1.csv` | NH3 (10, 50, 100 ppm) | ~40 pulses |
| `data/air_clean_sensor_1.csv` | Clean Air (0 ppm) | ~25 pulses |

### Data Cleaning (`clean_sensor_data.py`)

- Loại bỏ hardware spike artifacts (đường thẳng đột ngột do lỗi phần cứng ~30s)
- Áp dụng Savitzky-Golay smoothing filter
- Loại bỏ outlier pulses bằng IQR method
- Output: `*_clean.csv` files

### Model Training (`backend/train.py`)

- Feature Engineering: Statistical moments (mean, std, min, max, delta, slope) + anchor point sampling
- Dual-mode training: Pulse-level (offline) & Window-level (streaming)
- Validation: Zero-overlap stratified pulse cross-validation
- Artifacts: `model_gas.pkl`, `model_ppm.pkl`, `model_pulse_gas.pkl`, `model_pulse_ppm.pkl`

---

## Project Structure

```
AIoT/
├── README.md                          # Project documentation
├── clean_sensor_data.py               # Data cleaning pipeline
├── plot_sensors.py                    # Sensor data visualization
├── backend/
│   ├── app.py                         # FastAPI server + WebSocket streaming
│   ├── train.py                       # RandomForest dual-mode training
│   ├── gateway.py                     # Modbus RTU gateway
│   ├── requirements.txt               # Python dependencies
│   ├── classes.json                   # Model metadata & metrics
│   ├── model_gas.pkl                  # Window-level gas classifier
│   ├── model_ppm.pkl                  # Window-level ppm regressor
│   ├── model_pulse_gas.pkl            # Pulse-level gas classifier
│   ├── model_pulse_ppm.pkl            # Pulse-level ppm regressor
│   └── scaler.pkl                     # Feature scaler
├── dashboard/
│   ├── index.html                     # Industrial dark-mode dashboard (single-file SPA)
│   ├── gas_profiles.json              # Gas profile visualization data
│   ├── model_metrics.json             # Model performance metrics for UI
│   └── pulse_samples.json             # Sample pulse data for visualization
├── data/
│   ├── h2s_sensor_1.csv               # Raw H2S sensor data
│   ├── h2s_sensor_1_clean.csv         # Cleaned H2S data
│   ├── nh3_sensor_1.csv               # Raw NH3 sensor data
│   ├── nh3_sensor_1_clean.csv         # Cleaned NH3 data
│   ├── air_clean_sensor_1.csv         # Raw clean air data
│   └── air_clean_sensor_1_clean.csv   # Cleaned clean air data
└── docs/
    └── UseCase.md                     # Use case documentation
```

---

## Quick Start

### 1. Setup Environment

```bash
cd g:\Project\AIoT
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Clean Sensor Data (Optional - Already Cleaned)

```bash
python clean_sensor_data.py
```

### 3. Train Models

```bash
python -m backend.train
```

Expected output:
```
Pulse Classification Accuracy: 95.76%
Pulse Concentration MAE:       5.58 ppm (R2: 0.7947)
Window Real-Time Accuracy:     94.97%
Window ppm MAE:                2.47 ppm (R2: 0.9333)
```

### 4. Start Server & Dashboard

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8001
```

Open browser: **http://127.0.0.1:8001**

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Edge AI Model** | scikit-learn RandomForest (Classifier + Regressor) |
| **Backend Server** | FastAPI + Uvicorn (Python) |
| **Real-Time Comm** | WebSocket (streaming) + REST API |
| **Dashboard UI** | HTML5 + Tailwind CSS + Chart.js + Lucide Icons |
| **Data Processing** | Pandas + NumPy + SciPy (Savitzky-Golay) |
| **Hardware Gateway** | Raspberry Pi 5 + ESP32 + RS-485 Modbus RTU |
| **Cloud Platform** | Advantech WISE-IoT (MQTT) |
| **Sensor Array** | ZE03-H2S / MQ136 + MQ135 + DHT22 |