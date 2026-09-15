# Edge AI-Based Electronic Nose For Hydrogen Sulfide Leak Detection In Natural Gas Processing Plants

**Competition:** Advantech AIoT InnoWorks  
**Development Team:** TaskForce141  
**Academic Advisor:** Dr. Nguyen Dac Cu  
**Team Members:**  
1. Do Duc Khoi - Leader  
2. Le Pham Thanh Dat  
3. Vu Anh Kiet  

---

## Project Overview

Khí H2S Cực Độc Xuất Hiện Tại Các Mỏ Khí & Nhà Máy Lọc Hóa Dầu  
Đầu Báo Khí Cố Định Truyền Thống Thường Báo Động Muộn & Gây Báo Động Giả  
Hệ Thống E-Nose Kết Hợp Edge AI Xây Dựng Gas Fingerprint Của H2S  
Cảnh Báo Sớm Nguy Cơ Rò Rỉ Theo Động Học Time-Series  
Phân Cấp An Toàn 4 Cấp Độ: Normal, Warning, Hazardous, Emergency  
Truyền Thông Chống Nhiễu RS-485 Modbus RTU & Đồng Bộ WISE-IoT Cloud Qua MQTT  

---

## 5-Layer System Architecture

```
Application Layer: Web Dashboard - Operations Center
           ▲
           │ Internet MQTT / HTTPS
           ▼
Cloud Platform Layer: Advantech WISE-IoT Platform - Historical Storage, Analytics, Alarms
           ▲
           │ Internet MQTT Via Ethernet / Wi-Fi
           ▼
Edge AI Layer: Raspberry Pi 5 Gateway - Modbus Master, Filtering, Random Forest AI
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
Gas Leakage Tại Hiện Trường
           │
           ▼
Node ESP32 Sampling ADC & Nhiệt Ẩm
           │
           ▼
Modbus RTU Slave Đóng Gói Khung Truyền Qua RS-485
           │
           ▼
Raspberry Pi 5 Gateway Modbus Master Thu Thập Dữ Liệu
           │
           ├── Lọc Số EMA Filter & Bù Drift Nhiệt Ẩm
           ├── Trích Xuất Time-Series Feature Vector
           └── Chạy Edge AI Random Forest Model Nhận Dạng Gas Pattern & Classify Risk
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
  - Digital Filtering Bằng EMA Filter
  - Normalize Giá Trị Sensor So Với Clean Air Baseline
  - Temporal Sliding Window 20 Bước Thời Gian Cho Khảo Sát Động Học
- Edge AI Inference:
  - Multi-Task 1D-CNN Model Chạy Trên 4 Nhân Cortex-A76
  - Phân Tích Gas Fingerprint Matrix Tách Biệt H2S Leakage Với Background Odor
  - Real-Time Risk Classification 4 Level:
    - Normal: Safe Baseline Dưới 1.0 ppm
    - Warning: Early Leakage Từ 1.0 Đến 9.9 ppm, Alert Ca Trực
    - Hazardous: Exceed OSHA Limit Từ 10.0 Đến 49.9 ppm, Bật Siren & Strobe Light
    - Emergency: IDLH Danger Từ 50.0 ppm, Auto Shutdown Valve
- Fail-Safe Offline Mode: Local SQLite Logging & Cảnh Báo Hoạt Động Độc Lập 100% Khi Mất Network

### 4. Cloud Platform Layer - Cloud Synchronization & Analytics

- Gateway Publish Telemetry & Alert Event Qua MQTT Lên WISE-IoT
- WISE-IoT Platform:
  - Time-Series DB Lưu Trữ Lịch Sử
  - Device Health & Heartbeat Management
  - Alert Dispatch Qua Email

### 5. Application Layer - Visual Monitoring & Operations

- Web Dashboard:
  - Real-Time Industrial Dark Mode UI
  - Multi-Channel Time-Series Chart
  - Scenario Switching Giữa Các Kịch Bản Rò Rỉ Gas
- Operator Workflow: Định Vị Điểm Leak, Nhấn Acknowledge Để Log Response Time & Kích Hoạt Đội Safety Cô Lập Tuyến Ống

---

## Commands

```bash
pip install -r backend/requirements.txt
python -m backend.train
python -m backend.app

python -m http.server 8000
http://127.0.0.1:8000/dashboard/index.html
```