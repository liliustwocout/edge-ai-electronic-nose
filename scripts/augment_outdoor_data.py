#!/usr/bin/env python3
"""
scripts/augment_outdoor_data.py
Synthesizes outdoor field deployment pulses by superimposing pure laboratory gas response
signatures (ΔV) onto elevated outdoor baseline levels (0.35V - 0.70V).
"""
import os
import numpy as np
import pandas as pd

def generate_synthetic_outdoor_dataset(
    air_clean_path: str = 'data/air_clean_sensor_1_clean.csv',
    h2s_clean_path: str = 'data/h2s_sensor_1_clean.csv',
    nh3_clean_path: str = 'data/nh3_sensor_1_clean.csv',
    outdoor_air_path: str = 'data/air_outdoor_clean.csv',
    output_path: str = 'data/synthetic_outdoor_dataset_v2.csv',
    num_samples_per_gas: int = 60
):
    print("Loading cleaned laboratory datasets...")
    h2s_df = pd.read_csv(h2s_clean_path)
    nh3_df = pd.read_csv(nh3_clean_path)
    point_cols = [c for c in h2s_df.columns if c.startswith('Point_')]

    # Check if real recorded outdoor air exists, else generate high-fidelity empirical baseline profiles
    outdoor_baselines = []
    if os.path.exists(outdoor_air_path):
        print(f"Loading real recorded outdoor baselines from {outdoor_air_path}...")
        out_df = pd.read_csv(outdoor_air_path)
        out_cols = [c for c in out_df.columns if c.startswith('Point_')]
        for _, row in out_df.iterrows():
            outdoor_baselines.append(row[out_cols].values.astype(np.float32))

    # If fewer than 20 outdoor traces, generate realistic outdoor ambient traces
    np.random.seed(42)
    while len(outdoor_baselines) < 100:
        # Outdoor baseline centers between 0.35V and 0.70V
        base_center = np.random.uniform(0.35, 0.70)
        # Slow diurnal or thermal drift across 60 seconds (250 points)
        drift_slope = np.random.uniform(-0.02, 0.02)
        time_axis = np.linspace(0, 1, 250)
        drift = drift_slope * time_axis
        # Micro-fluctuations / sensor heater ripple / wind noise
        noise = np.random.normal(0, 0.0025, 250)
        baseline_profile = np.clip(base_center + drift + noise, 0.002, 1.20)
        outdoor_baselines.append(baseline_profile.astype(np.float32))

    synthetic_records = []

    # 1. Synthesize Outdoor Clean Air (Elevated Baseline but Flat)
    print(f"Synthesizing {num_samples_per_gas} Outdoor Clean Air pulses...")
    for idx in range(num_samples_per_gas):
        base_p = outdoor_baselines[idx % len(outdoor_baselines)].copy()
        # Add slight random fluctuation
        fluct = np.random.normal(0, 0.0015, 250)
        profile = np.clip(base_p + fluct, 0.002, 1.50)
        row_dict = {
            'Pulse_Index': f'Synth_Outdoor_Air_{idx+1}',
            'Gas': 'Clean Air',
            'ppm': 0.0,
            'is_outdoor_synthetic': 1
        }
        for pt_i in range(250):
            row_dict[f'Point_{pt_i}'] = round(float(profile[pt_i]), 5)
        synthetic_records.append(row_dict)

    # 2. Synthesize Outdoor H2S Pulses
    print(f"Synthesizing {num_samples_per_gas} Outdoor H2S pulses...")
    for idx in range(num_samples_per_gas):
        source_row = h2s_df.iloc[idx % len(h2s_df)]
        lab_points = source_row[point_cols].values.astype(np.float32)
        lab_base = float(lab_points[0])
        # Pure gas response trajectory above lab baseline
        delta_gas = np.maximum(0.0, lab_points - lab_base)

        # Pick an outdoor baseline
        base_p = outdoor_baselines[(idx + 25) % len(outdoor_baselines)].copy()
        # Thermal scaling factor (MOS sensitivity changes slightly with RH)
        alpha = np.random.uniform(0.92, 1.08)
        synth_points = np.clip(base_p + (alpha * delta_gas), 0.002, 3.30)

        # Parse concentration
        p_num = int(str(source_row['Pulse_Index']).replace('Pulse_', '').strip())
        ppm = 1.0 if p_num <= 37 else (5.0 if p_num <= 74 else 10.0)

        row_dict = {
            'Pulse_Index': f'Synth_Outdoor_H2S_{idx+1}',
            'Gas': 'H2S',
            'ppm': ppm,
            'is_outdoor_synthetic': 1
        }
        for pt_i in range(250):
            row_dict[f'Point_{pt_i}'] = round(float(synth_points[pt_i]), 5)
        synthetic_records.append(row_dict)

    # 3. Synthesize Outdoor NH3 Pulses
    print(f"Synthesizing {num_samples_per_gas} Outdoor NH3 pulses...")
    for idx in range(num_samples_per_gas):
        source_row = nh3_df.iloc[idx % len(nh3_df)]
        lab_points = source_row[point_cols].values.astype(np.float32)
        lab_base = float(lab_points[0])
        delta_gas = np.maximum(0.0, lab_points - lab_base)

        base_p = outdoor_baselines[(idx + 50) % len(outdoor_baselines)].copy()
        alpha = np.random.uniform(0.92, 1.08)
        synth_points = np.clip(base_p + (alpha * delta_gas), 0.002, 3.30)

        p_num = int(str(source_row['Pulse_Index']).replace('Pulse_', '').strip())
        ppm = 10.0 if p_num <= 42 else (50.0 if p_num <= 84 else 100.0)

        row_dict = {
            'Pulse_Index': f'Synth_Outdoor_NH3_{idx+1}',
            'Gas': 'NH3',
            'ppm': ppm,
            'is_outdoor_synthetic': 1
        }
        for pt_i in range(250):
            row_dict[f'Point_{pt_i}'] = round(float(synth_points[pt_i]), 5)
        synthetic_records.append(row_dict)

    synth_df = pd.DataFrame(synthetic_records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    synth_df.to_csv(output_path, index=False)
    print(f"Generated {len(synth_df)} synthetic pulses ({len(synthetic_records)//3} per gas class) -> Saved to {output_path}")
    return synth_df

if __name__ == '__main__':
    generate_synthetic_outdoor_dataset()
