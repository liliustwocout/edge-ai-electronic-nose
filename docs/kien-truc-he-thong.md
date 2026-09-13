# Kiến Trúc Hệ Thống (System Architecture)

> **Dự án:** Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection in Natural Gas Processing Plants  
> **Đội ngũ:** TaskForce141 (Advantech AIoT InnoWorks)  
> **Kiến trúc tổng thể:** Mô hình phân tầng 5 lớp (5-Layer AIoT Architecture)

---

## 1. Sơ Đồ Khối Tổng Thể (System Architecture Diagram)

```
+-----------------------------------------------------------------------------------+
|                           5. APPLICATION LAYER                                    |
|   [Web Dashboard]       [Mobile App]       [Alerts & Notifications]   [Operator]  |
+-----------------------------------------------------------------------------------+
                                         ▲
                                         │ Internet (MQTT / HTTPS)
                                         ▼
+-----------------------------------------------------------------------------------+
|                        4. CLOUD PLATFORM LAYER (WISE-IoT)                         |
|   - Data Storage             - Analytics & Visualization   - Alarm Management     |
|   - Device Management        - Reports & Export                                   |
+-----------------------------------------------------------------------------------+
                                         ▲
                                         │ Internet (MQTT via Ethernet / Wi-Fi)
                                         ▼
+-----------------------------------------------------------------------------------+
|                      3. EDGE AI LAYER (Raspberry Pi 5 Gateway)                    |
|  +---------------------------+  +-------------------+  +-----------------------+  |
|  | Data Acquisition (Master) |  |  Data Processing  |  |   Edge AI Inference   |  |
|  | - Polling Sensor Nodes    |  |  - Filtering      |  |   - Pattern Recogn.   |  |
|  | - Data Parsing            |  |  - Normalization  |  |   - Leak Detection    |  |
|  | - Time Synchronization    |  |  - Feature Extr.  |  |   - Risk Classif.     |  |
|  +---------------------------+  +-------------------+  +-----------------------+  |
|  +---------------------------+  +----------------------------------------------+  |
|  | Local Storage (SD/SSD)    |  | Decision & Alert Logic                       |  |
|  | - Raw Data, Inference Log |  | - Threshold Check     - Risk Assessment      |  |
|  | - Model File, System Log  |  | - Event Logging       - Alarm Triggering     |  |
|  +---------------------------+  +----------------------------------------------+  |
|  Communication: Modbus RTU (RS485) Master  |  MQTT Client (Internet)               |
+-----------------------------------------------------------------------------------+
                                         ▲
                                         │ RS-485 Bus (Modbus RTU - Daisy Chain)
                                         ▼
+-----------------------------------------------------------------------------------+
|                              2. COMMUNICATION LAYER                               |
|   Edge Gateway (RPi 5) ───[RS-485 Converter]                                      |
|          │                                                                        |
|          └─── Node 1 (E-Nose) ─── Node 2 (E-Nose) ─── ... ─── Node N ─── [120Ω]   |
+-----------------------------------------------------------------------------------+
                                         ▲
                                         │
+-----------------------------------------------------------------------------------+
|                     1. PERCEPTION LAYER (E-Nose Sensor Nodes)                     |
|  Mỗi Node gồm:                                                                    |
|  - MCU: ESP32 (Signal Conditioning, Modbus RTU Slave, Timestamp)                  |
|  - Sensors:                                                                       |
|      * ZE03-H2S / MQ136 (Khí đặc hiệu H2S)                                        |
|      * MQ135 (Khí tổng hợp / Cross-sensitive gas)                                 |
|      * DHT22 (Nhiệt độ & Độ ẩm để bù sai số)                                      |
|  - Phụ trợ:                                                                       |
|      * RS485 Transceiver (MAX485 / SP3485)                                        |
|      * Vỏ bảo vệ: IP65 Enclosure, lọc khí chống ăn mòn, gá gắn tường/cột          |
|      * Nguồn: Nguồn 12V DC / Pin dự phòng 12V 5Ah + DC-DC 5V (+ Tấm pin MT)       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Chi Tiết Các Tầng Chức Năng

### Tầng 1: Perception Layer (Tầng Thu Thập & Cảm Biến Hiện Trường)
- **Mục tiêu:** Giám sát nồng độ khí tại các vị trí rủi ro cao (van đường ống, máy nén khí, bồn chứa, trạm xử lý khí tự nhiên).
- **Phần cứng E-Nose:**
  - Vi điều khiển **ESP32** đóng vai trò Modbus Slave.
  - Cụm cảm biến E-Nose:
    - **ZE03-H2S / MQ136:** Cảm biến chuyên dụng phát hiện khí $H_2S$ độc hại.
    - **MQ135:** Cảm biến khí đa năng nhận diện các khí phụ trợ/mùi môi trường, phục vụ nhận dạng mẫu ma trận khí.
    - **DHT22:** Đo nhiệt độ và độ ẩm tương đối của môi trường xung quanh nhằm hiệu chuẩn sai lệch nhiệt/ẩm của cảm biến bán dẫn oxit kim loại (MOS).
  - **Module RS-485 Transceiver:** Chuyển đổi mức tín hiệu UART từ ESP32 sang chuẩn vi sai RS-485.
  - **Vỏ bảo vệ công nghiệp:** Chuẩn IP65 chống bụi và nước, có đầu lấy mẫu khí kèm màng lọc hạt/bụi (Gas Inlet with Filter), thiết kế chống ăn mòn hóa học, kèm phụ kiện giá treo tường hoặc cột.
  - **Nguồn cấp tại hiện trường:** Nguồn DC công nghiệp hoặc kết hợp Ắc quy/Pin 12V 5Ah qua mạch hạ áp xung DC-DC Buck Regulator (5V) và tấm pin năng lượng mặt trời tùy chọn (Solar Panel).

### Tầng 2: Communication Layer (Tầng Truyền Thông Công Nghiệp)
- **Chuẩn vật lý:** RS-485 (cặp dây xoắn chống nhiễu Shielded Twisted Pair - STP).
- **Giao thức:** Modbus RTU qua chuẩn nối tiếp bán song công (Half-Duplex).
- **Cấu hình mạng:**
  - Topology dạng Bus (Daisy-chain) kéo dài hàng trăm mét trong nhà máy lọc hóa dầu.
  - Trở kháng đầu cuối: Điện trở dập sóng phản xạ $120\,\Omega$ ở hai đầu tuyến bus.
  - Module chuyển đổi: USB-to-RS485 hoặc HAT RS-485 công nghiệp gắn trên Raspberry Pi 5.

### Tầng 3: Edge AI Layer (Tầng Tính Toán Biên - Edge Gateway)
- **Thiết bị:** Raspberry Pi 5 (Bộ xử lý Broadcom BCM2712 Quad-core Cortex-A76).
- **Nhiệm vụ chính:**
  - **Modbus Master Engine:** Thực hiện polling chu kỳ (1s - 5s) để đọc thanh ghi (Holding Registers) của từng Node 1..N.
  - **Tiền xử lý dữ liệu (Data Preprocessing):** Lọc nhiễu tín hiệu số (Moving Average / Kalman Filter), chuẩn hóa dữ liệu (Z-score / Min-Max Scaling), trích xuất đặc trưng chuỗi thời gian (Mean, Variance, Gradient/Slope theo thời gian).
  - **Mô hình Edge AI (TFLite / ONNX):**
    - Nhận dạng mẫu khí (Gas Signature Pattern Recognition).
    - Phát hiện sớm rò rỉ khí (Early Leak Detection).
    - Phân loại cấp độ rủi ro (Risk Classification): 
      - `Normal` (Bình thường - Xanh lục)
      - `Warning` (Cảnh báo sớm - Vàng)
      - `Hazardous` (Nguy hại - Cam)
      - `Emergency` (Khẩn cấp - Đỏ)
  - **Logic điều khiển & Cảnh báo tức thời:** So ngưỡng an toàn kết hợp suy luận mô hình AI, ghi nhận sự kiện khẩn cấp ngay cả khi mất mạng Internet.
  - **Lưu trữ cục bộ:** Lưu file cấu hình, mô hình ML, nhật ký suy luận (Inference Log) và dữ liệu thô phục vụ re-training trên thẻ nhớ SD hoặc SSD NVMe.
  - **MQTT Client:** Đóng gói JSON payload gửi dữ liệu và cảnh báo lên đám mây.

### Tầng 4: Cloud Platform Layer (WISE-IoT Platform)
- **Nền tảng:** Advantech WISE-IoT Cloud Platform.
- **Tính năng:**
  - Tiếp nhận telemetry và event qua MQTT broker bảo mật.
  - Lưu trữ cơ sở dữ liệu thời gian thực và lịch sử (Time-series Database).
  - Phân tích xu hướng dài hạn (Analytics & Trends).
  - Quản lý thiết bị từ xa (Device Management, Heartbeat/Health check).
  - Hệ thống gửi thông báo cảnh báo đa kênh (SMS, Email, Push Notifications, Webhook).
  - Báo cáo định kỳ và xuất dữ liệu (Reports & Data Export).

### Tầng 5: Application Layer (Tầng Ứng Dụng Người Dùng)
- **Web Dashboard:** Bảng điều khiển trực quan thời gian thực trên màn hình trung tâm điều hành nhà máy.
- **Mobile App:** Ứng dụng di động dành cho kỹ sư an toàn, kỹ thuật viên bảo trì tuần tra.
- **Hệ thống cảnh báo trực quan & âm thanh:** Đèn tháp, còi báo động, thông báo đẩy tới cán bộ giám sát an toàn.
- **Người vận hành (Operator):** Tiếp nhận thông tin, định vị chính xác vị trí Node phát hiện rò rỉ và triển khai quy trình an toàn nhà máy.
