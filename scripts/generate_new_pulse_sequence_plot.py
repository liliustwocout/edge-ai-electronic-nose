import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def generate_pulse_sequence_chart():
    # Load cleaned data
    df_nh3 = pd.read_csv('data/nh3_sensor_1_clean.csv')
    df_h2s = pd.read_csv('data/h2s_sensor_1_clean.csv')
    df_air = pd.read_csv('data/air_clean_sensor_1_clean.csv')

    # 133 laboratory clean air pulses for standard 361 pulse validation set
    if len(df_air) > 133:
        df_air_lab = df_air.iloc[:133]
    else:
        df_air_lab = df_air

    pts_nh3 = df_nh3.filter(regex=r'^Point_').values.flatten()
    pts_h2s = df_h2s.filter(regex=r'^Point_').values.flatten()
    pts_air = df_air_lab.filter(regex=r'^Point_').values.flatten()

    n_nh3 = len(df_nh3)
    n_h2s = len(df_h2s)
    n_air = len(df_air_lab)

    print(f"Plotting Continuous Sequences: NH3={n_nh3} pulses, H2S={n_h2s} pulses, Clean Air={n_air} pulses (Total: {n_nh3 + n_h2s + n_air} pulses)")

    # Color Palette matching industrial Advantech theme
    c_nh3 = '#0284c7'  # Tech blue
    c_h2s = '#dc2626'  # Danger red
    c_air = '#059669'  # Emerald green

    # Configure High-Resolution Figure (18x10.5 @ 300dpi = 5400x3150)
    fig, axes = plt.subplots(3, 1, figsize=(18, 10.5), sharey=False, dpi=300)
    plt.subplots_adjust(hspace=0.28, top=0.93, bottom=0.06, left=0.055, right=0.985)

    fig.suptitle("Sensor 1 Continuous Pulse Sequence (Marked At Start Of Each Concentration Range)", 
                 fontsize=16, fontweight='bold', y=0.97)

    # -------------------------------------------------------------
    # 1. NH3 SUBPLOT
    # -------------------------------------------------------------
    ax1 = axes[0]
    x_nh3 = np.arange(len(pts_nh3))
    ax1.plot(x_nh3, pts_nh3, color=c_nh3, linewidth=1.15, label='S1 (MQ136)')
    ax1.set_xlim(0, len(pts_nh3))
    ax1.set_ylim(0, 1.30)
    ax1.set_ylabel("Sensor 1 Voltage (V)", fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6, color='#94a3b8')
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(2500))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(500))

    # Badge Title in top left
    ax1.text(0.015, 0.90, f"● S1  @NH₃ ({n_nh3} Continuous Pulses)", transform=ax1.transAxes, 
             fontsize=12, fontweight='bold', color=c_nh3,
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0f9ff', edgecolor='#bae6fd', alpha=0.95))

    # Concentration annotations for NH3
    nh3_marks = [
        (50, 0.52, "Start: 10 ppm", 200, 0.76),
        (9500, 0.94, "Start: 50 ppm", 9600, 1.14),
        (20000, 1.02, "Start: 100 ppm", 20100, 1.18)
    ]
    for idx, (x_pos, y_target, text, tx_pos, ty_pos) in enumerate(nh3_marks):
        if idx > 0:
            ax1.axvline(x=x_pos, color='#64748b', linestyle='--', linewidth=1.2, alpha=0.85)
        ax1.annotate(text, xy=(x_pos, y_target), xytext=(tx_pos, ty_pos),
                     arrowprops=dict(facecolor='black', edgecolor='black', width=1.4, headwidth=5.5, headlength=6, shrink=0.08),
                     fontsize=10, fontweight='bold')

    # -------------------------------------------------------------
    # 2. H2S SUBPLOT
    # -------------------------------------------------------------
    ax2 = axes[1]
    x_h2s = np.arange(len(pts_h2s))
    ax2.plot(x_h2s, pts_h2s, color=c_h2s, linewidth=1.15, label='S1 (MQ136)')
    ax2.set_xlim(0, len(pts_h2s))
    ax2.set_ylim(0, 1.15)
    ax2.set_ylabel("Sensor 1 Voltage (V)", fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6, color='#94a3b8')
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(2500))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(500))

    # Badge Title in top left
    ax2.text(0.015, 0.90, f"● S1  @H₂S ({n_h2s} Continuous Pulses)", transform=ax2.transAxes, 
             fontsize=12, fontweight='bold', color=c_h2s,
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#fef2f2', edgecolor='#fecaca', alpha=0.95))

    # Concentration annotations for H2S
    h2s_marks = [
        (50, 0.35, "Start: 1 ppm", 200, 0.52),
        (5000, 0.55, "Start: 5 ppm", 5150, 0.72),
        (13750, 0.74, "Start: 10 ppm", 13900, 0.94),
        (22000, 0.84, "Start: 25 ppm", 22150, 1.02)
    ]
    for idx, (x_pos, y_target, text, tx_pos, ty_pos) in enumerate(h2s_marks):
        if idx > 0:
            ax2.axvline(x=x_pos, color='#64748b', linestyle='--', linewidth=1.2, alpha=0.85)
        ax2.annotate(text, xy=(x_pos, y_target), xytext=(tx_pos, ty_pos),
                     arrowprops=dict(facecolor='black', edgecolor='black', width=1.4, headwidth=5.5, headlength=6, shrink=0.08),
                     fontsize=10, fontweight='bold')

    # -------------------------------------------------------------
    # 3. CLEAN AIR SUBPLOT
    # -------------------------------------------------------------
    ax3 = axes[2]
    x_air = np.arange(len(pts_air))
    ax3.plot(x_air, pts_air, color=c_air, linewidth=1.15, label='S1 (MQ136)')
    ax3.set_xlim(0, len(pts_air))
    ax3.set_ylim(0, 0.65)
    ax3.set_xlabel("Sample Points (250 points / 60s pulse)", fontsize=11, fontweight='bold')
    ax3.set_ylabel("Sensor 1 Voltage (V)", fontsize=11, fontweight='bold')
    ax3.grid(True, linestyle=':', alpha=0.6, color='#94a3b8')
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(2500))
    ax3.xaxis.set_minor_locator(ticker.MultipleLocator(500))

    # Badge Title in top left
    ax3.text(0.015, 0.90, f"● S1  @Clean Air ({n_air} Continuous Pulses)", transform=ax3.transAxes, 
             fontsize=12, fontweight='bold', color=c_air,
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#ecfdf5', edgecolor='#a7f3d0', alpha=0.95))

    # Clean air annotation
    ax3.annotate("Start: 0 ppm (Clean Air Baseline)", xy=(50, 0.44), xytext=(200, 0.54),
                 arrowprops=dict(facecolor='black', edgecolor='black', width=1.4, headwidth=5.5, headlength=6, shrink=0.08),
                 fontsize=10, fontweight='bold')

    # Save to standee/image3_new.png and copy to standee/image3.png
    output_path = "standee/image3_new.png"
    plt.savefig(output_path, dpi=300, facecolor='white')
    plt.close()
    
    # Overwrite standee/image3.png with the new validated plot
    import shutil
    shutil.copyfile(output_path, "standee/image3.png")
    print(f"Successfully generated new pulse sequence chart and updated standee/image3.png: {output_path}")

if __name__ == "__main__":
    generate_pulse_sequence_chart()
