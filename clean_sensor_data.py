import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

def remove_hardware_spike(pulse, spike_start=125, search_range=15):
    """
    Detect and remove hardware spike at ~point 125.
    The spike shoots up suddenly then decays back to the pre-spike level.
    We find where it returns to normal, then interpolate across the gap.
    """
    pre_spike_val = pulse[spike_start - 1]  # Point_124
    
    # Find where signal decays back to pre-spike level
    recovery_idx = spike_start + search_range  # default fallback
    for j in range(spike_start, min(spike_start + search_range, len(pulse))):
        if pulse[j] <= pre_spike_val:
            recovery_idx = j
            break
    
    # Add a small margin after recovery to ensure clean transition
    recovery_idx = min(recovery_idx + 2, len(pulse) - 1)
    
    # Use cubic spline interpolation across the spike region
    # Anchor points: a few points before spike + a few points after recovery
    anchor_before = max(0, spike_start - 5)
    anchor_after = min(len(pulse), recovery_idx + 5)
    
    x_good = list(range(anchor_before, spike_start)) + list(range(recovery_idx, anchor_after))
    y_good = [pulse[i] for i in x_good]
    
    x_fill = list(range(spike_start, recovery_idx))
    
    if len(x_good) >= 4 and len(x_fill) > 0:
        cs = CubicSpline(x_good, y_good)
        pulse_fixed = pulse.copy()
        pulse_fixed[spike_start:recovery_idx] = cs(x_fill)
        return pulse_fixed
    
    return pulse


def clean_sensor_dataset(input_path, gas_name, filter_window=9, polyorder=2):
    df = pd.read_csv(input_path)
    pulse_indices = df['Pulse_Index'].values
    points = df.filter(regex=r'^Point_').values  # shape: (N, 250)
    
    initial_pulses = len(points)
    
    # === Step 1: Remove outlier pulses (MAE vs median) ===
    median_profile = np.median(points, axis=0)
    maes = np.mean(np.abs(points - median_profile), axis=1)
    threshold = np.mean(maes) + 2.5 * np.std(maes)
    valid_mask = maes <= max(threshold, 0.08)
    
    # Also reject pulses with abnormally low min values
    min_vals = np.min(points, axis=1)
    valid_mask = valid_mask & (min_vals >= 0.35)
    
    cleaned_pulses = points[valid_mask]
    cleaned_pulse_indices = pulse_indices[valid_mask]
    dropped = pulse_indices[~valid_mask]
    
    print(f"[{gas_name}] Step 1 - Outlier removal: {initial_pulses} -> {len(cleaned_pulses)} pulses (dropped {list(dropped)})")
    
    # === Step 2: Remove hardware spike at ~point 125 ===
    despike_pulses = np.zeros_like(cleaned_pulses)
    for i in range(len(cleaned_pulses)):
        despike_pulses[i] = remove_hardware_spike(cleaned_pulses[i])
    
    print(f"[{gas_name}] Step 2 - Hardware spike removed (interpolated around point 125)")
    
    # === Step 3: Savitzky-Golay smoothing ===
    smoothed_pulses = np.zeros_like(despike_pulses)
    for i in range(len(despike_pulses)):
        smoothed_pulses[i] = savgol_filter(despike_pulses[i], window_length=filter_window, polyorder=polyorder)
    
    print(f"[{gas_name}] Step 3 - Noise smoothing applied (Savitzky-Golay, window={filter_window})")
    
    # Build output DataFrame
    cols = [col for col in df.columns if col.startswith('Point_')]
    clean_df = pd.DataFrame(smoothed_pulses, columns=cols)
    clean_df.insert(0, 'Pulse_Index', cleaned_pulse_indices)
    
    return clean_df, smoothed_pulses


# === Run cleaning pipeline ===
files = {
    'NH3': 'data/nh3_sensor_1.csv',
    'H2S': 'data/h2s_sensor_1.csv',
    'Air Clean': 'data/air_clean_sensor_1.csv'
}

cleaned_data = {}
raw_data = {}

for name, path in files.items():
    # Keep raw for comparison
    raw_df = pd.read_csv(path)
    raw_data[name] = raw_df.filter(regex=r'^Point_').values
    
    # Clean
    clean_df, smoothed = clean_sensor_dataset(path, name)
    out_path = path.replace('.csv', '_clean.csv')
    clean_df.to_csv(out_path, index=False)
    cleaned_data[name] = smoothed
    print(f"-> Saved: {out_path}")
    print()


# ==========================================================
# PLOT: Before vs After comparison (3 gases x 2 columns)
# ==========================================================
time_axis = np.linspace(0, 60, 250)
colors = {'NH3': '#1f77b4', 'H2S': '#d62728', 'Air Clean': '#2ca02c'}

fig, axes = plt.subplots(3, 2, figsize=(16, 12))

for row_idx, (gas_name, raw_pulses) in enumerate(raw_data.items()):
    col = colors[gas_name]
    clean_pulses = cleaned_data[gas_name]
    
    # Left: Raw (before)
    ax_raw = axes[row_idx, 0]
    for i in range(raw_pulses.shape[0]):
        ax_raw.plot(time_axis, raw_pulses[i], color=col, alpha=0.2, linewidth=0.7)
    ax_raw.plot(time_axis, np.mean(raw_pulses, axis=0), color='black', linewidth=2, linestyle='--', label='Mean')
    ax_raw.axvline(x=30, color='red', linewidth=1, linestyle=':', alpha=0.7, label='Spike region')
    ax_raw.set_title(f"{gas_name} - BEFORE (Raw: {raw_pulses.shape[0]} pulses)", fontsize=12, fontweight='bold')
    ax_raw.set_ylabel("Voltage (V)", fontsize=10)
    ax_raw.grid(True, linestyle=':', alpha=0.5)
    ax_raw.legend(loc='upper right', fontsize=8)
    
    # Right: Cleaned (after)
    ax_clean = axes[row_idx, 1]
    for i in range(clean_pulses.shape[0]):
        ax_clean.plot(time_axis, clean_pulses[i], color=col, alpha=0.25, linewidth=0.8)
    ax_clean.plot(time_axis, np.mean(clean_pulses, axis=0), color='black', linewidth=2, linestyle='--', label='Mean')
    ax_clean.set_title(f"{gas_name} - AFTER (Cleaned: {clean_pulses.shape[0]} pulses)", fontsize=12, fontweight='bold')
    ax_clean.grid(True, linestyle=':', alpha=0.5)
    ax_clean.legend(loc='upper right', fontsize=8)
    
    if row_idx == 2:
        ax_raw.set_xlabel("Time (seconds)", fontsize=10)
        ax_clean.set_xlabel("Time (seconds)", fontsize=10)

plt.suptitle("Sensor 1 Data Cleaning: Before vs After\n(Outlier removal + Spike fix + Noise smoothing)", fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig("data/sensor1_before_after_cleaning.png", dpi=300)
print("Saved: data/sensor1_before_after_cleaning.png")
plt.close()

# ==========================================================
# PLOT: Clean comparison of 3 gases
# ==========================================================
plt.figure(figsize=(12, 6))

for gas_name, pulses in cleaned_data.items():
    col = colors[gas_name]
    mean_curve = np.mean(pulses, axis=0)
    std_curve = np.std(pulses, axis=0)
    plt.plot(time_axis, mean_curve, label=f"{gas_name} (Mean)", color=col, linewidth=2.5)
    plt.fill_between(time_axis, mean_curve - std_curve, mean_curve + std_curve, color=col, alpha=0.18)

plt.title("Sensor 1 Clean Response: NH3 vs H2S vs Air Clean (Spike Removed)", fontsize=14, fontweight='bold')
plt.xlabel("Time (seconds)", fontsize=12)
plt.ylabel("Sensor Voltage (V)", fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=11, loc='upper right')
plt.tight_layout()
plt.savefig("data/sensor1_clean_comparison.png", dpi=300)
print("Saved: data/sensor1_clean_comparison.png")
plt.close()
