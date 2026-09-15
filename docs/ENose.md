# E-Nose Node Hardware Design - Perception Layer

**Project:** Edge AI-Based Electronic Nose For Hydrogen Sulfide Leak Detection  
**Layer:** Perception Layer - Layer 1 & Power Supply  

---

## 1. MCU & Signal Processing Unit

- Vi Điều Khiển: ESP32-WROOM-32 Dual-Core Xtensa 32-Bit LX6 240MHz
- Lấy Mẫu ADC 12-Bit Từ Cụm Cảm Biến Khí
- Bộ Lọc Tín Hiệu Sơ Cấp Moving Average Filter
- Quản Lý Định Danh Node ID & Ánh Xạ Holding Registers Modbus
- Giao Tiếp Master Qua Cổng UART Nối RS-485 Transceiver

---

## 2. Sensor Array Matrix

| Sensor | Interface | Target Gas | Range | Role In System |
|---|---|---|---|---|
| ZE03-H2S / MQ136 | Analog ADC & UART | H2S Toxic Gas | 0 Đến 100 ppm | Phát Hiện Rò Rỉ Khí Độc Mục Tiêu |
| MQ135 | Analog ADC | Multi-Gas VOCs, Smoke, NH3 | 10 Đến 1000 ppm | Nhận Diện Nền Khí Tạo Gas Fingerprint |
| DHT22 AM2302 | Single-Bus Digital | Nhiệt Độ & Độ Ẩm | -40°C Đến 80°C, 0 Đến 100% RH | Bù Sai Lệch Nhiệt Ẩm Cho Cảm Biến MOS |

### ESP32 Pin Mapping:

```
ESP32 Pinout
├── GPIO34 ADC1_CH6 ←─── Analog Signal Từ MQ136
├── GPIO35 ADC1_CH7 ←─── Analog Signal Từ MQ135
├── GPIO4 ←─── Data Signal Từ DHT22
├── GPIO16 RX2 ←─── RO Module RS-485
├── GPIO17 TX2 ───→ DI Module RS-485
└── GPIO5 ───→ DE & RE Direction Control RS-485
```

---

## 3. Industrial RS-485 Transceiver

- IC Truyền Thông: MAX485 / SP3485 Tương Thích Mức Logic 3.3V & 5V
- Direction Control: Chân DE & RE Nối Chung Vào GPIO5 Của ESP32
  - Mức LOW: Chế Độ Nhận Modbus Request
  - Mức HIGH: Chế Độ Phát Modbus Response
- Tuyến Bus Vi Sai: 2 Dây Bus A & Bus B Nối Cáp Daisy-Chain RS-485

---

## 4. Field Enclosure Design

- Chuẩn Bảo Vệ IP65 Chống Bụi Mịn & Nước Phun Áp Lực
- Gas Inlet With Filter: Màng Lọc PTFE Hydrophobic Ngăn Nước Đọng & Bụi Bẩn
- Vật Liệu Chống Ăn Mòn: Vỏ ABS Chống Cháy Phủ Lớp Kháng H2S
- Gá Lắp Đặt: Khung Thép Không Gỉ Hỗ Trợ Wall Mount Hoặc Pole Mount

---

## 5. Power Supply Unit

- Phương Thức 1: Nguồn DC Tập Trung 12V Đến 24V Chạy Dọc Tuyến RS-485
- Phương Thức 2: Nguồn Độc Lập Solar Panel 20W Đến 50W & Pin LiFePO4 12V 5Ah Duy Trì 24/7
- Mạch Buck Converter: Hạ Áp Xung 12V Xuống 5V 3A Ổn Định Nuôi Sấy Cảm Biến MQ & ESP32
