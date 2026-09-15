# Communication Protocols Specification - Modbus RTU & MQTT

**Project:** Edge AI-Based Electronic Nose For Hydrogen Sulfide Leak Detection  
**Interface Layers:**  
- Field-To-Edge: RS-485 Modbus RTU  
- Edge-To-Cloud: Internet MQTT WISE-IoT  

---

## 1. Field Layer Protocol: RS-485 Modbus RTU

### 1.1. Physical Configuration & Transmission

- Standard: RS-485 Half-Duplex 2-Wire Differential
- Baudrate: 9600 bps Hoặc 19200 bps
- Frame Format: 8 Data Bits, No Parity, 1 Stop Bit 8N1
- Topology: Daisy-Chain Bus Với 120 Ohm Termination Resistor Tại 2 Đầu Bus
- Slave Address: Node 1 Đến Node 32 Trên Mỗi Segment

### 1.2. Modbus 16-Bit Holding Registers Map

- Gateway Raspberry Pi 5 Dùng Function Code 0x03 Polling Định Kỳ:

| Register Hex | Address Dec | Field Name | Data Type | Scale | Unit | Description |
|---|---|---|---|---|---|---|
| 0x0000 | 0 | nodeId | UINT16 | 1 | None | Mã Định Danh Node 1 Đến N |
| 0x0001 | 1 | s3RawInt | UINT16 | 1000 | Count | Tín Hiệu Thô Cảm Biến S3 Scale 1000 |
| 0x0002 | 2 | temperature | INT16 | 10 | °C | Nhiệt Độ Scale 10 |
| 0x0003 | 3 | humidity | UINT16 | 10 | % | Độ Ẩm Scale 10 |
| 0x0004 | 4 | sensorStatus | UINT16 | 1 | Bitmask | Bitmask Lỗi: 0 OK, Bit0 Lỗi Khí, Bit1 Lỗi DHT22 |
| 0x0005 - 0x0006 | 5 - 6 | timestampUptime | UINT32 | 1 | s | Thời Gian Uptime Hệ Thống |

---

## 2. Edge-To-Cloud Protocol: MQTT WISE-IoT Platform

- Raspberry Pi 5 Là MQTT Client Publish Telemetry & Subscribe Commands Từ WISE-IoT Broker

### 2.1. MQTT Topic Structure

```
/advantech/enose/v1/{plantId}/{gatewayId}/telemetry
/advantech/enose/v1/{plantId}/{gatewayId}/alert
/advantech/enose/v1/{plantId}/{gatewayId}/command
```

### 2.2. Telemetry Payload - Publish Định Kỳ 5s → 10s

Topic: `/advantech/enose/v1/p1/g1/telemetry`

```json
{
  "Timestamp": "2026-09-12T15:30:00.000Z",
  "GatewayID": "g1",
  "NodesData": [
    {
      "timestamp": "2026-09-12 15:30:00",
      "nodeID": 1,
      "s3Raw": 1.002,
      "s3Filtered": 1.002,
      "s3Compensated": 1.002,
      "temperature": 29.8,
      "humidity": 68.2,
      "mq136ADC": 1420,
      "mq135ADC": 980,
      "identifiedGas": "Clean Air",
      "estimatedppm": 2.45,
      "riskLevel": "Normal",
      "latencyMs": 12.5
    },
    {
      "timestamp": "2026-09-12 15:30:00",
      "nodeID": 2,
      "s3Raw": 1.350,
      "s3Filtered": 1.350,
      "s3Compensated": 1.350,
      "temperature": 30.1,
      "humidity": 67.5,
      "mq136ADC": 2850,
      "mq135ADC": 2100,
      "identifiedGas": "H2S",
      "estimatedppm": 18.75,
      "riskLevel": "Hazardous",
      "latencyMs": 14.2
    }
  ]
}
```

### 2.3. Instant Emergency Alert Payload

Topic: `/advantech/enose/v1/p1/g1/alert`

```json
{
  "AlertID": "ALT202609120042",
  "Timestamp": "2026-09-12T15:30:02.120Z",
  "GatewayID": "g1",
  "NodeID": 2,
  "Location": "Compressor Station Area 3",
  "RiskLevel": "Emergency",
  "concentrationppm": 52.3,
  "ThresholdExceeded": 50.0,
  "InferenceResult": {
    "PredictedEvent": "Rapid H2S Leakage Detected",
    "Confidence": 0.965,
    "PatternSignatureMatched": "Single Sensor Dynamic Trajectory S3"
  },
  "ActionRequired": "Evacuate Personnel & Isolate Supply Valve V302"
}
```
