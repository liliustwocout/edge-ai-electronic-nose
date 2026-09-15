# Use Case & Technical Specification - Advantech AIoT InnoWorks

**Competition:** Advantech AIoT InnoWorks  
**Team Name:** TaskForce141  
**Academic Advisor:** Dr. Nguyen Dac Cu  
**Team Members:**  
1. Do Duc Khoi - Leader  
2. Le Pham Thanh Dat - Member  
3. Vu Anh Kiet - Member  

---

## 1. Project Background & Rationale

- Khí H2S Cực Độc Xuất Hiện Phổ Biến Tại Mỏ Khí Tự Nhiên & Nhà Máy Lọc Hóa Dầu
- Fixed Gas Detector Truyền Thống Thường Báo Động Muộn & Gây Tỷ Lệ False Alarm Cao
- Hệ Thống E-Nose Lấy Cảm Hứng Từ Khứu Giác Sinh Học Sử Dụng Cụm Sensor Matrix
- Kết Hợp Edge AI Xây Dựng Gas Fingerprint Đặc Trưng Cho Khí H2S
- Phát Hiện Nguy Cơ Rò Rỉ Sớm Dựa Trên Động Học Chuỗi Thời Gian Time-Series
- Đảm Bảo An Toàn Tính Mạng Nhân Viên & Giảm Thiểu Thiệt Hại Vận Hành Nhà Máy

---

## 2. 5-Layer AIoT System Architecture

### 2.1. Layer 1: Perception Layer - Field Sensor Node

- Vi Điều Khiển ESP32 Đóng Gói Khung Truyền Modbus RTU Slave
- Cụm Cảm Biến Khí & Môi Trường Đa Chỉ Tiêu:
  - ZE03-H2S / MQ136: Đo Nồng Độ H2S Mục Tiêu Phạm Vi 0 Đến 100 ppm
  - MQ135: Nhận Diện Khí Nền VOCs, Smoke, NH3 Phục Vụ Tách Biệt Gas Fingerprint
  - DHT22: Đo Nhiệt Độ & Độ Ẩm Để Bù Sai Lệch Nhiệt Ẩm Cho Cảm Biến MOS
- Tiền Xử Lý Sơ Cấp: Lọc Nhiễu ADC 12-Bit Bằng Moving Average Filter
- Thiết Kế Vỏ Bảo Vệ Đạt Chuẩn IP65 Với Màng Lọc PTFE Hydrophobic Kháng Ăn Mòn H2S
- Nguồn Cấp DC 12V Tập Trung Hoặc Pin LiFePO4 12V Kết Hợp Solar Panel

### 2.2. Layer 2: Communication Layer - Industrial Network

- Chuẩn Giao Tiếp Vật Lý RS-485 Half-Duplex Chống Nhiễu Điện Từ Trường EMI Cao
- Tuyến Dây Cáp Daisy-Chain Bọc Kim STP Với 120 Ohm Termination Resistor Tại 2 Đầu Bus
- Giao Thức Công Nghiệp Modbus RTU Đảm Bảo Truyền Xa Hàng Trăm Mét
- Raspberry Pi 5 Đóng Vai Trò Modbus RTU Master Polling Định Kỳ Node 1 Đến N

### 2.3. Layer 3: Edge Computing Layer - Raspberry Pi 5 Gateway

- Bộ Xử Lý Trung Tâm Raspberry Pi 5 Broadcom BCM2712 Quad-Core Cortex-A76
- Preprocessing Pipeline:
  - Khử Nhiễu Dao Động Bằng Thuật Toán EMA Filter
  - Bù Trừ Sai Lệch Nhiệt Ẩm Drift Compensation
  - Trích Xuất Vector Đặc Trưng Time-Series: Độ Dốc Slope & Statistical Features (Mean, Std, Max, Min, Quartiles)
- Edge AI Inference:
  - Mô Hình Random Forest Tối Ưu Hóa Sang Định Dạng JSON
  - Phân Biệt Gas Fingerprint H2S Thực Sự Với Khí Nền VOCs Tránh False Alarm
  - Phân Cấp An Toàn 4 Level: Normal, Warning, Hazardous, Emergency
- Local Fail-Safe Storage: Ghi Dữ Liệu SQLite & Kích Hoạt Còi Đèn Cục Bộ Độc Lập Khi Mất Mạng

### 2.4. Layer 4: Cloud Platform Layer - Advantech WISE-IoT

- Đồng Bộ Dữ Liệu Lên Nền Tảng Đám Mây WISE-IoT Qua Giao Thức Bảo Mật MQTT
- Time-Series Database Lưu Trữ Toàn Bộ Dữ Liệu Telemetry & Lịch Sử Cảnh Báo
- Module Quản Lý Thiết Bị Giám Sát Uptime & Device Health Heartbeat
- Động Cơ Định Tuyến Cảnh Báo Khẩn Cấp Tức Thời Qua Email

### 2.5. Layer 5: Application Layer - Web Dashboard & Operations

- Trung Tâm Giám Sát Trực Quan Web Dashboard Với Industrial Dark Mode UI
- Biểu Đồ Diễn Biến Nồng Độ Khí H2S Thời Gian Thực
- Cơ Chế Xác Nhận Acknowledge Ghi Nhận Thời Gian Phản Hồi Của Nhân Viên Ca Trực

---

## 3. Edge AI Advantages & Safety Logic

### 3.1. Edge AI Decision Mechanism

- Thay Vì Phụ Thuộc Ngưỡng Nồng Độ Cố Định Hệ Thống Đánh Giá Xu Hướng Động Học
- Nhận Dạng Pattern Dị Thường Trước Khi Nồng Độ Đạt Ngưỡng Nguy Hiểm Tính Mạng
- Thời Gian Phản Hồi Dưới 1s Xử Lý Cục Bộ Không Phụ Thuộc Đường Truyền Đám Mây
- Giảm Băng Thông Mạng Nhờ Lọc Dữ Liệu & Chỉ Đẩy Event Bất Thường Khi Cần Thiết

### 3.2. 4-Level Safety Standard Classification

| Risk Level | Status | Concentration Threshold | System Action & Response |
|---|---|---|---|
| Level 1 | Normal | Dưới 1.0 ppm | Safe Baseline, Truyền Telemetry Định Kỳ |
| Level 2 | Warning | 1.0 Đến 9.9 ppm | Rò Rỉ Sớm, Cảnh Báo Nhân Viên Ca Trực Giám Sát |
| Level 3 | Hazardous | 10.0 Đến 49.9 ppm | Vượt Ngưỡng OSHA PEL, Bật Siren & Yêu Cầu Mặt Nạ Chuyên Dụng |
| Level 4 | Emergency | Từ 50.0 ppm | Mức Nguy Hiểm IDLH, Đóng Auto Shutdown Valve & Sơ Tán Khẩn Cấp |