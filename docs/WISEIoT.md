# WISE-IoT Cloud Platform & Web Dashboard Application - Layers 4 & 5

**Project:** Edge AI-Based Electronic Nose For Hydrogen Sulfide Leak Detection  
**Layer:** Cloud Platform Layer - Layer 4 & Application Layer - Layer 5  
**Platform:** Advantech WISE-IoT Cloud & Web Dashboard  

---

## 1. Cloud Platform Layer: Advantech WISE-IoT Platform

### 1.1. Core Platform Capabilities

- Data Storage: Lưu Trữ Telemetry Stream Thời Gian Thực & Lịch Sử Phục Vụ Hậu Kiểm
- Analytics & Visualization: Biểu Đồ Hóa Nồng Độ H2S & Phân Tích Xu Hướng Đa Chiều
- Alarm Management: Phân Phối Cảnh Báo Khẩn Cấp Theo Khu Vực & Ca Trực
- Device Management: Giám Sát Uptime, CPU Load, Nhiệt Độ Raspberry Pi 5 & Trạng Thái Mạng
- Reports & Export: Tự Động Xuất Báo Cáo Định Dạng PDF & Excel Theo Chu Kỳ Định Sẵn

### 1.2. Telemetry Ingestion & Storage Architecture

- Ingestion Broker: Tiếp Nhận Bản Tin JSON Telemetry Qua Secure MQTT Broker
- Time-Series Database: Lưu Trữ Dữ Liệu Cảm Biến Với Tần Suất 5s → 10s
- Event Database: Ghi Nhận Lịch Sử Cảnh Báo, Anomaly Score & Risk Level
- Long-Term Cold Storage: Lưu Trữ Lịch Sử Dài Hạn Phục Vụ Huấn Luyện Lại Mô Hình AI

---

## 2. Application Layer: Web Dashboard & Operations Center

### 2.1. Industrial Web Dashboard Interface

- Real-Time Gauges & Multi-Channel Trend Charts:
  - Biểu Đồ Nồng Độ H2S ppm Thời Gian Thực Cho Từng Node
  - Gas Fingerprint Pattern Score Từ Mô Hình AI
  - Ma Trận Trạng Thái Sensor Array: MQ136, MQ135, Nhiệt Độ, Độ Ẩm
- Event Log Table:
  - Liệt Kê Toàn Bộ Lịch Sử Kích Hoạt Cảnh Báo
  - Ghi Nhận Timestamp, Node ID, Nồng Độ ppm, Risk Level & Nhân Viên Xác Nhận

### 2.2. Alert & Notification Mechanism

- Web Dashboard Alert: Hộp Thoại Âm Thanh & Đèn Nhấp Nháy Màn Hình Trung Tâm Điều Hành
- Email Incident Report: Tự Động Gửi Báo Cáo Sự Cố Kèm Biểu Đồ Xu Hướng Trước & Sau Rò Rỉ
- Field Siren & Strobe Dispatch: Tự Động Kích Hoạt Còi Đèn Tại Khu Vực Phát Hiện Sự Cố

### 2.3. Plant Operator Workflow

- Bước 1 - Tiếp Nhận Cảnh Báo: Quan Sát Cấp Độ Rủi Ro Hiển Thị Trên Web Dashboard
- Bước 2 - Xác Định Vị Trí: Kiểm Tra Thông Tin Node Cảnh Báo Trên Bảng Sự Kiện Web Dashboard
- Bước 3 - Triển Khai Ứng Phó: Đóng Auto Shutdown Valve Hoặc Cử Đội Bảo Hộ Xử Lý Điểm Rò Rỉ
- Bước 4 - Xác Nhận Sự Cố: Nhấn Nút Acknowledge Trên Web Dashboard Để Ghi Nhận Hệ Thống
