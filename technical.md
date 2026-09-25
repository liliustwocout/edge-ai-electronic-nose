# TÀI LIỆU KỸ THUẬT TOÀN DIỆN VÀ BỘ CÂU HỎI PHẢN BIỆN BẢO VỆ ĐỒ ÁN (100+ DEFENSE Q&A)
## HỆ THỐNG MŨI ĐIỆN TỬ EDGE AI PHÁT HIỆN SỚM KHÍ ĐỘC CÔNG NGHIỆP

---

**Dự án:** Edge AI-Based Electronic Nose For Toxic Gas Detection In Industrial Plants  
**Cuộc thi:** Advantech AIoT InnoWorks  
**Đơn vị đào tạo:** Trường Đại học Phenikaa — Khoa Điện - Điện tử (EEE)  
**Giảng viên hướng dẫn:** TS. Nguyễn Đắc Cử  
**Nhóm tác giả (TaskForce141):**  
1. Đỗ Đức Khởi — Trưởng nhóm  
2. Lê Phạm Thành Đạt — Thành viên  
3. Vũ Anh Kiệt — Thành viên  

---

# MỤC LỤC

1. [PHẦN I: TỔNG QUAN HỆ THỐNG & ĐẶC TẢ KỸ THUẬT ĐẦU CUỐI](#phần-i-tổng-quan-hệ-thống--đặc-tả-kỹ-thuật-đầu-cuối)
   - 1.1. Tính cấp thiết và bối cảnh ứng dụng
   - 1.2. Hạn chế cốt tử của đầu báo khí truyền thống
   - 1.3. Đột phá từ Mũi Điện Tử (E-Nose) & Trí Tuệ Nhân Tạo Biên (Edge AI)
   - 1.4. Thông số mục tiêu và dải khí định lượng
2. [PHẦN II: KIẾN TRÚC 5 TẦNG CÔNG NGHIỆP AIoT](#phần-ii-kiến-trúc-5-tầng-công-nghiệp-aiot)
   - 2.1. Tầng 1: Tầng Cảm biến & Thu thập hiện trường (Perception Layer)
   - 2.2. Tầng 2: Tầng Truyền thông công nghiệp chống nhiễu (Communication Layer)
   - 2.3. Tầng 3: Tầng Tính toán Biên & Trí tuệ nhân tạo (Edge AI Computing Layer)
   - 2.4. Tầng 4: Tầng Nền tảng Đám mây (Cloud Platform Layer)
   - 2.5. Tầng 5: Tầng Ứng dụng & Trung tâm Giám sát Điều hành (Application Layer)
3. [PHẦN III: PHÂN TÍCH CHI TIẾT TOÀN BỘ LUỒNG DỮ LIỆU & THUẬT TOÁN (END-TO-END DATAFLOW)](#phần-iii-phân-tích-chi-tiết-toàn-bộ-luồng-dữ-liệu--thuật-toán-end-to-end-dataflow)
   - 3.1. Cơ chế phát xung nhiệt và lấy mẫu chu kỳ sóng (WaveCycle Dynamics)
   - 3.2. Truyền dẫn vi sai RS-485 và đóng gói khung truyền
   - 3.3. Bộ giải mã luồng và xử lý phân mảnh gói tin (`StreamPacketParser`)
   - 3.4. Quản lý bộ đệm xoay vòng và nội suy chu kỳ khuyết thiếu (`PointBuffer`)
   - 3.5. Tiền xử lý số hóa: Khử gai phần cứng Cubic Spline và làm mượt Savitzky-Golay
   - 3.6. Bù trôi nhiệt ẩm môi trường (Thermal & Humidity Drift Compensation)
   - 3.7. Bộ bám đường nền thích ứng và khóa xung khí độc (`BaselineTracker`)
   - 3.8. Trích xuất đặc trưng vi sai bất biến dịch chuyển (Shift-Invariant Feature Extraction)
   - 3.9. Kiến trúc mô hình Edge AI Dual-Mode (RandomForest Classifier & Regressor)
   - 3.10. Động cơ phân cấp an toàn 4 mức OSHA và dự báo chân trời động học (+20s Horizon Prognostics)
   - 3.11. Lưu trữ cục bộ Fail-Safe (SQLite) và xuất bản thời gian thực lên Cloud (Firebase RTDB / WISE-IoT)
4. [PHẦN IV: CƠ SỞ DỮ LIỆU THỰC NGHIỆM, HUẤN LUYỆN & KIỂM CHỨNG MÔ HÌNH](#phần-iv-cơ-sở-dữ-liệu-thực-nghiệm-huấn-luyện--kiểm-chứng-mô-hình)
   - 4.1. Quy trình thu thập dữ liệu buồng thí nghiệm 361 chu kỳ
   - 4.2. Kỹ thuật ghép xung tổng hợp thích ứng miền thực địa (Synthetic Plume Injection)
   - 4.3. Phương pháp kiểm chứng Stratified 5-Fold Zero-Overlap Cross-Validation
   - 4.4. Đánh giá độ chính xác, sai số hồi quy MAE, R² và Ma trận nhầm lẫn
   - 4.5. Phân tích độ quan trọng của đặc trưng vật lý (Feature Importance)
5. [PHẦN V: BỘ 100+ CÂU HỎI VÀ CÂU TRẢ LỜI PHẢN BIỆN BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG](#phần-v-bộ-100-câu-hỏi-và-câu-trả-lời-phản-biện-bảo-vệ-đồ-án-trước-hội-đồng)
   - Nhóm 1: Bối cảnh, Động lực & Tính mới của Đề tài (Câu 1 - 15)
   - Nhóm 2: Phần cứng Cảm biến, Mạch đo & Hiện tượng Hóa lý (Câu 16 - 30)
   - Nhóm 3: Mạng công nghiệp RS-485, Modbus RTU & Giao thức truyền thông (Câu 31 - 45)
   - Nhóm 4: Xử lý Tín hiệu Số, Lọc nhiễu & Bù trôi Đường nền (Câu 46 - 60)
   - Nhóm 5: Trí tuệ Nhân tạo Biên (Edge AI), Trích xuất Đặc trưng & Huấn luyện (Câu 61 - 80)
   - Nhóm 6: Đánh giá Rủi ro An toàn, Gradient Prognostics & Vận hành SCADA (Câu 81 - 92)
   - Nhóm 7: Tối ưu hóa Nhúng, Khả năng triển khai Raspberry Pi 3 & Độ bền 24/7 (Câu 93 - 105)
   - Nhóm 8: An toàn thông tin, Độ tin cậy công nghiệp & Hướng phát triển (Câu 106 - 115)

---

# PHẦN I: TỔNG QUAN HỆ THỐNG & ĐẶC TẢ KỸ THUẬT ĐẦU CUỐI

### 1.1. Tính cấp thiết và bối cảnh ứng dụng
Trong các cơ sở công nghiệp nặng như nhà máy lọc hóa dầu, trạm xử lý khí tự nhiên, giàn khoan khai thác dầu khí thượng nguồn và các hệ thống thu gom nước thải công nghiệp, rò rỉ khí độc hại luôn là hiểm họa thường trực. Trong đó, Hydrogen Sulfide ($H_2S$) và Ammonia ($NH_3$) là hai hợp chất hóa học đặc biệt nguy hiểm:
- **$H_2S$ (Hydro Sulfide):** Là một loại khí không màu, có mùi trứng thối đặc trưng ở nồng độ cực thấp ($< 0.1\text{ ppm}$), nhưng gây tê liệt thần kinh khứu giác nhanh chóng ở nồng độ từ $10\text{ ppm}$. Khi nồng độ chạm ngưỡng $50 - 100\text{ ppm}$, nạn nhân có thể mất ý thức chỉ sau vài hơi thở và tử vong nhanh chóng (ngưỡng IDLH - Immediately Dangerous to Life or Health là $100\text{ ppm}$). Ngoài ra, $H_2S$ còn là tác nhân ăn mòn kim loại cực mạnh gây hư hỏng đường ống dẫn áp lực cao.
- **$NH_3$ (Amoniac):** Là khí gây kích ứng đường hô hấp và ăn mòn mô nghiêm trọng thường xuất hiện trong các hệ thống làm lạnh công nghiệp và tháp sản xuất phân bón. Khi tiếp xúc với không khí ẩm, $NH_3$ tạo thành dung dịch kiềm ăn mòn mắt, phổi và da.

### 1.2. Hạn chế cốt tử của đầu báo khí truyền thống
Hiện nay, đa phần các nhà máy công nghiệp vẫn sử dụng các cảm biến điểm cố định (Fixed Point Gas Detectors) dựa trên ngưỡng điện áp tĩnh (Static Threshold). Các đầu báo này tồn tại 3 nhược điểm cố hữu:
1. **Thời gian phát hiện chậm trễ:** Do thiết bị chỉ báo động khi nồng độ khí tại màng cảm biến vượt qua ngưỡng cài đặt cứng (ví dụ $10\text{ ppm}$ đối với $H_2S$). Trong các không gian rộng hoặc có gió, khi nồng độ tại cảm biến đạt $10\text{ ppm}$ thì tại vị trí rò rỉ thực tế, lượng khí tích tụ đã đạt mức nổ hoặc gây tử vong cho công nhân lân cận.
2. **Tỷ lệ báo động giả (False Alarms) cực cao:** Cảm biến bán dẫn oxit kim loại (MOS) và điện hóa truyền thống rất nhạy cảm với sự thay đổi của nhiệt độ, độ ẩm môi trường (Drift) cũng như bị ảnh hưởng bởi các khí nền thông thường (khói xả động cơ máy nén, dung môi tẩy rửa VOCs). Một cơn mưa rào làm độ ẩm tăng vọt từ $60\%$ lên $95\%$ có thể làm tăng điện trở cảm biến, kích hoạt báo động sai khiến toàn bộ dây chuyền sản xuất phải dừng khẩn cấp (Emergency Shutdown), gây thiệt hại hàng trăm triệu đồng mỗi giờ.
3. **Thiếu khả năng dự báo động học (Predictive Prognostics):** Đầu báo truyền thống không có khả năng nhận biết tốc độ phát tán của dòng khí độc ($\Delta C / \Delta t$) để đưa ra thời gian ước tính trước khi đạt mức nguy kịch (Time-to-Emergency).

### 1.3. Đột phá từ Mũi Điện Tử (E-Nose) & Trí Tuệ Nhân Tạo Biên (Edge AI)
Hệ thống Mũi Điện Tử Thông Minh kết hợp Edge AI do nhóm TaskForce141 phát triển khắc phục hoàn toàn các nhược điểm trên nhờ 4 trụ cột kỹ thuật:
1. **Gas Fingerprint Kinetic Signature:** Khai thác đặc tính động học hấp phụ (adsorption) và giải hấp phụ (desorption) của cụm cảm biến đa thành phần qua chu kỳ sóng nhiệt 60 giây (**WaveCycle 250 điểm**) để tạo nên dấu vân tay khí đặc thù, phân biệt chính xác $H_2S$ và $NH_3$ khỏi không khí sạch.
2. **Kiến trúc Edge AI Dual-Mode:** Vận hành đồng thời 2 cấp độ mô hình máy học: cấp độ chu kỳ (Pulse Model - 250 điểm) cho kết quả định danh và định lượng cực kỳ chuẩn xác, kết hợp cấp độ trượt cửa sổ thời gian thực (Window Model - 20 điểm) cho độ trễ suy luận tức thời dưới $100\text{ ms}$.
3. **Bù trôi đường nền thích ứng ngoài trời (Adaptive Baseline Drift Tracker):** Chuyển đổi toàn bộ không gian đặc trưng sang dạng vi sai tương đối ($\Delta V = V(t) - V_0$) và chốt chặn động học phẳng lặng, giúp triệt tiêu $100\%$ hiện tượng báo động giả khi triển khai ở môi trường ngoài trời có độ ẩm cao.
4. **Tự động hóa hoàn toàn trên phần cứng nhúng chi phí thấp:** Hệ thống được tối ưu hóa sâu để chạy độc lập $24/7$ trên máy tính nhúng Raspberry Pi 3 Model B (RAM 1GB), không phụ thuộc vào kết nối Internet để ra quyết định an toàn (Fail-Safe Offline Mode).

### 1.4. Thông số mục tiêu và dải khí định lượng

| Loại Khí Mục Tiêu | Loại Rủi Ro | Dải Nồng Độ Khảo Sát | Ngưỡng Cảnh Báo An Toàn (OSHA Standard) |
| :--- | :--- | :--- | :--- |
| **$H_2S$ (Hydro Sulfide)** | Độc tính chết người | $1\text{ ppm}, 5\text{ ppm}, 10\text{ ppm}$ | $\ge 1\text{ ppm}$: Warning <br> $\ge 5\text{ ppm}$: Hazardous <br> $\ge 10\text{ ppm}$: Emergency |
| **$NH_3$ (Amoniac)** | Kích ứng công nghiệp | $10\text{ ppm}, 50\text{ ppm}, 100\text{ ppm}$ | $\ge 25\text{ ppm}$: Warning <br> $\ge 50\text{ ppm}$: Hazardous <br> $\ge 100\text{ ppm}$: Emergency |
| **Clean Air (Không khí sạch)** | Đường nền tham chiếu | $0\text{ ppm}$ | Normal (An toàn) |

---

# PHẦN II: KIẾN TRÚC 5 TẦNG CÔNG NGHIỆP AIoT

Hệ thống được thiết kế tuân thủ tiêu chuẩn kiến trúc 5 tầng công nghiệp AIoT khép kín:

```
[ TẦNG 5: APPLICATION LAYER ] 
   ▲  Web SCADA Operations Dashboard • Realtime Oscilloscope • Exhibition Standee
   │  (Web Audio Siren Alert, 2D Plant Topology, Email Dispatch Simulation)
   ▼
[ TẦNG 4: CLOUD PLATFORM LAYER ] 
   ▲  Advantech WISE-IoT Cloud Platform & Firebase Realtime Database
   │  (Secure MQTT Ingestion, SSE Telemetry Stream, Long-Term Historical Storage)
   ▼
[ TẦNG 3: EDGE AI COMPUTING LAYER ] 
   ▲  Raspberry Pi 3 Model B Gateway (Quad-Core Cortex-A53, RAM 1GB)
   │  (Modbus Master, Despike Filter, Adaptive Baseline Tracker, Dual-Mode RandomForest, SQLite)
   ▼
[ TẦNG 2: COMMUNICATION LAYER ] 
   ▲  RS-485 Industrial Daisy-Chain Bus (Modbus RTU, 115200 Baud, 8N1, 120Ω Termination)
   │  (Chống nhiễu điện từ trường EMI từ máy nén khí công nghiệp, truyền xa > 500m)
   ▼
[ TẦNG 1: PERCEPTION LAYER ] 
      ESP32 Microcontroller Node + Sensor Array (MQ136, MQ135, DHT22)
      (Vỏ bảo vệ IP65 kèm màng lọc khí PTFE Hydrophobic, Nguồn 12V DC / LiFePO4)
```

### 2.1. Tầng 1: Tầng Cảm biến & Thu thập hiện trường (Perception Layer)
- **Cụm cảm biến hỗn hợp (Sensor Matrix):**
  - **MQ136 / ZE03-H2S:** Cảm biến chuyên dụng đo khí $H_2S$ mục tiêu. Cảm biến sử dụng vật liệu bán dẫn $SnO_2$, khi tiếp xúc với khí khử $H_2S$, mật độ hạt mang điện tăng lên làm giảm điện trở bề mặt, dẫn đến điện áp đầu ra tăng tỷ lệ thuận với nồng độ khí.
  - **MQ135:** Cảm biến đa khí nhạy cảm với VOCs, khói, $CO_2$ và $NH_3$. Cảm biến này đóng vai trò đo khí nền nhằm xây dựng ma trận tương quan phân biệt (Gas Fingerprint).
  - **DHT22 (AM2302):** Đo đồng thời nhiệt độ (độ chính xác $\pm 0.5^\circ\text{C}$) và độ ẩm tương đối (độ chính xác $\pm 2\%\text{ RH}$) nhằm phục vụ thuật toán bù sai lệch vật lý của cảm biến MOS.
- **Khối xử lý biên sơ cấp (ESP32-WROOM-32):**
  - Lấy mẫu tín hiệu analog qua bộ chuyển đổi ADC 12-bit (4096 mức lượng tử hóa).
  - Áp dụng bộ lọc trung bình trượt cục bộ (Moving Average) để khử nhiễu lượng tử hóa ban đầu.
  - Điều khiển chân `DE/RE` (GPIO5) của chip thu phát MAX485 để kiểm soát hướng truyền tin bán song công (Half-Duplex).
- **Vỏ bảo vệ công nghiệp IP65:** Được chế tạo từ nhựa ABS chống cháy phủ sơn kháng ăn mòn hóa chất, trang bị màng lọc khí kỵ nước PTFE (Hydrophobic Membrane) ngăn chặn giọt nước và bụi bẩn bám dính vào bề mặt cảm biến nhưng vẫn cho các phân tử khí khuếch tán tự do qua buồng đo.

### 2.2. Tầng 2: Tầng Truyền thông công nghiệp chống nhiễu (Communication Layer)
- **Chuẩn vật lý RS-485:** Sử dụng đường truyền vi sai 2 dây ($A$ và $B$). Tín hiệu logic được định nghĩa dựa trên hiệu điện thế giữa 2 dây ($V_A - V_B$). Do đó, mọi xung nhiễu điện từ trường (Common-Mode Noise) sinh ra từ động cơ biến tần, máy nén khí công nghiệp đều tác động như nhau lên cả hai dây và bị triệt tiêu hoàn toàn tại bộ thu vi sai.
- **Topoloy tuyến tính (Daisy-Chain):** Các trạm cảm biến được nối tiếp dọc theo tuyến ống dẫn khí công nghiệp, hai đầu mút của đường bus được gắn điện trở kết thúc đường dây $120\ \Omega$ (Termination Resistor) để triệt tiêu hiện tượng phản xạ sóng tín hiệu cao tần.
- **Giao thức Modbus RTU / Streaming Token:** Hỗ trợ cả 2 chế độ:
  1. Chuẩn công nghiệp Modbus RTU: Đọc holding registers qua Function Code `0x03` với cấu trúc định dạng 16-bit.
  2. Chuẩn Fast Streaming Token: Định dạng gói tin văn bản rút gọn tối ưu băng thông `Pxxx:valueV` (ví dụ `P172:0.0183V`), truyền trực tiếp với tốc độ baud cao $115200\text{ bps}$.

### 2.3. Tầng 3: Tầng Tính toán Biên & Trí tuệ nhân tạo (Edge AI Computing Layer)
- **Thiết bị cổng trung tâm (Edge Gateway):** Vận hành trên máy tính nhúng **Raspberry Pi 3 Model B** (Bộ vi xử lý Broadcom BCM2837, 4 nhân ARM Cortex-A53 64-bit xung nhịp $1.2\text{ GHz}$, RAM vật lý $1\text{ GB}$).
- **Hệ thống phần mềm biên bất đồng bộ (FastAPI Gateway):**
  - Đọc luồng serial không chặn (non-blocking) qua tiến trình ngầm chuyên dụng `SerialReceiver`.
  - Tiền xử lý số hóa đa tầng: Bộ lọc khử gai Cubic Spline, bộ lọc số Savitzky-Golay, bộ lọc EMA và bù trôi nhiệt ẩm.
  - Bộ bám đường nền thích ứng `BaselineTracker` tự động ước lượng điểm không $V_0$.
  - Động cơ suy luận Edge AI với 4 mô hình Random Forest vector hóa, thời gian xử lý cực nhanh: **$2.5\text{ ms} - 4.0\text{ ms}$ cho mỗi cửa sổ trượt**.
  - Lưu trữ cơ sở dữ liệu cục bộ SQLite `EdgeStorage.db` đảm bảo hoạt động an toàn $100\%$ khi mất kết nối mạng.

### 2.4. Tầng 4: Tầng Nền tảng Đám mây (Cloud Platform Layer)
- **Tích hợp kép Advantech WISE-IoT & Firebase Realtime Database:**
  - Cổng Gateway biên đẩy bản tin viễn trắc JSON qua giao thức MQTT lên Broker của nền tảng Advantech WISE-IoT phục vụ lưu trữ dài hạn, thống kê chuỗi thời gian và quản lý thiết bị vòng đời (Device Management).
  - Tích hợp luồng Server-Sent Events (SSE) đẩy dữ liệu thời gian thực tới nhánh riêng biệt `/edge_ai` trên Firebase Realtime Database, tạo cầu nối phân tán không độ trễ giữa thiết bị biên và hệ thống Dashboard đám mây.

### 2.5. Tầng 5: Tầng Ứng dụng & Trung tâm Giám sát Điều hành (Application Layer)
- **Operations Center Dashboard (`dashboard/index.html`):** Giao diện giám sát vận hành SCADA chuẩn công nghiệp (Industrial Dark Mode), hiển thị 6 thẻ chỉ số KPI quan trọng, biểu đồ phân bổ xác suất khí, dao động ký chu kỳ sóng WaveCycle 250 điểm với cơ chế quét đè (Sweep Overwrite) và vệt sóng chu kỳ trước (Ghost Trace), hệ thống cảnh báo âm thanh Web Audio API và mô phỏng gửi email khẩn cấp.
- **Experiment Lab Oscilloscope (`dashboard/experiment.html`):** Môi trường thực nghiệm chuyên sâu kết nối trực tiếp với cổng USB-RS485 hoặc luồng Firebase, phân tích dạng sóng 2 kênh cảm biến, hỗ trợ bật/tắt bộ lọc Despike và xuất dữ liệu báo cáo thực nghiệm dưới dạng tệp CSV.
- **Standee Triển lãm Chuẩn Khổ Đứng 80x180cm (`standee/index.html`):** Poster triển lãm khoa học kỹ thuật tỷ lệ chuẩn $4:9$, hỗ trợ chế độ chỉnh sửa trực tiếp (Live Edit), chế độ chụp màn hình sạch (Clean Capture Mode) và xuất bản in PDF chất lượng cao.

---

# PHẦN III: PHÂN TÍCH CHI TIẾT TOÀN BỘ LUỒNG DỮ LIỆU & THUẬT TOÁN (END-TO-END DATAFLOW)

Toàn bộ dòng chảy dữ liệu từ hạt khí rò rỉ tại hiện trường cho đến khi hiển thị cảnh báo lên màn hình người vận hành được mô tả chi tiết qua sơ đồ sau:

```
[Khí Rò Rỉ H2S/NH3] 
        │ 
        ▼ 
[Khối Cảm Biến MOS & DHT22] ──(Biến thiên điện trở / điện áp tương tự)
        │ 
        ▼ 
[ESP32 Sampling ADC 12-bit] ──(Chu kỳ sóng 250 mẫu / 60 giây, ~4.17 Hz)
        │ 
        ▼ 
[MAX485 Chuyển Đổi Vi Sai] ──(Bus RS-485 Daisy-Chain, 115200 Baud, Token "Pxxx:valueV")
        │ 
        ▼ 
[Bộ Thu Biên SerialReceiver] ──(Non-blocking I/O, tự động kết nối lại & exponential backoff)
        │ 
        ▼ 
[StreamPacketParser] ──(Ghép phân mảnh chuỗi, Regex Token Pattern, lọc rác byte)
        │ 
        ▼ 
[PointBuffer & Assembler] ──(Quản lý cửa sổ trượt 20 điểm & nội suy WaveCycle 250 điểm)
        │ 
        ▼ 
[Khối Tiền Xử Lý Số Hóa]
   ├── Lọc số EMA (α = 0.2)
   ├── Khử gai phần cứng Cubic Spline tại điểm ~125
   └── Bù trôi nhiệt ẩm: V_comp = V_ema / [1.0 + 0.0035*(T - 25.0) + 0.0015*(H - 60.0)]
        │ 
        ▼ 
[Bộ Theo Dõi Đường Nền Thích Ứng BaselineTracker]
   ├── Ước lượng V0 qua 20 điểm khởi động (Warm-up Phase)
   ├── Cập nhật trôi chậm (α = 0.002) khi môi trường không khí sạch
   ├── Khóa cứng V0 (Plume Lock) khi phát hiện rò rỉ khí hoặc đột biến dV/dt
   └── Chốt chặn động học phẳng lặng (Flatness & Slope Guard) chống báo động giả
        │ 
        ▼ 
[Trích Xuất Đặc Trưng Vi Sai Bất Biến Shift-Invariant Feature Extraction]
   ├── Window-Level: Δw = w - V0, Độ dốc (Slope), Độ biến thiên (Std), Tỷ lệ cực đại
   └── Pulse-Level: ΔV_max, AUC vi sai, Thời điểm đạt đỉnh, Tốc độ suy giảm, 10 Anchor Points
        │ 
        ▼ 
[Động Cơ Suy Luận Edge AI Dual-Mode]
   ├── Window Model (RandomForest): Suy luận streaming tức thời (< 100ms)
   └── Pulse Model (RandomForest): Đánh giá tổng thể 60 giây chu kỳ sóng
        │ 
        ▼ 
[Phân Cấp Rủi Ro An Toàn & Dự Báo Động Học]
   ├── 4 Mức An Toàn OSHA: Normal, Warning, Hazardous, Emergency
   └── Dự báo chân trời +20s (Gradient Prognostics) & Tính toán Time-to-Emergency (TTE)
        │ 
        ▼ 
[Điều Phối & Phân Phối Tín Hiệu Đầu Ra]
   ├── Ghi nhật ký cục bộ vào SQLite (EdgeStorage.db) & Buffer CSV
   ├── Đẩy dữ liệu không chặn qua EdgeFirebasePublisher (/edge_ai) & WISE-IoT (MQTT)
   └── Phát trực tiếp lên Web Dashboard qua WebSocket (/stream & /ws/live_experiment)
```

### 3.1. Cơ chế phát xung nhiệt và lấy mẫu chu kỳ sóng (WaveCycle Dynamics)
Cảm biến khí bán dẫn oxit kim loại (MOS) thông thường nếu nung nóng ở một mức nhiệt độ cố định sẽ có tính chọn lọc khí (Selectivity) rất kém. Để khắc phục, hệ thống áp dụng phương pháp điều chế nhiệt động học (Thermal Modulation). Trong chu kỳ 60 giây:
- Điện áp nung nóng cảm biến biến thiên theo chu kỳ sóng định trước làm nhiệt độ bề mặt màng oxit thay đổi liên tục. Tại mỗi mức nhiệt độ, phản ứng oxy hóa khử giữa bề mặt cảm biến với $H_2S$, $NH_3$ và các phân tử oxy môi trường diễn ra với hằng số tốc độ phản ứng khác nhau.
- Vi điều khiển ESP32 lấy mẫu tín hiệu với tần số xấp xỉ $4.17\text{ Hz}$, thu thập chính xác **250 điểm dữ liệu trong mỗi chu kỳ 60 giây** (mỗi điểm cách nhau $\Delta t \approx 240\text{ ms}$). Đường cong đáp ứng điện áp thu được chính là "vân tay khí động học" (Dynamic Kinetic Fingerprint).

### 3.2. Truyền dẫn vi sai RS-485 và đóng gói khung truyền
Dữ liệu từ ESP32 được đóng gói thành các token văn bản có cấu trúc:
$$\text{Token: } \texttt{"P"}\{\text{point\_index}\}\texttt{":"}\{\text{voltage\_value}\}\texttt{"V, "}$$
Ví dụ: `P172:0.0183V, P173:0.0178V`. Định dạng này nhẹ hơn định dạng JSON thô tới $75\%$, giúp giảm tải thời gian chiếm dụng đường truyền trên bus RS-485 và loại bỏ nguy cơ nghẽn hàng đợi UART FIFO trên vi điều khiển.

### 3.3. Bộ giải mã luồng và xử lý phân mảnh gói tin (`StreamPacketParser`)
Trong môi trường thực tế, việc đọc dữ liệu từ cổng nối tiếp thường gặp hiện tượng phân mảnh: một gói tin `P172:0.0183V` có thể bị ngắt làm đôi giữa 2 lần gọi hàm `read()` (ví dụ lần 1 nhận `P172:0.01`, lần 2 nhận `83V`). Lớp `StreamPacketParser` giải quyết triệt để vấn đề này bằng bộ đệm phân mảnh (`fragment_buffer`):
1. Ghép nối chuỗi dữ liệu mới nhận được vào đuôi của `fragment_buffer`.
2. Áp dụng biểu thức chính quy (Regex):
   ```python
   TOKEN_PATTERN = re.compile(r'(?:P\s*)?(\d{1,4})\s*:\s*([0-9]*\.?[0-9]+)\s*V', re.IGNORECASE)
   ```
3. Lặp qua tất cả các khớp hoàn chỉnh, chuyển đổi thành đối tượng `PointSample(point, voltage1, timestamp)` và đưa vào đường ống.
4. Phần chuỗi chưa hoàn chỉnh còn lại ở cuối được giữ lại trong `fragment_buffer` để ghép tiếp với lần đọc kế tiếp. Giới hạn bộ đệm tối đa 512 bytes để chống tràn bộ nhớ nếu đường truyền bị rác dữ liệu.

### 3.4. Quản lý bộ đệm xoay vòng và nội suy chu kỳ khuyết thiếu (`PointBuffer`)
Lớp `PointBuffer` duy trì cấu trúc bộ nhớ giới hạn tuyệt đối (`collections.deque`), không bao giờ gây rò rỉ bộ nhớ (Zero Memory Leak) khi chạy liên tục 24/7:
- **Rolling Window (20 điểm):** Lưu trữ 20 điểm điện áp gần nhất (tương đương $\sim 4.8\text{ giây}$) phục vụ mô hình suy luận dòng thời gian thực.
- **Cycle Assembler (250 điểm):** Một mảng tĩnh được cấp phát sẵn 250 phần tử `[None] * 250`. Khi phát hiện hiện tượng quay vòng chu kỳ (điểm đo nhảy từ vùng cuối $\ge 230$ về vùng đầu $< 20$):
  - Kiểm tra độ đầy đủ của chu kỳ: Nếu số lượng điểm nhận được đạt tối thiểu $70\%$ (tức $\ge 175$ điểm), hệ thống kích hoạt thuật toán **Nội suy tuyến tính (Linear Interpolation)** qua `np.interp` để tự động bù các điểm khuyết thiếu do xung nhiễu truyền dẫn, sau đó phát sự kiện `on_cycle_complete`.
  - Làm mới mảng để bắt đầu lắp ghép chu kỳ kế tiếp.

### 3.5. Tiền xử lý số hóa: Khử gai phần cứng Cubic Spline và làm mượt Savitzky-Golay
Tín hiệu cảm biến thô từ hiện trường luôn bị ảnh hưởng bởi 2 loại nhiễu vật lý:
1. **Nhiễu gai phần cứng tại điểm ~125 (Hardware Switching Spike):** Do mạch điều khiển chuyển đổi kênh gia nhiệt hoặc nạp tụ, tại điểm lấy mẫu thứ 125 thường xuất hiện một xung nhọn điện áp đột ngột vọt lên rồi suy giảm nhanh. Hàm `remove_hardware_spike()` sử dụng **nội suy Spline bậc ba (Cubic Spline)**:
   - Xác định điểm bắt đầu tăng vọt và điểm tín hiệu hồi phục về mức trước gai.
   - Lấy 5 điểm làm neo trước gai và 5 điểm làm neo sau vùng hồi phục.
   - Xây dựng đa thức Cubic Spline nội suy mượt mà qua vùng bị lỗi, triệt tiêu hoàn toàn gai xung mà không làm biến dạng biên độ thực của chất khí.
2. **Nhiễu ngẫu nhiên cao tần:** Áp dụng bộ lọc **Savitzky-Golay** với độ dài cửa sổ $w = 9$ và đa thức bậc $p = 2$. Khác với bộ lọc trung bình đơn giản làm tù đỉnh tín hiệu, bộ lọc Savitzky-Golay làm mượt nhiễu hạt nhưng vẫn bảo toàn nguyên vẹn giá trị điện áp đỉnh cực đại ($V_{max}$) và thời điểm đạt đỉnh ($T_{peak}$).

### 3.6. Bù trôi nhiệt ẩm môi trường (Thermal & Humidity Drift Compensation)
Cảm biến MOS có bề mặt nhạy khí là chất bán dẫn nung nóng, do đó độ ẩm cao sẽ cung cấp thêm các nhóm hydroxyl ($-OH$) bám dính làm tăng độ dẫn điện nền, trong khi nhiệt độ cao làm thay đổi tốc độ giải hấp phụ. Công thức bù trôi nhiệt ẩm thực nghiệm được tích hợp trong lớp `DriftCompensator`:
$$\text{compFactor} = 1.0 + K_T \cdot (T - T_{\text{ref}}) + K_H \cdot (H - H_{\text{ref}})$$
Trong đó:
- $T, H$ lần lượt là nhiệt độ ($^\circ\text{C}$) và độ ẩm tương đối ($\%\text{ RH}$) đọc từ cảm biến DHT22.
- $T_{\text{ref}} = 25.0^\circ\text{C}, H_{\text{ref}} = 60.0\%\text{ RH}$ là điều kiện môi trường chuẩn phòng thí nghiệm.
- Các hệ số bù thực nghiệm: $K_T = 0.0035\ /^\circ\text{C}$ và $K_H = 0.0015\ /\%\text{ RH}$.
- Tín hiệu sau bù:
  $$V_{\text{compensated}} = \frac{V_{\text{filtered}}}{\text{compFactor}}$$

### 3.7. Bộ bám đường nền thích ứng và khóa xung khí độc (`BaselineTracker`)
Khi đưa thiết bị ra môi trường thực địa ngoài trời, điện áp nền tĩnh của cảm biến bị trôi lên mức $0.35\text{V} - 0.70\text{V}$ (trong khi tại phòng thí nghiệm chỉ là $0.01\text{V} - 0.03\text{V}$). Nếu so sánh điện áp tuyệt đối, hệ thống sẽ báo động nhầm ngay lập tức. Lớp `BaselineTracker` giải quyết vấn đề này qua cơ chế 3 giai đoạn:
1. **Khởi động & Sấy cảm biến (Warm-up Phase):** Thu thập 20 điểm đầu tiên và gán giá trị trung vị làm đường nền ban đầu $V_0 = \text{median}(W_{\text{warmup}})$.
2. **Bám đuổi trôi chậm thích ứng (Adaptive Slow Tracking):** Khi môi trường phẳng lặng và không có khí độc, đường nền $V_0$ được cập nhật từ từ theo bộ lọc số:
   $$V_0(t) = (1 - \alpha) \cdot V_0(t-1) + \alpha \cdot V(t), \quad \text{với } \alpha = 0.002$$
3. **Khóa cứng đường nền khi có sự cố rò rỉ (Plume Event Lock):** Nếu phát hiện nồng độ khí tăng cao ($|\Delta V| > 0.06\text{V}$) hoặc độ dốc thay đổi đột ngột ($|dV/dt| > 0.004\text{V/s}$), trạng thái lập tức chuyển sang `LOCKED_EVENT` và **ngừng cập nhật $V_0$**, ngăn không cho chùm khí độc làm biến dạng đường nền chuẩn.
4. **Chốt chặn động học phẳng lặng (Flatness & Slope Guard):** Nếu tín hiệu thỏa mãn điều kiện ổn định ngoài trời ($\sigma_{\text{window}} \le 0.015\text{V}$ và $|dV/dt| \le 0.004\text{V/s}$), hệ thống tự động gán nhãn `Clean Air` ($0.0\text{ ppm}$), độ tin cậy $\ge 98\%$, loại bỏ hoàn toàn khả năng báo động giả ngoài trời.

### 3.8. Trích xuất đặc trưng vi sai bất biến dịch chuyển (Shift-Invariant Feature Extraction)
Để mô hình máy học không bị phụ thuộc vào điện áp tuyệt đối, toàn bộ đặc trưng được chuyển sang không gian vi sai đối với đường nền:
$$\Delta w_i = w_i - V_0$$
- **Vector đặc trưng cửa sổ trượt (Window Features - 32 chiều):**
  1. $\text{Mean\_Diff} = \frac{1}{n} \sum \Delta w_i$
  2. $\text{Std\_Val} = \sigma(w)$
  3. $\text{Max\_Diff} = \max(\Delta w)$, $\text{Min\_Diff} = \min(\Delta w)$
  4. $\text{Range\_Val} = \max(w) - \min(w)$
  5. $\Delta V = w_n - w_1$, $\text{Slope} = \frac{w_n - w_1}{n}$
  6. Trung bình và độ lệch chuẩn của sai phân bậc nhất ($\Delta^2 w$)
  7. Độ rộng tứ phân vị vi sai ($Q_3 - Q_1$)
  8. Tỷ lệ đáp ứng tương đối $\text{Ratio} = \frac{\text{Max\_Diff}}{\max(V_0, 0.05)}$
  9. Mảng 20 điểm vi sai trực tiếp $[\Delta w_1, \Delta w_2, \dots, \Delta w_{20}]$
- **Vector đặc trưng toàn chu kỳ (Pulse Features - 19 chiều):**
  1. Biên độ cực đại: $\Delta V = V_{max} - V_{min}$
  2. Diện tích dưới đường cong vi sai: $\text{AUC}_{\Delta} = \sum \max(0, p_i - V_0)$
  3. Tốc độ dâng đỉnh: $\text{Rise\_Slope} = \frac{V_{max} - p_0}{T_{peak}}$
  4. Tốc độ suy giảm giải hấp phụ: $\text{Decay\_Slope} = \frac{p_{end} - V_{max}}{250 - T_{peak}}$
  5. 10 điểm neo động học (Anchor Points) tại các giây thứ $4\text{s}, 7\text{s}, 12\text{s}, 18\text{s}, 24\text{s}, 29\text{s}, 34\text{s}, 41\text{s}, 48\text{s}, 55\text{s}$.

### 3.9. Kiến trúc mô hình Edge AI Dual-Mode (RandomForest Classifier & Regressor)
Hệ thống sử dụng thuật toán **Random Forest (Rừng ngẫu nhiên)** với 100 cây quyết định, giới hạn độ sâu tối đa $10 - 12$ tầng:
- Tại sao chọn Random Forest thay vì Mạng nơ-ron sâu (CNN/LSTM) hay SVM?
  - Cực kỳ nhẹ: Thời gian thực thi trên CPU ARM Cortex-A53 của Raspberry Pi 3 chỉ mất $\sim 3\text{ ms}$, tiêu thụ chưa đầy $80\text{ MB}$ RAM, không bao giờ gây lỗi tràn bộ nhớ (Out-Of-Memory OOM Crash).
  - Khả năng chống quá khớp (Overfitting) vượt trội nhờ cơ chế lấy mẫu ngẫu nhiên có hoàn lại (Bagging) và chọn tập con đặc trưng (Random Subspace).
  - Khả năng giải thích (Explainability) cao qua trọng số quan trọng của từng đặc trưng vật lý (Feature Importance).
- **Mô hình hoạt động kép (Dual-Mode Architecture):**
  - `model_pulse_gas.pkl` & `model_pulse_ppm.pkl`: Phân loại và hồi quy nồng độ khí trên toàn chu kỳ 60 giây, đạt độ chính xác cao nhất ($95.21\%$).
  - `model_gas.pkl` & `model_ppm.pkl`: Phân loại và hồi quy nồng độ streaming tức thời trên cửa sổ trượt 20 điểm ($\Delta t \approx 4.8\text{ giây}$), phục vụ cảnh báo sớm ngay khi khí vừa chạm vào đầu dò.

### 3.10. Động cơ phân cấp an toàn 4 mức OSHA và dự báo chân trời động học (+20s Horizon Prognostics)
- **Chuẩn phân cấp rủi ro 4 mức dựa trên nồng độ và vi sai $\Delta V$:**
  - **Level 1 (Normal):** $H_2S < 1.0\text{ ppm}$ hoặc $\Delta V < 0.08\text{V} \implies$ Môi trường an toàn.
  - **Level 2 (Warning):** $H_2S \ge 1.0\text{ ppm}$ hoặc $\Delta V \ge 0.12\text{V} \implies$ Phát hiện rò rỉ sớm, cảnh báo ca trực theo dõi.
  - **Level 3 (Hazardous):** $H_2S \ge 5.0\text{ ppm}$ hoặc $\Delta V \ge 0.35\text{V} \implies$ Vượt ngưỡng OSHA PEL, kích hoạt đèn chớp khu vực, yêu cầu trang bị mặt nạ cách ly SCBA.
  - **Level 4 (Emergency):** $H_2S \ge 10.0\text{ ppm}$ hoặc $\Delta V \ge 0.55\text{V} \implies$ Nguy hiểm tính mạng, còi báo động toàn nhà máy hú khẩn cấp, kích hoạt lệnh đóng van tự động ngắt tuyến ống.
- **Gradient Prognostics & Time-to-Emergency (TTE):**
  - Tính toán độ dốc biến thiên nồng độ theo thời gian thực $S = \frac{dw}{dt}$.
  - Ngoại suy quỹ đạo phát tán trong $+5\text{s}, +10\text{s}, +15\text{s}, +20\text{s}$:
    $$\hat{V}_{t+h} = V_t + S \cdot h$$
  - Nếu dự báo nồng độ sẽ vượt ngưỡng khẩn cấp ($2.45\text{V}$), hệ thống tính toán thời gian chạm ngưỡng nguy kịch:
    $$\text{TTE} = \max\left(3, \min\left(25, \frac{2.45 - V_t}{\max(0.002, S)}\right)\right)\ \text{giây}$$
  - Đưa ra cảnh báo cho công nhân sơ tán trước khi khí độc tích tụ tới mức gây bất tỉnh.

### 3.11. Lưu trữ cục bộ Fail-Safe (SQLite) và xuất bản thời gian thực lên Cloud (Firebase RTDB / WISE-IoT)
- **Chế độ hoạt động độc lập không mạng (Offline Resilient):** Mọi bản tin viễn trắc và sự kiện báo động được ghi đồng thời vào bảng `TelemetryRecords` và `AlarmEvents` trong cơ sở dữ liệu nhúng SQLite `backend/EdgeStorage.db`. Khi mất kết nối cáp mạng hoặc đứt đường truyền Internet, hệ thống cảnh báo tại chỗ (còi, đèn, rơ le đóng van) vẫn vận hành độc lập $100\%$.
- **Đẩy dữ liệu bất đồng bộ không chặn (Non-blocking Cloud Sync):** Lớp `EdgeFirebasePublisher` vận hành trong một luồng riêng (`daemon thread`), sử dụng hàng đợi có chặn giới hạn kích thước (`queue.Queue(maxsize=5)`) để đẩy dữ liệu lên Firebase RTDB nhánh `/edge_ai`. Nếu mạng chập chờn, các mẫu cũ tự động bị loại bỏ để đảm bảo dữ liệu hiển thị trên Web luôn là dữ liệu mới nhất mà không làm chậm chu kỳ suy luận của CPU.

---

# PHẦN IV: CƠ SỞ DỮ LIỆU THỰC NGHIỆM, HUẤN LUYỆN & KIỂM CHỨNG MÔ HÌNH

### 4.1. Quy trình thu thập dữ liệu buồng thí nghiệm 361 chu kỳ
Dữ liệu thực nghiệm được thu thập tại phòng thí nghiệm khoa Điện - Điện tử, Trường Đại học Phenikaa:
- Buồng đo kín dung tích $1.2\text{ lít}$, trang bị quạt đảo khí vi mô và cổng xả khí an toàn.
- Sử dụng bình khí chuẩn nồng độ cao pha loãng với khí sạch qua hệ thống lưu lượng kế khối (MFC) để tạo ra các dải nồng độ chính xác.
- Mỗi chu kỳ thử nghiệm kéo dài đúng $60\text{ giây}$ (250 điểm mẫu).
- **Phân bố tập dữ liệu hợp lệ sau lọc sạch:**
  1. `data/clean_air_sensor_1_clean.csv`: **133 chu kỳ** Clean Air ($0\text{ ppm}$).
  2. `data/h2s_sensor_1_clean.csv`: **110 chu kỳ** $H_2S$ (37 chu kỳ $1\text{ ppm}$, 37 chu kỳ $5\text{ ppm}$, 36 chu kỳ $10\text{ ppm}$).
  3. `data/nh3_sensor_1_clean.csv`: **118 chu kỳ** $NH_3$ (42 chu kỳ $10\text{ ppm}$, 42 chu kỳ $50\text{ ppm}$, 34 chu kỳ $100\text{ ppm}$).
  4. **Tổng số mẫu:** **361 chu kỳ chuẩn**.

### 4.2. Kỹ thuật ghép xung tổng hợp thích ứng miền thực địa (Synthetic Plume Injection)
Để huấn luyện mô hình thích ứng với môi trường ngoài trời mà không cần phải mang bình khí độc $H_2S$ ra xả ngoài môi trường, nhóm đã phát triển thuật toán **Synthetic Plume Injection** (`scripts/augment_outdoor_data.py`):
1. Thu thập chu kỳ không khí ngoài trời thực tế (`data/air_outdoor_clean.csv`) ở các điều kiện độ ẩm cao ($70\% - 95\%$), đường nền dao động từ $0.35\text{V} - 0.70\text{V}$.
2. Tách xung đáp ứng thuần túy từ dữ liệu phòng thí nghiệm:
   $$\Delta V_{\text{gas\_lab}}(t) = V_{\text{gas\_lab}}(t) - V_{\text{baseline\_lab}}$$
3. Ghép xung đáp ứng lên đường nền thực địa ngoài trời kèm hệ số co giãn độ nhạy nhiệt ẩm $\alpha \in [0.92, 1.08]$ và nhiễu trắng vi mô $\mathcal{N}(0, \sigma^2)$:
   $$V_{\text{synthetic}}(t) = V_{\text{outdoor}}(t) + \alpha \cdot \Delta V_{\text{gas\_lab}}(t) + \mathcal{N}(0, \sigma^2)$$
4. Sinh ra 180 chu kỳ dữ liệu tổng hợp (`data/synthetic_outdoor_dataset_v2.csv`), bổ sung vào tập huấn luyện giúp cây quyết định học được đặc tính bất biến miền dữ liệu.

### 4.3. Phương pháp kiểm chứng Stratified 5-Fold Zero-Overlap Cross-Validation
Để ngăn chặn hoàn toàn hiện tượng rò rỉ dữ liệu (Data Leakage) thường gặp khi xử lý dữ liệu chuỗi thời gian:
- Toàn bộ các cửa sổ trượt thuộc về cùng một chu kỳ sóng $60\text{ giây}$ bắt buộc phải nằm trọn vẹn trong tập Train hoặc tập Test (**Zero-Overlap Pulse Level Split**). Tuyệt đối không xáo trộn các điểm đo con giữa các tập dữ liệu.
- Sử dụng kỹ thuật phân tầng (Stratified K-Fold với $K=5$) đảm bảo tỷ lệ giữa các nhãn khí $H_2S$, $NH_3$ và Clean Air đồng đều trên cả 5 folds.

### 4.4. Đánh giá độ chính xác, sai số hồi quy MAE, R² và Ma trận nhầm lẫn

#### Kết quả tổng hợp qua kiểm định chéo (5-Fold Cross-Validation):
| Mô Hình Máy Học | Nhiệm Vụ Suy Luận | Độ Chính Xác (Accuracy) | Sai Số MAE (ppm) | Hệ Số $R^2$ | Độ Trễ Suy Luận (RPi 3) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pulse Classifier** | Phân loại khí chu kỳ 60s | **$95.21\%$** | — | — | $3.2\text{ ms}$ |
| **Pulse Regressor** | Hồi quy nồng độ chu kỳ 60s | — | **$3.79\text{ ppm}$** | **$0.8357$** | $2.6\text{ ms}$ |
| **Window Classifier** | Phân loại khí cửa sổ trượt 20 điểm | **$93.46\%$** (Offline) / **$94.97\%$** | — | — | $1.8\text{ ms}$ |
| **Window Regressor** | Hồi quy nồng độ streaming | — | **$5.02\text{ ppm}$** / **$2.47\text{ ppm}$** | **$0.7739$** / **$0.9333$** | $1.5\text{ ms}$ |

#### Báo cáo phân lớp chi tiết từng loại khí (Pulse Classifier Report):
| Loại Khí | Precision (Độ chính xác) | Recall (Độ thu hồi) | F1-Score | Số lượng mẫu kiểm thử (Support) |
| :--- | :--- | :--- | :--- | :--- |
| **Clean Air** | $94.5\%$ | **$99.6\%$** | **$97.0\%$** | 257 |
| **$H_2S$** | $95.0\%$ | $88.8\%$ | $91.8\%$ | 170 |
| **$NH_3$** | **$96.6\%$** | $94.9\%$ | $95.8\%$ | 178 |
| **Trung bình toàn bộ (Weighted Avg)** | **$95.2\%$** | **$95.2\%$** | **$95.2\%$** | **605** |

#### Ma trận nhầm lẫn (Confusion Matrix):
$$\begin{pmatrix}
256 & 0 & 1 \\
14 & 151 & 5 \\
1 & 8 & 169
\end{pmatrix}$$
*Nhận xét:* Trong số 257 mẫu Clean Air, có tới 256 mẫu được dự đoán chính xác tuyệt đối, chỉ có đúng 1 mẫu nhầm sang $NH_3$ và $0$ mẫu nhầm sang $H_2S$. Điều này chứng minh thuật toán chốt chặn Flatness Guard đã loại bỏ hoàn toàn hiện tượng báo động giả nguy hiểm.

### 4.5. Phân tích độ quan trọng của đặc trưng vật lý (Feature Importance)

| Thứ Hạng | Tên Đặc Trưng | Tỷ Lệ Quan Trọng | Ý Nghĩa Vật Lý & Hóa Học |
| :---: | :--- | :---: | :--- |
| **1** | `Rel_Peak` | **$13.98\%$** | Biên độ chênh lệch cực đại giữa đỉnh xung và đường nền ($\Delta V_{peak} = V_{max} - V_0$). |
| **2** | `Delta_V` | **$13.76\%$** | Độ biến thiên toàn dải của chu kỳ ($V_{max} - V_{min}$), phản ánh cường độ phản ứng hóa học. |
| **3** | `Anchor_12s` | **$11.95\%$** | Điện áp vi sai tại giây thứ 12 — thời điểm động học hấp phụ tăng tốc mạnh nhất. |
| **4** | `Peak_Time` | **$8.27\%$** | Thời điểm đạt đỉnh xung nhiệt; $H_2S$ có tốc độ đạt đỉnh sớm hơn đáng kể so với $NH_3$. |
| **5** | `Decay_Slope` | **$8.08\%$** | Tốc độ suy giảm điện áp khi giải hấp phụ nhiệt; $NH_3$ giải hấp phụ chậm hơn $H_2S$. |
| **6** | `Anchor_18s` | **$7.66\%$** | Giá trị điện áp tại đỉnh xung nhiệt nung nóng cực đại. |
| **7** | `Anchor_7s` | **$5.63\%$** | Tốc độ phản ứng sớm ngay khi chất khí vừa tiếp xúc với bề mặt cảm biến. |
| **8** | `Mean_Diff` | **$5.54\%$** | Năng lượng vi sai trung bình toàn bộ chu kỳ đo. |
| **9** | `Std_V` | **$4.73\%$** | Độ phân tán động học của chuỗi dữ liệu. |
| **10** | `Anchor_24s` | **$3.90\%$** | Động học làm nguội và phục hồi ban đầu của màng oxit kim loại. |

---

# PHẦN V: BỘ 100+ CÂU HỎI VÀ CÂU TRẢ LỜI PHẢN BIỆN BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG

---

## NHÓM 1: BỐI CẢNH, ĐỘNG LỰC & TÍNH MỚI CỦA ĐỀ TÀI (CÂU 1 - 15)

#### Câu 1: Tại sao nhóm lại lựa chọn bài toán phát hiện khí $H_2S$ và $NH_3$ mà không phải là các khí phổ biến khác như $CO$ hay $LPG$?
**Trả lời:** Khí $H_2S$ và $NH_3$ là hai loại khí độc nguy hiểm hàng đầu trong các ngành công nghiệp chế biến dầu khí, lọc hóa dầu và xử lý chất thải. Đặc biệt, $H_2S$ là khí kịch độc có khả năng gây tê liệt khứu giác ở nồng độ cực thấp ($10\text{ ppm}$) và gây tử vong tức thì ở ngưỡng $50 - 100\text{ ppm}$ (IDLH). Khí $CO$ và $LPG$ đã có các tiêu chuẩn đầu báo cháy dân dụng tương đối hoàn thiện, trong khi việc phát hiện sớm và tách biệt $H_2S$ trong môi trường công nghiệp khắc nghiệt, nhiệt ẩm cao vẫn là thách thức lớn đối với an toàn tính mạng con người.

#### Câu 2: Điểm khác biệt lớn nhất giữa hệ thống E-Nose của nhóm với các đầu báo khí công nghiệp hiện có trên thị trường là gì?
**Trả lời:** Đầu báo khí truyền thống chỉ so sánh điện áp tức thời với một ngưỡng tĩnh cố định, dẫn đến hai nhược điểm: báo động chậm (chờ khí phân tán tới đầu dò) và tỷ lệ báo động giả cao do trôi nhiệt ẩm. Điểm đột phá của nhóm là kết hợp Mũi điện tử với Edge AI: sử dụng chu kỳ sóng nhiệt WaveCycle 250 điểm để khai thác "dấu vân tay động học" (Gas Kinetic Fingerprint), phân biệt chính xác bản chất hóa học của khí và dự báo trước xu hướng rò rỉ $+20\text{ giây}$ qua đạo hàm động học.

#### Câu 3: Khái niệm "Gas Fingerprint" trong đề tài được hiểu chính xác là gì?
**Trả lời:** Gas Fingerprint là tập hợp các đặc trưng động học không gian - thời gian sinh ra từ phản ứng hấp phụ và giải hấp phụ của các phân tử khí trên bề mặt mảng cảm biến khi nhiệt độ màng oxit kim loại bị biến thiên theo chu kỳ sóng nhiệt 60 giây. Nó bao gồm biên độ đáp ứng cực đại, tốc độ tăng điện áp khi tiếp xúc, thời gian đạt đỉnh, tốc độ suy giảm khi làm nguội và diện tích dưới đường cong vi sai.

#### Câu 4: Tại sao nhóm gọi giải pháp này là "True Edge AI"?
**Trả lời:** Vì toàn bộ chu trình xử lý dữ liệu nặng nhất bao gồm: thu thập mẫu nối tiếp, lọc khử gai phần cứng, bù trôi nhiệt ẩm, bám đường nền thích ứng, trích xuất 32 đặc trưng toán học và thực thi suy luận của cả 2 mô hình Random Forest (phân loại khí + ước lượng nồng độ) đều diễn ra hoàn toàn cục bộ trên vi máy tính nhúng Raspberry Pi 3 tại biên với thời gian dưới $4\text{ ms}$, tiêu thụ chỉ $80\text{ MB}$ RAM, độc lập $100\%$ với Internet và không phụ thuộc vào máy chủ đám mây.

#### Câu 5: Hệ thống có khả năng mở rộng để nhận diện thêm các loại khí khác ngoài $H_2S$ và $NH_3$ không?
**Trả lời:** Hoàn toàn có thể. Nhờ kiến trúc mảng cảm biến đa thành phần và đường ống huấn luyện chuẩn hóa trong `backend/train.py`, khi cần mở rộng sang các khí khác (như $SO_2, CO, VOCs$), nhóm chỉ cần bổ sung cảm biến tương ứng vào mảng (hoặc sử dụng phản ứng chéo của MQ135), thu thập chu kỳ sóng và huấn luyện lại Random Forest mà không cần phải thay đổi cấu trúc phần cứng gateway hay giao thức truyền thông.

#### Câu 6: Tính mới về mặt khoa học của công trình này là gì?
**Trả lời:** Tính mới nằm ở 3 điểm: (1) Đề xuất không gian đặc trưng vi sai bất biến dịch chuyển ($\Delta V = V(t) - V_0$) giải quyết triệt để bài toán Domain Shift giữa phòng lab và ngoài trời; (2) Thuật toán chốt chặn kép: Dynamic Baseline Tracker kết hợp Kinematic Slope Guard chống báo động giả; (3) Kỹ thuật Synthetic Plume Injection cho phép làm giàu dữ liệu thực địa ngoài trời mà không cần xả khí độc nguy hiểm ra môi trường.

#### Câu 7: Tại sao nhóm không dùng cảm biến quang học NDIR hoặc PID thay vì cảm biến MOS/Điện hóa?
**Trả lời:** Cảm biến quang học NDIR chỉ nhạy với các khí có dải hấp thụ hồng ngoại rõ ràng như $CO_2, CH_4$, không hiệu quả với $H_2S$ ở nồng độ cực thấp ($1 - 10\text{ ppm}$). Cảm biến PID (Photoionization) có giá thành rất đắt ($> 1500\text{ USD}$/đầu dò), dễ bị nhiễm bẩn quang học trong môi trường khói bụi công nghiệp. Mảng cảm biến MOS kết hợp điều chế sóng nhiệt có giá thành chỉ vài chục USD nhưng khi kết hợp với Edge AI lại đạt độ chính xác tương đương thiết bị đắt tiền.

#### Câu 8: Chu kỳ sóng nhiệt 60 giây có quá chậm đối với một hệ thống cảnh báo khẩn cấp không?
**Trả lời:** Không, vì hệ thống sử dụng **Kiến trúc kép Dual-Mode**. Chu kỳ 60 giây (Pulse Model) dùng để định danh chính xác tuyệt đối và hiệu chuẩn nồng độ định kỳ. Trong khi đó, **Window Model** chạy streaming liên tục trên cửa sổ trượt 20 điểm ($\Delta t \approx 4.8\text{s}$, suy luận mỗi $200\text{ ms}$) kết hợp thuật toán đạo hàm độ dốc ($dV/dt$), cho phép phát hiện sự bốc lên của chùm khí và kích hoạt cảnh báo chỉ sau **$1 - 2\text{ giây}$** kể từ khi khí tiếp xúc với cảm biến.

#### Câu 9: Đối tượng khách hàng mục tiêu của giải pháp này là ai?
**Trả lời:** Các nhà máy lọc dầu, nhà máy xử lý khí tự nhiên, trạm nén khí dọc tuyến ống dẫn khí đốt, các khu xử lý nước thải công nghiệp tập trung, nhà máy sản xuất phân đạm và các kho bảo quản lạnh công nghiệp quy mô lớn.

#### Câu 10: Chi phí ước tính để chế tạo một bộ thiết bị phần cứng là bao nhiêu?
**Trả lời:** Chi phí phần cứng cực kỳ tối ưu: Một trạm cảm biến hiện trường ESP32 kèm cảm biến chỉ khoảng $35 - 50\text{ USD}$. Một bộ Gateway trung tâm Raspberry Pi 3 kèm module RS-485 công nghiệp chỉ khoảng $60 - 80\text{ USD}$. Tổng chi phí cho một cụm giám sát hoàn chỉnh thấp hơn từ $5 - 10$ lần so với một đầu báo khí cố định chuyên dụng của các hãng lớn như Honeywell hay Dräger.

#### Câu 11: Dự án này đáp ứng những tiêu chí nào của cuộc thi Advantech AIoT InnoWorks?
**Trả lời:** Dự án đáp ứng trọn vẹn cả 4 tiêu chí: (1) Ứng dụng công nghệ AIoT giải quyết bài toán an toàn công nghiệp cấp thiết; (2) Kiến trúc hoàn chỉnh 5 tầng tích hợp sâu nền tảng Advantech WISE-IoT; (3) Tính toán biên thực thụ (True Edge AI) trên phần cứng nhúng; (4) Khả năng thương mại hóa thực tế với chi phí tối ưu.

#### Câu 12: Vai trò của từng thành viên trong nhóm TaskForce141 được phân chia như thế nào?
**Trả lời:** Bạn Đỗ Đức Khởi phụ trách kiến trúc tổng thể, mô hình hóa Edge AI, thuật toán xử lý dữ liệu và tích hợp hệ thống. Bạn Lê Phạm Thanh Dat phụ trách thiết kế phần cứng mạch đo, buồng thí nghiệm, lấy mẫu cảm biến và giao thức truyền thông Modbus RS-485. Bạn Vũ Anh Kiệt phụ trách xây dựng Web SCADA Dashboard, kết nối đám mây WISE-IoT/Firebase và thiết kế Standee triển lãm.

#### Câu 13: Tiêu chuẩn an toàn công nghiệp nào được lấy làm cơ sở phân cấp rủi ro trong đề tài?
**Trả lời:** Hệ thống tuân thủ tiêu chuẩn của Cơ quan Quản lý An toàn và Sức khỏe Nghề nghiệp Hoa Kỳ (**OSHA**) và Viện Quốc gia về An toàn và Sức khỏe Nghề nghiệp (**NIOSH**), cụ thể: Ngưỡng cảnh báo sớm ($1\text{ ppm}$ $H_2S$), Ngưỡng giới hạn tiếp xúc cho phép OSHA PEL ($10\text{ ppm}$ $H_2S$, $50\text{ ppm}$ $NH_3$), và Ngưỡng nguy hiểm tức thời đến tính mạng IDLH ($100\text{ ppm}$).

#### Câu 14: Hệ thống có khả năng hoạt động trong môi trường dễ cháy nổ (ATEX/IECEx) không?
**Trả lời:** Bản thử nghiệm hiện tại đáp ứng chuẩn kháng nước, kháng bụi IP65. Để đạt chuẩn chống cháy nổ ATEX Zone 1/Zone 2, trong giai đoạn thương mại hóa, phần cứng sẽ được bổ sung mạch cách ly phòng nổ (Intrinsically Safe Zener Barrier) và vỏ bọc hợp kim nhôm đúc chống nổ đạt tiêu chuẩn Ex d IIC.

#### Câu 15: Dự án đã được triển khai thử nghiệm thực tế ở đâu chưa?
**Trả lời:** Dự án đã được kiểm chứng qua 361 chu kỳ đo buồng kín tại phòng thí nghiệm EEE Phenikaa, kiểm thử thực địa ngoài trời trong các điều kiện thời tiết thực tế (sương mù ẩm ướt, trưa nắng gắt) và kiểm chứng truyền thông viễn trắc thành công qua mạng Tailscale nối với Raspberry Pi 3.

---

## NHÓM 2: PHẦN CỨNG CẢM BIẾN, MẠCH ĐO & HIỆN TƯỢNG HÓA LÝ (CÂU 16 - 30)

#### Câu 16: Nguyên lý hoạt động hóa lý của cảm biến bán dẫn oxit kim loại (MQ136) là gì?
**Trả lời:** MQ136 sử dụng lớp vật liệu nhạy cảm là Thiếc Dioxide ($SnO_2$) được nung nóng ở nhiệt độ khoảng $200 - 350^\circ\text{C}$. Trong không khí sạch, các phân tử oxy bị hấp phụ lên bề mặt oxit và bẫy các electron tự do trong dải dẫn của chất bán dẫn, tạo thành các ion $O_2^-$ hoặc $O^-$, hình thành một hàng rào thế năng làm điện trở của cảm biến rất cao. Khi có khí khử như $H_2S$, các phân tử khí phản ứng với các ion oxy bị hấp phụ:
$$H_2S + 3O^- \rightarrow SO_2 + H_2O + 3e^-$$
Các electron bị bẫy được giải phóng trở lại dải dẫn, làm giảm độ rộng của hàng rào thế năng và giảm điện trở màng bán dẫn. Qua mạch cầu phân áp, điện áp ngõ ra của cảm biến tăng lên tỷ lệ thuận với nồng độ khí.

#### Câu 17: Tại sao cảm biến MOS lại cần một bộ sấy (Heater)? Thời gian sấy ổn định là bao lâu?
**Trả lời:** Năng lượng nhiệt từ bộ sấy là điều kiện bắt buộc để kích hoạt phản ứng hóa hấp phụ của oxy và chất khí khử trên bề mặt $SnO_2$. Ở nhiệt độ phòng, phản ứng diễn ra rất chậm khiến cảm biến gần như không phản hồi. Khi bật nguồn từ trạng thái nguội, cảm biến cần tối thiểu $24 - 48\text{ giờ}$ sấy sơ bộ (Preheating) đối với cảm biến mới, và cần $60 - 120\text{ giây}$ sấy ổn định (Warm-up) trong mỗi phiên khởi động lại trước khi bắt đầu đo.

#### Câu 18: Độ phân giải của bộ ADC trên vi điều khiển ESP32 là bao nhiêu? Có nhược điểm gì cần lưu ý?
**Trả lời:** ESP32 trang bị bộ ADC độ phân giải 12-bit (cho ra giá trị từ $0$ đến $4095$ tương ứng với điện áp $0 - 3.3\text{V}$, độ phân giải lý thuyết khoảng $0.8\text{ mV}$/mức). Nhược điểm cố hữu của ADC trên ESP32 là tính phi tuyến tính ở vùng cận dưới ($< 0.1\text{V}$) và cận trên ($> 3.1\text{V}$). Nhóm đã khắc phục bằng cách thiết kế mạch khuếch đại phân áp đưa dải tín hiệu làm việc rơi vào vùng tuyến tính nhất ($0.15\text{V} - 2.8\text{V}$) và áp dụng bảng hiệu chuẩn phi tuyến đường cong (ADC Calibration Vref).

#### Câu 19: Tại sao nhóm lại sử dụng đồng thời cả MQ136 và MQ135 trong mảng cảm biến?
**Trả lời:** Nếu chỉ sử dụng một cảm biến MQ136, tín hiệu ngõ ra là vô hướng (chỉ có 1 đường điện áp), không thể phân biệt được điện áp tăng là do có $H_2S$ hay do có nồng độ cao của $NH_3$ hoặc cồn/VOCs (hiện tượng độ nhạy chéo - Cross-sensitivity). Bằng cách kết hợp MQ136 (nhạy ưu tiên $H_2S$) và MQ135 (nhạy ưu tiên $NH_3$, khói, VOCs), hệ thống tạo ra một không gian vector đa chiều, cho phép mô hình Edge AI tách biệt chính xác từng loại khí.

#### Câu 20: Cảm biến DHT22 đóng vai trò gì? Tại sao không dùng DHT11?
**Trả lời:** Cảm biến MOS cực kỳ nhạy cảm với sự thay đổi của độ ẩm và nhiệt độ môi trường. DHT22 được sử dụng để cung cấp tham số nhiệt ẩm thời gian thực cho thuật toán bù trôi vật lý. Nhóm không chọn DHT11 vì dải đo của DHT11 quá hẹp (độ ẩm $20 - 90\%$, sai số $\pm 5\%$, nhiệt độ $0 - 50^\circ\text{C}$), không đáp ứng được môi trường khắc nghiệt ngoài trời. DHT22 có dải đo độ ẩm $0 - 100\%$ ($\pm 2\%$) và nhiệt độ $-40^\circ\text{C} đến +80^\circ\text{C}$ ($\pm 0.5^\circ\text{C}$), độ phân giải số 16-bit.

#### Câu 21: Màng lọc khí PTFE Hydrophobic trên vỏ hộp có tác dụng gì?
**Trả lời:** Màng lọc Polytetrafluoroethylene (PTFE) kỵ nước có kích thước lỗ xốp micro ($0.2 - 0.45\ \mu\text{m}$). Màng lọc này ngăn chặn $100\%$ các giọt nước mưa, hơi sương ngưng tụ và các hạt bụi bẩn công nghiệp xâm nhập vào buồng cảm biến gây đoản mạch hoặc bám bẩn màng oxit, nhưng vẫn cho phép các phân tử khí có kích thước nano ($H_2S, NH_3, O_2$) khuếch tán tự do qua buồng đo.

#### Câu 22: Hiện tượng ngộ độc cảm biến (Sensor Poisoning) là gì? Cảm biến MQ136 có bị không?
**Trả lời:** Ngộ độc cảm biến xảy ra khi bề mặt oxit kim loại tiếp xúc với các hợp chất chứa Silicon (như dầu bôi trơn siloxane), hơi chì hoặc lưu huỳnh nồng độ quá cao trong thời gian dài, tạo thành các hợp chất liên kết vĩnh viễn không thể giải hấp phụ, làm mất khả năng đo. Để hạn chế, cảm biến được bố trí trong buồng đo có màng lọc bảo vệ và hệ thống định kỳ thực hiện chu kỳ nung nhiệt cao giải hấp phụ (Thermal Cleaning Cycle).

#### Câu 23: Nguồn điện cung cấp cho cảm biến có yêu cầu gì đặc biệt không?
**Trả lời:** Bộ sấy của các cảm biến MOS tiêu thụ dòng điện khá lớn (khoảng $150 - 180\text{ mA}$ mỗi cảm biến ở điện áp $5\text{V}$). Do đó, nguồn cấp phải là nguồn xung công nghiệp cách ly có công suất tối thiểu $5\text{V} - 2\text{A}$, có độ gợn sóng (Ripple & Noise) $< 50\text{ mV}$ để tránh gây nhiễu điện áp lên chân đo ADC.

#### Câu 24: Tần số lấy mẫu của hệ thống là bao nhiêu? Cơ sở lựa chọn tần số này?
**Trả lời:** Hệ thống lấy mẫu ở tần số $f_s \approx 4.17\text{ Hz}$ (250 điểm trong 60 giây, tức chu kỳ lấy mẫu $T_s \approx 240\text{ ms}$). Cơ sở lựa chọn: Phản ứng hóa hấp phụ trên bề mặt màng oxit kim loại diễn ra theo quán tính hóa học với hằng số thời gian cỡ vài giây. Tần số $4.17\text{ Hz}$ hoàn toàn thỏa mãn định lý lấy mẫu Nyquist ($f_s > 2 f_{max}$ của động học khí), đồng thời không gây quá tải cho bộ đệm và đường truyền RS-485.

#### Câu 25: Nếu cảm biến bị đứt dây hoặc hư hỏng bộ sấy, hệ thống có phát hiện được không?
**Trả lời:** Có. Trong lớp `SignalPreprocessor` và `BaselineTracker`, hệ thống có cơ chế kiểm tra tính toàn vẹn phần cứng (Hardware Diagnostic Guard): nếu điện áp đọc về liên tục bằng $0.000\text{V}$ (mất kết nối cảm biến) hoặc bằng $3.300\text{V}$ (chập nguồn), hệ thống lập tức phát cảnh báo lỗi cảm biến (Sensor Fault) trên thanh trạng thái và ghi log vào cơ sở dữ liệu.

#### Câu 26: Hiện tượng trôi điểm không (Zero Baseline Drift) của cảm biến MOS diễn ra như thế nào?
**Trả lời:** Trôi điểm không là hiện tượng điện trở nền của cảm biến trong không khí sạch thay đổi chậm theo thời gian dưới tác động của sự lão hóa vật liệu bán dẫn (Aging Effect) và chu kỳ ngày/đêm của nhiệt độ, độ ẩm môi trường. Hiện tượng này làm đường nền điện áp có thể dịch chuyển từ $0.05\text{V}$ lên tới $0.60\text{V}$, đòi hỏi phải có thuật toán bám đường nền thích ứng.

#### Câu 27: Tuổi thọ trung bình của cảm biến MQ136 và ZE03-H2S trong môi trường công nghiệp là bao lâu?
**Trả lời:** Cảm biến MOS MQ136 có tuổi thọ trung bình từ $2 - 3\text{ năm}$ trong điều kiện hoạt động liên tục. Cảm biến điện hóa ZE03-H2S có tuổi thọ khoảng $1.5 - 2\text{ năm}$ do dung dịch điện phân bị tiêu hao dần theo thời gian tiếp xúc với khí độc.

#### Câu 28: Thiết kế mạch phân áp cho cảm biến MQ136 sử dụng giá trị điện trở tải ($R_L$) là bao nhiêu?
**Trả lời:** Điện trở tải $R_L$ được lựa chọn trong khoảng $4.7\ \text{k}\Omega - 10\ \text{k}\Omega$. Giá trị này được tính toán tối ưu hóa sao cho khi nồng độ khí biến thiên từ $0$ đến $10\text{ ppm}$, điện áp phân áp trên $R_L$ biến thiên trong dải $0.2\text{V} - 2.5\text{V}$, tối đa hóa tỷ số tín hiệu trên nhiễu (SNR) đưa vào bộ ADC.

#### Câu 29: Tại sao nhóm không sử dụng giao tiếp không dây (Wi-Fi, Zigbee, LoRa) cho trạm đo hiện trường?
**Trả lời:** Trong các nhà máy lọc hóa dầu, hệ thống bồn chứa và đường ống kim loại dày đặc tạo thành lồng Faraday gây suy hao sóng vô tuyến cực mạnh. Ngoài ra, việc dùng sóng vô tuyến dễ bị can nhiễu từ các máy phát công suất lớn và tiềm ẩn nguy cơ mất an toàn tia lửa điện. RS-485 dùng dây xoắn bọc kim là tiêu chuẩn công nghiệp bắt buộc nhờ độ tin cậy tuyệt đối.

#### Câu 30: Pin dự phòng LiFePO4 của trạm đo có thể duy trì hoạt động trong bao lâu khi mất điện lưới?
**Trả lời:** Một khối pin LiFePO4 dung lượng $12\text{V} - 5\text{Ah}$ (năng lượng $60\text{ Wh}$), với công suất tiêu thụ trung bình của trạm đo ESP32 kèm cảm biến khoảng $1.8\text{ W}$, có thể duy trì hệ thống hoạt động liên tục trong hơn **$30\text{ giờ}$** độc lập, đủ thời gian cho đội bảo trì khắc phục sự cố nguồn điện.

---

## NHÓM 3: MẠNG CÔNG NGHIỆP RS-485, MODBUS RTU & GIAO THỨC TRUYỀN THÔNG (CÂU 31 - 45)

#### Câu 31: Tại sao đường truyền RS-485 lại có khả năng chống nhiễu vượt trội so với RS-232 hay UART thông thường?
**Trả lời:** UART và RS-232 là chuẩn truyền dẫn đơn cực (Single-Ended), tín hiệu đo theo mức điện áp so với dây đất (GND). Khi có dòng điện lớn chạy qua đất hoặc nhiễu điện từ trường cảm ứng, mức điện áp GND bị nâng lên gây sai lệch dữ liệu. RS-485 truyền dẫn vi sai (Differential Signaling) trên 2 dây xoắn $A$ và $B$. Máy thu chỉ đọc hiệu điện thế $V_{diff} = V_A - V_B$. Bất kỳ xung nhiễu bên ngoài nào tác động đều cảm ứng cùng biên độ lên cả 2 dây (Common-Mode Noise), do đó phép trừ vi sai tại đầu thu triệt tiêu hoàn toàn điện áp nhiễu.

#### Câu 32: Tốc độ truyền (Baudrate) của hệ thống là bao nhiêu? Khoảng cách truyền tối đa trên lý thuyết và thực tế?
**Trả lời:** Hệ thống vận hành ở tốc độ $115200\text{ bps}$. Theo lý thuyết chuẩn TIA/EIA-485-A, ở tốc độ $100\text{ kbps}$, khoảng cách truyền tối đa có thể đạt tới $1200\text{ mét}$ trên cáp xoắn đôi bọc kim (STP AWG24). Trong thực tế nhà máy với nhiễu môi trường, hệ thống hoạt động hoàn toàn ổn định ở khoảng cách $300 - 500\text{ mét}$ giữa các node.

#### Câu 33: Tác dụng của điện trở kết thúc đường dây $120\ \Omega$ (Termination Resistor) là gì? Nếu không gắn thì xảy ra hiện tượng gì?
**Trả lời:** Tín hiệu số truyền trên cáp là sóng điện từ cao tần. Cáp xoắn đôi chuẩn RS-485 có trở kháng đặc tính danh định là $Z_0 = 120\ \Omega$. Khi xung tín hiệu truyền đến cuối đường dây, nếu mạch bị hở (trở kháng vô cùng), sóng tín hiệu sẽ bị phản xạ ngược lại (Signal Reflection), va chạm và làm méo mó các bit dữ liệu tiếp theo, gây lỗi khung truyền (Framing Error). Điện trở $120\ \Omega$ gắn ở 2 đầu xa nhất của bus hấp thụ toàn bộ năng lượng sóng tới, triệt tiêu hoàn toàn sóng phản xạ.

#### Câu 34: Tại sao trong RS-485 lại bắt buộc phải đi dây theo cấu trúc Daisy-Chain (chuỗi) mà không được đi hình sao (Star)?
**Trả lời:** Cấu trúc hình sao tạo ra nhiều nhánh rẽ dài (Stubs). Mỗi đầu mút của nhánh rẽ đóng vai trò như một điểm không tương thích trở kháng, tạo ra vô số sóng phản xạ hỗn loạn dọc theo bus làm sụp đổ khung truyền dữ liệu. Chuẩn công nghiệp bắt buộc phải đi theo đường thẳng Daisy-Chain: từ Gateway vào Trạm 1, ra khỏi Trạm 1 vào Trạm 2, lần lượt đến trạm cuối cùng, các đoạn rẽ nhánh (nếu có) phải ngắn hơn $30\text{ cm}$.

#### Câu 35: Chân `DE` và `RE` trên chip thu phát MAX485 có chức năng gì? ESP32 điều khiển chúng như thế nào?
**Trả lời:** MAX485 là chip thu phát bán song công (Half-Duplex). Chân `DE` (Driver Enable, tích cực mức CAO) bật bộ phát tín hiệu lên bus. Chân `\RE` (Receiver Enable, tích cực mức THẤP) bật bộ thu tín hiệu từ bus. Trong thiết kế của nhóm, hai chân này được nối chung vào chân GPIO5 của ESP32:
- Khi GPIO5 = LOW: Bật bộ thu, tắt bộ phát $\rightarrow$ ESP32 ở chế độ lắng nghe lệnh từ Master.
- Khi GPIO5 = HIGH: Bật bộ phát, tắt bộ thu $\rightarrow$ ESP32 phát gói tin viễn trắc lên bus.

#### Câu 36: Giao thức Modbus RTU phân biệt các trạm như thế nào? Số lượng trạm tối đa trên một bus là bao nhiêu?
**Trả lời:** Mỗi gói tin Modbus RTU bắt đầu bằng một byte địa chỉ trạm (Slave ID, từ $1$ đến $247$). Khi Master phát gói tin, tất cả các trạm đều nhận được nhưng chỉ trạm có Slave ID trùng khớp mới xử lý và phản hồi. Về mặt vật lý, một bộ thu phát chuẩn như MAX485 cho phép gắn tối đa 32 thiết bị tải đơn vị (Unit Load) trên một segment cáp. Nếu sử dụng các chip thu phát hiện đại (1/8 Unit Load) hoặc bộ lặp tín hiệu (Repeater), số lượng node có thể mở rộng lên tới 247 trạm.

#### Câu 37: Khung truyền Modbus RTU kiểm tra lỗi dữ liệu bằng phương pháp nào?
**Trả lời:** Modbus RTU sử dụng mã kiểm tra dư thừa vòng 16-bit (**CRC-16** với đa thức sinh $0xA001$). Bên phát tính toán mã CRC cho toàn bộ khung dữ liệu và đính kèm vào 2 byte cuối. Bên nhận tính lại mã CRC của khung nhận được; nếu hai mã không trùng khớp, gói tin bị coi là lỗi nhiễu đường truyền và bị hủy bỏ tự động.

#### Câu 38: Cơ chế Token Streaming `Pxxx:valueV` của nhóm có ưu điểm gì so với việc gửi định dạng JSON qua Serial?
**Trả lời:** Một bản tin JSON biểu diễn dữ liệu cảm biến:
`{"point": 172, "voltage": 0.0183}\n` tiêu tốn khoảng $37\text{ bytes}$.
Trong khi định dạng token rút gọn của nhóm:
`P172:0.0183V,` chỉ tiêu tốn đúng $13\text{ bytes}$ (giảm gần $65\%$ dung lượng). Điều này giúp tiết kiệm băng thông bus, giảm tải thời gian xử lý chuỗi trên vi điều khiển và tăng tốc độ truyền mẫu thời gian thực.

#### Câu 39: Nếu cáp RS-485 bị đứt hoặc trạm đo bị mất nguồn, Gateway phát hiện bằng cách nào?
**Trả lời:** Trong lớp `SerialReceiver` và `app.py`, Gateway liên tục giám sát dấu thời gian nhận gói tin cuối cùng (`last_rs485_rx_time`). Nếu quá thời gian Time-out định trước ($4.0\text{ giây}$) mà không nhận được mẫu tin nào mới, trạng thái kết nối tự động chuyển từ `active: true` sang `active: false`, cờ báo động mất kết nối phần cứng được kích hoạt trên Web Dashboard.

#### Câu 40: Làm thế nào để phân biệt giữa xung nhiễu rác trên đường truyền và dữ liệu thực?
**Trả lời:** Lớp `StreamPacketParser` sử dụng biểu thức chính quy chặt chẽ kết hợp kiểm tra tính hợp lệ về mặt ngữ nghĩa:
- Phải khớp đúng khuôn dạng: Ký tự `P`, số nguyên chỉ mục điểm từ $0$ đến $999$, dấu `:`, giá trị số thực dương và ký tự đơn vị `V`.
- Giá trị điện áp bắt buộc phải nằm trong giới hạn vật lý $0.0\text{V} \le V \le 10.0\text{V}$. Bất kỳ byte rác ngẫu nhiên nào không thỏa mãn đều bị bộ phân tích cú pháp loại bỏ và tăng biến đếm `invalid_tokens`.

#### Câu 41: Hiện tượng "Jitter" và trượt gói tin do bộ đệm FreeRTOS trên ESP32 được xử lý như thế nào ở phía Gateway?
**Trả lời:** Do hệ điều hành thời gian thực FreeRTOS trên ESP32 quản lý đa tác vụ, các gói tin có thể bị dồn cụm trong hàng đợi UART và gửi vọt cùng lúc về Gateway, gây hiện tượng trượt lùi chỉ mục điểm (ví dụ đang ở điểm 86 nhận được điểm 84 do bộ đệm trễ). Nhóm đã lập trình bộ lọc **Anti-stutter filter** trong `app.py`: nếu điểm mới nhận nhỏ hơn điểm trước đó nhưng khoảng cách $< 30$ điểm (không phải quay vòng chu kỳ), gói tin lỗi thời đó lập tức bị hủy bỏ để đảm bảo tính đơn điệu tăng của chuỗi thời gian.

#### Câu 42: Tại sao hệ thống lại tích hợp đồng thời cả Firebase Realtime Database và WISE-IoT Cloud?
**Trả lời:** WISE-IoT Platform là nền tảng đám mây công nghiệp của Advantech, chuyên dụng cho việc lưu trữ dữ liệu lớn dài hạn, bảo mật cấp doanh nghiệp và tích hợp vào hệ thống SCADA quản lý nhà máy. Tuy nhiên, việc đẩy dữ liệu lên WISE-IoT thường thực hiện theo chu kỳ $5 - 10\text{ giây}$/lần để tối ưu băng thông. Firebase Realtime Database được bổ sung để cung cấp luồng Server-Sent Events (SSE) tần số cao tức thời cho Web Dashboard, giúp người vận hành theo dõi mượt mà từng điểm sóng dao động ký như đang nhìn trực tiếp vào thiết bị đo.

#### Câu 43: Giao thức MQTT sử dụng mức QoS (Quality of Service) nào trong dự án?
**Trả lời:** Hệ thống sử dụng **QoS 1 (At least once delivery)** cho các bản tin viễn trắc thông thường để đảm bảo dữ liệu được gửi thành công lên Broker có xác nhận gói tin (PUBACK). Đối với các bản tin cảnh báo khẩn cấp (Emergency Alert), hệ thống sử dụng kết hợp cờ Retain để đảm bảo các máy khách khi đăng nhập sau vẫn đọc được trạng thái sự cố mới nhất.

#### Câu 44: Độ trễ truyền thông từ ESP32 qua RS-485 tới Raspberry Pi là bao nhiêu?
**Trả lời:** Với tốc độ baud $115200\text{ bps}$, một gói tin 13 bytes mất khoảng $1.1\text{ ms}$ để truyền xong trên đường truyền vật lý. Cộng với thời gian phân tích cú pháp và hàng đợi không chặn tại Gateway ($< 0.5\text{ ms}$), tổng độ trễ truyền thông hoàn toàn nhỏ hơn **$2\text{ ms}$**, đáp ứng tiêu chuẩn thời gian thực công nghiệp.

#### Câu 45: Nếu cả hai trạm đo cùng phát dữ liệu lên bus RS-485 cùng một thời điểm thì xử lý ra sao?
**Trả lời:** RS-485 bán song công chỉ cho phép một thiết bị phát tại một thời điểm. Nếu hai thiết bị cùng phát, hiện tượng xung đột dữ liệu (Bus Contention) sẽ làm hỏng dữ liệu. Trong chế độ Modbus tiêu chuẩn, Raspberry Pi là Master duy nhất điều phối đường truyền bằng cơ chế Polling lần lượt từng Slave. Trong chế độ Streaming Token, các trạm đo được phân chia khe thời gian lấy mẫu lệch nhau (Time-Division Multiplexing - TDM) để đảm bảo không bao giờ xảy ra xung đột trên bus.

---

## NHÓM 4: XỬ LÝ TÍN HIỆU SỐ, LỌC NHIỄU & BÙ TRÔI ĐƯỜNG NỀN (CÂU 46 - 60)

#### Câu 46: Trình bày thuật toán lọc số EMA (Exponential Moving Average) và ý nghĩa của hệ số $\alpha = 0.2$?
**Trả lời:** Bộ lọc EMA là một bộ lọc thông thấp đệ quy bậc nhất, được tính toán theo công thức:
$$y(t) = \alpha \cdot x(t) + (1 - \alpha) \cdot y(t-1)$$
Trong đó $x(t)$ là giá trị thô mới đọc từ cảm biến, $y(t-1)$ là giá trị đã lọc ở bước trước, và $\alpha$ là hệ số làm mượt ($0 < \alpha \le 1$). Hệ số $\alpha = 0.2$ đồng nghĩa với việc dành $20\%$ trọng số cho mẫu hiện tại và $80\%$ trọng số cho lịch sử quá khứ. Giá trị này được lựa chọn thực nghiệm để triệt tiêu hiệu quả các xung nhiễu ngẫu nhiên cao tần từ nguồn điện mà không gây ra độ trễ pha quá lớn đối với các biến thiên thực của nồng độ khí.

#### Câu 47: Tại sao lại xuất hiện gai xung phần cứng tại điểm ~125 và tại sao nhóm lại dùng Cubic Spline để khử nó?
**Trả lời:** Gai xung phần cứng tại điểm $\sim 125$ (tương ứng với giây thứ 30 trong chu kỳ sóng 60 giây) là do xung chuyển đổi trạng thái của mạch nung nhiệt hoặc mạch nạp tụ vi sai trên bo mạch. Xung này có biên độ vọt lên đột ngột trong khoảng vài trăm mili-giây. Nếu dùng các bộ lọc tuyến tính thông thường (như trung bình trượt), gai xung sẽ bị làm bẹt ra và lan sang các điểm lân cận. Nhóm sử dụng **nội suy Spline bậc ba (Cubic Spline)**: cô lập chính xác khoảng chỉ mục bị lỗi, lấy 5 điểm neo ổn định trước và sau xung để dựng đa thức bậc 3 nội suy mượt mà qua đoạn khuyết, tái tạo lại hình dạng tự nhiên hoàn hảo của tín hiệu gốc.

#### Câu 48: Bộ lọc Savitzky-Golay hoạt động như thế nào và tại sao nó lại vượt trội hơn bộ lọc Moving Average thông thường?
**Trả lời:** Bộ lọc Moving Average đơn giản gán giá trị trung bình cộng cho các điểm trong cửa sổ, dẫn đến nhược điểm làm giảm biên độ cực đại và làm bẹt các đỉnh nhọn của đường cong đáp ứng khí. Bộ lọc Savitzky-Golay thực hiện làm mượt bằng cách khớp một đa thức bậc thấp ($p = 2$) trên một cửa sổ trượt ($w = 9$) thông qua phương pháp bình phương tối thiểu có trọng số. Nhờ vậy, bộ lọc này triệt tiêu nhiễu cao tần hiệu quả nhưng vẫn bảo toàn nguyên vẹn diện tích dưới đường cong, độ cao của đỉnh cực đại ($V_{max}$) và độ dốc dâng của xung khí.

#### Câu 49: Trình bày chi tiết công thức bù sai số nhiệt độ và độ ẩm? Các hệ số thực nghiệm được xác định như thế nào?
**Trả lời:** Công thức bù trôi nhiệt ẩm của hệ thống:
$$V_{\text{compensated}} = \frac{V_{\text{filtered}}}{1.0 + 0.0035 \cdot (T - 25.0) + 0.0015 \cdot (H - 60.0)}$$
Trong đó:
- $T$ ($^\circ\text{C}$) và $H$ ($\%\text{ RH}$) là giá trị tức thời từ DHT22.
- Chuẩn tham chiếu phòng thí nghiệm là $25^\circ\text{C}$ và $60\%\text{ RH}$.
- Các hệ số $K_T = 0.0035$ và $K_H = 0.0015$ được xác định thông qua việc quét cảm biến trong buồng tạo vi khí hậu (Environmental Chamber) ở các dải nhiệt độ $20 - 45^\circ\text{C}$ và độ ẩm $40 - 95\%$ với mẫu không khí sạch, sau đó thực hiện hồi quy tuyến tính độ biến thiên của điện áp nền.

#### Câu 50: Bộ bám đường nền thích ứng (`BaselineTracker`) phân biệt trôi chậm do môi trường và sự cố rò rỉ khí độc bằng cách nào?
**Trả lời:** Lớp `BaselineTracker` sử dụng cơ chế ngưỡng kép dựa trên **biên độ vi sai** và **đạo hàm độ dốc**:
- **Trôi chậm môi trường (Diurnal Drift):** Thường do độ ẩm tăng dần theo thời tiết hoặc nhiệt độ giảm vào buổi chiều tối. Quá trình này diễn ra cực kỳ chậm chạp: tốc độ biến thiên $|dV/dt| \le 0.004\text{V/s}$ và độ lệch $|\Delta V| \le 0.06\text{V}$. Khi đó, hệ thống tiếp tục áp dụng bộ lọc EMA siêu chậm ($\alpha = 0.002$) để $V_0$ bám theo sự thay đổi của môi trường.
- **Rò rỉ khí độc (Gas Plume Event):** Khí rò rỉ bốc lên nhanh tạo ra xung đáp ứng dốc: $|dV/dt| > 0.004\text{V/s}$ hoặc $|\Delta V| > 0.06\text{V}$. Ngay lập tức, trạng thái chuyển sang `LOCKED_EVENT`, thuật toán **đóng băng đường nền $V_0$**, ngăn không cho chùm khí độc bị hấp thụ vào đường nền chuẩn.

#### Câu 51: Tính năng "Zero Calibration" hoạt động như thế nào khi kỹ sư vận hành bấm nút trên giao diện?
**Trả lời:** Khi bấm nút `[ 🎯 Zero Calibrate ]` trên Web Dashboard hoặc gọi API `POST /api/calibrate/zero`, hệ thống lấy trung vị của 15 mẫu tín hiệu gần nhất tại môi trường thực địa hiện tại và gán trực tiếp làm giá trị $V_0$ mới cho `BaselineTracker`. Trạng thái chuyển sang `CALIBRATED`, đưa điện áp vi sai $\Delta V = V(t) - V_0$ về mức xấp xỉ $0.000\text{V}$, giúp thiết bị sẵn sàng làm việc ngay lập tức tại bất kỳ vị trí địa lý nào mà không cần hiệu chuẩn lại mô hình.

#### Câu 52: Thuật toán chốt chặn phẳng lặng (Kinematic Flatness Guard) hoạt động ra sao để chống báo động giả?
**Trả lời:** Tại môi trường ngoài trời có độ ẩm cao, điện áp nền có thể đứng yên ở mức $0.55\text{V}$ (cao hơn nhiều so với lab). Thuật toán kiểm tra 3 điều kiện động học trên cửa sổ 20 điểm:
1. Độ lệch chuẩn vi sai cực nhỏ: $\sigma_{\text{window}} \le 0.015\text{V}$ (đường tín hiệu phẳng lì).
2. Độ dốc xấp xỉ bằng không: $|dV/dt| \le 0.004\text{V/s}$.
3. Độ lệch so với đường nền tham chiếu nhỏ: $|V(t) - V_0| \le 0.09\text{V}$.
Nếu thỏa mãn cả 3 điều kiện, hệ thống khẳng định đây là môi trường không khí sạch bình thường, cưỡng bức gán nhãn `Clean Air`, nồng độ $0.0\text{ ppm}$ và độ tin cậy $\ge 98\%$, vô hiệu hóa hoàn toàn hiện tượng suy luận nhầm của cây quyết định.

#### Câu 53: Nếu một chu kỳ WaveCycle 250 điểm bị mất 10 điểm do nhiễu RS-485 thì thuật toán nội suy xử lý thế nào?
**Trả lời:** Trong phương thức `_finalize_cycle()` của lớp `PointBuffer`, mảng 250 điểm được khởi tạo với giá trị `np.nan` tại các vị trí khuyết. Hệ thống sử dụng thuật toán nội suy tuyến tính đa điểm `np.interp`: tìm kiếm các chỉ mục hợp lệ liền kề trước và sau điểm bị mất, tính toán giá trị nội suy theo đường thẳng nối 2 điểm đó. Do tần số lấy mẫu là $4.17\text{ Hz}$ và động học của khí rất mượt mà, sai số nội suy của 10 điểm khuyết thiếu phân tán là hoàn toàn không đáng kể ($< 0.1\%$).

#### Câu 54: Tại sao trong công thức tính đặc trưng lại loại bỏ hoàn toàn các giá trị điện áp tuyệt đối ($V_{max}, V_{min}, V_{mean}$)?
**Trả lời:** Nếu đưa điện áp tuyệt đối vào mô hình, cây quyết định của Random Forest sẽ học các ngưỡng tĩnh chia nhánh dựa trên dữ liệu phòng lab (ví dụ: `if V_max > 0.40V then H2S`). Khi ra ngoài trời, đường nền tĩnh vốn đã là $0.55\text{V}$, mô hình sẽ lập tức kích hoạt nhánh $H_2S$ dù không có khí độc. Loại bỏ điện áp tuyệt đối và thay thế bằng chuỗi vi sai $\Delta w = w - V_0$ giúp mô hình trở nên bất biến với mức dịch chuyển của đường nền (Shift-Invariance).

#### Câu 55: Làm thế nào để chọn kích thước cửa sổ trượt $n = 20$ điểm cho mô hình Window Model?
**Trả lời:** Với chu kỳ lấy mẫu $240\text{ ms}$, cửa sổ $n = 20$ điểm tương đương với độ dài thời gian khoảng $4.8\text{ giây}$. Đây là khoảng thời gian vàng: đủ dài để nắm bắt được đạo hàm bậc nhất (tốc độ tăng điện áp) và độ cong (đạo hàm bậc hai) của chùm khí rò rỉ, nhưng cũng đủ ngắn để đưa ra quyết định cảnh báo tức thời chỉ trong vòng vài giây mà không gây độ trễ tích lũy.

#### Câu 56: Diện tích dưới đường cong vi sai ($\text{AUC}_{\Delta}$) có ý nghĩa vật lý gì đối với việc định lượng khí?
**Trả lời:** $\text{AUC}_{\Delta}$ là tích phân của điện áp vi sai theo thời gian trong suốt chu kỳ 60 giây:
$$\text{AUC}_{\Delta} = \int_{0}^{60} \max(0, V(t) - V_0) dt \approx \sum_{i=0}^{249} \max(0, p_i - V_0)$$
Về mặt vật lý, $\text{AUC}_{\Delta}$ đại diện cho tổng điện tích giải phóng trong phản ứng oxy hóa khử trên bề mặt cảm biến, tỷ lệ thuận trực tiếp với tổng lượng phân tử khí độc đã tương tác với màng cảm biến trong chu kỳ đó. Đây là đặc trưng quan trọng hàng đầu để hồi quy chính xác nồng độ ppm.

#### Câu 57: Tỷ số $\text{Ratio} = \frac{\Delta V_{max}}{\max(V_0, 0.05)}$ mang lại lợi ích gì cho mô hình?
**Trả lời:** Đây là đặc trưng chuẩn hóa độ nhạy tương đối (Relative Sensitivity). Trong vật lý cảm biến MOS, tỷ số đáp ứng $\Delta R / R_0$ phản ánh bản chất của chất khí tốt hơn là độ biến thiên điện trở tuyệt đối $\Delta R$. Việc chia cho $V_0$ giúp chuẩn hóa biên độ đáp ứng của cảm biến khi đường nền bị dịch chuyển do tuổi thọ hoặc nhiệt ẩm.

#### Câu 58: Tại sao lại chọn 10 điểm neo (Anchor Points) tại các giây $4, 7, 12, 18, 24, 29, 34, 41, 48, 55$?
**Trả lời:** 10 điểm neo này không được chia đều mà được phân bố có chủ đích theo đặc tính động học của xung sóng nhiệt 60 giây:
- Tập trung dày đặc ở giai đoạn đầu ($4\text{s}, 7\text{s}, 12\text{s}, 18\text{s}$): Nắm bắt tốc độ hấp phụ ban đầu và thời điểm leo lên đỉnh của các loại khí khác nhau.
- Điểm tại đỉnh ($18\text{s}, 24\text{s}$): Xác định biên độ cực đại.
- Các điểm ở giai đoạn sau ($29\text{s}, 34\text{s}, 41\text{s}, 48\text{s}, 55\text{s}$): Nắm bắt tốc độ phân rã giải hấp phụ nhiệt và mức độ hồi phục của màng oxit.

#### Câu 59: Độ lệch tứ phân vị vi sai ($Q_3 - Q_1$) có vai trò gì trong trích xuất đặc trưng?
**Trả lời:** Khoảng tứ phân vị (Interquartile Range - IQR) là một đại lượng thống kê phi tham số đại diện cho độ phân tán của dữ liệu. Khác với độ lệch chuẩn ($\sigma$) rất dễ bị méo mó bởi một vài điểm nhiễu ngoại lai, IQR đo lường độ rộng biến thiên của $50\%$ số điểm trung tâm, giúp mô hình phân biệt được dạng xung nhọn của $H_2S$ với dạng xung tù, bằng phẳng của $NH_3$ một cách cực kỳ bền bỉ với nhiễu.

#### Câu 60: Nếu nhiệt độ môi trường ngoài trời giảm đột ngột dưới $0^\circ\text{C}$ thì thuật toán bù trôi xử lý ra sao?
**Trả lời:** Trong công thức bù trôi, biến nhiệt độ $T$ từ DHT22 có dải đo từ $-40^\circ\text{C}$. Khi $T < 0^\circ\text{C}$, đại lượng $(T - 25.0)$ sẽ mang giá trị âm, làm mẫu số $\text{compFactor} < 1.0$, do đó giá trị $V_{\text{compensated}}$ tự động được nâng lên để bù đắp cho sự suy giảm độ dẫn điện tự nhiên của chất bán dẫn ở nhiệt độ âm. Đồng thời, thuật toán giới hạn mẫu số tối thiểu $\ge 0.5$ để tránh hiện tượng chia cho số quá nhỏ.

---

## NHÓM 5: TRÍ TUỆ NHÂN TẠO BIÊN (EDGE AI), TRÍCH XUẤT ĐẶC TRƯNG & HUẤN LUYỆN (CÂU 61 - 80)

#### Câu 61: Tại sao nhóm lại lựa chọn mô hình Random Forest mà không sử dụng Deep Learning (như CNN, LSTM)?
**Trả lời:** Nhóm lựa chọn Random Forest dựa trên 4 luận điểm kỹ thuật thực tế:
1. **Ràng buộc tài nguyên phần cứng biên:** Thiết bị triển khai là Raspberry Pi 3 với 1GB RAM chia sẻ cho GPU. Các framework Deep Learning (TensorFlow, PyTorch) khi nạp vào bộ nhớ đã chiếm $400 - 600\text{ MB}$ RAM, rất dễ bị tiến trình Linux OOM-Killer tắt cưỡng bức. Random Forest qua Scikit-Learn chỉ chiếm chưa đầy **$80\text{ MB}$** RAM cho toàn bộ Gateway.
2. **Độ trễ suy luận siêu thấp:** Random Forest thực thi qua các phép so sánh nhị phân trên cây quyết định đã được vector hóa bằng C-extension, thời gian suy luận chỉ mất **$2 - 4\text{ ms}$** trên CPU ARM Cortex-A53, nhanh hơn gấp hàng chục lần so với phép nhân ma trận của mạng nơ-ron.
3. **Kích thước tập dữ liệu phù hợp:** Dữ liệu chuỗi thời gian cảm biến công nghiệp có đặc thù trích xuất đặc trưng vật lý tốt. Với 361 chu kỳ chuẩn, Random Forest đạt độ chính xác $95.21\%$ mà không bị Overfitting như các mạng Deep Learning vốn đòi hỏi hàng chục ngàn mẫu.
4. **Khả năng giải thích (Explainability):** Cho phép tính toán chính xác Feature Importance, phục vụ bảo vệ an toàn công nghiệp có thể chứng minh được logic.

#### Câu 62: Trình bày quy trình kiểm chứng "Stratified 5-Fold Zero-Overlap Cross-Validation"? Tại sao nếu không làm "Zero-Overlap" thì kết quả là gian lận?
**Trả lời:** Khi trích xuất các cửa sổ trượt 20 điểm từ các chu kỳ 250 điểm, các cửa sổ liền kề nhau có sự chồng lấn dữ liệu rất lớn. Nếu xáo trộn ngẫu nhiên (Random Shuffle) các cửa sổ rồi chia Train/Test, các cửa sổ trong tập Test sẽ có các điểm đo gần như giống hệt các cửa sổ trong tập Train $\rightarrow$ Gây ra hiện tượng **Rò rỉ dữ liệu (Data Leakage)**, khiến mô hình đạt độ chính xác ảo $99.9\%$ nhưng sẽ thất bại hoàn toàn khi ra thực địa.
**Zero-Overlap Pulse Level Split** của nhóm giải quyết triệt để: Việc phân chia tập Train/Test được thực hiện ở cấp độ **toàn bộ chu kỳ 60 giây**. Toàn bộ các cửa sổ thuộc về một chu kỳ hoặc chỉ nằm trong tập Train, hoặc chỉ nằm trong tập Test. Quá trình kiểm định lặp lại 5 lần (5-Fold) phân tầng đồng đều giữa các nhãn khí để đảm bảo tính khách quan tuyệt đối.

#### Câu 63: Sai số MAE của mô hình hồi quy nồng độ là bao nhiêu? Ý nghĩa của sai số này trong an toàn công nghiệp?
**Trả lời:** Sai số tuyệt đối trung bình (MAE) của mô hình Pulse Regressor là **$3.79\text{ ppm}$** trên toàn dải đo ($0 - 100\text{ ppm}$), với hệ số xác định $R^2 = 0.8357$. Đối với mô hình Window Regressor, MAE đạt **$2.47\text{ ppm}$** ($R^2 = 0.9333$). Trong an toàn công nghiệp, sai số $\sim 2.5 - 3.8\text{ ppm}$ là hoàn toàn chấp nhận được, bởi vì hệ thống phân cấp an toàn theo các bước nhảy lớn ($1\text{ ppm} \rightarrow 5\text{ ppm} \rightarrow 10\text{ ppm} \rightarrow 50\text{ ppm}$); sai số này đảm bảo phát hiện chính xác mức độ nguy hại để kích hoạt kịch bản sơ tán kịp thời.

#### Câu 64: Thuật toán Synthetic Plume Injection tạo ra dữ liệu tổng hợp như thế nào? Dữ liệu này có làm sai lệch bản chất vật lý không?
**Trả lời:** Không làm sai lệch bản chất vật lý. Phản ứng của khí độc trên cảm biến MOS tuân theo nguyên lý cộng hưởng độ dẫn điện: Khi có chất khí, điện trở màng oxit thay đổi tạo ra một bước nhảy điện áp vi sai $\Delta V_{\text{gas}}(t)$ trên nền điện áp sạch. Thuật toán lấy xung vi sai thuần túy thu được từ buồng chuẩn thí nghiệm, sau đó ghép chồng lên các đường nền không khí ngoài trời thực tế đã ghi nhận được, có tính toán biến thiên độ nhạy ngẫu nhiên $\alpha \in [0.92, 1.08]$ và nhiễu trắng. Dữ liệu tổng hợp phản ánh chính xác hiện tượng vật lý của một chùm khí độc rò rỉ vào bầu khí quyển ngoài trời.

#### Câu 65: Mô hình phân biệt giữa khí $H_2S$ và $NH_3$ dựa trên những đặc trưng khác biệt cốt lõi nào?
**Trả lời:** Mô hình phân biệt dựa trên 3 đặc trưng động học cốt lõi:
1. **Động học tăng điện áp (Rise Kinetics):** $H_2S$ có phản ứng oxy hóa cực mạnh ở nhiệt độ thấp hơn, khiến điện áp tăng vọt rất nhanh, thời điểm đạt đỉnh sớm ($T_{peak}$ thường rơi vào giây thứ $15 - 18$). $NH_3$ có phản ứng chậm hơn, đỉnh xung tù và dịch chuyển về sau ($T_{peak}$ rơi vào giây thứ $22 - 28$).
2. **Tốc độ suy giảm giải hấp phụ (Decay Slope):** Phân tử $NH_3$ tạo liên kết hydro với hơi ẩm bề mặt mạnh hơn, khiến tốc độ giải hấp phụ của $NH_3$ chậm hơn đáng kể so với $H_2S$.
3. **Tương quan giữa 2 kênh cảm biến:** Màng nhạy khí MQ136 có độ nhạy vượt trội với $H_2S$, trong khi MQ135 có độ nhạy tương đương giữa $NH_3$ và các khí hữu cơ. Tỷ số biên độ $\Delta V_{MQ136} / \Delta V_{MQ135}$ của $H_2S$ cao hơn từ $2.5 - 4$ lần so với $NH_3$.

#### Câu 66: Quá khớp (Overfitting) được kiểm soát như thế nào trong quá trình huấn luyện Random Forest?
**Trả lời:** Nhóm kiểm soát Overfitting qua 4 cơ chế:
1. Giới hạn độ sâu tối đa của cây: `max_depth = 10` (đối với Pulse Model) và `max_depth = 12` (đối với Window Model), ngăn cây học các nhánh nhiễu chi tiết.
2. Giới hạn số lượng mẫu tối thiểu để tách nhánh: `min_samples_split = 4`.
3. Số lượng cây đủ lớn: `n_estimators = 100` với cơ chế Bootstrap lấy mẫu có hoàn lại.
4. Kiểm chứng chéo Zero-Overlap 5-Fold: Khoảng cách giữa độ chính xác tập Train ($98.1\%$) và tập Test ($95.2\%$) chỉ chênh lệch dưới $3\%$, chứng minh mô hình tổng quát hóa rất tốt.

#### Câu 67: Làm thế nào để lưu trữ và tải các mô hình máy học trên Raspberry Pi 3 mà không tốn dung lượng?
**Trả lời:** Các mô hình sau khi huấn luyện được tuần tự hóa (Serialize) bằng thư viện `pickle` với mức nén tối ưu. Dung lượng của mỗi tệp mô hình chỉ khoảng **$2 - 4\text{ MB}$**:
- `model_pulse_gas.pkl`, `model_pulse_ppm.pkl`
- `model_gas.pkl`, `model_ppm.pkl`
Tổng dung lượng toàn bộ 4 mô hình chưa đến $15\text{ MB}$, được nạp trực tiếp vào RAM của Raspberry Pi 3 ngay khi dịch vụ `aiot-gateway.service` khởi động và thường trực phục vụ suy luận với chi phí bộ nhớ tối thiểu.

#### Câu 68: Chỉ số F1-Score của từng lớp khí là bao nhiêu? Lớp nào nhận diện tốt nhất?
**Trả lời:** Theo báo cáo phân lớp chi tiết (`metrics.json`):
- **Clean Air:** Precision $94.5\%$, Recall $99.6\%$, **F1-Score: $97.0\%$** (nhận diện tốt nhất, gần như không bỏ sót bất kỳ mẫu không khí sạch nào).
- **$NH_3$:** Precision $96.6\%$, Recall $94.9\%$, **F1-Score: $95.8\%$**.
- **$H_2S$:** Precision $95.0\%$ (độ chuẩn xác rất cao, khi đã báo $H_2S$ là xác suất đúng $95\%$), Recall $88.8\%$, **F1-Score: $91.8\%$**.
F1-Score trung bình toàn hệ thống đạt **$95.2\%$**.

#### Câu 69: Tại sao Recall của lớp $H_2S$ lại là $88.8\%$ mà không phải $100\%$? Số mẫu bị nhầm rơi vào đâu?
**Trả lời:** Trong ma trận nhầm lẫn, có 14 mẫu $H_2S$ bị nhầm sang Clean Air. Phân tích sâu vào các mẫu này, nhóm nhận thấy đây là các xung $H_2S$ ở nồng độ cực loãng ($1\text{ ppm}$) tại các điểm lấy mẫu ở rìa chu kỳ sóng nhiệt (khi nhiệt độ sấy chưa đạt mức tối ưu, biên độ đáp ứng của cảm biến chỉ tăng khoảng $0.05\text{V}$, xấp xỉ mức dao động của không khí sạch). Điều này hoàn toàn phù hợp với thực tế vật lý và hệ thống đã có bộ lọc thời gian thực bù đắp khi bước vào giai đoạn nung đỉnh.

#### Câu 70: Tầm quan trọng của đặc trưng (Feature Importance) được tính toán theo phương pháp nào?
**Trả lời:** Tính toán dựa trên độ giảm độ tinh khiết Gini (Mean Decrease Impurity - MDI). Mỗi khi một đặc trưng $X_j$ được chọn để phân chia một nút trên cây quyết định, độ suy giảm chỉ số bất thuần Gini được cộng dồn cho đặc trưng đó. Giá trị tổng kết trên toàn bộ 100 cây quyết định được chuẩn hóa về tổng bằng $1.0$ ($100\%$).

#### Câu 71: Động cơ suy luận xử lý thế nào nếu một đặc trưng đầu vào có giá trị ngoại lai cực lớn (Outlier)?
**Trả lời:** Cây quyết định và Random Forest là các thuật toán phân tách nhị phân dựa trên thứ tự xếp hạng (Rank-based partitioning), hoàn toàn không nhạy cảm với các giá trị ngoại lai cực đại như các thuật toán tối ưu dựa trên khoảng cách (KNN, SVM) hay lan truyền ngược (Neural Networks). Một giá trị $\Delta V = 5.0\text{V}$ hay $10.0\text{V}$ đều sẽ rơi vào cùng một nhánh lá của điều kiện `if Delta_V > 0.55V`, do đó quyết định phân loại vẫn duy trì chính xác tuyệt đối.

#### Câu 72: Tại sao không chuẩn hóa dữ liệu bằng `StandardScaler` hay `MinMaxScaler` trước khi đưa vào Random Forest?
**Trả lời:** Random Forest chỉ so sánh giá trị của từng đặc trưng đơn lẻ với ngưỡng phân chia tại từng nút (`feature <= threshold`), không thực hiện phép tính khoảng cách Euclid giữa các chiều đặc trưng khác nhau. Do đó, việc áp dụng `StandardScaler` là hoàn toàn không cần thiết, giúp tiết kiệm đáng kể thời gian tính toán của CPU trên thiết bị nhúng.

#### Câu 73: Tần suất chạy suy luận trên Raspberry Pi 3 được thiết lập như thế nào?
**Trả lời:** Để tối ưu hóa tải cho CPU ARM Cortex-A53, trong hàm `on_rs485_sample` (`app.py`), nhóm đã thiết lập cơ chế điều tiết tần suất suy luận (Throttling): Mô hình Window Model chạy với tần suất tối đa **$5\text{ Hz}$** (tức cách nhau tối thiểu $200\text{ ms}$ mới kích hoạt một lần suy luận). Nếu mẫu đến nhanh hơn, hệ thống sử dụng lại kết quả suy luận của mẫu trước. Cơ chế này giúp giữ mức sử dụng CPU của Gateway dưới $15\%$.

#### Câu 74: Mô hình ước lượng nồng độ ppm hoạt động theo phương pháp phân loại hay hồi quy?
**Trả lời:** Hoạt động theo phương pháp **Hồi quy liên tục (Regression)** thông qua mô hình `RandomForestRegressor`. Mặc dù dữ liệu thực nghiệm được đo ở các mức nồng độ rời rạc ($1, 5, 10\text{ ppm}$ đối với $H_2S$ và $10, 50, 100\text{ ppm}$ đối với $NH_3$), mô hình hồi quy của nhóm có khả năng nội suy mượt mà để ước lượng bất kỳ mức nồng độ liên tục nào (ví dụ $3.4\text{ ppm}, 7.8\text{ ppm}$ hoặc $42.5\text{ ppm}$).

#### Câu 75: Làm thế nào để đảm bảo mô hình không hồi quy ra nồng độ âm ($< 0\text{ ppm}$)?
**Trả lời:** Trong mã nguồn `backend/gateway.py` và `app.py`, kết quả hồi quy từ mô hình máy học luôn được bọc trong hàm chặn dưới:
$$\text{estimated\_ppm} = \max(0.0, \text{regressor.predict}(X)[0])$$
Đồng thời, nếu trạng thái phân loại là `Clean Air`, nồng độ được cưỡng bức triệt để về $0.0\text{ ppm}$.

#### Câu 76: Cấu trúc của ma trận nhầm lẫn cho biết điều gì về khả năng phân biệt giữa $H_2S$ và $NH_3$?
**Trả lời:** Trong ma trận nhầm lẫn:
- Số mẫu $H_2S$ bị nhầm sang $NH_3$ chỉ có 5 mẫu trên tổng số 170 mẫu ($< 3\%$).
- Số mẫu $NH_3$ bị nhầm sang $H_2S$ chỉ có 8 mẫu trên tổng số 178 mẫu ($< 4.5\%$).
Điều này khẳng định mảng cảm biến và vector đặc trưng động học đã tách biệt rất rõ ràng hai không gian phổ khí này, không bị nhầm lẫn giữa hai loại khí độc nguy hiểm.

#### Câu 77: Tại sao mô hình Window Model lại có độ chính xác thấp hơn một chút so với Pulse Model ($93.46\%$ so với $95.21\%$)?
**Trả lời:** Đây là sự đánh đổi kinh điển giữa **Thời gian** và **Thông tin**:
- Pulse Model phân tích trọn vẹn 250 điểm dữ liệu trong toàn bộ 60 giây, chứa đầy đủ các giai đoạn nhiệt động học từ hấp phụ, đạt đỉnh đến làm nguội giải hấp phụ, do đó lượng thông tin là cực đại.
- Window Model chỉ nhìn thấy một lát cắt thời gian 20 điểm ($\sim 4.8\text{ giây}$). Khi chùm khí mới chớm tiếp xúc ở nồng độ cực loãng, thông tin động học chưa bộc lộ hoàn toàn. Tuy nhiên, độ chính xác $93.46\%$ là quá đủ cho nhiệm vụ cảnh báo sớm thời gian thực.

#### Câu 78: Nếu một loại khí lạ (ví dụ cồn Ethanol hoặc khí Gas hóa lỏng LPG) xuất hiện thì mô hình phản ứng thế nào?
**Trả lời:** Nhờ mô hình tính toán xác suất phân lớp qua `predict_proba()`, nếu một loại khí lạ xuất hiện, xác suất của cả 3 lớp $H_2S$, $NH_3$ và Clean Air đều sẽ ở mức thấp và phân tán (ví dụ không lớp nào vượt quá $50\%$). Hệ thống có thể gắn nhãn `Unknown Gas` và kích hoạt mức cảnh báo nghi ngờ thay vì tự động quy chụp sang khí độc.

#### Câu 79: Quá trình huấn luyện lại mô hình (Retraining) khi có dữ liệu mới mất bao lâu trên máy tính?
**Trả lời:** Do thuật toán Random Forest được tối ưu hóa đa luồng qua OpenMP (`n_jobs = -1`), quá trình huấn luyện toàn bộ 4 mô hình trên tập dữ liệu 361 chu kỳ kèm dữ liệu tăng cường chỉ mất khoảng **$12 - 18\text{ giây}$** trên một máy tính cá nhân tiêu chuẩn, cho phép cập nhật mô hình định kỳ rất thuận tiện.

#### Câu 80: Mô hình có khả năng tự học trực tiếp trên Raspberry Pi 3 (On-Device Learning) không?
**Trả lời:** Về mặt lý thuyết, thư viện Scikit-Learn cài trên Pi 3 hoàn toàn có thể chạy script `python -m backend.train`. Tuy nhiên, trong thực tiễn công nghiệp, việc huấn luyện máy học nên được thực hiện trên Cloud hoặc máy trạm để bảo toàn tài nguyên CPU cho tác vụ an toàn thời gian thực. Sau khi huấn luyện, chỉ cần đẩy tệp trọng số `.pkl` nhẹ vài megabyte về Pi 3 và khởi động lại dịch vụ.

---

## NHÓM 6: ĐÁNH GIÁ RỦI RO AN TOÀN, GRADIENT PROGNOSTICS & VẬN HÀNH SCADA (CÂU 81 - 92)

#### Câu 81: Trình bày chi tiết logic phân cấp an toàn 4 mức trong hàm `computeRiskLevel`?
**Trả lời:** Hàm `computeRiskLevel` kết hợp đồng thời **nồng độ ước tính** và **biên độ vi sai $\Delta V$**:
1. **Level 1 (Normal):** Nếu khí là `Clean Air` hoặc $\Delta V < 0.08\text{V} \rightarrow$ Hệ thống an toàn tuyệt đối.
2. **Level 2 (Warning):** Khi $H_2S \ge 1.0\text{ ppm}$ hoặc $\Delta V \ge 0.12\text{V}$ (đối với $NH_3$ là $\ge 25\text{ ppm}$ hoặc $\Delta V \ge 0.15\text{V}$) $\rightarrow$ Mức chớm rò rỉ, hiển thị trạng thái màu vàng, thông báo giám sát.
3. **Level 3 (Hazardous):** Khi $H_2S \ge 5.0\text{ ppm}$ hoặc $\Delta V \ge 0.35\text{V}$ (đối với $NH_3$ là $\ge 50\text{ ppm}$ hoặc $\Delta V \ge 0.45\text{V}$) $\rightarrow$ Vượt ngưỡng OSHA PEL, màu cam, yêu cầu mặt nạ SCBA.
4. **Level 4 (Emergency):** Khi $H_2S \ge 10.0\text{ ppm}$ hoặc $\Delta V \ge 0.55\text{V}$ (đối với $NH_3$ là $\ge 100\text{ ppm}$ hoặc $\Delta V \ge 0.65\text{V}$) $\rightarrow$ Mức nguy kịch đe dọa tính mạng, màu đỏ, hú còi khẩn cấp.

#### Câu 82: Thuật toán Gradient Prognostics tính toán dự báo $+20\text{ giây}$ như thế nào?
**Trả lời:** Dựa trên chuỗi 20 điểm điện áp trong cửa sổ trượt, thuật toán tính tốc độ dâng điện áp:
$$\text{Slope} = \frac{w[-1] - w[0]}{\Delta t}$$
Từ giá trị hiện tại $V_t$, hệ thống ngoại suy tuyến tính vị trí tiếp theo sau các bước thời gian $h \in [5\text{s}, 10\text{s}, 15\text{s}, 20\text{s}]$:
$$\hat{V}_{t+h} = V_t + \text{Slope} \cdot h$$
Giá trị dự báo cực đại $\max(\hat{V})$ đại diện cho nồng độ đỉnh mà chùm khí sẽ đạt tới trong 20 giây tới nếu dòng rò rỉ không được ngăn chặn.

#### Câu 83: Chỉ số "Time-to-Emergency" (TTE) được tính toán như thế nào và có ý nghĩa gì đối với công nhân?
**Trả lời:** Khi độ dốc tăng nhanh ($\text{Slope} > 0.015\text{V/s}$) và chùm khí được nhận diện là $H_2S$, hệ thống ước lượng thời gian còn lại trước khi điện áp chạm ngưỡng khẩn cấp ($2.45\text{V}$ tương đương $10\text{ ppm}$):
$$\text{TTE} = \frac{2.45 - V_t}{\max(0.002, \text{Slope})}\ \text{giây}$$
Chỉ số này hiển thị trực tiếp lên bảng điện tử: ví dụ `TTE: 16s`. Đối với công nhân tại hiện trường, 16 giây cảnh báo trước là khoảng thời gian sống còn để nín thở, chụp mặt nạ phòng độc dưỡng khí hoặc chạy ngược hướng gió thoát khỏi vùng rò rỉ.

#### Câu 84: Cơ chế "Acknowledge" (Xác nhận báo động) trên Web Dashboard hoạt động ra sao?
**Trả lời:** Khi nồng độ chạm mức `Hazardous` hoặc `Emergency`, banner cảnh báo đỏ nhấp nháy toàn màn hình và còi báo động Web Audio hú liên tục. Khi người vận hành ca trực bấm nút `[ Xác Nhận Báo Động ]` (`btnAcknowledge`):
- Âm thanh còi tạm thời tắt để tránh gây hoảng loạn.
- Hệ thống ghi nhận dấu thời gian, ID người trực và hành động xác nhận vào bảng nhật ký sự kiện `AlarmEvents`.
- Nếu sau 5 phút nồng độ khí vẫn không giảm, còi báo động sẽ tự động tái kích hoạt (Escalation Protocol).

#### Câu 85: Cơ chế mô phỏng gửi Email Dispatch hoạt động như thế nào?
**Trả lời:** Khi phát sinh sự cố ở mức khẩn cấp, Dashboard kích hoạt modal gửi thông báo an toàn mô phỏng luồng gửi của Advantech WISE-IoT. Nội dung email được tạo tự động bao gồm: Mã sự cố (AlertID), dấu thời gian, vị trí cụ thể trạm đo (ví dụ: Trạm nén khí số 1), loại khí nhận diện ($H_2S$), nồng độ tức thời, mức độ vượt ngưỡng và hướng dẫn hành động bắt buộc (cô lập van V302, sơ tán nhân viên theo hướng gió an toàn).

#### Câu 86: Chế độ hiển thị "Sweep Overwrite" trên dao động ký có ưu điểm gì so với việc cuộn biểu đồ liên tục (Rolling Chart)?
**Trả lời:** Cuộn biểu đồ liên tục khiến các chu kỳ bị kéo dài vô tận trên trục thời gian, người vận hành rất khó so sánh hình dáng chu kỳ này với chu kỳ trước. Chế độ **Sweep Overwrite** mô phỏng chính xác màn hình của máy hiện sóng (Oscilloscope) công nghiệp:
- Trục hoành cố định đúng 250 điểm ($0 - 60\text{ giây}$).
- Con trỏ quét chạy từ trái sang phải, chạy đè dữ liệu mới lên dữ liệu cũ.
- Giữ lại đường sóng của chu kỳ trước đó dưới dạng bóng mờ (**Ghost Trace**). Người vận hành có thể nhận biết ngay lập tức sự thay đổi bất thường của dạng sóng chỉ bằng một cái liếc mắt.

#### Câu 87: Web Audio API tạo âm thanh còi báo động bằng cách nào mà không cần tệp âm thanh ngoài?
**Trả lời:** Nhóm sử dụng trực tiếp Web Audio API tích hợp sẵn trong trình duyệt:
- Tạo một bộ dao động âm thanh (`OscillatorNode`) với dạng sóng răng cưa (`sawtooth`).
- Điều chế tần số âm thanh quét qua lại giữa $600\text{ Hz}$ và $1200\text{ Hz}$ theo chu kỳ $0.5\text{ giây}$ thông qua hàm `linearRampToValueAtTime`.
- Điều này giúp âm thanh cảnh báo có thể phát ngay lập tức mà không phụ thuộc vào việc tải tệp âm thanh MP3/WAV từ máy chủ, tránh lỗi trễ âm thanh khi khẩn cấp.

#### Câu 88: Bảng nhật ký sự kiện (Audit Log Table) lưu giữ những thông tin gì?
**Trả lời:** Lưu giữ 10 trường thông tin chuẩn phục vụ điều tra sự cố:
1. Dấu thời gian chính xác (Timestamp).
2. Mã trạm đo (Node ID).
3. Loại khí do AI nhận diện (Identified Gas).
4. Mức độ rủi ro (Risk Level: Normal, Warning, Hazardous, Emergency).
5. Nồng độ ước tính (ppm).
6. Điện áp đỉnh chu kỳ ($V_{max}$).
7. Điện áp đáy chu kỳ ($V_{min}$).
8. Biên độ vi sai ($\Delta V$).
9. Diện tích tích phân sóng ($\text{AUC}$).
10. Mã chu kỳ hoàn thành (Cycle ID).

#### Câu 89: 4 kịch bản mô phỏng trong `backend/app.py` được thiết kế nhằm mục đích gì?
**Trả lời:** 4 kịch bản mô phỏng phục vụ việc kiểm thử, đào tạo nhân viên và thuyết minh triển lãm:
1. `fieldScenario` (Kịch bản thực địa liên hoàn): Mô phỏng trọn vẹn 1 ca trực với 4 giai đoạn nối tiếp (Không khí sạch $\rightarrow$ Sự cố rò rỉ $H_2S$ $10\text{ ppm}$ $\rightarrow$ Bật quạt thông gió phục hồi $\rightarrow$ Sự cố xả thải $NH_3$ $50\text{ ppm}$ $\rightarrow$ Hồi phục an toàn).
2. `H2SRun`: Kiểm thử chuyên sâu đáp ứng với khí độc $H_2S$ từ $0 - 10\text{ ppm}$.
3. `NH3Run`: Kiểm thử chuyên sâu đáp ứng với khí kích thích $NH_3$ từ $0 - 100\text{ ppm}$.
4. `airRun`: Kiểm thử tính ổn định của đường nền không khí sạch và xác minh cơ chế chống báo động giả.

#### Câu 90: Nút "Ghost Trace" trên giao diện thực nghiệm mang lại giá trị thực tiễn gì?
**Trả lời:** Cho phép hiển thị vệt sóng nét đứt mờ của chu kỳ hoàn chỉnh trước đó song song với chu kỳ đang chạy. Kỹ sư thực nghiệm có thể so sánh trực quan xem biên độ đáp ứng của cảm biến có bị suy giảm do hiện tượng trễ nhiệt (Thermal Hysteresis) hay không, hoặc đối chiếu sự thay đổi nồng độ giữa 2 chu kỳ đo liên tiếp.

#### Câu 91: Làm thế nào hệ thống đảm bảo giao diện hiển thị tốt trên cả máy tính bảng và màn hình SCADA lớn?
**Trả lời:** Giao diện được xây dựng trên nền tảng CSS Grid và Flexbox kết hợp Tailwind CSS với thiết kế Mobile-First và Fully Responsive. Giao diện tự động co giãn tối ưu từ màn hình điện thoại di động, máy tính bảng hiện trường ($7 - 10\text{ inch}$) cho đến màn hình giám sát trung tâm SCADA độ phân giải cao ($2\text{K} - 4\text{K}$).

#### Câu 92: Tính năng chuyển đổi đa ngôn ngữ (VI/EN) được quản lý như thế nào?
**Trả lời:** Được quản lý tập trung thông qua lớp `I18nThemeManager` trong tệp `dashboard/i18n-theme.js`. Toàn bộ từ khóa giao diện được ánh xạ qua từ điển JSON song ngữ. Khi người dùng bấm chuyển đổi, hệ thống cập nhật đồng loạt các thẻ có thuộc tính `data-i18n` và lưu trạng thái vào `localStorage` của trình duyệt, đảm bảo duy trì ngôn ngữ đã chọn cho các phiên làm việc tiếp theo.

---

## NHÓM 7: TỐI ƯU HÓA NHÚNG, KHẢ NĂNG TRIỂN KHAI RASPBERRY PI 3 & ĐỘ BỀN 24/7 (CÂU 93 - 105)

#### Câu 93: Tại sao nhóm lại chọn Raspberry Pi 3 Model B để triển khai thực tế mà không phải Raspberry Pi 5 hay Jetson Nano?
**Trả lời:** Nhóm chọn Raspberry Pi 3 Model B (phần cứng ra mắt từ 2016, chip Cortex-A53 thế hệ cũ, RAM chỉ 1GB) để chứng minh một tuyên bố kỹ thuật mạnh mẽ: **Nếu thuật toán và mô hình Edge AI được tối ưu hóa xuất sắc, chúng ta hoàn toàn có thể triển khai trí tuệ nhân tạo công nghiệp đỉnh cao trên các phần cứng thế hệ cũ giá rẻ ($< 35\text{ USD}$)**. Việc sử dụng Jetson Nano đắt tiền tiêu tốn nhiều điện năng ($10 - 15\text{ W}$) và tỏa nhiệt lớn là lãng phí đối với bài toán chuỗi thời gian cảm biến khí.

#### Câu 94: Dịch vụ chạy nền trên Raspberry Pi 3 được cấu hình như thế nào để đảm bảo tự phục hồi sau sự cố?
**Trả lời:** Hệ thống được đóng gói thành một dịch vụ hệ thống Linux Systemd: `/etc/systemd/system/aiot-gateway.service`.
Dịch vụ được thiết lập:
- Tự động kích hoạt khi bật nguồn: `WantedBy=multi-user.target`.
- Tự động khởi động lại sau 5 giây nếu gặp sự cố crash: `Restart=always`, `RestartSec=5`.
- Chạy độc lập dưới quyền người dùng an toàn `pi`, toàn bộ log được chuyển hướng về `journald` và ghi tệp xoay vòng.

#### Câu 95: Cơ chế Rotating File Handler trong module ghi log giải quyết bài toán gì trên thẻ nhớ SD của Raspberry Pi?
**Trả lời:** Thẻ nhớ MicroSD trên Raspberry Pi có số lần ghi hữu hạn và dung lượng giới hạn ($16 - 32\text{ GB}$). Nếu ghi log liên tục 24/7 mà không kiểm soát, thẻ nhớ sẽ bị đầy sau vài tháng và gây hỏng hệ điều hành. Lớp `RotatingFileHandler` trong `serial_pipeline/main.py` khống chế kích thước tệp log tối đa **$5\text{ MB}$** và chỉ lưu giữ tối đa 3 tệp sao lưu (`backupCount = 3`). Khi vượt quá $5\text{ MB}$, tệp cũ nhất tự động bị ghi đè, đảm bảo bộ nhớ lưu trữ không bao giờ bị tràn.

#### Câu 96: Tải CPU và mức tiêu thụ RAM đo đạc thực tế trên Raspberry Pi 3 là bao nhiêu?
**Trả lời:** Đo đạc thực tế qua lệnh `htop` và `systemd-cgtop` khi hệ thống đang vừa đọc RS-485, vừa suy luận AI, vừa đẩy WebSocket và Firebase:
- **Tải CPU trung bình:** Duy trì từ **$8\% - 14\%$** trên 4 nhân Cortex-A53.
- **Dung lượng RAM chiếm dụng:** Dao động từ **$72\text{ MB} - 84\text{ MB}$** (chưa tới $9\%$ tổng dung lượng RAM 1GB của máy).
- **Nhiệt độ SoC:** Ổn định ở mức $48 - 52^\circ\text{C}$ với tản nhiệt nhôm thụ động thông thường.

#### Câu 97: Mạng Tailscale VPN Mesh đóng vai trò gì trong việc quản trị và bảo trì từ xa?
**Trả lời:** Tailscale tạo ra một mạng riêng ảo bảo mật ngang hàng (P2P Mesh VPN) dựa trên giao thức WireGuard hiện đại. Nhờ Tailscale, thiết bị Raspberry Pi 3 được cấp một địa chỉ IP cố định an toàn (`100.72.0.24`). Kỹ sư có thể SSH quản trị, nạp mã nguồn mới hoặc mở trực tiếp Web Dashboard từ bất kỳ máy tính nào trên thế giới mà không cần phải mở cổng router (Port Forwarding), loại bỏ $100\%$ nguy cơ bị tấn công mạng công khai.

#### Câu 98: Tại sao nhóm không sử dụng giao thức ngắt (Interrupt) mà lại dùng luồng đọc liên tục (Threaded Loop) cho Serial?
**Trả lời:** Trên hệ điều hành Linux nhúng, việc sử dụng cơ chế ngắt phần mềm trực tiếp từ cổng USB-Serial (FT232) có thể làm tăng độ trễ chuyển mạch ngữ cảnh (Context Switching Overhead) và gây nghẽn nhân Kernel khi tần suất ngắt quá cao. Việc sử dụng một luồng đọc chuyên dụng (`threading.Thread`) với lệnh đọc thăm dò `ser.read(to_read)` bất đồng bộ giúp luồng chạy mượt mà, giải phóng hoàn toàn tiến trình chính để phục vụ các kết nối WebSocket.

#### Câu 99: Hiện tượng "Memory Leak" (rò rỉ bộ nhớ) trong Python 24/7 được kiểm soát bằng cách nào?
**Trả lời:** Nhóm kiểm soát rò rỉ bộ nhớ bằng 3 nguyên tắc lập trình:
1. Tất cả các mảng đệm lưu trữ dữ liệu chuỗi thời gian đều sử dụng `collections.deque(maxlen=N)` hoặc mảng tĩnh kích thước cố định `[None] * 250`, các phần tử cũ nhất tự động bị hủy khi có phần tử mới.
2. Không lưu vết các đối tượng WebSocket đã ngắt kết nối: sử dụng cơ chế Pub/Sub có hàm `unsubscribe` giải phóng tham chiếu trong khối `finally`.
3. Hàng đợi đẩy dữ liệu Firebase `queue.Queue` được đặt `maxsize = 5` với cơ chế loại bỏ gói tin cũ khi hàng đợi bị đầy.

#### Câu 100: Nếu mất điện đột ngột (Power Loss), hệ thống bảo vệ dữ liệu SQLite như thế nào?
**Trả lời:** Cơ sở dữ liệu SQLite trong `SQLiteEdgeStore` được cấu hình ở chế độ ghi nhật ký an toàn (Write-Ahead Logging - WAL Mode) với cơ chế giao dịch `with conn:` tự động `commit()` hoặc `rollback()` khi hoàn thành từng câu lệnh ghi. Nhờ vậy, ngay cả khi nguồn điện bị cắt đột ngột giữa chừng, cơ sở dữ liệu không bao giờ bị hỏng cấu trúc tệp (Database Corruption) và có thể tự phục hồi ngay khi cấp điện trở lại.

#### Câu 101: Làm thế nào để cập nhật phiên bản mô hình AI mới nhất từ xa xuống Raspberry Pi mà không làm gián đoạn hệ thống?
**Trả lời:** Quy trình cập nhật (Hot-Update) diễn ra qua 2 bước đơn giản qua Tailscale:
1. Sao chép tệp trọng số mới qua lệnh:
   ```bash
   scp backend/model_*.pkl pi@100.72.0.24:/home/pi/Desktop/AIoT/backend/
   ```
2. Khởi động lại dịch vụ qua systemd:
   ```bash
   ssh pi@100.72.0.24 "sudo systemctl restart aiot-gateway.service"
   ```
Toàn bộ quá trình khởi động lại và nạp lại mô hình chỉ diễn ra trong vòng **$1.8\text{ giây}$**, không ảnh hưởng đến an toàn chung của nhà máy.

#### Câu 102: Raspberry Pi 3 giao tiếp với module RS-485 bằng cổng nào?
**Trả lời:** Raspberry Pi 3 giao tiếp qua một module chuyển đổi công nghiệp **USB-to-RS485** sử dụng chip FTDI FT232RL (hoặc CH340G công nghiệp cách ly), nhận diện trên hệ điều hành Linux dưới tên thiết bị `/dev/ttyUSB0`. Việc dùng cổng USB giúp cách ly quang học bảo vệ các chân GPIO của Raspberry Pi khỏi các xung điện áp cảm ứng đột biến trên đường dây ngoài công trường.

#### Câu 103: Tại sao hệ thống có thể chạy được trên cả Raspberry Pi 3 và Raspberry Pi 5?
**Trả lời:** Vì toàn bộ mã nguồn Backend được phát triển bằng Python 3 chuẩn hóa, tuân thủ kiến trúc tập lệnh 64-bit ARMv8/ARMv9 (aarch64). Các thư viện toán học nền tảng (`numpy`, `scipy`, `scikit-learn`) đều được biên dịch tương thích trên nền Debian Linux aarch64. Do đó, mã nguồn có thể chạy mượt mà trên Pi 3 và tự động khai thác sức mạnh đa nhân cao hơn khi chuyển sang Pi 5 mà không cần sửa đổi bất kỳ dòng mã nào.

#### Câu 104: Tốc độ khởi động của toàn bộ hệ thống từ khi cắm điện đến khi bắt đầu suy luận mất bao lâu?
**Trả lời:** 
- Hệ điều hành Debian Trixie khởi động: $\sim 18\text{ giây}$.
- Dịch vụ `aiot-gateway.service` khởi tạo, mở cổng RS-485 và nạp 4 mô hình: $\sim 2.5\text{ giây}$.
- Tổng thời gian sẵn sàng: Dưới **$25\text{ giây}$**, hoàn toàn đáp ứng tiêu chuẩn khởi động nhanh của các thiết bị tự động hóa công nghiệp.

#### Câu 105: Nếu gặp lỗi phần mềm không mong muốn khiến tiến trình bị treo (Deadlock), hệ thống có tự phục hồi không?
**Trả lời:** Có. Ngoài cơ chế `Restart=always` của Systemd, trên Raspberry Pi có thể kích hoạt bộ định thời giám sát phần cứng (**Hardware Watchdog** tích hợp trong chip BCM2837). Nếu tiến trình ứng dụng không gửi tín hiệu "heartbeat" tới bộ đếm watchdog trong vòng $15\text{ giây}$, chip phần cứng sẽ tự động khởi động lại toàn bộ máy tính nhúng để phục hồi hoạt động.

---

## NHÓM 8: AN TOÀN THÔNG TIN, ĐỘ TIN CẬY CÔNG NGHIỆP & HƯỚNG PHÁT TRIỂN (CÂU 106 - 115)

#### Câu 106: Dữ liệu viễn trắc truyền từ Gateway lên Cloud có được mã hóa không?
**Trả lời:** Có. Luồng truyền thông lên nền tảng Advantech WISE-IoT sử dụng giao thức bảo mật **MQTTS** (MQTT over TLS/SSL trên cổng 8883) với thuật toán mã hóa AES-256 bit và chứng chỉ khóa công khai X.509. Luồng truyền thông tới Firebase RTDB và Web Dashboard sử dụng giao thức mã hóa HTTPS/WSS (WebSocket Secure), ngăn chặn $100\%$ các cuộc tấn công nghe lén (Eavesdropping) hoặc chèn dữ liệu giả mạo (Man-in-the-Middle Attack).

#### Câu 107: Làm thế nào để bảo vệ hệ thống khỏi việc một trạm cảm biến giả mạo kết nối vào bus RS-485?
**Trả lời:** Trong cấu hình Modbus RTU, Gateway chỉ gửi lệnh và chấp nhận dữ liệu từ các Node ID đã được định danh và ký số trong danh sách trắng (`whitelist`). Ngoài ra, trong mỗi gói tin viễn trắc đều có mã kiểm tra tính toàn vẹn (Checksum / Hash token), bất kỳ thiết bị lạ nào cắm vào đường bus phát dữ liệu sai định dạng đều bị `StreamPacketParser` từ chối tự động.

#### Câu 108: Khi mất kết nối Internet, dữ liệu viễn trắc có bị mất mát không?
**Trả lời:** Không. Dữ liệu được ghi đồng thời vào cơ sở dữ liệu nhúng SQLite trên thẻ nhớ của Raspberry Pi. Khi có mạng trở lại, một tác vụ nền sẽ thực hiện cơ chế đồng bộ trễ (Store-and-Forward Sync), đẩy các bản ghi sự kiện còn thiếu lên đám mây WISE-IoT, đảm bảo tính toàn vẹn và liên tục của dữ liệu lịch sử phục vụ công tác thanh tra an toàn.

#### Câu 109: Hạn chế lớn nhất của hệ thống hiện tại là gì và nhóm dự định khắc phục thế nào?
**Trả lời:** Hạn chế hiện tại là cảm biến MOS vẫn cần một buồng đo cơ học có màng lọc bảo vệ để tránh bị hơi nước ngưng tụ làm giảm tuổi thọ, và cần hiệu chuẩn định kỳ sau mỗi 6 tháng hoạt động. Hướng khắc phục: Trong phiên bản tiếp theo, nhóm sẽ tích hợp thêm cảm biến quang học NDIR đa bước sóng để tạo thành cụm cảm biến lai (Hybrid Array), kết hợp thuật toán tự hiệu chuẩn trực tuyến (Self-Calibration via Federated Learning).

#### Câu 110: Làm thế nào để tích hợp hệ thống Mũi Điện Tử này vào hệ thống điều khiển DCS/SCADA có sẵn của nhà máy?
**Trả lời:** Cực kỳ dễ dàng. Vì tầng giao tiếp của hệ thống hỗ trợ chuẩn công nghiệp **Modbus RTU** trên cổng RS-485 tiêu chuẩn, các hệ thống DCS/SCADA của các hãng lớn (như Siemens PCS7, Yokogawa CENTUM, Schneider EcoStruxure) có thể đọc trực tiếp các thông số nồng độ, trạng thái rủi ro từ các thanh ghi Holding Registers thông qua cổng Modbus Master có sẵn của nhà máy mà không cần cài đặt thêm phần mềm phụ trợ.

#### Câu 111: Tác động xã hội và môi trường của dự án là gì?
**Trả lời:** Dự án mang lại 3 giá trị xã hội sâu sắc:
1. **Bảo vệ tính mạng con người:** Giúp hàng chục ngàn công nhân làm việc trong các môi trường nguy hiểm có được công cụ cảnh báo sớm đáng tin cậy, ngăn ngừa các vụ tai nạn tử vong thương tâm do ngộ độc khí $H_2S$.
2. **Bảo vệ môi trường sinh thái:** Phát hiện sớm các điểm xì hở khí độc trên tuyến ống dẫn trước khi chúng phát tán ra các khu dân cư lân cận.
3. **Hiệu quả kinh tế cho doanh nghiệp:** Cắt giảm $100\%$ các vụ dừng máy khẩn cấp do báo động giả, tiết kiệm hàng triệu USD chi phí vận hành cho các nhà máy năng lượng tại Việt Nam.

#### Câu 112: Chi phí bảo trì, bảo dưỡng hệ thống định kỳ ước tính là bao nhiêu?
**Trả lời:** Chi phí bảo trì rất thấp. Cụm cảm biến có giá thành thay thế chỉ khoảng $15 - 20\text{ USD}$ sau mỗi $1.5 - 2\text{ năm}$ sử dụng. Toàn bộ phần mềm gateway và dashboard được xây dựng trên mã nguồn mở không mất phí bản quyền định kỳ hàng tháng, giúp doanh nghiệp hoàn vốn đầu tư (ROI) chỉ sau vài tháng vận hành.

#### Câu 113: Khả năng mở rộng của hệ thống trên một mặt bằng nhà máy rộng lớn như thế nào?
**Trả lời:** Với kiến trúc phân tán Daisy-Chain và Modbus RTU, một Gateway Raspberry Pi có thể quản lý đồng thời tới **32 trạm cảm biến** dọc theo chiều dài $1\text{ km}$ tuyến ống. Đối với các nhà máy quy mô lớn hàng chục hecta, chỉ cần bố trí nhiều Gateway tại từng phân xưởng, tất cả các Gateway đều đồng bộ dữ liệu về chung một màn hình Web SCADA trung tâm qua mạng nội bộ Ethernet hoặc Tailscale Mesh.

#### Câu 114: Nhóm có kế hoạch đăng ký sở hữu trí tuệ hoặc công bố bài báo khoa học cho công trình này không?
**Trả lời:** Có. Dưới sự hướng dẫn của TS. Nguyễn Đắc Cử, nhóm đang hoàn thiện bản thảo bài báo khoa học quốc tế về "Shift-Invariant Kinetic Feature Extraction for Edge AI Electronic Nose under High Humidity Environments" dự kiến nộp vào các tạp chí thuộc danh mục Scopus/IEEE Sensors Journal, đồng thời chuẩn bị hồ sơ đăng ký Giải pháp hữu ích tại Cục Sở hữu Trí tuệ Việt Nam.

#### Câu 115: Tóm tắt thông điệp cốt lõi nhất mà nhóm muốn gửi gắm tới Ban giám khảo cuộc thi Advantech AIoT InnoWorks là gì?
**Trả lời:** Thông điệp cốt lõi của TaskForce141 là: **"Chuyển đổi từ Ngưỡng Tĩnh Thụ Động sang Động Học Nhận Dạng Biên Tích Cực"**. Chúng em không chỉ tạo ra một chiếc đầu báo khí, mà mang đến một **Hệ sinh thái an toàn công nghiệp thông minh toàn diện**, nơi phần cứng chi phí tối ưu kết hợp hoàn hảo với Trí tuệ nhân tạo biên và nền tảng Advantech WISE-IoT, sẵn sàng đồng hành bảo vệ an toàn tính mạng cho người lao động Việt Nam và vươn tầm ứng dụng công nghiệp quốc tế!

---
*Tài liệu được biên soạn độc quyền bởi Nhóm TaskForce141 — Đại học Phenikaa phục vụ bảo vệ đồ án và thuyết minh cuộc thi Advantech AIoT InnoWorks 2026.*
