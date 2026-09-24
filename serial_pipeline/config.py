"""
serial_pipeline/config.py
Configuration parameters for RS-485 Serial Communication and Data Buffer.
"""
import os
from dataclasses import dataclass, field

@dataclass
class SerialConfig:
    port: str = os.getenv('RS485_PORT', '/dev/ttyUSB0')
    baudrate: int = int(os.getenv('RS485_BAUDRATE', '115200'))
    bytesize: int = 8
    parity: str = 'N'
    stopbits: int = 1
    timeout: float = 1.0  # seconds
    reconnect_interval_sec: float = 2.0
    max_reconnect_backoff_sec: float = 10.0

@dataclass
class BufferConfig:
    cycle_length: int = 250          # 250 points per 60-second cycle
    window_length: int = 20          # 20 points per real-time sliding window (~4.8s)
    raw_queue_size: int = 5000       # Maximum raw items in thread queue
    max_history_points: int = 1000   # Retain last 1000 points in memory ring buffer

@dataclass
class LogConfig:
    log_dir: str = 'logs'
    log_file: str = 'logs/serial_receiver.log'
    max_bytes: int = 5 * 1024 * 1024  # 5 MB
    backup_count: int = 3
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')

@dataclass
class AppConfig:
    serial: SerialConfig = field(default_factory=SerialConfig)
    buffer: BufferConfig = field(default_factory=BufferConfig)
    logging: LogConfig = field(default_factory=LogConfig)

config = AppConfig()
