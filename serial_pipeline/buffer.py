"""
serial_pipeline/buffer.py
Data Buffer & WaveCycle Assembler:
- Maintains rolling window (e.g. 20 points) for instant Edge AI inference.
- Reconstructs complete 250-point WaveCycle for 60-second pulse inference.
- Tracks packet continuity, detected gaps, and drop rates.
- Performs linear interpolation for minor missing points in cycles.
- Strictly bounded memory structures (collections.deque, preallocated arrays) to prevent memory leaks 24/7.
"""
import time
import numpy as np
from collections import deque
from typing import Optional, List, Dict, Callable
from .parser import PointSample

class PointBuffer:
    def __init__(self, cycle_length: int = 250, window_length: int = 20):
        self.cycle_length = cycle_length
        self.window_length = window_length

        # Rolling window for real-time 4.8s inference
        self._rolling_window = deque(maxlen=window_length)
        # Recent points history for visualization/debugging (capped at 1000)
        self._history = deque(maxlen=1000)

        # Full cycle assembly buffer
        self._current_cycle = [None] * cycle_length
        self._cycle_timestamps = [None] * cycle_length
        self._cycle_id: int = 0
        self._points_in_current_cycle: int = 0

        # Continuity and drop monitoring
        self._last_point: Optional[int] = None
        self._total_received: int = 0
        self._total_gaps: int = 0
        self._total_dropped_points: int = 0

        # Callbacks (optional hook for AI or UI handlers)
        self.on_new_sample: Optional[Callable[[PointSample], None]] = None
        self.on_window_ready: Optional[Callable[[List[float]], None]] = None
        self.on_cycle_complete: Optional[Callable[[int, np.ndarray, Dict], None]] = None

    def push(self, sample: PointSample):
        """
        Pushes a new parsed PointSample into the buffer.
        """
        pt = sample.point
        v = sample.voltage1
        ts = sample.timestamp

        self._total_received += 1
        self._rolling_window.append(v)
        self._history.append((pt, v, ts))

        # Check point continuity
        if self._last_point is not None:
            expected = (self._last_point + 1) % self.cycle_length
            if pt != expected:
                diff = (pt - expected) % self.cycle_length
                self._total_gaps += 1
                self._total_dropped_points += diff

            # Detect cycle wrap-around (e.g. from end of cycle back to beginning)
            if (self._last_point >= self.cycle_length - 20 and pt < 20) or (pt == 0 and self._last_point > 0):
                self._finalize_cycle()

        # Update slot in current cycle
        if 0 <= pt < self.cycle_length:
            self._current_cycle[pt] = v
            self._cycle_timestamps[pt] = ts
            self._points_in_current_cycle += 1

        self._last_point = pt

        # Trigger sample callback
        if self.on_new_sample:
            self.on_new_sample(sample)

        # Trigger window callback when full window of 20 points is available
        if len(self._rolling_window) == self.window_length:
            if self.on_window_ready:
                self.on_window_ready(list(self._rolling_window))

    def _finalize_cycle(self):
        """
        Finalizes the 250-point cycle, interpolates any small gaps, and emits event.
        """
        self._cycle_id += 1
        filled_count = sum(1 for x in self._current_cycle if x is not None)

        # If we have at least 70% of points, reconstruct the full 250-point array
        if filled_count >= int(self.cycle_length * 0.70):
            arr = np.array([x if x is not None else np.nan for x in self._current_cycle], dtype=np.float32)
            # Linear interpolation for any missing points
            nans = np.isnan(arr)
            if np.any(nans):
                x_valid = np.where(~nans)[0]
                y_valid = arr[~nans]
                x_nans = np.where(nans)[0]
                arr[x_nans] = np.interp(x_nans, x_valid, y_valid)

            metrics = {
                'cycle_id': self._cycle_id,
                'filled_points': filled_count,
                'total_points': self.cycle_length,
                'completeness_pct': round((filled_count / self.cycle_length) * 100.0, 1),
                'max_v': round(float(np.max(arr)), 4),
                'min_v': round(float(np.min(arr)), 4),
                'delta_v': round(float(np.max(arr) - np.min(arr)), 4)
            }

            if self.on_cycle_complete:
                self.on_cycle_complete(self._cycle_id, arr, metrics)

        # Reset buffer for next cycle
        self._current_cycle = [None] * self.cycle_length
        self._cycle_timestamps = [None] * self.cycle_length
        self._points_in_current_cycle = 0

    def get_current_window(self) -> List[float]:
        """Returns the current 20-point rolling window."""
        return list(self._rolling_window)

    def get_stats(self) -> Dict:
        """Returns buffer health and packet loss statistics."""
        total_exp = self._total_received + self._total_dropped_points
        loss_rate = (self._total_dropped_points / total_exp * 100.0) if total_exp > 0 else 0.0
        return {
            'total_received': self._total_received,
            'total_dropped_points': self._total_dropped_points,
            'total_gaps': self._total_gaps,
            'packet_loss_rate_pct': round(loss_rate, 2),
            'cycle_id': self._cycle_id,
            'last_point': self._last_point,
            'rolling_window_len': len(self._rolling_window)
        }

    def reset_stats(self):
        self._total_received = 0
        self._total_gaps = 0
        self._total_dropped_points = 0
