# Edge AI Model Design & Risk Alert Logic - Raspberry Pi Gateway

**Project:** Edge AI-Based Electronic Nose For Toxic Gas Detection ($H_2S$ & $NH_3$)  
**Layer:** Edge AI Layer - Layer 3  
**Hardware Platforms:** Raspberry Pi 3 Model B (Cortex-A53) & Raspberry Pi 5 (Cortex-A76)  

---

## 1. Edge Pipeline

```
Modbus RTU Master Polling Telemetry / Live Stream
       │
       ▼
Data Preprocessing
  ├── Digital Filtering Qua EMA Filter (α = 0.2)
  ├── Hardware Despike Filter (Khử gai xung phần cứng tại điểm ~125)
  ├── Drift Compensation Cho Nhiệt Độ & Độ Ẩm
  └── Time-Series Feature Extraction:
        ├── Full Pulse (250 points / 60s): Mean, Std, Min, Max, Delta, Slopes, AUC, 10 Anchor Points
        └── Sliding Window (20 points): Mean, Std, Min, Max, Delta, Slope, Sub-Windows
       │
       ▼
Edge AI Inference (RandomForest Dual-Mode)
  ├── Gas Fingerprint Pattern Recognition (Clean Air vs H2S vs NH3)
  ├── Concentration Estimation (ppm Regression)
  ├── Baseline Guard Chốt Chặn Báo Động Giả (compS3 ≤ 0.32V → Clean Air 0 ppm)
  └── Gradient Prognostics (+20s Horizon & Time-to-Emergency TTE)
       │
       ▼
Decision & Alert Logic
  ├── Multi-Criteria Threshold & AI Confidence Check
  ├── Local Event Logging Vào SQLite & Buffer CSV
  └── Instant Alert Dispatch Qua Siren Web Audio, Email Alert & MQTT Lên WISE-IoT Cloud
```

---

## 2. Dữ Liệu Thực Nghiệm & Tiền Xử Lý

### 2.1. Tập Dữ Liệu Thực Nghiệm Mới
Dữ liệu được thu thập từ mảng cảm biến vật lý (MQ136, MQ135, DHT22) với 250 điểm lấy mẫu trong mỗi chu kỳ 60 giây:

| Loại Khí | Dải Nồng Độ Thực Nghiệm | Số Lượng Chu Kỳ (Pulses) Hợp Lệ | Nền Baseline |
| :--- | :--- | :--- | :--- |
| **Clean Air** | 0 ppm | **133 pulses** | Điện áp nền $V_{baseline} \approx 0.005 - 0.03\text{ V}$ |
| **$H_2S$** | 1, 5, 10 ppm | **110 pulses** | 1..37: 1 ppm, 38..74: 5 ppm, 75..111: 10 ppm |
| **$NH_3$** | 10, 50, 100 ppm | **118 pulses** | 1..42: 10 ppm, 43..84: 50 ppm, 85..126: 100 ppm |
| **Tổng cộng** | - | **361 pulses** | Không bị rò rỉ dữ liệu giữa các pulse (Zero-Overlap) |

### 2.2. Lọc Số & Khử Gai Phần Cứng (`clean_sensor_data.py`)
- Áp dụng bộ lọc **Savitzky-Golay** (cửa sổ 9, bậc 2) làm mượt đường cong tín hiệu mà vẫn giữ nguyên đặc trưng động học đỉnh.
- Khử nhiễu bước nhảy phần cứng (Hardware Artifact Spikes) bằng nội suy Cubic Spline.
- Loại bỏ các xung ngoại lai (Outliers) dựa trên phân tích phân vị IQR và khoảng cách MAE so với đường trung vị phổ khí.

---

## 3. Kiến Trúc Mô Hình Edge AI (RandomForest Dual-Mode)

Để đảm bảo khả năng chạy mượt mà trên các vi máy tính tài nguyên thấp như Raspberry Pi 3 (RAM 1GB), hệ thống sử dụng kiến trúc **RandomForest Dual-Mode**:

```
                       ┌──────────────────────────────────────────────────┐
                       │           TÍN HIỆU CẢM BIẾN THỜI GIAN THỰC       │
                       └────────┬────────────────────────────────┬────────┘
                                │                                │
                      [Cửa sổ trượt 20 điểm]             [Trọn chu kỳ 250 điểm]
                                │                                │
                                ▼                                ▼
                       ┌───────────────────┐            ┌───────────────────┐
                       │ Window-Level Model│            │ Pulse-Level Model │
                       │ (Streaming 800ms) │            │  (Batch Cycle 60s)│
                       └────────┬──────────┘            └────────┬──────────┘
                                │                                │
                                ├─ Accuracy: 94.71%              ├─ Accuracy: 94.18%
                                └─ MAE: 5.22 ppm                 └─ MAE: 3.93 ppm (R²: 0.8534)
```

### 3.1. Kết Quả Huấn Luyện (5-Fold Stratified Cross-Validation)

| Mô Hình | Nhiệm Vụ | Độ Chính Xác (Accuracy) | Sai Số Nồng Độ (MAE) | Hệ Số $R^2$ | Độ Trễ Suy Luận (RPi 3) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`model_pulse_gas.pkl`** | Phân loại khí theo chu kỳ 60s | **94.18%** | - | - | 3.2 ms |
| **`model_pulse_ppm.pkl`** | Hồi quy nồng độ khí theo chu kỳ | - | **3.93 ppm** | **0.8534** | 2.6 ms |
| **`model_gas.pkl`** | Phân loại khí streaming liên tục | **94.71%** | - | - | 1.8 ms |
| **`model_ppm.pkl`** | Hồi quy nồng độ khí streaming | - | **5.22 ppm** | **0.7525** | 1.5 ms |

### 3.2. Báo Cáo Phân Lớp Chi Tiết (Pulse Classifier)

| Nhãn Khí | Độ Chính Xác (Precision) | Độ Thu Hồi (Recall) | Điểm F1-Score | Số Lượng Mẫu (Support) |
| :--- | :--- | :--- | :--- | :--- |
| **Clean Air** | 89.7% | **98.5%** | 93.9% | 133 |
| **$H_2S$** | **96.0%** | 86.4% | 90.9% | 110 |
| **$NH_3$** | **98.3%** | **96.6%** | **97.4%** | 118 |
| **Trung Bình Toàn Bộ** | **94.7%** | **93.8%** | **94.1%** | **361** |

### 3.3. Các Đặc Trưng Quan Trọng Nhất (Feature Importance)
1. **Delta_V ($V_{max} - V_{min}$):** 12.63% (Biên độ phản ứng mạnh nhất)
2. **Anchor_18s:** 10.17% (Giá trị điện áp tại giây thứ 18 - giai đoạn tăng đỉnh)
3. **Peak_Time:** 8.64% (Thời gian đạt điện áp cực đại)
4. **Decay_Slope:** 8.43% (Tốc độ suy giảm giải hấp phụ khí)
5. **Anchor_55s:** 6.64% (Giá trị điện áp phục hồi cuối chu kỳ)
6. **Max_V:** 6.13% (Điện áp đỉnh tuyệt đối)

### 3.4. Cơ Chế Chốt Chặn Baseline Guard
Trong thực tế, khi không có khí độc, điện áp cảm biến thường rất nhỏ ($< 0.1\text{V}$). Để triệt tiêu 100% tình trạng mô hình bị nhiễu vi mô dẫn tới phân loại nhầm:
$$\text{Nếu } V_{compensated} \le 0.32\text{V} \implies \text{Ép về nhãn Clean Air, 0.0 ppm, Confidence } \ge 96\%$$

---

## 4. Chuẩn Phân Cấp Nguy Cơ 4 Cấp Độ (4 Risk Levels)

| Cấp Độ | Trạng Thái | Màu Sắc | Ngưỡng Khí $H_2S$ | Ngưỡng Khí $NH_3$ | Hành Động Hệ Thống |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Level 1** | **Normal** | Xanh lục | $< 1.0\text{ ppm}$ | $< 25.0\text{ ppm}$ | An toàn, hiển thị telemetry chu kỳ bình thường. |
| **Level 2** | **Warning** | Vàng | $1.0 - 4.9\text{ ppm}$ | $25.0 - 49.9\text{ ppm}$ | Phát hiện rò rỉ sớm, gửi thông báo cảnh báo ca trực. |
| **Level 3** | **Hazardous** | Cam | $5.0 - 9.9\text{ ppm}$ | $50.0 - 99.9\text{ ppm}$ | Vượt ngưỡng OSHA PEL, kích hoạt đèn chớp, yêu cầu đồ bảo hộ. |
| **Level 4** | **Emergency** | Đỏ | $\ge 10.0\text{ ppm}$ | $\ge 100.0\text{ ppm}$ | Nguy hiểm tử vong IDLH, còi hú khẩn cấp, cắt van tự động. |
