# Tài Liệu Đặc Tả Kịch Bản Vận Hành (Operating Scenarios)

**Dự án:** Edge AI-Based Electronic Nose for Toxic Gas Detection  
**Mục tiêu:** Mô phỏng dòng dữ liệu cảm biến thực tế, kiểm chứng khả năng phát hiện khí và cơ chế cảnh báo sớm theo thời gian thực của hệ thống Edge AI trên Raspberry Pi.

---

## 1. Tổng Quan Các Kịch Bản

Hệ thống được tích hợp sẵn **4 kịch bản mô phỏng dòng dữ liệu thời gian thực** (định nghĩa tại hàm `buildScenarios()` trong [backend/app.py](file:///g:/Project/AIoT/backend/app.py)). Mỗi kịch bản đại diện cho một điều kiện môi trường hoặc tình huống công nghiệp đặc thù:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        4 KỊCH BẢN VẬN HÀNH SCADA                       │
├────────────────────┬───────────────────────────────────────────────────┤
│ 1. fieldScenario   │ Kịch Bản Thực Địa - Tự Động (Liên hoàn 4 pha)     │
│ 2. H2SRun          │ Rò Rỉ H2S Nguy Hiểm (0 - 10 ppm lặp lại)          │
│ 3. NH3Run          │ Khí NH3 Công Nghiệp (0 - 100 ppm lặp lại)         │
│ 4. airRun          │ Không Khí Sạch Chuẩn (Kiểm tra Baseline ổn định)  │
└────────────────────┴───────────────────────────────────────────────────┘
```

---

## 2. Chi Tiết Từng Kịch Bản

### 2.1. Kịch Bản 1: `fieldScenario` (Kịch Bản Thực Địa - Tự Động)
- **Tên hiển thị:** *Kịch Bản Thực Địa - Tự Động* (hoặc *Field Industrial Scenario - Auto*)
- **Mục đích:** Mô phỏng trọn vẹn một ca trực thực tế tại nhà máy với các sự cố rò rỉ khí độc xảy ra ngẫu nhiên và quy trình ứng phó tự động.
- **Tổng số bước thời gian:** 545 điểm (chu kỳ phát mặc định: 800ms / điểm, ~7 phút thời gian thực).
- **Diễn biến 4 giai đoạn:**
  1. **Pha 1 - Baseline Môi Trường Sạch (0s - 25s, 25 điểm):**
     - Môi trường không khí sạch an toàn.
     - Cảm biến ở mức baseline ổn định ($S_3 \approx 0.01 - 0.03\text{ V}$).
     - AI trả về nhãn `Clean Air`, 0.0 ppm, trạng thái `Normal` (Màu xanh lục).
  2. **Pha 2 - Sự Cố Rò Rỉ Khí H2S (25s - 85s, 250 điểm từ Pulse 95):**
     - Xảy ra rò rỉ khí độc $H_2S$ nồng độ cao (10 ppm).
     - Điện áp cảm biến tăng vọt theo động học hấp phụ từ $0.02\text{V} \to 2.45\text{V}$ với độ dốc lớn.
     - Thuật toán Gradient Prognostics tính toán thời gian chạm ngưỡng nguy kịch (**Time to Emergency - TTE ~15-25s**).
     - Hệ thống tự động nâng cấp mức cảnh báo từ `Warning` $\to$ `Hazardous` $\to$ `Emergency` (Màu đỏ khẩn cấp), kích hoạt còi báo động Web Audio và tạo Email Dispatch.
  3. **Pha 3 - Phục Hồi & Thông Gió Cưỡng Bức (85s - 105s, 20 điểm):**
     - Hệ thống Scrubber / quạt thông gió hoạt động thổi sạch khí độc.
     - Tín hiệu cảm biến hạ nhiệt trở về đường baseline an toàn, trạng thái quay lại `Normal`.
  4. **Pha 4 - Sự Cố Xả Thải Khí NH3 Công Nghiệp (105s - 165s, 250 điểm từ Pulse 60):**
     - Khí Amoniac nồng độ 50 ppm xuất hiện trong môi trường.
     - Dạng sóng cảm biến mang đặc trưng của $NH_3$ (độ cong và tốc độ suy giảm khác biệt với $H_2S$).
     - AI phân loại chính xác nhãn `NH3`, nồng độ ước tính ~50 ppm, trạng thái chuyển sang `Hazardous` (Màu cam).
     - Kết thúc chu kỳ, hệ thống thông gió lại và tự động quay vòng về Pha 1.

---

### 2.2. Kịch Bản 2: `H2SRun` (Rò Rỉ H2S Nguy Hiểm - 0 - 10 ppm)
- **Tên hiển thị:** *Rò Rỉ H2S Nguy Hiểm - 0 - 10 ppm* (hoặc *H2S Lethal Leak Run*)
- **Mục đích:** Đánh giá chuyên sâu năng lực phát hiện khí Hydro Sulfide ($H_2S$) - loại khí cực độc gây tê liệt khứu giác ở nồng độ thấp và gây tử vong ở nồng độ cao.
- **Dữ liệu nguồn:** Trích xuất từ xung thực nghiệm [h2s_sensor_1_clean.csv](file:///g:/Project/AIoT/data/h2s_sensor_1_clean.csv) (*Pulse 95*, nồng độ 10 ppm).
- **Đặc trưng:**
  - Chu kỳ sóng 250 điểm (60 giây thời gian thực).
  - Biên độ điện áp đỉnh đạt xấp xỉ $2.4\text{ V}$.
  - Kiểm tra khả năng nhận diện của mô hình với thời gian suy luận dưới 4ms trên Raspberry Pi 3.

---

### 2.3. Kịch Bản 3: `NH3Run` (Khí NH3 Công Nghiệp - 0 - 100 ppm)
- **Tên hiển thị:** *Khí NH3 Công Nghiệp - 0 - 100 ppm* (hoặc *NH3 Industrial Run*)
- **Mục đích:** Kiểm tra khả năng phân loại và ước lượng nồng độ khí Amoniac ($NH_3$) - loại khí ăn mòn và gây kích ứng đường hô hấp phổ biến trong các hệ thống làm lạnh công nghiệp và phân bón.
- **Dữ liệu nguồn:** Trích xuất từ xung thực nghiệm [nh3_sensor_1_clean.csv](file:///g:/Project/AIoT/data/nh3_sensor_1_clean.csv) (*Pulse 60*, nồng độ 50 ppm).
- **Đặc trưng:**
  - Chu kỳ sóng 250 điểm (60 giây thời gian thực).
  - Giúp đánh giá khả năng tách biệt Gas Fingerprint giữa $NH_3$ và $H_2S$ của mô hình Random Forest.

---

### 2.4. Kịch Bản 4: `airRun` (Không Khí Sạch Chuẩn)
- **Tên hiển thị:** *Không Khí Sạch Chuẩn* (hoặc *Clean Air Baseline - Ambient*)
- **Mục đích:** Xác minh độ ổn định của hệ thống trong điều kiện bình thường, đảm bảo loại bỏ hoàn toàn hiện tượng báo động giả (False Positive).
- **Dữ liệu nguồn:** Trích xuất từ xung [air_clean_sensor_1_clean.csv](file:///g:/Project/AIoT/data/air_clean_sensor_1_clean.csv) (*Pulse 5*).
- **Đặc trưng:**
  - Điện áp dao động nhỏ quanh mức baseline tự nhiên ($0.005\text{V} - 0.03\text{V}$).
  - Kích hoạt cơ chế chốt chặn an toàn (Baseline Threshold Guard: $V \le 0.32\text{V} \implies \text{Clean Air}, 0\text{ ppm}$, Confidence $\ge 96\%$).

---

## 3. Hướng Dẫn Thay Đổi Kịch Bản

### Cách 1: Thao tác trên giao diện Web Dashboard
1. Truy cập: `http://100.72.0.24:8001/dashboard/index.html` (qua Tailscale) hoặc `http://localhost:8001/dashboard/index.html`.
2. Trên thanh điều khiển **Kịch Bản:**, nhấp chọn một trong 4 tab:
   - `[Kịch Bản Thực Địa - Tự Động]`
   - `[Rò Rỉ H2S Nguy Hiểm - 0 - 10 ppm]`
   - `[Khí NH3 Công Nghiệp - 0 - 100 ppm]`
   - `[Không Khí Sạch Chuẩn]`
3. Giao diện sẽ tự động gửi lệnh chuyển đổi xuống Pi 3 và xóa đồ thị cũ để vẽ luồng dữ liệu mới.
4. **Các nút điều khiển phụ:**
   - **Tạm Dừng / Tiếp Tục (`btnPlayPause`):** Tạm dừng dòng dữ liệu để quan sát hoặc phân tích các điểm bất thường.
   - **1x / 2.5x (`speed1x`, `speed2x`):** Thay đổi tốc độ gửi dữ liệu giữa 800ms/điểm (tốc độ thường) và 320ms/điểm (tua nhanh).

### Cách 2: Lập trình điều khiển qua WebSocket API
Ứng dụng hoặc script kiểm thử có thể kết nối tới endpoint `/stream` và gửi lệnh dạng JSON:

```python
import asyncio
import json
import websockets

async def change_scenario(mode_name):
    uri = "ws://100.72.0.24:8001/stream"
    async with websockets.connect(uri) as ws:
        # Gửi lệnh đổi kịch bản: fieldScenario, H2SRun, NH3Run, airRun
        await ws.send(json.dumps({
            "action": "setMode",
            "mode": mode_name
        }))
        # Nhận gói tin phản hồi đầu tiên
        packet = await ws.recv()
        print("Đã chuyển sang:", mode_name, packet)

# Chạy đổi sang H2SRun
asyncio.run(change_scenario("H2SRun"))
```

### Cách 3: Thêm kịch bản tùy biến trong Backend
Để thêm một kịch bản kiểm thử mới (ví dụ $H_2S$ 1 ppm hoặc $NH_3$ 100 ppm):
1. Mở file [backend/app.py](file:///g:/Project/AIoT/backend/app.py#L62-L165).
2. Trong hàm `buildScenarios()`, chọn pulse mong muốn từ DataFrame đã nạp:
   ```python
   # Ví dụ: lấy xung H2S 1ppm (Pulse_15)
   h2s_1ppm = h2sDf[h2sDf['Pulse_Index'] == 'Pulse_15'][point_cols].values[0].tolist()
   ```
3. Đăng ký kịch bản mới trong dictionary trả về:
   ```python
   'H2S_1ppm_Test': [{
       's3': round(float(v), 4),
       's3Raw': round(float(v + np.random.normal(0, 0.002)), 4),
       'temperature': 29.0,
       'humidity': 64.0,
       'trueGas': 'H2S' if idx <= 140 else 'Clean Air',
       'trueppm': 1.0 if (20 <= idx <= 125) else 0.0,
       'phase': 'H2S 1ppm Low Exposure'
   } for idx, v in enumerate(h2s_1ppm)]
   ```
4. Thêm nút bấm tương ứng trên [dashboard/index.html](file:///g:/Project/AIoT/dashboard/index.html):
   ```html
   <button class="gasTab px-3 py-1.5 rounded bg-slate-800/50 border border-slate-700 hover:bg-slate-800 text-slate-400 text-xs" data-mode="H2S_1ppm_Test">
     H2S 1 ppm Nhẹ
   </button>
   ```

---

## 4. Cấu Trúc Gói Tin Telemetry WebSocket

Mỗi gói tin được Backend phát qua WebSocket `/stream` có cấu trúc JSON như sau:

```json
{
  "timestamp": "10:15:23 PM",
  "s3": 0.8542,
  "s3Raw": 0.8571,
  "temperature": 29.2,
  "humidity": 65.1,
  "gas": "H2S",
  "trueGas": "H2S",
  "trueppm": 10.0,
  "estimatedppm": 9.42,
  "riskLevel": "Hazardous",
  "confidence": 98,
  "probabilities": {
    "Clean Air": 0.01,
    "H2S": 0.98,
    "NH3": 0.01
  },
  "latencyMs": 2.85,
  "phase": "H2S Leakage",
  "features": {
    "slope": 0.0182,
    "ema": 0.8542
  },
  "prognostics": {
    "trajectory": [0.945, 1.036, 1.127, 1.218],
    "isEmergencyProjected": true,
    "timeToEmergencySec": 16
  }
}
```
