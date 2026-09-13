# Tài Liệu Nền Tảng Đám Mây WISE-IoT & Giao Diện Ứng Dụng

> **Dự án:** Edge AI-Based Electronic Nose for Hydrogen Sulfide Leak Detection  
> **Tầng:** Cloud Platform Layer (Layer 4) & Application Layer (Layer 5)

---

## 1. Tầng Nền Tảng Đám Mây: Advantech WISE-IoT Platform

### 1.1 Vai trò
Nền tảng WISE-IoT đóng vai trò trung tâm trong việc quản lý toàn bộ hệ sinh thái giám sát an toàn nhà máy khí:
- **Lưu trữ dữ liệu (Data Storage):** Lưu trữ dữ liệu thời gian thực (real-time stream) và dữ liệu lịch sử lâu dài phục vụ hậu kiểm.
- **Phân tích & Trực quan hóa (Analytics & Visualization):** Biểu đồ hóa diễn biến nồng độ khí $H_2S$, so sánh giữa các Node theo sơ đồ mặt bằng thực tế.
- **Quản lý cảnh báo (Alarm Management):** Định tuyến thông báo khẩn cấp đến đúng đối tượng theo ca trực và khu vực quản lý.
- **Quản lý thiết bị (Device Management):** Giám sát trạng thái hoạt động (Online/Offline, Uptime, CPU Load, Nhiệt độ RPi5).
- **Báo cáo & Xuất dữ liệu (Reports & Export):** Tự động lập báo cáo tuân thủ an toàn môi trường theo ngày/tuần/tháng (định dạng PDF/Excel).

---

## 2. Tầng Ứng Dụng: User Access & Visualization

### 2.1 Web Dashboard (Bảng điều khiển trung tâm)
- **Mặt bằng bố trí thiết bị (Digital Map / P&ID Layout):** Hiển thị vị trí thực tế của từng Node 1..N trên bản đồ phân khu nhà máy với mã màu trực quan tương ứng với 4 cấp độ rủi ro (Xanh, Vàng, Cam, Đỏ).
- **Đồng hồ đo & Biểu đồ xu hướng (Gauges & Trends):**
  - Biểu đồ nồng độ $H_2S$ (ppm) theo thời gian thực.
  - Tỷ lệ nhận dạng mẫu khí từ mô hình AI.
  - Ma trận hiển thị trạng thái từng cảm biến thành phần (MQ136, MQ135, Temp, Humidity).
- **Bảng theo dõi sự kiện (Event Log Table):** Liệt kê lịch sử các lần kích hoạt cảnh báo, thời gian phản hồi và xác nhận của nhân viên trực.

### 2.2 Ứng Dụng Di Động (Mobile App)
- Dành cho kỹ sư an toàn và kỹ thuật viên tuần tra hiện trường.
- Nhận thông báo đẩy (Push Notification) tức thì kèm tọa độ vị trí khi có rò rỉ.
- Xem nhanh tình trạng các Node xung quanh khu vực đang tuần tra.

### 2.3 Cơ Chế Cảnh Báo & Thông Báo Đa Kênh (Alerts & Notifications)
1. **Thông báo qua Ứng dụng & Web:** Popup âm thanh và hình ảnh chớp nháy trên màn hình trung tâm điều hành.
2. **Tin nhắn SMS / Cuộc gọi khẩn cấp (Emergency Call):** Tự động gửi tới số điện thoại trưởng ca an toàn khi chạm mức `Emergency`.
3. **Email Báo cáo sự cố:** Tự động gửi đính kèm biểu đồ diễn biến nồng độ trước và sau thời điểm xảy ra sự cố.

### 2.4 Người Vận Hành (Operator Role & Workflow)
- **Bước 1 - Tiếp nhận cảnh báo:** Quan sát mức độ rủi ro hiển thị trên Dashboard hoặc qua Notification.
- **Bước 2 - Xác định vị trí:** Kiểm tra vị trí Node cảnh báo trên bản đồ nhà máy (ví dụ: Trạm nén khí số 3).
- **Bước 3 - Triển khai ứng phó:** Kích hoạt hệ thống cô lập van đường ống từ xa hoặc cử đội xử lý sự cố mang đồ bảo hộ chuyên dụng tới hiện trường.
- **Bước 4 - Xác nhận sự cố:** Nhấn nút "Acknowledge" trên Dashboard để ghi nhận thời gian và người đã xử lý vào hệ thống lưu trữ.
