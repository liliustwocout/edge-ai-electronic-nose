"""
serial_pipeline package
Edge AI Electronic Nose RS-485 Data Acquisition & Preprocessing Pipeline
"""
from .config import config
from .parser import StreamPacketParser, PointSample
from .buffer import PointBuffer
from .serial_receiver import SerialReceiver
from .preprocessing import SignalPreprocessor
from .feature_extraction import extract_window_features, extract_pulse_features
from .inference import EdgeAIInferenceEngine

__all__ = [
    'config',
    'StreamPacketParser',
    'PointSample',
    'PointBuffer',
    'SerialReceiver',
    'SignalPreprocessor',
    'extract_window_features',
    'extract_pulse_features',
    'EdgeAIInferenceEngine'
]
