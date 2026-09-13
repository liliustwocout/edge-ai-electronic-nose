# Thiết Kế Mô Hình Edge AI & Logic Cảnh Báo (Raspberry Pi 5)

> **Dự án:** Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection  
> **Tầng:** Edge AI Layer (Layer 3)  
> **Phần cứng thực thi:** Raspberry Pi 5 (Cortex-A76)

---

## 1. Luồng Xử Lý Dữ Liệu Tại Biên (Edge Pipeline)

```
[Modbus RTU Master]
       │ (Raw telemetry polling)
       ▼
[Data Preprocessing]
  ├── Digital Filtering (Bộ lọc trung bình trượt / Kalman)
  ├── Environmental Normalization (Bù trôi nhiệt độ & độ ẩm)
  └── Temporal Feature Extraction (Mean, Delta, Slope, Ratio MQ136/MQ135)
       │
       ▼
[Edge AI Inference (TFLite Runtime)]
  ├── Pattern Recognition (Nhận dạng vân tay khí)
  ├── Anomaly / Leak Detection (Phát hiện rò rỉ bất thường)
  └── Risk Classification (Phân loại 4 mức rủi ro)
       │
       ▼
[Decision & Alert Logic]
  ├── Multi-criteria Check (Ngưỡng nồng độ + Xác suất dự đoán AI)
  ├── Local Event Logging (SQLite / Parquet trên thẻ nhớ / SSD)
  └── Instant Alarm Dispatch (Còi/Đèn cục bộ + MQTT Alert lên WISE-IoT)
```

---

## 2. Các Bước Tiền Xử Lý Dữ Liệu (Data Processing)

### 2.1 Lọc nhiễu & Chuẩn hóa (Filtering & Normalization)
- **Lọc nhiễu:** Cảm biến MOS thường nhạy cảm với dao động điện áp và luồng gió. Áp dụng bộ lọc Exponential Moving Average (EMA) với hệ số $\alpha = 0.2$:
  $$y_t = \alpha \cdot x_t + (1 - \alpha) \cdot y_{t-1}$$
- **Bù nhiệt độ & độ ẩm:**
  $$R_{compensated} = \frac{R_s}{f(T, RH)}$$
  Trong đó $f(T, RH)$ là hàm hiệu chỉnh theo đồ thị đáp ứng đặc tính của cảm biến MQ136/MQ135.

### 2.2 Trích xuất đặc trưng chuỗi thời gian (Feature Extraction)
Sử dụng cửa sổ thời gian trượt (Sliding Window) $W = 30$ giây:
1. **Giá trị tức thời (Instantaneous Values):** $H_2S$ (ppm), $MQ136_{ADC}$, $MQ135_{ADC}$, Temp, Humidity.
2. **Tốc độ biến thiên (Gradient / First Derivative):** $\frac{\Delta C_{H_2S}}{\Delta t}$ (độ dốc nồng độ tăng nhanh - chỉ báo nguy cơ bùng phát rò rỉ khí).
3. **Tỷ số phản hồi ma trận khí (Sensor Array Ratio):** $\frac{R_{MQ136}}{R_{MQ135}}$ để phân biệt rò rỉ $H_2S$ thực sự với khí nền giao thoa (VOCs, khói xả).

---

## 3. Kiến Trúc Mô Hình Học Máy & Suy Luận Biên (Edge AI Inference)

### 3.1 Lựa chọn mô hình (Model Architecture)
- **Mô hình triển khai:** 1D-CNN kết hợp Bi-LSTM rút gọn hoặc Mô hình Ensemble nhẹ (LightGBM / Random Forest) được tối ưu hóa sang định dạng **TensorFlow Lite (TFLite) float16/int8**.
- **Đầu vào (Inputs):** Vector $K$ đặc trưng trong cửa sổ quan sát thời gian gần nhất.
- **Đầu ra (Outputs):**
  - **Xác suất rò rỉ (Leak Probability):** $[0.0 - 1.0]$
  - **Phân loại cấp độ rủi ro (Risk Class):** 4 mức độ.

### 3.2 Tiêu Chuẩn 4 Mức Độ Rủi Ro (Risk Levels)

Theo tiêu chuẩn an toàn công nghiệp dầu khí (OSHA / NIOSH đối với khí $H_2S$):

| Cấp độ | Tên trạng thái | Màu hiển thị | Ngưỡng nồng độ tham chiếu | Hành vi của mô hình AI & Hệ thống |
|---|---|---|---|---|
| **Level 1** | **Normal** | 🟢 Xanh lục | $< 1.0$ ppm | Môi trường an toàn. Đo lường và truyền telemetry chu kỳ bình thường. |
| **Level 2** | **Warning** | 🟡 Vàng | $1.0 - 9.9$ ppm | Nồng độ tăng bất thường hoặc độ dốc nồng độ tăng đột biến. Bật còi cảnh báo nhẹ, thông báo cho giám sát ca. |
| **Level 3** | **Hazardous** | 🟠 Cam | $10.0 - 49.9$ ppm | Đạt ngưỡng phơi nhiễm giới hạn (PEL/REL). Nguy cơ ngộ độc cấp tính. Kích hoạt thông báo còi đèn khu vực, yêu cầu bảo hộ mặt nạ lọc. |
| **Level 4** | **Emergency** | 🔴 Đỏ | $\ge 50.0$ ppm (hoặc nồng độ tăng vọt) | Mức nguy hiểm tính mạng (IDLH). Tự động ngắt van an toàn, phát lệnh sơ tán khẩn cấp toàn khu vực qua WISE-IoT và còi báo động. |

---

## 4. Quản Lý Lưu Trữ Cục Bộ (Local Storage & Fail-safe)
- **Cơ sở dữ liệu cục bộ:** SQLite / DuckDB lưu trên Raspberry Pi 5.
- **Dữ liệu được lưu trữ:**
  - Raw sensor logs (Dữ liệu thô dùng cho re-training mô hình).
  - Inference history & confidence score.
  - Alarms & system state logs.
- **Cơ chế hoạt động khi mất kết nối mạng (Offline Operation):**
  - Toàn bộ việc suy luận AI và kích hoạt còi/đèn cảnh báo cục bộ vẫn hoạt động liên tục 100% tại biên mà không cần Internet.
  - Dữ liệu chưa gửi được sẽ đưa vào hàng đợi đệm (Offline Message Buffer) và tự động đồng bộ lên WISE-IoT ngay khi kết nối Internet phục hồi.
