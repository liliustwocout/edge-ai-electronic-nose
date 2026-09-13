# Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection in Natural Gas Processing Plants

> **Cuộc thi:** Advantech AIoT InnoWorks  
> **Nhóm phát triển:** TaskForce141  
> **Cố vấn chuyên môn:** TS. Nguyễn Đắc Cử  
> **Thành viên nhóm:**  
> 1. Đỗ Đức Khôi (Leader)  
> 2. Lê Phạm Thành Đạt  
> 3. Vũ Anh Kiệt  

---

## 📖 Giới Thiệu Dự Án

Khí Hydro Sunfua ($H_2S$) là một loại khí cực độc, không màu, có mùi trứng thối đặc trưng ở nồng độ thấp nhưng làm tê liệt khứu giác ở nồng độ cao, thường xuất hiện trong các mỏ khí và nhà máy lọc hóa dầu. Các hệ thống cảnh báo truyền thống chỉ dựa vào một đầu dò cố định với ngưỡng nồng độ tĩnh, thường báo động muộn hoặc gây ra cảnh báo giả do các khí giao thoa trong môi trường công nghiệp.

Dự án này ứng dụng mô hình **Mũi điện tử (Electronic Nose - E-Nose)** kết hợp **Trí tuệ nhân tạo tại biên (Edge AI)** để:
1. Thu nhận ma trận phản ứng đa cảm biến nhằm xây dựng **chữ ký vân tay khí (Gas Signature/Fingerprint)** đặc trưng của $H_2S$.
2. Phát hiện sớm nguy cơ rò rỉ khí thông qua xu hướng động học chuỗi thời gian thay vì chỉ chờ vượt ngưỡng tĩnh.
3. Phân cấp mức độ nguy hiểm theo tiêu chuẩn an toàn thành 4 cấp độ: **Normal 🟢**, **Warning 🟡**, **Hazardous 🟠**, **Emergency 🔴**.
4. Truyền thông đa điểm công nghiệp chống nhiễu qua **RS-485 Modbus RTU** và đồng bộ hóa đám mây **Advantech WISE-IoT qua MQTT**.

---

## 🏗 Kiến Trúc Hệ Thống 5 Tầng (5-Layer Architecture)

```
[ 5. APPLICATION LAYER ]     Web Dashboard (Trung tâm điều hành) | Mobile App (Kỹ sư tuần tra)
           ▲
           │ Internet (MQTT / HTTPS)
           ▼
[ 4. CLOUD PLATFORM LAYER ]  Advantech WISE-IoT Platform (Lưu trữ lịch sử, Phân tích xu hướng, Cảnh báo đa kênh)
           ▲
           │ Internet (MQTT via Ethernet / Wi-Fi)
           ▼
[ 3. EDGE AI LAYER ]         Raspberry Pi 5 Gateway (Modbus Master, Lọc nhiễu, TFLite AI Inference, 4 Mức Cảnh Báo)
           ▲
           │ RS-485 Bus (Modbus RTU - Cáp xoắn chống nhiễu STP, Trở cuối 120Ω)
           ▼
[ 2. COMMUNICATION LAYER ]   Daisy-Chain Bus: Node 1 ─── Node 2 ─── Node 3 ─── ... ─── Node N
           ▲
           │
           ▼
[ 1. PERCEPTION LAYER ]      ESP32 Nodes + Cụm cảm biến E-Nose (ZE03/MQ136, MQ135, DHT22) + Hộp IP65 + Nguồn 12V
```

---

## ⚙️ Cách Thức Hoạt Động Của Dự Án

Quy trình hoạt động khép kín của hệ thống từ hiện trường đến người vận hành diễn ra qua 5 bước chính:

```
[Khí rò rỉ tại hiện trường]
           │
           ▼
(1) Cụm E-Nose Node (ESP32) lấy mẫu ADC & nhiệt ẩm
           │
           ▼
(2) Đóng gói Modbus RTU Slave, gửi qua tuyến RS-485
           │
           ▼
(3) Raspberry Pi 5 Gateway (Modbus Master) thu thập dữ liệu
           │
           ├── Lọc số (EMA) & Bù sai lệch nhiệt/ẩm
           ├── Trích xuất đặc trưng chuỗi thời gian
           └── Chạy mô hình Edge AI (TFLite) nhận dạng mẫu khí & phân loại rủi ro
           │
           ▼
(4) Ra quyết định cảnh báo tại biên (Fail-safe ngay cả khi mất mạng)
           │
           ▼
(5) Đẩy Telemetry & Event qua MQTT lên WISE-IoT Cloud -> Hiển thị trên Web Dashboard / Mobile App
```

### 1. Thu thập dữ liệu tại hiện trường (Tầng 1: Perception Layer)
- Mỗi Node cảm biến E-Nose đặt tại các điểm nhạy cảm (trạm nén khí, van tiết lưu, bồn chứa).
- Vi điều khiển **ESP32** lấy mẫu tín hiệu liên tục từ:
  - **Cảm biến chuyên dụng $H_2S$ (ZE03 / MQ136):** Bắt phản ứng nồng độ khí mục tiêu.
  - **Cảm biến khí tổng hợp (MQ135):** Thu nhận phản ứng nền với các hợp chất hữu cơ dễ bay hơi (VOCs), khói, $NH_3$, tạo nên ma trận tỷ số mùi.
  - **Cảm biến nhiệt độ & độ ẩm (DHT22):** Đo đạc vi khí hậu để phục vụ bù trôi sai số nhiệt/ẩm đặc thù của cảm biến bán dẫn oxit kim loại (MOS).
- Dữ liệu thô được bộ lọc sơ cấp trên ESP32 làm mịn, sau đó ánh xạ vào các thanh ghi **Modbus Holding Registers (16-bit)**.

### 2. Truyền dẫn công nghiệp chống nhiễu (Tầng 2: Communication Layer)
- Các Node được mắc nối tiếp dạng **Daisy-chain** dọc theo tuyến ống bằng cáp xoắn đôi chống nhiễu **RS-485**.
- Đầu cuối tuyến bus gắn điện trở dập sóng phản xạ **$120\,\Omega$**.
- Chuẩn giao tiếp **Modbus RTU** đảm bảo tín hiệu truyền xa hàng trăm mét trong môi trường nhà máy lọc hóa dầu nhiều động cơ công suất lớn mà không bị suy hao hay nhiễu điện từ trường (EMI).

### 3. Tính toán biên & Nhận dạng mẫu khí bằng AI (Tầng 3: Edge AI Layer)
- **Raspberry Pi 5** đóng vai trò **Edge Gateway** và là **Modbus RTU Master**, thực hiện polling tuần tự từng Node 1..N theo chu kỳ 1 - 2 giây.
- **Tiền xử lý tín hiệu (Preprocessing):**
  - Áp dụng bộ lọc số trung bình trượt Exponential Moving Average (EMA).
  - Chuẩn hóa tỷ số điện trở đáp ứng $R/R_0$ so với không khí sạch (Baseline).
  - Trích xuất đặc trưng chuỗi thời gian: độ dốc biến thiên $\frac{\Delta C}{\Delta t}$, tỷ số giữa các kênh $\frac{R_{MQ136}}{R_{MQ135}}$.
- **Suy luận mô hình Edge AI (TFLite):**
  - Mô hình học máy gọn nhẹ (1D-CNN / Ensemble Model) được tối ưu hóa sang TensorFlow Lite chạy trực tiếp trên 4 nhân Cortex-A76 của Raspberry Pi 5.
  - Mô hình phân tích ma trận chữ ký khí để phân biệt giữa rò rỉ $H_2S$ thực sự với các mùi nền khác.
  - Phân loại rủi ro tức thì thành **4 cấp độ**:
    - 🟢 **Normal:** Khí quyển an toàn ($< 1.0$ ppm).
    - 🟡 **Warning:** Nồng độ tăng bất thường hoặc độ dốc tăng nhanh ($1.0 - 9.9$ ppm) $\rightarrow$ Cảnh báo sớm cho ca trực.
    - 🟠 **Hazardous:** Vượt ngưỡng cho phép của OSHA ($10.0 - 49.9$ ppm) $\rightarrow$ Bật còi đèn khu vực, yêu cầu đeo mặt nạ dưỡng khí.
    - 🔴 **Emergency:** Nguy hiểm tính mạng ($\ge 50.0$ ppm) $\rightarrow$ Báo động toàn nhà máy, kích hoạt đóng ngắt van tự động.
- **Khả năng hoạt động ngoại tuyến (Fail-safe):** Mọi quyết định cảnh báo, đóng còi/đèn và ghi nhật ký cục bộ (Local SQLite) đều chạy độc lập tại biên, đảm bảo an toàn ngay cả khi mất toàn bộ mạng Internet ra ngoài.

### 4. Đồng bộ đám mây & Phân tích chuyên sâu (Tầng 4: Cloud Platform Layer)
- Gateway sử dụng **MQTT Client** xuất bản (Publish) dữ liệu telemetry định kỳ và các sự kiện bất thường qua mạng Ethernet / Wi-Fi lên nền tảng **Advantech WISE-IoT**.
- WISE-IoT đóng vai trò:
  - Lưu trữ cơ sở dữ liệu chuỗi thời gian (Time-series DB) phục vụ phân tích lâu dài.
  - Quản lý tình trạng thiết bị (Device Health, Heartbeat).
  - Tự động kích hoạt thông báo đa kênh (SMS, Email, Push Notification) tới người phụ trách.

### 5. Giám sát trực quan & Điều hành (Tầng 5: Application Layer)
- **Web Dashboard & Mobile App:**
  - Giao diện trực quan thời gian thực thiết kế theo chuẩn Dark Mode công nghiệp hiện đại.
  - Biểu đồ **Radar Chart (Vân tay khí E-Nose)** mô phỏng hình học 8 đỉnh tương ứng các kênh cảm biến, tự động đổi màu theo mức độ nguy cơ.
  - Biểu đồ **Time-Series đa kênh** thể hiện diễn biến nồng độ khí tức thời.
  - **Bản đồ mặt bằng 2D** định vị chính xác vị trí Node đang phát tín hiệu cảnh báo.
  - Hỗ trợ chuyển đổi kiểm chứng giữa 8 loại khí thực nghiệm ($H_2S, CO, NH_3, SO_2, NO_2, CH_3OCH_3, C_2H_5OH, H_2$).
- **Quy trình Người vận hành (Operator):** Khi có cảnh báo đỏ, Operator quan sát vị trí rò rỉ, nhấn nút **"Xác Nhận Xử Lý" (Acknowledge)** để ghi nhận thời gian phản ứng, và kích hoạt đội bảo hộ cô lập tuyến ống.

---

## 📂 Cấu Trúc Mã Nguồn & Tài Liệu

```
AIoT/
├── README.md                      # Tài liệu giải thích cách hoạt động của dự án (File này)
│
├── dashboard/                     # Ứng dụng Web Dashboard & Mobile Responsive
│   ├── index.html                 # Giao diện chính của Dashboard
│   ├── css/
│   │   ├── style.css              # Giao diện Dark Mode, Glassmorphism chuẩn công nghiệp
│   │   └── responsive.css         # Breakpoint tối ưu điện thoại di động & tablet
│   ├── js/
│   │   ├── app.js                 # Điều phối luồng dữ liệu & tương tác người dùng
│   │   ├── data-stream.js         # Engine mô phỏng phát dữ liệu 8 loại khí
│   │   ├── charts.js              # Quản lý biểu đồ Radar & Time-Series Chart.js
│   │   └── alarm.js               # Logic phân loại 4 cấp cảnh báo & âm thanh báo động
│   └── data/
│       └── gases_sample.json      # Mẫu dữ liệu 8 khí trích xuất từ tập thực nghiệm
│
├── dataset/                       # Dữ liệu thực nghiệm ma trận 8 cảm biến E-Nose
│   └── 8_gases/                   # CSV của H2S, CO, NH3, SO2, NO2, CH3OCH3, C2H5OH, H2
│
└── docs/                          # Bộ tài liệu kỹ thuật chi tiết
    ├── README.md                  # Mục lục và tổng quan hệ thống docs
    ├── dac-ta.md                  # Bản đặc tả kỹ thuật dự án & kế hoạch tuần
    ├── kien-truc-he-thong.md      # Chi tiết kiến trúc 5 tầng
    ├── phan-cung-e-nose.md        # Thiết kế phần cứng ESP32, cảm biến, vỏ IP65 & nguồn
    ├── giao-thuc-truyen-thong.md  # Đặc tả Modbus RTU Register Map & MQTT Payload
    ├── edge-ai-va-logic-canh-bao.md # Pipeline tiền xử lý, mô hình TFLite & 4 mức cảnh báo
    └── cloud-va-ung-dung.md       # Nền tảng WISE-IoT Cloud & Dashboard ứng dụng
```

---

## 🚀 Hướng Dẫn Khởi Chạy Web Dashboard

Yêu cầu máy tính đã cài đặt Python (hoặc bất kỳ HTTP Web Server tĩnh nào):

```bash
# Di chuyển vào thư mục dự án
cd g:/Project/AIoT

# Khởi chạy server nội bộ
python -m http.server 3000 --directory dashboard
```

Mở trình duyệt web và truy cập địa chỉ:  
👉 **`http://localhost:3000`**
