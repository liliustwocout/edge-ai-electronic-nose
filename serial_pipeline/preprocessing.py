"""
serial_pipeline/preprocessing.py
Signal Preprocessing Module for Electronic Nose RS-485 Sensor Stream:
- Exponential Moving Average (EMA) Filter for noise suppression.
- Despike / Median filter for outlier suppression.
- Baseline subtraction / drift compensation.
"""
import numpy as np
from typing import List, Union

class SignalPreprocessor:
    def __init__(self, ema_alpha: float = 0.35, despike_threshold: float = 0.08):
        self.ema_alpha = ema_alpha
        self.despike_threshold = despike_threshold
        self._last_ema: Optional[float] = None

    def apply_ema(self, value: float) -> float:
        """Applies single-point Exponential Moving Average filter."""
        if self._last_ema is None:
            self._last_ema = value
            return value
        self._last_ema = (self.ema_alpha * value) + ((1.0 - self.ema_alpha) * self._last_ema)
        return float(self._last_ema)

    @staticmethod
    def despike_window(window: Union[List[float], np.ndarray], max_diff: float = 0.08) -> np.ndarray:
        """
        Replaces sudden single-point spikes with the local neighborhood median.
        """
        arr = np.array(window, dtype=np.float32).copy()
        n = len(arr)
        if n < 3:
            return arr

        for i in range(1, n - 1):
            median_neighbors = 0.5 * (arr[i - 1] + arr[i + 1])
            if abs(arr[i] - median_neighbors) > max_diff:
                arr[i] = median_neighbors
        return arr

    @staticmethod
    def remove_baseline(window: Union[List[float], np.ndarray], base_v: float) -> np.ndarray:
        """Converts raw voltage to delta voltage relative to baseline (ΔV)."""
        return np.array(window, dtype=np.float32) - float(base_v)
