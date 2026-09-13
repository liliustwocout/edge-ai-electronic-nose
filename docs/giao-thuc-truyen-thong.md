# Đặc Tả Giao Thức Truyền Thông (Modbus RTU & MQTT)

> **Dự án:** Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection  
> **Các tầng giao tiếp:**  
> - **Field-to-Edge:** RS-485 / Modbus RTU  
> - **Edge-to-Cloud / App:** Internet / MQTT (WISE-IoT)

---

## 1. Giao Thức Tầng Hiện Trường: RS-485 Modbus RTU

### 1.1 Cấu hình vật lý & đường truyền
- **Chuẩn truyền:** RS-485 vi sai (Half-duplex 2-wire).
- **Tốc độ Baud (Baudrate):** `9600 bps` (hoặc `19200 bps` tùy khoảng cách dây).
- **Data frame format:** `8 Data bits`, `No Parity`, `1 Stop bit` (8N1).
- **Topology:** Tuyến dây trục chính Daisy-chain, 2 đầu trang bị điện trở kết thúc đường truyền **$120\,\Omega$**.
- **Địa chỉ Slave (Slave ID):** 
  - Node 1: `0x01`
  - Node 2: `0x02`
  - Node 3: `0x03`
  - ... Node N: `0x0N` (hỗ trợ tối đa 32 nodes trên 1 segment RS485).

### 1.2 Bảng Ánh Xạ Thanh Ghi Modbus (Modbus Register Map - 16-bit Holding Registers)
Gateway Raspberry Pi 5 sử dụng Function Code `0x03` (Read Holding Registers) để polling dữ liệu định kỳ từ mỗi Node:

| Địa chỉ Register (Hex) | Địa chỉ (Dec) | Tên trường dữ liệu | Kiểu dữ liệu | Hệ số quy đổi (Scale factor) | Đơn vị | Mô tả |
|---|---|---|---|---|---|---|
| `0x0000` | 0 | `NODE_ID` | UINT16 | 1 | - | Mã định danh node (1..N) |
| `0x0001` | 1 | `H2S_CONCENTRATION_INT` | UINT16 | 100 | ppm | Nồng độ H2S (giá trị x 100, ví dụ 2550 = 25.50 ppm) |
| `0x0002` | 2 | `MQ136_RAW_ADC` | UINT16 | 1 | count | Giá trị điện áp/ADC thô của cảm biến MQ136 (0 - 4095) |
| `0x0003` | 3 | `MQ135_RAW_ADC` | UINT16 | 1 | count | Giá trị điện áp/ADC thô của cảm biến MQ135 (0 - 4095) |
| `0x0004` | 4 | `TEMPERATURE` | INT16 | 10 | °C | Nhiệt độ môi trường (giá trị x 10, ví dụ 285 = 28.5 °C) |
| `0x0005` | 5 | `HUMIDITY` | UINT16 | 10 | % | Độ ẩm tương đối (giá trị x 10, ví dụ 650 = 65.0 %RH) |
| `0x0006` | 6 | `SENSOR_STATUS` | UINT16 | 1 | Bitmask | Trạng thái lỗi cảm biến: 0=OK, bit0=Lỗi H2S, bit1=Lỗi DHT22 |
| `0x0007` - `0x0008` | 7 - 8 | `TIMESTAMP_UPTIME` | UINT32 | 1 | giây | Thời gian hoạt động liên tục kể từ khi khởi động (Uptime) |

---

## 2. Giao Thức Tầng Biên Lên Đám Mây: MQTT (WISE-IoT Platform)

Gateway Raspberry Pi 5 đóng vai trò là **MQTT Client** xuất bản (Publish) dữ liệu telemetry và nhận lệnh cấu hình (Subscribe) từ **WISE-IoT Broker**.

### 2.1 Cấu trúc Topic MQTT
```
/advantech/enose/v1/{plant_id}/{gateway_id}/telemetry
/advantech/enose/v1/{plant_id}/{gateway_id}/alert
/advantech/enose/v1/{plant_id}/{gateway_id}/command
```

### 2.2 Định dạng Dữ liệu Telemetry (Publish định kỳ 5s - 10s)
Topic: `/advantech/enose/v1/factory01/rpi5_gw01/telemetry`
```json
{
  "timestamp": "2026-09-12T15:30:00.000Z",
  "gateway_id": "rpi5_gw01",
  "nodes_data": [
    {
      "node_id": 1,
      "h2s_ppm": 2.45,
      "mq136_adc": 1420,
      "mq135_adc": 980,
      "temperature_c": 29.8,
      "humidity_pct": 68.2,
      "risk_level": "Normal",
      "anomaly_score": 0.08
    },
    {
      "node_id": 2,
      "h2s_ppm": 18.75,
      "mq136_adc": 2850,
      "mq135_adc": 2100,
      "temperature_c": 30.1,
      "humidity_pct": 67.5,
      "risk_level": "Hazardous",
      "anomaly_score": 0.89
    }
  ]
}
```

### 2.3 Định dạng Cảnh Báo Khẩn (Publish ngay lập tức khi phát hiện rò rỉ)
Topic: `/advantech/enose/v1/factory01/rpi5_gw01/alert`
```json
{
  "alert_id": "ALT-20260912-0042",
  "timestamp": "2026-09-12T15:30:02.120Z",
  "gateway_id": "rpi5_gw01",
  "node_id": 2,
  "location": "Compressor Station Area 3",
  "risk_level": "Emergency",
  "h2s_concentration_ppm": 52.3,
  "threshold_exceeded": 50.0,
  "inference_result": {
    "predicted_event": "Rapid H2S Leakage Detected",
    "confidence": 0.965,
    "pattern_signature_matched": "Seal_Failure_Pattern_A"
  },
  "action_required": "Evacuate personnel and isolate supply valve V-302"
}
```
