#!/usr/bin/env python3
"""
scripts/record_outdoor_air.py
Utility to record outdoor ambient air cycles directly from Firebase RTDB or local WebSocket.
Saves 250-point pulses (60s cycles) to data/air_outdoor_clean.csv.
"""
import os
import sys
import time
import json
import argparse
import numpy as np
import pandas as pd
import urllib.request
import urllib.error

DEFAULT_RTDB_URL = 'https://enose-1aeb7-default-rtdb.asia-southeast1.firebasedatabase.app/sensor/latest.json?auth=qbtMtFdVKPlt5kBvQoD7ELUITrqs1qoPPuNmgQ0y'

def record_from_firebase(rtdb_url: str, target_pulses: int = 50, output_path: str = 'data/air_outdoor_clean.csv'):
    print(f"Connecting to Firebase RTDB: {rtdb_url[:55]}...")
    print(f"Target: {target_pulses} pulses (250 points each). Output: {output_path}")

    current_pulse = []
    pulse_records = []
    last_point_idx = -1
    pulse_count = 0

    while pulse_count < target_pulses:
        try:
            req = urllib.request.Request(rtdb_url, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                if resp.getcode() == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    pt = int(data.get('point', 0))
                    v1 = float(data.get('voltage1', 0.0))

                    # Detect new pulse start (wrap-around from high point to low point)
                    if last_point_idx >= 220 and pt < 30:
                        if len(current_pulse) >= 200:
                            # Interpolate or pad to exactly 250 points
                            if len(current_pulse) < 250:
                                current_pulse.extend([current_pulse[-1]] * (250 - len(current_pulse)))
                            pulse_count += 1
                            pulse_records.append({
                                'Pulse_Index': f'Pulse_Outdoor_{pulse_count}',
                                **{f'Point_{i}': round(float(current_pulse[i]), 5) for i in range(250)}
                            })
                            print(f"[Captured Pulse {pulse_count}/{target_pulses}] Baseline Mean: {np.mean(current_pulse):.4f}V, Min: {np.min(current_pulse):.4f}V, Max: {np.max(current_pulse):.4f}V")

                        current_pulse = []

                    last_point_idx = pt
                    current_pulse.append(v1)
                    time.sleep(0.2)
        except Exception as e:
            print(f"Error fetching telemetry: {e}")
            time.sleep(1.0)

    df = pd.DataFrame(pulse_records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Successfully recorded {len(df)} outdoor ambient air pulses to {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Record outdoor ambient air pulses")
    parser.add_argument('--pulses', type=int, default=50, help="Number of 250-point pulses to record")
    parser.add_argument('--url', type=str, default=DEFAULT_RTDB_URL, help="Firebase RTDB URL")
    parser.add_argument('--out', type=str, default='data/air_outdoor_clean.csv', help="Output CSV file path")
    args = parser.parse_args()

    record_from_firebase(args.url, args.pulses, args.out)
