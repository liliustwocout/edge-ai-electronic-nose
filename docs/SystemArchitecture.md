# 5-Layer AIoT System Architecture

**Project:** Edge AI-Based Electronic Nose For Hydrogen Sulfide Leak Detection  
**Development Team:** TaskForce141 - Advantech AIoT InnoWorks  
**Architecture Model:** 5-Layer AIoT Industrial Safety Architecture  

---

## 1. System Architecture Diagram

```
Application Layer: Web Dashboard Operations Center & Safety Dispatch
       ▲
       │ Internet MQTT / HTTPS
       ▼
Cloud Platform Layer: Advantech WISE-IoT Platform - Historical Storage, Analytics, Alarms
       ▲
       │ Internet MQTT Via Ethernet / Wi-Fi
       ▼
Edge AI Layer: Raspberry Pi 5 Gateway - Modbus Master, Filtering, Random Forest AI
  ├── Data Acquisition: Modbus Master Engine Polling Node 1 Đến N
  ├── Data Preprocessing: EMA Filter & Drift Compensation
  ├── Edge AI Inference: Random Forest Model Nhận Dạng Gas Fingerprint
  ├── Decision Logic: Ngưỡng OSHA & Confidence Score Phân Cấp 4 Level
  └── Local Storage: Lưu Config, SQLite DB & Inference Logs Độc Lập
       ▲
       │ RS-485 Bus Modbus RTU - STP Twisted Pair, 120 Ohm Termination
       ▼
Communication Layer: Industrial Daisy-Chain Bus: Node 1 ─── Node 2 ─── Node N
       ▲
       │
       ▼
Perception Layer: ESP32 Nodes + ZE03-H2S / MQ136, MQ135, DHT22 + IP65 Enclosure + 12V Power
```

---

## 2. Detailed Functional Layers

### Layer 1: Perception Layer - Field Sensor Nodes

- Giám Sát Nồng Độ Khí Tại Van Đường Ống, Máy Nén Khí, Bồn Chứa
- Cấu Trúc Mỗi Node:
  - ESP32 MCU Xử Lý ADC 12-Bit & Đóng Gói Modbus Slave
  - ZE03-H2S / MQ136: Cảm Biến Chuyên Dụng Phát Hiện Khí H2S
  - MQ135: Cảm Biến Đa Năng Nhận Diện Khí Nền VOCs, Smoke, NH3
  - DHT22: Đo Nhiệt Độ & Độ Ẩm Để Bù Sai Số Cảm Biến MOS
  - Module RS-485 Transceiver Chuyển Đổi UART Sang Tín Hiệu Vi Sai
  - Vỏ Bảo Vệ IP65 Kèm Màng Lọc Khí PTFE Hydrophobic Chống Ăn Mòn H2S
  - Nguồn Cấp DC 12V Hoặc Pin LiFePO4 12V 5Ah Qua Buck Converter 5V

### Layer 2: Communication Layer - Industrial Network

- Chuẩn Vật Lý: RS-485 Cặp Dây Xoắn Chống Nhiễu STP Half-Duplex
- Giao Thức: Modbus RTU Truyền Xa Hàng Trăm Mét Kháng Nhiễu Động Cơ EMI
- Topology: Tuyến Bus Daisy-Chain Với 120 Ohm Termination Resistor Tại 2 Đầu Bus
- Giao Tiếp Gateway: Industrial USB-To-RS485 Hoặc RS-485 HAT Gắn Trên Raspberry Pi 5

### Layer 3: Edge AI Layer - Edge Computing & Gateway

- Phần Cứng: Raspberry Pi 5 Broadcom BCM2712 Quad-Core Cortex-A76
- Modbus Master Engine: Polling Định Kỳ 1s → 2s Đọc Holding Registers Node 1 Đến N
- Preprocessing: EMA Filter Khử Nhiễu & Trích Xuất Slope ΔC / Δt
- Edge AI Random Forest: Nhận Dạng Gas Fingerprint & Phân Cấp An Toàn 4 Level:
  - Normal: An Toàn Dưới 1.0 ppm
  - Warning: Rò Rỉ Sớm 1.0 Đến 9.9 ppm
  - Hazardous: Vượt Ngưỡng OSHA 10.0 Đến 49.9 ppm
  - Emergency: Nguy Hiểm Tính Mạng Từ 50.0 ppm
- Fail-Safe Decision: Kích Hoạt Còi Đèn Cục Bộ & Ghi Local SQLite Khi Mất Mạng
- MQTT Client: Đóng Gói JSON Telemetry & Alert Gửi Lên WISE-IoT Cloud

### Layer 4: Cloud Platform Layer - Advantech WISE-IoT

- Tiếp Nhận Telemetry & Alert Event Qua Secure MQTT Broker
- Time-Series Database Lưu Trữ Dữ Liệu Thời Gian Thực & Lịch Sử
- Analytics & Trends: Phân Tích Xu Hướng Nồng Độ Dài Hạn
- Device Management: Giám Sát Uptime & Device Health Heartbeat
- Email Alarm Dispatch: Gửi Cảnh Báo Khẩn Qua Email
- Export Reports: Tự Động Xuất Báo Cáo An Toàn Định Kỳ

### Layer 5: Application Layer - Visual Monitoring & Operations

- Web Dashboard Trung Tâm Điều Hành Hiển Thị Trực Quan Thời Gian Thực
- Multi-Channel Chart Biểu Diễn Diễn Biến Nồng Độ Khí Tức Thời
- Bản Đồ 2D Định Vị Chính Xác Vị Trí Node Phát Cảnh Báo Rò Rỉ
- Hệ Thống Còi Báo Động & Đèn Tháp Khu Vực
- Operator Workflow: Nhấn Acknowledge Xác Nhận Xử Lý & Kích Hoạt Đội Bảo Hộ Cô Lập Tuyến Ống
