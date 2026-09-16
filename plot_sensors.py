import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Đọc dữ liệu từ 3 file CSV
files = {
    'NH3': 'data/nh3_sensor_1.csv',
    'H2S': 'data/h2s_sensor_1.csv',
    'Air Clean': 'data/air_clean_sensor_1.csv'
}

data_dict = {}
for name, path in files.items():
    df = pd.read_csv(path)
    # Lấy các cột Point_0 đến Point_249 (bỏ cột Pulse_Index)
    features = df.filter(regex=r'^Point_').values
    data_dict[name] = features
    print(f"[{name}] Read {features.shape[0]} pulses, each with {features.shape[1]} points.")

# Trục thời gian: 250 mẫu trong 60 giây (từ 0 đến 60s)
time_axis = np.linspace(0, 60, 250)

# Cấu hình màu sắc
colors = {
    'NH3': '#1f77b4',       # Xanh dương
    'H2S': '#d62728',       # Đỏ
    'Air Clean': '#2ca02c'  # Xanh lá
}

# ==========================================================
# HÌNH 1: 3 Subplots - Hiển thị toàn bộ các Pulse của từng loại khí
# ==========================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

for ax, (gas_name, pulses) in zip(axes, data_dict.items()):
    col = colors[gas_name]
    # Vẽ từng pulse đơn lẻ với độ mờ (alpha)
    for i in range(pulses.shape[0]):
        ax.plot(time_axis, pulses[i], color=col, alpha=0.25, linewidth=0.8)
    
    # Vẽ đường trung bình (Mean) đậm nét
    mean_pulse = np.mean(pulses, axis=0)
    ax.plot(time_axis, mean_pulse, color='black', linewidth=2.2, linestyle='--', label='Đường trung bình (Mean)')
    
    ax.set_title(f"Khí: {gas_name} ({pulses.shape[0]} pulses)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Thời gian (giây)", fontsize=11)
    ax.set_ylabel("Điện áp / Tín hiệu Cảm biến (V)" if ax == axes[0] else "", fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right')

plt.suptitle("Đặc tính đáp ứng cảm biến Sensor 1 cho từng loại khí (Chu kỳ 60 giây)", fontsize=15, fontweight='bold')
plt.tight_layout()
output_all = "data/sensor1_all_pulses_plot.png"
plt.savefig(output_all, dpi=300)
print(f"Saved: {output_all}")
plt.close()

# ==========================================================
# HINH 2: So sanh gia tri trung binh giua 3 loai khi
# ==========================================================
plt.figure(figsize=(12, 6))

for gas_name, pulses in data_dict.items():
    col = colors[gas_name]
    mean_curve = np.mean(pulses, axis=0)
    std_curve = np.std(pulses, axis=0)
    
    # Duong trung binh
    plt.plot(time_axis, mean_curve, label=f"{gas_name} (Mean)", color=col, linewidth=2.5)
    # Vung dao dong do lech chuan (+/- 1 Std)
    plt.fill_between(time_axis, mean_curve - std_curve, mean_curve + std_curve, color=col, alpha=0.18)

plt.title("Sensor 1 Response Comparison: NH3 vs H2S vs Air Clean (60s Cycle)", fontsize=14, fontweight='bold')
plt.xlabel("Time (seconds)", fontsize=12)
plt.ylabel("Sensor Voltage / Signal (V)", fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=11, loc='upper right')
plt.tight_layout()

output_compare = "data/sensor1_comparison_plot.png"
plt.savefig(output_compare, dpi=300)
print(f"Saved: {output_compare}")
plt.close()
