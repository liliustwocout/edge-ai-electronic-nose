"""
serial_pipeline/inference.py
Edge AI Inference Engine (Modular Stage for Future Integration):
- Loads pre-trained RandomForest models (Window & Pulse).
- Provides predict_window() and predict_cycle().
- Implements shift-invariant dynamic baseline compensation.
"""
import os
import json
import pickle
import logging
from typing import Optional, Dict, List
import numpy as np

from .feature_extraction import extract_window_features, extract_pulse_features

logger = logging.getLogger('serial_pipeline.inference')

class EdgeAIInferenceEngine:
    def __init__(self, backend_dir: str = 'backend'):
        self.backend_dir = backend_dir
        self.clf_win = None
        self.reg_win = None
        self.clf_pulse = None
        self.reg_pulse = None
        self.classes = ['Clean Air', 'H2S', 'NH3']
        self.is_loaded = False

        self._load_models()

    def _load_models(self):
        """Attempts to load pre-trained models from backend directory."""
        win_clf_path = os.path.join(self.backend_dir, 'model_gas.pkl')
        win_reg_path = os.path.join(self.backend_dir, 'model_ppm.pkl')
        pulse_clf_path = os.path.join(self.backend_dir, 'model_pulse_gas.pkl')
        pulse_reg_path = os.path.join(self.backend_dir, 'model_pulse_ppm.pkl')
        meta_path = os.path.join(self.backend_dir, 'classes.json')

        try:
            if os.path.exists(meta_path):
                with open(meta_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    self.classes = meta.get('classes', self.classes)

            if os.path.exists(win_clf_path) and os.path.exists(win_reg_path):
                with open(win_clf_path, 'rb') as f:
                    self.clf_win = pickle.load(f)
                with open(win_reg_path, 'rb') as f:
                    self.reg_win = pickle.load(f)

            if os.path.exists(pulse_clf_path) and os.path.exists(pulse_reg_path):
                with open(pulse_clf_path, 'rb') as f:
                    self.clf_pulse = pickle.load(f)
                with open(pulse_reg_path, 'rb') as f:
                    self.reg_pulse = pickle.load(f)

            if self.clf_win and self.clf_pulse:
                self.is_loaded = True
                logger.info("Successfully loaded all 4 Edge AI models into serial pipeline.")
            else:
                logger.info("Edge AI models not yet loaded. Operating in pass-through data acquisition mode.")
        except Exception as e:
            logger.warning(f"Could not load Edge AI models: {e}. Operating in pass-through mode.")
            self.is_loaded = False

    def predict_window(self, window_20: List[float], base_v: float = 0.0) -> Optional[Dict]:
        """Runs real-time inference on a 20-point sliding window."""
        if not self.is_loaded or self.clf_win is None:
            return None
        try:
            feat = extract_window_features(window_20, base_v=base_v)
            gas_idx = int(self.clf_win.predict([feat])[0])
            gas_name = self.classes[gas_idx] if gas_idx < len(self.classes) else "Unknown"
            ppm = float(self.reg_win.predict([feat])[0]) if self.reg_win else 0.0
            return {'gas': gas_name, 'ppm': max(0.0, round(ppm, 2))}
        except Exception as e:
            logger.error(f"Error in window inference: {e}")
            return None

    def predict_cycle(self, pulse_250: np.ndarray, base_v: float = 0.0) -> Optional[Dict]:
        """Runs 60-second cycle inference on a full 250-point WaveCycle."""
        if not self.is_loaded or self.clf_pulse is None:
            return None
        try:
            feat = extract_pulse_features(pulse_250, base_v=base_v)
            gas_idx = int(self.clf_pulse.predict([feat])[0])
            gas_name = self.classes[gas_idx] if gas_idx < len(self.classes) else "Unknown"
            ppm = float(self.reg_pulse.predict([feat])[0]) if self.reg_pulse else 0.0
            return {'gas': gas_name, 'ppm': max(0.0, round(ppm, 2))}
        except Exception as e:
            logger.error(f"Error in cycle inference: {e}")
            return None
