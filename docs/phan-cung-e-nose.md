# Thiết Kế Phần Cứng Nút Cảm Biến Mũi Điện Tử (E-Nose Node Hardware)

> **Dự án:** Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection  
> **Tầng:** Perception Layer (Layer 1) & Power Supply

---

## 1. Khối Vi Điều Khiển & Xử Lý Tín Hiệu (MCU Unit)
- **Bộ vi điều khiển:** ESP32-WROOM-32 (Dual-core Xtensa 32-bit LX6, 240MHz).
- **Chức năng:**
  - Lấy mẫu ADC 12-bit từ các cảm biến khí tương tự/số.
  - Xử lý bộ lọc tín hiệu mức sơ cấp (Moving average filter).
  - Quản lý định danh Node (`Node_ID`) và ánh xạ thanh ghi Modbus.
  - Phục vụ yêu cầu đọc từ Master qua cổng UART nối với RS-485 transceiver.

---

## 2. Cụm Ma Trận Cảm Biến Khí (Sensor Array)

| Tên cảm biến | Loại tín hiệu / Giao tiếp | Đối tượng đo lường | Dải đo & Đặc tính | Mục đích trong hệ thống |
|---|---|---|---|---|
| **ZE03-H2S / MQ136** | Analog ADC / UART | Khí Hydro Sunfua ($H_2S$) | 0 - 50 / 100 ppm, độ nhạy cao với lưu huỳnh | Cảm biến mục tiêu phát hiện rò rỉ khí độc chính |
| **MQ135** | Analog ADC | Khí tổng hợp ($NH_3$, NOx, Benzen, Khói, CO2) | 10 - 1000 ppm | Cảm biến phụ trợ tạo chữ ký mùi (Gas Fingerprint) nhận diện nền |
| **DHT22 (AM2302)** | Single-bus Digital | Nhiệt độ & Độ ẩm không khí | -40°C đến 80°C, 0 - 100% RH | Bù sai lệch nhiệt/ẩm môi trường cho cảm biến MOS |

### Sơ đồ nguyên lý kết nối chân (Pin Mapping ESP32):
```
[ESP32]
├── GPIO34 (ADC1_CH6)  <--- Tín hiệu Analog từ MQ136
├── GPIO35 (ADC1_CH7)  <--- Tín hiệu Analog từ MQ135
├── GPIO4              <--- Tín hiệu Data từ DHT22
├── GPIO16 (RX2)       <--- RO (Receiver Out) module RS485
├── GPIO17 (TX2)       ---> DI (Driver In) module RS485
└── GPIO5              ---> DE & RE (Direction Control) module RS485
```

---

## 3. Khối Giao Tiếp RS-485 (Industrial RS-485 Transceiver)
- **IC truyền thông:** MAX485 / SP3485 (hỗ trợ mức logic 3.3V/5V tương thích ESP32).
- **Điều khiển luồng:** Chân điều khiển chiều thu phát $DE$ và $\overline{RE}$ được chập chung vào GPIO5 của ESP32:
  - Mức `LOW`: Chế độ nhận dữ liệu (Listening/Receiving Modbus Request).
  - Mức `HIGH`: Chế độ phát dữ liệu (Transmitting Modbus Response).
- **Đầu ra đường truyền:** 2 dây vi sai Bus A và Bus B nối vào cáp RS-485 dạng Daisy-chain.

---

## 4. Thiết Kế Vỏ Bảo Vệ Hiện Trường (E-Nose Node Enclosure)
Theo đặc thù nhà máy lọc hóa dầu & xử lý khí tự nhiên có môi trường ăn mòn và khắc nghiệt:
- **Chuẩn bảo vệ:** Hộp vỏ tiêu chuẩn **IP65** kháng nước phun, chống bụi mịn hoàn toàn.
- **Lấy mẫu khí (Gas Inlet with Filter):** Cổng nạp khí có màng lọc PTFE hydrophobic/particulate filter, ngăn chặn hơi nước đọng và bụi bẩn thâm nhập làm hỏng buồng cảm biến.
- **Vật liệu chống ăn mòn (Anti-corrosion):** Vỏ nhựa ABS chống cháy gia cố sợi thủy tinh hoặc phủ sơn kháng $H_2S$.
- **Gá lắp đặt cơ khí:** Đế kim loại/thép không gỉ hỗ trợ kẹp ống dẫn khí, gắn tường (Wall Mounting) hoặc siết đai cột (Pole Mounting).

---

## 5. Khối Cung Cấp Nguồn Điện (Power Supply Unit)
Hệ thống hỗ trợ 2 phương thức cấp nguồn linh hoạt tại hiện trường:
1. **Nguồn DC công nghiệp tập trung:** Đường nguồn DC 12V - 24V chạy song song đường dây tín hiệu RS-485.
2. **Hệ thống nguồn độc lập (Field Autonomous Power):**
   - **Tấm pin năng lượng mặt trời (Solar Panel):** Công suất 20W - 50W (Optional khi triển khai ngoài trời xa nguồn điện).
   - **Bộ lưu điện (Battery Backup):** Bình ắc quy/Pin Lithium LiFePO4 **12V / 5Ah** đảm bảo duy trì hoạt động 24/7 cả khi mất điện lưới.
   - **Mạch hạ áp DC-DC Regulator:** Bộ hạ áp xung Step-down Buck Converter (12V xuống 5V / 3A ổn định) cấp nguồn cho cụm sấy cảm biến MQ và vi điều khiển.
