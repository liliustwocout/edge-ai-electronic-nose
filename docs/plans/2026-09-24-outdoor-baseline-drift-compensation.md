# Kế Hoạch Triển Khai: Khắc Phục Lệch Đường Nền & Báo Nhầm Khí Ngoài Trời (Outdoor Baseline Drift Compensation)

> **Mục tiêu:** Loại bỏ hoàn toàn hiện tượng báo động nhầm $H_2S$ và $NH_3$ ngoài trời do trôi đường nền (Baseline Drift ~0.35V - 0.70V), tối ưu hóa pipeline tiền xử lý thành vi sai tương đối ($\Delta V$), xây dựng cơ chế Zero Calibration và huấn luyện mô hình thích ứng miền dữ liệu bằng Data Augmentation.  
> **Kiến trúc áp dụng:** Differential Feature Extraction + Dynamic Kinematic Guard + Adaptive Baseline Tracking + Synthetic Plume Superposition.  
> **Nền tảng:** Python 3.11+, Scikit-Learn 1.9+, FastAPI, WebSocket, Edge Deployment trên Raspberry Pi 3 (Debian aarch64, RAM 1GB).

---

## 1. Phân Tích Kỹ Thuật & Nguyên Nhân Gốc Rễ (Root Cause Analysis)

### 1.1. Hiện tượng sai lệch miền dữ liệu (Domain Shift)
- **Trong Phòng Lab:** Mẫu Clean Air đo trong buồng kín có điện áp tĩnh cực thấp: $V_{baseline\_lab} \approx 0.005\text{V} - 0.03\text{V}$. Khi có $H_2S$ (1 ppm) hoặc $NH_3$ (10 ppm), điện áp cảm biến MQ136/MQ135 vọt lên $0.40\text{V} - 0.85\text{V}$.
- **Ngoài Trời Thực Tế:** Độ ẩm tương đối ($RH$) thường ở mức $70\% - 95\%$, nhiệt độ môi trường biến thiên, kết hợp với các hợp chất hữu cơ bay hơi tự nhiên (biogenic VOCs, khói xe) khiến điện áp nền tĩnh của cảm biến MOS bị dịch chuyển lên mức $V_{baseline\_outdoor} \approx 0.35\text{V} - 0.70\text{V}$.

### 1.2. Sai sót trong Pipeline hiện tại của Codebase
Qua rà soát chi tiết [backend/train.py](file:///g:/Project/AIoT/backend/train.py), [backend/gateway.py](file:///g:/Project/AIoT/backend/gateway.py) và [backend/app.py](file:///g:/Project/AIoT/backend/app.py), phát hiện 3 điểm nghẽn trí mạng:
1. **Trích xuất đặc trưng phụ thuộc điện áp tuyệt đối:**
   - Trong `extract_window_features`: Mảng đặc trưng chứa `mean_val`, `min_val`, `max_val` và toàn bộ 20 điểm thô $w_i$.
   - Trong `extract_pulse_features`: Chứa `v_min`, `v_max`, `mean_v`, `auc` và 10 điểm neo `anchors`.
   - *Hậu quả:* Cây quyết định (Random Forest) học các ngưỡng chia tuyệt đối (ví dụ `mean_v > 0.35V` hoặc `max_val > 0.40V` $\rightarrow$ $H_2S$). Khi ra ngoài trời, tín hiệu phẳng lì ở 0.55V lập tức bị gán nhãn $H_2S$ với độ tin cậy > 90%.
2. **Chốt chặn tĩnh (Hardcoded Guard) bị phá vỡ:**
   - Trong `gateway.py` (dòng 128) và `app.py` (dòng 189):
     `if compS3 <= 0.32: gas = 'Clean Air'`
   - Khi điện áp ngoài trời là 0.55V, điều kiện `compS3 <= 0.32` luôn **SAI**, làm vô hiệu hóa bộ lọc an toàn.
3. **Mức rủi ro gắn chặt vào điện áp thô:**
   - Trong `computeRiskLevel`: `if compVal >= 0.40: risk = 'Warning'`, `if compVal >= 0.60: risk = 'Hazardous'`.
   - Khi mô hình báo nhầm $H_2S$, mức điện áp ngoài trời 0.55V kích hoạt cảnh báo nguy hiểm (Warning/Hazardous) dù không có phân tử khí độc nào.

---

## 2. Lộ Trình Triển Khai Chi Tiết (Phased Roadmap)

```mermaid
graph TD
    subgraph Phase 1: Thuật Toán & Tiền Xử Lý
        A1[Chuyển đổi đặc trưng sang Vi sai ΔV] --> A2[Bộ theo dõi đường nền Adaptive Baseline Tracker]
        A2 --> A3[Chốt chặn động học Slope & Flatness Guard]
        A3 --> A4[Tách rời Logic Risk Level khỏi V tuyệt đối]
    end

    subgraph Phase 2: Dữ Liệu & Huấn Luyện AI
        B1[Thu thập chu kỳ Không khí ngoài trời thực tế] --> B2[Synthetic Plume Injection: Ghép xung Lab lên nền ngoài trời]
        B2 --> B3[Huấn luyện lại Dual-Mode Random Forest v2]
        B3 --> B4[Đánh giá Cross-Validation & Domain Invariance]
    end

    subgraph Phase 3: Dashboard & Edge Deployment
        C1[Tích hợp nút Zero Calibration trên Web UI] --> C2[Hiển thị đồng thời V_raw, V_0 và ΔV]
        C2 --> C3[Đồng bộ code & model lên Raspberry Pi 3]
        C3 --> C4[Kiểm thử thực địa & Giám sát tài nguyên]
    end

    Phase 1 --> Phase 2
    Phase 2 --> Phase 3
```

---

## 3. Giai Đoạn 1: Cải Tiến Thuật Toán & Tiền Xử Lý (Triển Khai Ngay - Zero Gas Needed)

### Nhiệm vụ 1.1: Chuyển đổi trích xuất đặc trưng sang Bất Biến Dịch Tuyệt Đối (Shift-Invariant Features)
- **Mục tiêu:** Toàn bộ đặc trưng đưa vào Random Forest phải biểu diễn sự thay đổi động học so với đường nền, không phụ thuộc vào điện áp nền đang ở 0.01V hay 0.60V.
- **Tập tin tác động:**
  - [backend/train.py](file:///g:/Project/AIoT/backend/train.py)
  - [backend/gateway.py](file:///g:/Project/AIoT/backend/gateway.py)
  - [backend/app.py](file:///g:/Project/AIoT/backend/app.py)

#### Công thức toán học:
Cho cửa sổ tín hiệu $W = [v_1, v_2, \dots, v_n]$ và đường nền hiện tại $V_0$:
1. Chuỗi vi sai chuẩn hóa:
   $$\Delta w_i = v_i - V_0$$
2. Tốc độ biến thiên (Slope):
   $$\text{Slope} = \frac{v_n - v_1}{n \cdot \Delta t}$$
3. Độ lệch chuẩn vi sai:
   $$\sigma_{\Delta} = \text{std}(\Delta W)$$
4. Tỷ lệ đáp ứng tương đối:
   $$\text{Relative Amplitude} = \frac{\max(W) - V_0}{V_0 + \epsilon}$$
5. Độ dốc bậc hai (Curvature):
   $$\Delta^2 v_t = v_t - 2v_{t-1} + v_{t-2}$$

> **Quy tắc:** Loại bỏ hoàn toàn `mean_val`, `min_val`, `max_val` tuyệt đối và mảng $w$ thô ra khỏi vector đặc trưng; thay thế bằng `[v - V_0 for v in w]`.

---

### Nhiệm vụ 1.2: Xây dựng Module Quản Lý & Cân Chỉnh Đường Nền (`backend/calibration.py`)
- **Tập tin tạo mới:** `backend/calibration.py`
- **Chức năng:**
  1. **Khởi động & Sấy cảm biến (Warm-up Phase):**
     - Đếm 30–60 điểm đầu tiên (khoảng 60–120s) khi khởi động thiết bị để cảm biến đạt nhiệt độ sấy ổn định.
     - Tự động gán $V_0 = \text{median}(V_{\text{warmup}})$.
  2. **Cân chỉnh tức thì (Manual Zero Calibration):**
     - Cho phép người dùng bấm nút trên Dashboard hoặc gọi API `POST /api/calibrate/zero` khi đặt thiết bị ở không khí sạch ngoài trời.
     - Lấy trung vị 15 mẫu gần nhất làm giá trị $V_0$ mới.
  3. **Tự động theo dõi trôi chậm (Adaptive Slow Tracking):**
     - Khi hệ thống đang ở trạng thái an toàn (Clean Air) và tín hiệu ổn định, đường nền $V_0$ được cập nhật từ từ bằng bộ lọc EMA siêu chậm:
       $$V_0(t) = (1 - \alpha) V_0(t-1) + \alpha V(t), \quad \alpha \approx 0.002$$
     - Khi phát hiện biến thiên bất thường ($|\Delta V| > 0.08\text{V}$ hoặc $|dV/dt| > 0.005\text{V/s}$), **KHÓA NGAY** việc cập nhật $V_0$ để tránh trường hợp khí độc làm dịch đường nền.

---

### Nhiệm vụ 1.3: Bộ Chốt Chặn Động Học (Kinematic Slope & Flatness Guard)
- **Tập tin tác động:** [backend/gateway.py](file:///g:/Project/AIoT/backend/gateway.py) và [backend/app.py](file:///g:/Project/AIoT/backend/app.py)
- **Nguyên lý:**
  - Khí độc rò rỉ phát tán theo chùm (gas plume) luôn có giai đoạn bốc lên nhanh (sharp rising edge): $dV/dt > 0.01\text{V/s}$ và $\Delta V \ge 0.10\text{V}$.
  - Không khí ngoài trời dù ẩm (V = 0.55V) nhưng phẳng lặng:
    $$\text{std}(W_{20}) < 0.015\text{V} \quad \text{và} \quad |dV/dt| < 0.004\text{V/s} \quad \text{và} \quad |V(t) - V_0| < 0.06\text{V}$$
  - **Hành vi chốt chặn:** Nếu thỏa mãn điều kiện phẳng lặng trên, hệ thống cưỡng bức phân loại là `Clean Air`, gán `ppm = 0.0`, độ tin cậy `confidence >= 98%`, bỏ qua dự đoán của Random Forest.

---

### Nhiệm vụ 1.4: Tách rời Logic Cảnh Báo Rủi Ro Khỏi Điện Áp Tuyệt Đối
- **Tập tin tác động:** Hàm `computeRiskLevel` trong [backend/app.py](file:///g:/Project/AIoT/backend/app.py) và [backend/gateway.py](file:///g:/Project/AIoT/backend/gateway.py)
- **Sửa đổi logic:**
  ```python
  # TRƯỚC (LỖI): Dựa vào điện áp tuyệt đối
  # if gas == 'H2S': if ppmVal >= 10.0 or compVal >= 0.85: risk = 'Emergency' ... elif compVal >= 0.40: risk = 'Warning'

  # SAU (CHUẨN): Dựa vào nồng độ ppm ước lượng và biên độ vi sai delta_V
  def computeRiskLevel(gas, ppmVal, deltaV):
      if gas == 'Clean Air' or deltaV < 0.08:
          return 'Normal'
      if gas == 'H2S':
          if ppmVal >= 10.0 or deltaV >= 0.55:
              return 'Emergency'
          elif ppmVal >= 5.0 or deltaV >= 0.35:
              return 'Hazardous'
          elif ppmVal >= 1.0 or deltaV >= 0.12:
              return 'Warning'
      elif gas == 'NH3':
          if ppmVal >= 100.0 or deltaV >= 0.65:
              return 'Emergency'
          elif ppmVal >= 50.0 or deltaV >= 0.45:
              return 'Hazardous'
          elif ppmVal >= 25.0 or deltaV >= 0.15:
              return 'Warning'
      return 'Normal'
  ```

---

## 4. Giai Đoạn 2: Làm Giàu Dữ Liệu & Huấn Luyện AI (Synthetic Data Augmentation)

### Nhiệm vụ 2.1: Thu thập bộ dữ liệu Môi trường Ngoài trời (Outdoor Clean Air)
- **Mục tiêu:** Thu thập 50–100 chu kỳ (mỗi chu kỳ 250 điểm, 60 giây) của không khí ngoài trời thực tế ở các điều kiện khác nhau.
- **Tập tin công cụ:** Tạo script `scripts/record_outdoor_air.py` để tự động lắng nghe WebSocket hoặc Firebase RTDB và lưu chu kỳ vào `data/air_outdoor_clean.csv`.
- **Kịch bản thu mẫu thực tế:**
  1. Buổi sáng sớm (độ ẩm cao 85–95%, sương sớm).
  2. Buổi trưa nắng ráo (độ ẩm 55–65%, nhiệt độ cao).
  3. Buổi chiều tối (nhiệt độ hạ, lưu lượng xe cộ tăng).

---

### Nhiệm vụ 2.2: Kỹ thuật Ghép Xung Khí Độc Lên Nền Ngoài Trời (Synthetic Plume Injection)
- **Tập tin công cụ:** `scripts/augment_outdoor_data.py`
- **Nguyên lý:**
  - Không cần đem bình khí độc nguy hiểm ra ngoài trời.
  - Từ dữ liệu Lab đã có ([data/h2s_sensor_1_clean.csv](file:///g:/Project/AIoT/data/h2s_sensor_1_clean.csv), [data/nh3_sensor_1_clean.csv](file:///g:/Project/AIoT/data/nh3_sensor_1_clean.csv)):
    Trích xuất xung thuần túy đã trừ nền Lab:
    $$\Delta V_{\text{gas\_lab}}(t) = V_{\text{gas\_lab}}(t) - V_{\text{baseline\_lab}}$$
  - Lấy đường nền ngoài trời $V_{\text{outdoor}}(t)$ từ tập mẫu thu được ở Bước 2.1.
  - Tổng hợp chu kỳ mới:
    $$V_{\text{synthetic}}(t) = V_{\text{outdoor}}(t) + \alpha_{\text{drift}} \cdot \Delta V_{\text{gas\_lab}}(t) + \mathcal{N}(0, \sigma_{\text{noise}})$$
    Trong đó:
    - $\alpha_{\text{drift}} \in [0.9, 1.1]$: Hệ số co giãn độ nhạy cảm biến theo nhiệt ẩm.
    - $\sigma_{\text{noise}} \approx 0.003\text{V}$: Nhiễu trắng mô phỏng gió ngoài trời.
- **Kết quả:** Sinh ra 300+ chu kỳ $H_2S$ và $NH_3$ với nhiều mức nồng độ đặt trên nền ngoài trời thực tế dao động từ 0.35V đến 0.70V.

---

### Nhiệm vụ 2.3: Huấn Luyện Lại Cặp Mô Hình Dual-Mode Random Forest v2
- **Tập tin tác động:** [backend/train.py](file:///g:/Project/AIoT/backend/train.py)
- **Pipeline huấn luyện:**
  1. Tải cả tập Clean Air Lab và Clean Air Ngoài trời $\rightarrow$ Gán toàn bộ nhãn là `Clean Air`.
  2. Trích xuất đặc trưng sử dụng hàm vi sai mới (Shift-Invariant).
  3. Chạy 5-Fold Stratified Cross-Validation để kiểm tra độ chính xác phân loại và MAE nồng độ ppm.
  4. Xuất 4 tệp mô hình mới:
     - `backend/model_gas.pkl` (Window Classifier)
     - `backend/model_ppm.pkl` (Window Regressor)
     - `backend/model_pulse_gas.pkl` (Pulse Classifier)
     - `backend/model_pulse_ppm.pkl` (Pulse Regressor)
  5. Cập nhật `dashboard/model_metrics.json` và `dashboard/gas_profiles.json`.

---

## 5. Giai Đoạn 3: Nâng Cấp Web Dashboard & Triển Khai Raspberry Pi 3

### Nhiệm vụ 3.1: Nâng cấp Giao diện Điều Khiển (Web Dashboard)
- **Tập tin tác động:**
  - [dashboard/index.html](file:///g:/Project/AIoT/dashboard/index.html)
  - [dashboard/experiment.html](file:///g:/Project/AIoT/dashboard/experiment.html)
- **Các thành phần bổ sung:**
  1. **Nút "Zero Calibration" (Cân Chỉnh Nền):**
     - Nút bấm trực quan trên thanh điều hướng/thanh trạng thái: `[ 🎯 Zero Calibrate ]`.
     - Nhãn hiển thị trạng thái đường nền hiện tại: `Baseline: 0.542V | Mode: Outdoor Adaptive`.
  2. **Biểu đồ kép (Dual Trace Graph):**
     - Cho phép chuyển đổi hoặc vẽ đồng thời 2 đường:
       - Đường 1: Điện áp cảm biến thô $V(t)$ (để kỹ sư theo dõi tình trạng phần cứng).
       - Đường 2: Điện áp vi sai $\Delta V(t) = V(t) - V_0$ (tín hiệu thực sự quyết định khí độc).
  3. **Huy hiệu Chốt chặn Động học (Guard Indicator):**
     - Khi tín hiệu phẳng lặng, hiển thị badge xanh lá: `● Flat Baseline Protected (Clean Air)`.

---

### Nhiệm vụ 3.2: Triển Khai & Kiểm Thử Trên Raspberry Pi 3
- **Thiết bị:** Raspberry Pi 3 Model B (`pi@100.72.0.24`, Debian Trixie 64-bit).
- **Quy trình triển khai:**
  1. Chạy unit test kiểm tra tính tương thích trên máy cục bộ:
     `pytest tests/test_calibration_and_guards.py -v`
  2. Đẩy mã nguồn và 4 file model `.pkl` lên Raspberry Pi qua Tailscale SSH:
     ```bash
     rsync -avz --exclude '.venv' --exclude '__pycache__' ./ pi@100.72.0.24:/home/pi/Desktop/AIoT/
     ```
  3. Khởi động lại dịch vụ `aiot-gateway.service`:
     ```bash
     sudo systemctl restart aiot-gateway.service
     sudo journalctl -u aiot-gateway.service -f
     ```
  4. Xác nhận hiệu năng trên Pi 3:
     - Tải RAM: `< 90MB RAM`.
     - Độ trễ suy luận vi sai: `~3.0 ms / lần suy luận`.
     - Không còn báo nhầm $H_2S$/$NH_3$ khi đưa máy ra ban công/ngoài trời.

---

## 6. Kế Hoạch Kiểm Thử & Tiêu Chí Nghiệm Thu (Acceptance Criteria)

| STT | Kịch bản kiểm thử | Dữ liệu đầu vào | Kết quả mong đợi |
|:---:|:---|:---|:---|
| 1 | **Clean Air Ngoài Trời Ổn Định** | $V = 0.55\text{V} \pm 0.005\text{V}$, phẳng lặng trong 60s | Phân loại: `Clean Air` (100%), `ppm = 0.0`, Risk: `Normal`. |
| 2 | **Độ Ẩm Tăng Chậm Ngoài Trời** | $V$ trôi từ $0.50\text{V} \rightarrow 0.65\text{V}$ trong 10 phút | Đường nền $V_0$ tự động bám theo; Phân loại duy trì `Clean Air`. |
| 3 | **Bấm Nút Zero Calibrate** | Đang ở môi trường nền $V = 0.58\text{V}$, bấm nút | $V_0$ cập nhật về $0.58\text{V}$, $\Delta V$ về $0.0\text{V}$, hệ thống sẵn sàng. |
| 4 | **Rò Rỉ $H_2S$ Thật Ngoài Trời (Giả lập)** | $V$ vọt từ $0.55\text{V} \rightarrow 1.15\text{V}$ ($dV/dt > 0.03\text{V/s}$) | Khóa cập nhật $V_0$; Nhận diện chính xác `H2S`, báo động `Hazardous/Emergency`. |
| 5 | **Hồi Phục Sau Rò Rỉ** | Khí tan, $V$ hạ từ $1.15\text{V}$ về lại $0.55\text{V}$ | Trở về trạng thái `Normal`, mở lại chế độ theo dõi đường nền tự động. |
| 6 | **Tài Nguyên Raspberry Pi 3** | Chạy liên tục trong 2 giờ streaming | RAM $< 100\text{MB}$, CPU $< 15\%$, không bị OOM killer. |

---

## 7. Đề Xuất Hành Động Ngay Tiếp Theo

Sau khi thống nhất kế hoạch này, các bước thực hiện tiếp theo được chia thành 2 phiên làm việc:
1. **Phiên 1:** Triển khai **Giai đoạn 1** (Viết module `backend/calibration.py`, tái cấu trúc `extract_window_features` sang vi sai $\Delta V$, cập nhật chốt chặn `Slope & Flatness Guard`, sửa `computeRiskLevel`). Đã có thể giải quyết ngay 85% lỗi báo nhầm trên hiện trường.
2. **Phiên 2:** Triển khai **Giai đoạn 2 & 3** (Viết script sinh dữ liệu Synthetic Augmentation, retrain lại model, thêm nút Zero Calibrate lên Web Dashboard, và deploy trực tiếp lên Raspberry Pi 3).
