import time
import numpy as np
from typing import List, Optional, Dict, Any

class BaselineTracker:
    """
    Adaptive Baseline Tracker for MOS Gas Sensors (e.g. MQ136, MQ135).
    Addresses environmental background matrix drift, humidity/temperature shifts,
    and supports rapid Zero Calibration on outdoor deployment.
    """
    def __init__(
        self,
        warmup_points: int = 30,
        slow_alpha: float = 0.002,
        drift_guard_threshold: float = 0.06,
        slope_guard_threshold: float = 0.004
    ):
        self.warmup_points = warmup_points
        self.slow_alpha = slow_alpha
        self.drift_guard_threshold = drift_guard_threshold
        self.slope_guard_threshold = slope_guard_threshold

        self.warmup_buffer: List[float] = []
        self.v0: float = 0.0
        self.is_calibrated: bool = False
        self.state: str = "WARMING_UP"  # WARMING_UP, CALIBRATED, TRACKING, LOCKED_EVENT
        self.last_update_ts: float = time.time()
        self.samples_count: int = 0
        self.manual_override: bool = False

    def update(self, val: float, is_gas_detected: bool = False, slope: float = 0.0) -> float:
        """
        Feed a new sensor reading into the baseline tracker.
        Returns the current estimated baseline voltage V0.
        """
        self.samples_count += 1
        now = time.time()

        # Phase 1: Sensor warm-up / initialization
        if not self.is_calibrated and len(self.warmup_buffer) < self.warmup_points:
            self.warmup_buffer.append(float(val))
            self.v0 = float(np.median(self.warmup_buffer))
            if len(self.warmup_buffer) >= self.warmup_points:
                self.is_calibrated = True
                self.state = "TRACKING"
            else:
                self.state = "WARMING_UP"
            self.last_update_ts = now
            return self.v0

        # Phase 2: If manual calibration was performed, maintain calibrated state
        if not self.is_calibrated and len(self.warmup_buffer) >= self.warmup_points:
            self.is_calibrated = True
            self.state = "TRACKING"

        # Phase 3: Adaptive Slow Drift Tracking vs Gas Event Locking
        delta = abs(val - self.v0)
        abs_slope = abs(slope)

        # Freeze/lock baseline update if gas is detected, sudden jump occurs, or slope is steep
        if is_gas_detected or delta > self.drift_guard_threshold or abs_slope > self.slope_guard_threshold:
            self.state = "LOCKED_EVENT"
        else:
            # Baseline is flat and in clean ambient air: adapt slowly to diurnal thermal/RH drift
            self.v0 = (1.0 - self.slow_alpha) * self.v0 + (self.slow_alpha * float(val))
            self.state = "TRACKING"

        self.last_update_ts = now
        return self.v0

    def recalibrate(self, recent_samples: Optional[List[float]] = None, target_val: Optional[float] = None) -> float:
        """
        Manually trigger Zero Calibration (e.g. when field engineer presses 'Zero Calibrate' outdoors).
        """
        if target_val is not None:
            self.v0 = float(target_val)
        elif recent_samples and len(recent_samples) > 0:
            self.v0 = float(np.median(recent_samples))
        elif len(self.warmup_buffer) > 0:
            self.v0 = float(np.median(self.warmup_buffer[-10:]))
        
        self.is_calibrated = True
        self.state = "CALIBRATED"
        self.manual_override = True
        self.last_update_ts = time.time()
        return self.v0

    def get_delta(self, val: float) -> float:
        """
        Compute relative differential voltage: ΔV = V(t) - V0
        """
        return float(val - self.v0)

    def is_flat_baseline(self, window_vals: List[float], max_std: float = 0.015, max_slope: float = 0.004) -> bool:
        """
        Kinematic check: returns True if signal is flat and stable (indicative of Ambient Air).
        """
        if not window_vals or len(window_vals) < 5:
            return False
        w = np.array(window_vals, dtype=np.float32)
        std_val = float(np.std(w))
        delta_val = float(w[-1] - w[0])
        slope_val = float(abs(delta_val) / max(len(w), 1))
        delta_to_baseline = abs(float(w[-1]) - self.v0)

        return (
            std_val <= max_std and
            slope_val <= max_slope and
            delta_to_baseline <= (self.drift_guard_threshold * 1.5)
        )

    def get_status(self) -> Dict[str, Any]:
        return {
            'v0': round(float(self.v0), 4),
            'state': self.state,
            'isCalibrated': self.is_calibrated,
            'samplesCount': self.samples_count,
            'warmupProgress': min(100, int((len(self.warmup_buffer) / max(self.warmup_points, 1)) * 100)),
            'lastUpdateTs': self.last_update_ts
        }
