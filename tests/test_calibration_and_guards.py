import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import unittest
import numpy as np
from backend.calibration import BaselineTracker
from backend.train import extract_window_features, extract_pulse_features
from backend.gateway import computeRiskLevel, EdgeAIGateway
from backend.app import runInference, runPulseInference, app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestCalibrationAndGuards(unittest.TestCase):
    def test_baseline_tracker_warmup_and_recalibrate(self):
        tracker = BaselineTracker(warmup_points=10)
        self.assertEqual(tracker.state, "WARMING_UP")

        # Feed 10 warmup points around 0.55V
        for i in range(10):
            v0 = tracker.update(0.55 + 0.001 * i, is_gas_detected=False, slope=0.0001)

        self.assertTrue(tracker.is_calibrated)
        self.assertEqual(tracker.state, "TRACKING")
        self.assertTrue(0.54 <= v0 <= 0.56)

        # Test manual recalibrate
        new_v0 = tracker.recalibrate(target_val=0.62)
        self.assertEqual(tracker.state, "CALIBRATED")
        self.assertEqual(new_v0, 0.62)
        self.assertAlmostEqual(tracker.get_delta(0.65), 0.03, places=3)

    def test_baseline_tracker_gas_event_lock(self):
        tracker = BaselineTracker(warmup_points=5)
        for _ in range(5):
            tracker.update(0.50, is_gas_detected=False)

        baseline_before = tracker.v0

        # Simulate sudden gas surge (1.10V, large slope)
        tracker.update(1.10, is_gas_detected=True, slope=0.05)
        self.assertEqual(tracker.state, "LOCKED_EVENT")
        self.assertEqual(tracker.v0, baseline_before)  # Baseline should not be corrupted by gas plume!

    def test_flatness_guard_detection(self):
        tracker = BaselineTracker(warmup_points=5)
        tracker.recalibrate(target_val=0.55)

        flat_window = [0.55 + 0.001 * np.sin(i) for i in range(20)]
        self.assertTrue(tracker.is_flat_baseline(flat_window))

        surge_window = [0.55 + 0.04 * i for i in range(20)]
        self.assertFalse(tracker.is_flat_baseline(surge_window))

    def test_shift_invariance_features(self):
        # Window 1: Lab baseline (0.01V)
        w_lab = [0.010 + 0.0005 * i for i in range(20)]
        feat_lab = extract_window_features(w_lab, base_v=0.010)

        # Window 2: Outdoor baseline (0.55V)
        w_outdoor = [0.550 + 0.0005 * i for i in range(20)]
        feat_outdoor = extract_window_features(w_outdoor, base_v=0.550)

        # Differential features and relative delta points should match closely
        self.assertTrue(np.allclose(feat_lab[:6], feat_outdoor[:6], atol=1e-3))

    def test_outdoor_flat_baseline_inference(self):
        # Test that a flat outdoor signal of 0.55V NEVER triggers false H2S / NH3
        flat_window = [0.550 + 0.001 * (i % 2) for i in range(20)]
        result = runInference(flat_window, compS3=0.550)

        self.assertEqual(result['gas'], 'Clean Air')
        self.assertEqual(result['estimatedppm'], 0.0)
        self.assertEqual(result['riskLevel'], 'Normal')
        self.assertGreaterEqual(result['confidence'], 95)

    def test_pulse_outdoor_flat_inference(self):
        # 250 points flat outdoor trace at 0.55V
        pulse_outdoor = [0.550 + 0.002 * np.sin(i * 0.1) for i in range(250)]
        result = runPulseInference(pulse_outdoor)

        self.assertEqual(result['gas'], 'Clean Air')
        self.assertEqual(result['estimatedppm'], 0.0)
        self.assertEqual(result['riskLevel'], 'Normal')

    def test_compute_risk_level_decoupling(self):
        # Raw voltage is high (0.65V), but differential delta is tiny (Clean Air background) -> Normal
        self.assertEqual(computeRiskLevel('Clean Air', ppmVal=0.0, deltaV=0.02), 'Normal')

        # True gas surge: H2S with deltaV > 0.40 and ppm > 5 -> Hazardous / Emergency
        self.assertEqual(computeRiskLevel('H2S', ppmVal=6.0, deltaV=0.45), 'Hazardous')
        self.assertEqual(computeRiskLevel('H2S', ppmVal=12.0, deltaV=0.60), 'Emergency')

    def test_api_calibration_endpoints(self):
        # Status endpoint
        resp = client.get('/api/calibrate/status')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('v0', data)
        self.assertIn('state', data)

        # Zero Calibration endpoint
        resp = client.post('/api/calibrate/zero', json={'targetVoltage': 0.5432})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['baselineVoltage'], 0.5432)

if __name__ == '__main__':
    unittest.main()
