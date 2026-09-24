import unittest
import numpy as np
from serial_pipeline.parser import StreamPacketParser, PointSample
from serial_pipeline.buffer import PointBuffer
from serial_pipeline.inference import EdgeAIInferenceEngine

class TestStreamPacketParser(unittest.TestCase):
    def setUp(self):
        self.parser = StreamPacketParser()

    def test_single_token(self):
        samples = self.parser.parse_chunk("P172:0.0183V")
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].point, 172)
        self.assertAlmostEqual(samples[0].voltage1, 0.0183, places=4)

    def test_multiple_tokens_with_newlines_and_spaces(self):
        chunk = "P172:0.0183V, P173:0.0178V, P174:0.0174V\n"
        samples = self.parser.parse_chunk(chunk)
        self.assertEqual(len(samples), 3)
        self.assertEqual([s.point for s in samples], [172, 173, 174])
        self.assertEqual([round(s.voltage1, 4) for s in samples], [0.0183, 0.0178, 0.0174])

    def test_split_across_chunks(self):
        # Chunk 1 cuts mid-voltage
        chunk1 = "P50:0.418"
        samples1 = self.parser.parse_chunk(chunk1)
        self.assertEqual(len(samples1), 0)  # Incomplete, held in fragment buffer

        # Chunk 2 delivers remainder
        chunk2 = "9V, P51:0.4176V\n"
        samples2 = self.parser.parse_chunk(chunk2)
        self.assertEqual(len(samples2), 2)
        self.assertEqual(samples2[0].point, 50)
        self.assertAlmostEqual(samples2[0].voltage1, 0.4189, places=4)
        self.assertEqual(samples2[1].point, 51)
        self.assertAlmostEqual(samples2[1].voltage1, 0.4176, places=4)

    def test_noisy_bytes_rejection(self):
        chunk = "###GARBAGE%%%P200:0.0105V***NOISE&&&"
        samples = self.parser.parse_chunk(chunk)
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0].point, 200)
        self.assertAlmostEqual(samples[0].voltage1, 0.0105, places=4)

class TestPointBuffer(unittest.TestCase):
    def setUp(self):
        self.buffer = PointBuffer(cycle_length=250, window_length=20)

    def test_rolling_window_bound(self):
        for i in range(50):
            self.buffer.push(PointSample(point=i, voltage1=float(i) * 0.01, timestamp=float(i)))
        win = self.buffer.get_current_window()
        self.assertEqual(len(win), 20)
        # Should contain the last 20 voltages (30 * 0.01 to 49 * 0.01)
        self.assertAlmostEqual(win[0], 0.30, places=2)
        self.assertAlmostEqual(win[-1], 0.49, places=2)

    def test_packet_drop_detection(self):
        # Sequential
        self.buffer.push(PointSample(point=10, voltage1=0.2, timestamp=1.0))
        self.buffer.push(PointSample(point=11, voltage1=0.21, timestamp=1.1))
        # Jump from 11 to 15 (missing 12, 13, 14 -> 3 dropped points)
        self.buffer.push(PointSample(point=15, voltage1=0.25, timestamp=1.5))

        stats = self.buffer.get_stats()
        self.assertEqual(stats['total_received'], 3)
        self.assertEqual(stats['total_gaps'], 1)
        self.assertEqual(stats['total_dropped_points'], 3)
        self.assertGreater(stats['packet_loss_rate_pct'], 0.0)

    def test_cycle_completion_and_interpolation(self):
        completed_cycles = []
        def on_cycle(cycle_id, arr, metrics):
            completed_cycles.append((cycle_id, arr, metrics))

        self.buffer.on_cycle_complete = on_cycle

        # Push points 0 to 249 with 1 point missing (point 100 missing)
        for i in range(250):
            if i == 100:
                continue  # simulate single missing point
            self.buffer.push(PointSample(point=i, voltage1=0.1 + (i * 0.001), timestamp=float(i)))

        # Push point 0 of next cycle to trigger wrap-around
        self.buffer.push(PointSample(point=0, voltage1=0.1, timestamp=250.0))

        self.assertEqual(len(completed_cycles), 1)
        cid, arr, metrics = completed_cycles[0]
        self.assertEqual(cid, 1)
        self.assertEqual(len(arr), 250)
        # Check that missing point 100 was linearly interpolated
        self.assertFalse(np.isnan(arr[100]))
        self.assertAlmostEqual(arr[100], 0.20, delta=0.01)
        self.assertEqual(metrics['filled_points'], 249)

class TestInferenceEngine(unittest.TestCase):
    def test_inference_loading(self):
        engine = EdgeAIInferenceEngine()
        self.assertTrue(engine.is_loaded)

        # Test window inference
        sample_win = [0.01] * 20
        res_win = engine.predict_window(sample_win, base_v=0.01)
        self.assertIsNotNone(res_win)
        self.assertIn('gas', res_win)
        self.assertEqual(res_win['gas'], 'Clean Air')

        # Test cycle inference
        sample_pulse = np.full(250, 0.01, dtype=np.float32)
        res_pulse = engine.predict_cycle(sample_pulse, base_v=0.01)
        self.assertIsNotNone(res_pulse)
        self.assertIn('gas', res_pulse)
        self.assertEqual(res_pulse['gas'], 'Clean Air')

if __name__ == '__main__':
    unittest.main()
