"""
serial_pipeline/serial_receiver.py
High-Reliability 24/7 RS-485 Serial Communication Engine for Raspberry Pi.
Features:
- Non-blocking continuous read loop in dedicated worker thread.
- Hardware disconnect detection and automatic reconnect with exponential backoff.
- Fragment-safe parsing via StreamPacketParser.
- Thread-safe queues and callbacks to decoupling I/O from computation.
- Clean shutdown on SIGINT/SIGTERM without port locking.
"""
import os
import time
import logging
import threading
from typing import Optional, Callable
import serial
from serial import SerialException

from .config import SerialConfig, config
from .parser import StreamPacketParser, PointSample

logger = logging.getLogger('serial_pipeline.receiver')

class SerialReceiver:
    def __init__(self, cfg: Optional[SerialConfig] = None, on_sample_callback: Optional[Callable[[PointSample], None]] = None):
        self.cfg = cfg or config.serial
        self.parser = StreamPacketParser()
        self.on_sample = on_sample_callback

        self._ser: Optional[serial.Serial] = None
        self._thread: Optional[threading.Thread] = None
        self._running = threading.Event()
        self._is_connected = False

        # Telemetry metrics
        self._reconnect_count: int = 0
        self._bytes_received: int = 0
        self._connection_start_time: float = 0.0

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def start(self):
        """Starts the serial receiver background thread."""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("SerialReceiver is already running.")
            return

        self._running.set()
        self._thread = threading.Thread(target=self._run_loop, name="RS485-Receiver-Thread", daemon=True)
        self._thread.start()
        logger.info(f"RS485 Serial Receiver started on {self.cfg.port} ({self.cfg.baudrate} baud).")

    def stop(self):
        """Stops the receiver thread and releases the serial port cleanly."""
        logger.info("Stopping RS485 Serial Receiver...")
        self._running.clear()
        if self._thread is not None:
            self._thread.join(timeout=3.0)
        self._close_serial()
        logger.info("RS485 Serial Receiver stopped cleanly.")

    def _open_serial(self) -> bool:
        """Attempts to open the serial port."""
        try:
            self._close_serial()
            if not os.path.exists(self.cfg.port):
                return False

            self._ser = serial.Serial(
                port=self.cfg.port,
                baudrate=self.cfg.baudrate,
                bytesize=self.cfg.bytesize,
                parity=self.cfg.parity,
                stopbits=self.cfg.stopbits,
                timeout=self.cfg.timeout
            )
            # Flush any residual garbage
            self._ser.reset_input_buffer()
            self.parser.reset()
            self._is_connected = True
            self._connection_start_time = time.time()
            logger.info(f"Successfully opened serial port {self.cfg.port}.")
            return True
        except (SerialException, OSError) as e:
            self._is_connected = False
            return False

    def _close_serial(self):
        """Safely closes the serial port."""
        if self._ser is not None:
            try:
                if self._ser.is_open:
                    self._ser.close()
            except Exception:
                pass
            self._ser = None
        self._is_connected = False

    def _run_loop(self):
        """Continuous reading loop with auto-reconnection and backoff."""
        backoff = self.cfg.reconnect_interval_sec

        while self._running.is_set():
            # If not connected, attempt connection with backoff
            if not self._is_connected or self._ser is None or not self._ser.is_open:
                success = self._open_serial()
                if not success:
                    self._reconnect_count += 1
                    logger.warning(
                        f"Serial port {self.cfg.port} unavailable. "
                        f"Retrying in {backoff:.1f}s (attempts: {self._reconnect_count})..."
                    )
                    time.sleep(backoff)
                    backoff = min(backoff * 1.5, self.cfg.max_reconnect_backoff_sec)
                    continue
                else:
                    backoff = self.cfg.reconnect_interval_sec

            # Read stream
            try:
                # Read whatever bytes are available immediately (zero latency)
                in_w = self._ser.in_waiting if hasattr(self._ser, 'in_waiting') else 0
                to_read = max(in_w, 1) if in_w > 0 else 1
                raw_bytes = self._ser.read(to_read)
                if not raw_bytes:
                    continue

                self._bytes_received += len(raw_bytes)
                text = raw_bytes.decode('ascii', errors='ignore')

                # Parse packets from text
                samples = self.parser.parse_chunk(text)
                for s in samples:
                    if self.on_sample:
                        try:
                            self.on_sample(s)
                        except Exception as cb_err:
                            logger.error(f"Error in on_sample callback: {cb_err}")

            except (SerialException, OSError) as read_err:
                logger.error(f"Serial communication error on {self.cfg.port}: {read_err}. Reconnecting...")
                self._close_serial()
                time.sleep(1.0)
            except Exception as unk_err:
                logger.error(f"Unexpected error in serial read loop: {unk_err}", exc_info=True)
                time.sleep(0.5)

        self._close_serial()

    def get_telemetry(self) -> dict:
        """Returns receiver status and connection statistics."""
        uptime = (time.time() - self._connection_start_time) if self._is_connected else 0.0
        return {
            'is_connected': self._is_connected,
            'port': self.cfg.port,
            'baudrate': self.cfg.baudrate,
            'bytes_received': self._bytes_received,
            'total_parsed': self.parser.total_parsed,
            'invalid_tokens': self.parser.invalid_tokens,
            'reconnect_count': self._reconnect_count,
            'uptime_seconds': round(uptime, 1)
        }
