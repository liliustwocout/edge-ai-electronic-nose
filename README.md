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
Cảnh Báo Sớm Nguy Cơ Rò Rỉ Theo Động Học Time-Series & Chu Kỳ Sóng WaveCycle  
Phân Cấp An Toàn 4 Cấp Độ: Normal, Warning, Hazardous, Emergency  
Truyền Thông Chống Nhiễu RS-485 Modbus RTU & Đồng Bộ Firebase Realtime DB / WISE-IoT Cloud  

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

Phân tích toàn bộ 250 điểm dữ liệu trong 60 giây mỗi pulse (WaveCycle).

| Metric | Value |
|--------|-------|
| **Gas Classification Accuracy** | **94.18%** |
| **Concentration MAE** | **3.93 ppm** |
| **Concentration R²** | **0.8534** |

### Window-Level Model (Real-Time Streaming)

Trích xuất feature từ sliding window 20 bước thời gian cho inference liên tục.

| Metric | Value |
|--------|-------|
| **Gas Classification Accuracy** | **94.71%** |
| **Concentration MAE** | 5.22 ppm |
| **Concentration R²** | 0.7525 |

### Per-Class Classification Report (Pulse Model)

| Gas | Precision | Recall | F1-Score | Support |
|-----|-----------|--------|----------|---------|
| Clean Air | 89.7% | **98.5%** | 93.9% | 133 |
| H2S | **96.0%** | 86.4% | 90.9% | 110 |
| NH3 | **98.3%** | **96.6%** | **97.4%** | 118 |
| **Total / Weighted Avg** | **94.4%** | **94.2%** | **94.1%** | **361** |

### Top Feature Importance (RandomForest)

| Feature | Importance | Ý Nghĩa Vật Lý |
|---------|-----------|----------------|
| **Delta_V** | 12.63% | Biên độ chênh lệch điện áp cực đại ($V_{max} - V_{min}$) |
| **Anchor_18s** | 10.17% | Điện áp tức thời tại mốc 18 giây (giai đoạn tăng đỉnh) |
| **Peak_Time** | 8.64% | Thời điểm cảm biến đạt giá trị cực đại |
| **Decay_Slope** | 8.43% | Tốc độ suy giảm điện áp khi giải hấp phụ |
| **Anchor_55s** | 6.64% | Điện áp cuối chu kỳ đo mức độ hồi phục |
| **Anchor_12s** | 6.33% | Tốc độ đáp ứng sớm khi khí vừa tiếp xúc |
| **Max_V** | 6.13% | Điện áp cực đại tuyệt đối |

---

## 5-Layer System Architecture

```
Application Layer: Web Dashboard (Operations Center & Live WaveCycle Oscilloscope)
           ▲
           │ Internet WebSocket / Firebase RTDB / HTTPS
           ▼
Cloud Platform Layer: Advantech WISE-IoT Platform & Firebase Realtime Database
           ▲
           │ Internet MQTT / SSE Stream Via Ethernet / Wi-Fi
           ▼
Edge AI Layer: Raspberry Pi 5 Gateway - Modbus Master, Filtering, RandomForest AI
           ▲
           │ RS-485 Bus Modbus RTU - STP Twisted Pair, 120 Ohm Termination
           ▼
Communication Layer: Daisy-Chain Bus: Node 1 ─── Node 2 ─── Node 3 ─── Node N
           ▲
           │
           ▼
Perception Layer: ESP32 Nodes + Sensor Array (MQ136 / ZE03-H2S, MQ135, DHT22)
```

---

## System Operating Workflow

Closed-Loop Operating Process Từ Hiện Trường Đến Operator:

```
Gas Leakage Tại Hiện Trường (H2S / NH3)
           │
           ▼
Node ESP32 Sampling ADC & Nhiệt Ẩm (250 samples / 60s per WaveCycle)
           │
           ▼
Modbus RTU Slave Đóng Gói Khung Truyền Qua RS-485 / Firebase RTDB
           │
           ▼
Raspberry Pi 5 Gateway Thu Thập Dữ Liệu
           │
           ├── Lọc Số EMA Filter (α=0.2) & Khử Gai Hardware Despike
           ├── Bù Drift Nhiệt Ẩm (compFactor theo DHT22)
           ├── Trích Xuất Time-Series Feature Vector (Sliding Window & Full Pulse)
           └── Chạy Edge AI RandomForest Model Nhận Dạng Gas Pattern & Classify Risk
           │
           ▼
Fail-Safe Decision Cảnh Báo Tại Biên Ngay Cả Khi Mất Network
           │
           ▼
Publish Telemetry & Event Qua MQTT / WebSocket Lên Dashboard & Cloud
```

### 1. Perception Layer - Field Data Acquisition

- Node Cảm Biến Bố Trí Tại Compressor Station, Throttle Valve, Storage Tank
- ESP32 Sampling Liên Tục Từ Sensor Array:
  - **MQ136 / ZE03-H2S**: Đo Nồng Độ Target Gas H2S
  - **MQ135**: Đo Background Gas VOCs, Smoke, NH3 Nhận Diện Nền Khí Tạo Gas Fingerprint
  - **DHT22**: Bù Drift Nhiệt Ẩm Cho Cảm Biến Bán Dẫn MOS
- ESP32 Lọc Tín Hiệu Sơ Cấp & Map Vào Modbus Holding Registers 16-Bit

### 2. Communication Layer - Industrial Anti-Interference Bus

- Tuyến Daisy-Chain Dọc Tuyến Ống Bằng Twisted Pair Shielded Cable RS-485
- Gắn 120 Ohm Termination Resistor Tại 2 Đầu Bus
- Modbus RTU Truyền Xa Hàng Trăm Mét, Chống EMI Noise Từ Động Cơ Lớn

### 3. Edge AI Layer - Edge Computing & AI Pattern Recognition

- Raspberry Pi 5 Làm Gateway Modbus Master Polling Chu Kỳ 1s → 2s
- Preprocessing Pipeline:
  - Digital Filtering Bằng EMA Filter ($\alpha=0.2$)
  - Bù Trôi Nhiệt Độ / Độ Ẩm: $\text{compFactor} = 1.0 + 0.0035 \times (T - 25.0) + 0.0015 \times (H - 60.0)$
  - Hardware Despike Filter: Tự động phát hiện và nội suy làm mượt gai xung phần cứng tại điểm ~125
  - Temporal Sliding Window 20 Bước Thời Gian Cho Khảo Sát Động Học
- Edge AI Inference:
  - **RandomForest Dual-Mode Model** Chạy Trên 4 Nhân Cortex-A76
  - **Pulse-Level**: Phân Tích Toàn Bộ Pulse (250 points / 60s) $\rightarrow$ Gas Classification + ppm Estimation
  - **Window-Level**: Streaming Inference Từ 20-Step Sliding Window $\rightarrow$ Real-Time Detection
  - Phân Tích Gas Fingerprint Matrix Tách Biệt H2S / NH3 Leakage Với Clean Air
  - Real-Time Risk Classification 4 Level:
    - **Normal**: Safe Baseline - Dưới Ngưỡng Phát Hiện
    - **Warning**: Early Leakage - H2S ≥1 ppm Hoặc NH3 ≥25 ppm
    - **Hazardous**: Exceed OSHA PEL - H2S ≥10 ppm Hoặc NH3 ≥50 ppm
    - **Emergency**: IDLH Danger - H2S ≥50 ppm Hoặc NH3 ≥100 ppm
- Fail-Safe Offline Mode: Lưu trữ Local CSV/SQLite & Cảnh Báo Hoạt Động Độc Lập 100% Khi Mất Network

### 4. Cloud Platform Layer - Cloud Synchronization & Analytics

- Gateway Publish Telemetry & Alert Event Qua MQTT Lên WISE-IoT & Firebase Realtime Database
- Đồng Bộ 2 Chiều: Cập Nhật Trạng Thái Thiết Bị, Phân Tích Lịch Sử, Dispatch Alert Qua Email

### 5. Application Layer - Visual Monitoring & Operations

Hệ thống cung cấp **2 giao diện web chuyên biệt**:

#### A. Main Operations Dashboard (`dashboard/index.html`)

- **Real-Time Industrial Dark Mode UI**: Thiết kế giao diện công nghiệp chuẩn SCADA (Tailwind CSS + Chart.js + Lucide Icons).
- **6 KPI Cards**: Concentration (ppm), Sensor S3 Voltage & Velocity Slope (%/s), Target Gas Classification, Projected +20s Horizon, Risk Safety Level, Model Accuracy & Confidence.
- **Biểu Đồ Trực Quan Thời Gian Thực**:
  - **Gas Probability Bar**: Xác suất phân loại tức thời từ mô hình Random Forest (Clean Air, H2S, NH3).
  - **WaveCycle Oscilloscope (250 Points / 60s)**: Biểu đồ dao động ký tích hợp chu kỳ sóng 250 điểm, cơ chế **Sweep Overwrite (chạy đè dữ liệu cũ)**, hiển thị vệt sóng chu kỳ trước (**Ghost Trace**), con trỏ phát sáng tại điểm quét hoạt động, tự động đổi màu theo trạng thái cảnh báo (*Normal / Warning / Hazardous / Emergency*), thanh tiến trình chu kỳ 0–100% và chỉ số `Point: X/249 (Xs)`.
  - **Classification Donut**: Tỉ lệ nhận diện thành phần khí.
  - **AI Confidence Gauge & RF Inference Latency Chart**: Đánh giá độ trễ suy luận (~2-4 ms).
- **Hardware Status Monitoring**: Giám sát CPU RPi 5, Memory Buffer, RS-485 Bus Traffic, MQTT Cloud Sync.
- **4 Scenario Modes**:
  - `Field Industrial Scenario (Auto)`: Kịch bản liên hoàn 4 giai đoạn (*Baseline $\rightarrow$ H2S Leakage $\rightarrow$ Recovery $\rightarrow$ NH3 Exhaust*).
  - `H2S Lethal Leak Run (0 - 10 ppm)`: Kiểm thử phản ứng rò rỉ khí H2S.
  - `NH3 Industrial Run (0 - 100 ppm)`: Kiểm thử phơi nhiễm NH3 công nghiệp.
  - `Clean Air Baseline (Ambient)`: Kiểm tra đường nền sạch.
- **Hệ Thống Báo Động & Vận Hành**: Âm thanh cảnh báo (Web Audio API), Alert Banner khẩn cấp, Bảng Audit Log, Xuất CSV và Giả lập gửi Email Dispatch tới đội an toàn nhà máy.

#### B. Live Hardware Experiment Dashboard (`dashboard/experiment.html`)

- **Oscilloscope WaveCycle Trực Tiếp Từ Phần Cứng**: Kết nối trực tiếp qua **Firebase Realtime Database** (SSE Stream) hoặc WebSocket Gateway.
- **Dual-Sensor Monitoring**: Giám sát đồng thời 2 kênh cảm biến **Voltage 1 (MQ135)** và **Voltage 2 (MQ136)**.
- **Real-Time Despike Filter**: Bật/tắt bộ lọc loại bỏ gai phần cứng tại mốc ~điểm 125.
- **Ghost Trace Comparison**: Bật/tắt đường sóng chu kỳ trước để đối chiếu sai lệch đáp ứng.
- **Chế Độ Hiển Thị**: Chuyển đổi giữa *Per Point (0–249)* và *Per Second (0–60s)*; kiểu sóng *Liền Mạch (Continuous)* hoặc *Quét Đè (Sweep Overwrite)*.
- **WaveCycle History Log**: Tự động lưu bảng lịch sử các chu kỳ sóng đã hoàn thành (*Cycle #, Max V1, Min V1, $\Delta V$, AUC, Peak Point, Risk*).
- **Xuất Dữ Liệu Thực Nghiệm**: Tải báo cáo CSV cho từng gói tin thô (*Raw Packets CSV*) hoặc từng chu kỳ hoàn chỉnh (*Cycles Report CSV*).

---

## Data Pipeline

### Raw Data Collection

Dữ liệu được thu thập từ mảng cảm biến phần cứng thực tế (sensor array), ghi dưới dạng các tập tin Excel đa sheet hoặc CSV trong 60 giây, mỗi pulse/WaveCycle gồm 250 điểm dữ liệu:

| File Nguồn Thực Nghiệm | Gas | Số Lượng Pulses Hợp Lệ | Phân Bố Nồng Độ |
|------------------------|-----|------------------------|-----------------|
| `data/clean_air_sensor_1.xlsx` | Clean Air (Baseline) | **133 pulses** | 0 ppm ($V_{baseline} \approx 0.005 - 0.03\text{ V}$) |
| `data/h2s_sensor_1.xlsx` | H2S (1, 5, 10 ppm) | **110 pulses** | Pulses 1–37: 1 ppm, 38–74: 5 ppm, 75–111: 10 ppm |
| `data/nh3_1_sensor_1.xlsx` | NH3 (10, 50, 100 ppm) | **118 pulses** | Pulses 1–42: 10 ppm, 43–84: 50 ppm, 85–126: 100 ppm |

### Data Cleaning (`clean_sensor_data.py`)

- Tự động nạp trực tiếp dữ liệu từ các file Excel/CSV thô.
- Loại bỏ hardware spike artifacts (bước nhảy điện áp đột ngột do xung chuyển kênh phần cứng tại điểm ~125 bằng nội suy Cubic Spline).
- Áp dụng bộ lọc Savitzky-Golay smoothing filter (`window=9, polyorder=2`) để làm mượt mà vẫn bảo toàn biên độ cực đại.
- Loại bỏ các pulse lỗi hoặc ngoại lai bằng thống kê IQR và khoảng cách MAE so với median profile.
- Output: `data/air_clean_sensor_1_clean.csv`, `data/h2s_sensor_1_clean.csv`, `data/nh3_sensor_1_clean.csv`.

### Model Training (`backend/train.py`)

- **Feature Engineering**: Statistical moments (mean, std, min, max, delta, slope, AUC) kết hợp 10 điểm anchor points dọc chu kỳ 60s.
- **Dual-Mode Architecture**:
  - **Pulse-level**: Phân tích toàn chu kỳ 250 điểm (60s) $\to$ Gas Classification + ppm Regression.
  - **Window-level**: Streaming inference từ cửa sổ trượt 20 điểm ($\Delta t = 800\text{ms}$).
- **Validation**: Zero-overlap stratified pulse 5-fold cross-validation.
- **Artifacts Sinh Ra**: `model_gas.pkl`, `model_ppm.pkl`, `model_pulse_gas.pkl`, `model_pulse_ppm.pkl`, `scaler.pkl`, `gas_profiles.json`, `pulse_samples.json`, `classes.json`, `metrics.json`.

---

## Project Structure

```
AIoT/
├── README.md                          # Tài liệu tổng quan dự án
├── clean_sensor_data.py               # Pipeline làm sạch dữ liệu & khử gai phần cứng
├── plot_sensors.py                    # Script trực quan hóa phổ sóng cảm biến
├── backend/
│   ├── app.py                         # FastAPI server, REST API & WebSocket gateways (/stream, /ws/live_experiment, /predict)
│   ├── train.py                       # Huấn luyện mô hình RandomForest Dual-Mode & trích xuất profile
│   ├── gateway.py                     # Modbus RTU gateway đọc dữ liệu RS-485
│   ├── firebase.py                    # Dịch vụ Firebase RTDB SSE client, live buffer & CSV recorder
│   ├── requirements.txt               # Danh sách thư viện Python phụ thuộc
│   ├── classes.json                   # Metadata phân lớp và cấu hình model
│   ├── metrics.json                   # Chỉ số đánh giá mô hình (Accuracy, MAE, R², Confusion Matrix)
│   ├── model_gas.pkl                  # Window-level classifier (RandomForest)
│   ├── model_ppm.pkl                  # Window-level ppm regressor (RandomForest)
│   ├── model_pulse_gas.pkl            # Pulse-level classifier (RandomForest)
│   ├── model_pulse_ppm.pkl            # Pulse-level ppm regressor (RandomForest)
│   └── scaler.pkl                     # Feature scaler
├── dashboard/
│   ├── index.html                     # Web Dashboard vận hành chính (Song ngữ Anh-Việt, Dark/Light mode)
│   ├── experiment.html                # Web Dashboard thực nghiệm dao động ký WaveCycle & E-Nose trực tiếp
│   ├── theme.css                      # Hệ thống CSS theme (Dark/Light mode, độ tương phản cao, SCADA industrial)
│   ├── i18n-theme.js                  # Quản lý đa ngôn ngữ (VI/EN) & chuyển đổi giao diện sáng/tối tự động lưu trữ
│   ├── gas_profiles.json              # Dữ liệu đường cong đáp ứng trung bình & độ lệch chuẩn từng loại khí
│   ├── model_metrics.json             # Chỉ số huấn luyện phục vụ hiển thị trên giao diện
│   └── pulse_samples.json             # Tập mẫu WaveCycle tiêu biểu dùng cho đối chiếu dạng sóng
├── data/
│   ├── clean_air_sensor_1.xlsx        # File Excel thô đo Clean Air
│   ├── air_clean_sensor_1_clean.csv   # Dữ liệu Clean Air sau làm sạch & khử gai (133 pulses)
│   ├── h2s_sensor_1.xlsx              # File Excel thô đo H2S
│   ├── h2s_sensor_1_clean.csv         # Dữ liệu H2S sau làm sạch & khử gai (110 pulses)
│   ├── nh3_1_sensor_1.xlsx            # File Excel thô đo NH3
│   ├── nh3_sensor_1_clean.csv         # Dữ liệu NH3 sau làm sạch & khử gai (118 pulses)
│   ├── CleanAir_live.csv              # Dữ liệu stream thực nghiệm trực tiếp từ Firebase
│   ├── H2S_live.csv                   # Dữ liệu H2S stream thực nghiệm
│   └── NH3_live.csv                   # Dữ liệu NH3 stream thực nghiệm
└── docs/
    ├── DEPLOYMENT_PI3.md              # [MỚI] Hướng dẫn chi tiết triển khai lên Raspberry Pi 3 qua Tailscale
    ├── OPERATING_SCENARIOS.md         # [MỚI] Đặc tả 4 kịch bản vận hành & hướng dẫn đổi kịch bản
    ├── EdgeAI.md                      # Tài liệu thiết kế mô hình Edge AI & kiểm chứng
    ├── SystemArchitecture.md          # Tài liệu kiến trúc 5 tầng của hệ thống
    ├── Modbus.md                      # Chuẩn giao tiếp RS-485 Modbus RTU
    ├── ENose.md                       # Nguyên lý mũi điện tử & sensor array
    ├── WISEIoT.md                     # Tích hợp nền tảng đám mây Advantech WISE-IoT
    └── UseCase.md                     # Tài liệu kịch bản sử dụng chi tiết
```

---

## Quick Start

### 1. Huấn Luyện & Khởi Chạy Local (Máy tính cá nhân)

```bash
# 1. Cài đặt môi trường
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt

# 2. Làm sạch dữ liệu và huấn luyện mô hình
python clean_sensor_data.py
python -m backend.train

# 3. Khởi chạy FastAPI Gateway
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8001
```

Truy cập Dashboard: [http://127.0.0.1:8001/dashboard/index.html](http://127.0.0.1:8001/dashboard/index.html)

### 2. Triển Khai & Vận Hành Trên Raspberry Pi 3 (Qua Tailscale)

Hệ thống đã được đóng gói và cấu hình dịch vụ tự động trên Raspberry Pi 3:
- **Địa chỉ Tailscale:** `100.72.0.24` (SSH: `pi@100.72.0.24`)
- **Dịch vụ chạy nền:** `aiot-gateway.service` (Systemd)

```bash
# Đăng nhập vào Pi 3 qua Tailscale
ssh pi@100.72.0.24

# Quản lý dịch vụ trên Pi
sudo systemctl status aiot-gateway.service   # Kiểm tra trạng thái
sudo systemctl restart aiot-gateway.service  # Khởi động lại dịch vụ
journalctl -u aiot-gateway.service -f        # Xem log thời gian thực
```

Mở trình duyệt truy cập trực tiếp từ bất kỳ máy nào trong mạng Tailscale:
- **Dashboard Vận Hành:** [http://100.72.0.24:8001/dashboard/index.html](http://100.72.0.24:8001/dashboard/index.html)
- **Thực Nghiệm Phần Cứng:** [http://100.72.0.24:8001/dashboard/experiment.html](http://100.72.0.24:8001/dashboard/experiment.html)
- **Kiểm Tra Trạng Thái API:** [http://100.72.0.24:8001/health](http://100.72.0.24:8001/health)

*(Xem hướng dẫn đầy đủ tại [docs/DEPLOYMENT_PI3.md](file:///g:/Project/AIoT/docs/DEPLOYMENT_PI3.md) và [docs/OPERATING_SCENARIOS.md](file:///g:/Project/AIoT/docs/OPERATING_SCENARIOS.md))*

---

## Technology Stack

| Thành Phần | Công Nghệ Sử Dụng |
|------------|-------------------|
| **Edge AI Model** | scikit-learn RandomForest (Classifier + Regressor), Dual-Mode (Pulse & Window) |
| **Backend Server** | FastAPI + Uvicorn (Asynchronous Python) |
| **Real-Time Streaming** | WebSocket (`/stream`, `/ws/live_experiment`) + Firebase Realtime Database (SSE) |
| **Dashboard UI** | HTML5 + Vanilla CSS + Tailwind CSS (CDN) + Chart.js + Lucide Icons |
| **Data Processing** | Pandas + NumPy + SciPy (Savitzky-Golay filter & Cubic Spline Interpolation) |
| **Hardware Gateway** | Raspberry Pi 3 Model B (Cortex-A53, RAM 1GB) & Raspberry Pi 5 + ESP32 Nodes |
| **Industrial Bus** | RS-485 Modbus RTU (Daisy-Chain Topology) |
| **Cloud & Mesh Network** | Tailscale VPN Mesh, Advantech WISE-IoT (MQTT) & Firebase Realtime Database |
| **Sensor Array** | MQ136 / ZE03-H2S ($H_2S$) + MQ135 (VOCs/$NH_3$) + DHT22 (Nhiệt/Ẩm) |
