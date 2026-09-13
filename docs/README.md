# Tài Liệu Kỹ Thuật Dự Án (Project Documentation Index)

> **Tên đề tài:** Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection in Natural Gas Processing Plants  
> **Đội ngũ phát triển:** TaskForce141 (Advantech AIoT InnoWorks)  
> **Cố vấn chuyên môn:** Dr. Nguyen Dac Cu  

---

## 📌 Danh Mục Tài Liệu Kỹ Thuật

Bộ tài liệu được xây dựng hoàn chỉnh và bám sát trực tiếp mô hình kiến trúc 5 tầng của dự án:

```
docs/
├── README.md                     # Tổng quan và mục lục tài liệu (File này)
├── dac-ta.md                     # Bản đặc tả dự án tổng quát (Project Overview & Timelines)
├── kien-truc-he-thong.md         # Chi tiết kiến trúc 5 tầng (5-Layer System Architecture)
├── phan-cung-e-nose.md           # Thiết kế phần cứng E-Nose Node, vỏ IP65 & khối nguồn
├── giao-thuc-truyen-thong.md     # Đặc tả truyền thông Modbus RTU (RS-485) & MQTT (WISE-IoT)
├── edge-ai-va-logic-canh-bao.md  # Quy trình tiền xử lý, mô hình Edge AI và logic 4 cấp cảnh báo
└── cloud-va-ung-dung.md          # Nền tảng WISE-IoT Cloud và giao diện Web Dashboard / Mobile App
```

---

## 🏗 Tóm Tắt 5 Tầng Kiến Trúc

| Tầng | Tên Tầng | Thiết Bị / Công Nghệ Chính | Vai Trò & Chức Năng |
|:---:|---|---|---|
| **5** | **Application Layer** | Web Dashboard, Mobile App, Alert System | Giao diện trực quan thời gian thực, quản lý cảnh báo và điều phối vận hành nhà máy. |
| **4** | **Cloud Platform Layer** | Advantech WISE-IoT Platform | Lưu trữ dữ liệu chuỗi thời gian, phân tích xu hướng, quản lý thiết bị và báo cáo. |
| **3** | **Edge AI Layer** | Raspberry Pi 5 (Edge Gateway + Edge AI) | Modbus Master polling, lọc nhiễu, suy luận mô hình TFLite, phân loại 4 mức rủi ro, cảnh báo tức thời. |
| **2** | **Communication Layer** | RS-485 Bus (Modbus RTU), Trở $120\,\Omega$ | Mạng truyền thông công nghiệp đa điểm dạng Daisy-chain, chống nhiễu, khoảng cách xa. |
| **1** | **Perception Layer** | ESP32, ZE03/MQ136, MQ135, DHT22, Hộp IP65, Pin 12V | Thu thập dữ liệu nồng độ $H_2S$, chữ ký ma trận khí, bù nhiệt/ẩm, đóng gói khung Modbus Slave. |

---

## 🚦 Phân Cấp 4 Mức Độ Cảnh Báo (Risk Levels)
- 🟢 **Normal (Bình thường):** Khí an toàn ($< 1.0$ ppm).
- 🟡 **Warning (Cảnh báo sớm):** Nồng độ tăng hoặc có dấu hiệu rò rỉ sớm ($1.0 - 9.9$ ppm).
- 🟠 **Hazardous (Nguy hại):** Vượt ngưỡng phơi nhiễm cho phép ($10.0 - 49.9$ ppm).
- 🔴 **Emergency (Khẩn cấp):** Nguy hiểm tính mạng ($\ge 50.0$ ppm), kích hoạt còi đèn và ngắt van khẩn cấp.
