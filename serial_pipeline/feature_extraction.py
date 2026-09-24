"""
serial_pipeline/feature_extraction.py
Feature Extraction Module for Edge AI Inference.
Lightweight pure-numpy implementation for low latency and zero memory overhead on Raspberry Pi 3.
"""
from typing import List, Union
import numpy as np

def extract_window_features(w: Union[List[float], np.ndarray], base_v: float = None) -> List[float]:
    """
    Extract shift-invariant window features relative to dynamic baseline (ΔV).
    Raw points are converted to Δw = w - b to prevent static voltage domain shift.
    """
    w = np.array(w, dtype=np.float32)
    n = len(w)
    b = float(base_v) if base_v is not None else float(w[0])
    w_diff = w - b

    mean_diff = float(np.mean(w_diff))
    std_val = float(np.std(w))
    max_diff = float(np.max(w_diff))
    min_diff = float(np.min(w_diff))
    rng_val = float(np.max(w) - np.min(w))
    delta_val = float(w[-1] - w[0])
    slope_val = float(delta_val / max(n, 1))
    diffs = np.diff(w)
    diff_mean = float(np.mean(diffs)) if len(diffs) > 0 else 0.0
    diff_std = float(np.std(diffs)) if len(diffs) > 0 else 0.0
    q_diff = float(np.percentile(w_diff, 75) - np.percentile(w_diff, 25))
    ratio = float(max_diff / max(b, 0.05))

    features = [mean_diff, std_val, max_diff, min_diff, rng_val, delta_val, slope_val, diff_mean, diff_std, q_diff, max_diff, ratio]
    features.extend([float(v) for v in w_diff])
    return features

def extract_pulse_features(p: Union[List[float], np.ndarray], base_v: float = None) -> List[float]:
    """
    Extract shift-invariant pulse features relative to dynamic baseline (ΔV).
    Ensures complete robustness to elevated outdoor baselines.
    """
    p = np.array(p, dtype=np.float32)
    b = float(base_v) if base_v is not None else float(np.median(p[:10]))
    p_diff = p - b

    delta_v = float(np.max(p) - np.min(p))
    auc_diff = float(np.sum(np.maximum(0.0, p_diff)))
    mean_diff = float(np.mean(p_diff))
    std_v = float(np.std(p))
    peak_idx = int(np.argmax(p))
    rise_slope = float((np.max(p) - p[0]) / max(peak_idx, 1))
    decay_slope = float((p[-1] - np.max(p)) / max(len(p) - peak_idx, 1))
    rel_peak = float(np.max(p) - b)
    rel_ratio = float(rel_peak / max(b, 0.05))

    anchors_idx = [15, 30, 50, 75, 100, 120, 140, 170, 200, 230]
    anchors_diff = [float(p[idx] - b) for idx in anchors_idx]

    return [delta_v, auc_diff, mean_diff, std_v, float(peak_idx), rise_slope, decay_slope, rel_peak, rel_ratio] + anchors_diff
