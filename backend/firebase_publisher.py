"""
backend/firebase_publisher.py
High-Reliability Edge AI & RS-485 Firebase RTDB Publisher.
Publishes live telemetry, edge AI inference results, and cycle summaries
from Raspberry Pi 3 directly to a dedicated Firebase branch (/edge_ai),
completely separate from ESP32's branch (/sensor).
"""
import os
import time
import json
import logging
import threading
import queue
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

logger = logging.getLogger('backend.firebase_publisher')

DEFAULT_BASE_URL = os.getenv('FIREBASE_RTDB_URL', 'https://enose-1aeb7-default-rtdb.asia-southeast1.firebasedatabase.app').rstrip('/')
DEFAULT_AUTH = os.getenv('FIREBASE_AUTH_SECRET', 'qbtMtFdVKPlt5kBvQoD7ELUITrqs1qoPPuNmgQ0y')
DEFAULT_BRANCH = os.getenv('FIREBASE_EDGE_BRANCH', 'edge_ai')


class EdgeFirebasePublisher:
    """
    Dedicated worker for streaming Raspberry Pi 3 RS-485 and Edge AI inference
    results to a custom Firebase Realtime Database branch without blocking serial I/O.
    """
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        auth_secret: str = DEFAULT_AUTH,
        branch: str = DEFAULT_BRANCH,
        min_push_interval_sec: float = 0.25,
        enabled: bool = True
    ):
        self.base_url = base_url.rstrip('/')
        self.auth_secret = auth_secret
        self.branch = branch.strip('/')
        self.min_push_interval_sec = min_push_interval_sec
        self.enabled = enabled

        # Bounded queues to guarantee zero memory leak
        self._sample_queue = queue.Queue(maxsize=5)
        self._cycle_queue = queue.Queue(maxsize=10)

        # Worker thread
        self._running = threading.Event()
        self._thread: Optional[threading.Thread] = None

        # Statistics & telemetry
        self._lock = threading.Lock()
        self._total_pushed: int = 0
        self._cycle_pushed: int = 0
        self._push_errors: int = 0
        self._last_push_ts: float = 0.0
        self._last_latency_ms: float = 0.0
        self._is_online: bool = False
        self._last_error: str = ""

    @property
    def is_running(self) -> bool:
        return self._running.is_set()

    def start(self):
        """Starts the background publisher thread."""
        if not self.enabled:
            logger.info("EdgeFirebasePublisher is disabled via config.")
            return

        if self._thread is not None and self._thread.is_alive():
            logger.warning("EdgeFirebasePublisher worker is already running.")
            return

        self._running.set()
        self._thread = threading.Thread(
            target=self._worker_loop,
            name="Firebase-EdgePublisher-Thread",
            daemon=True
        )
        self._thread.start()
        logger.info(f"EdgeFirebasePublisher started. Publishing to /{self.branch} on {self.base_url}")

    def stop(self):
        """Stops the worker thread cleanly."""
        self._running.clear()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        logger.info("EdgeFirebasePublisher stopped.")

    def push_sample(self, telemetry: Dict[str, Any], inference: Optional[Dict[str, Any]] = None, cycle_idx: int = 1):
        """
        Enqueues the latest RS-485 sample and Edge AI inference for publishing.
        If the queue is full (network lag), the oldest item is discarded to preserve freshness.
        """
        if not self.enabled or not self._running.is_set():
            return

        payload = {
            'device': 'Raspberry Pi 3 Model B (Edge Gateway)',
            'source': telemetry.get('source', 'RS485_FT232'),
            'port': telemetry.get('port', '/dev/ttyUSB0'),
            'baudrate': telemetry.get('baudrate', 115200),
            'point': telemetry.get('point', 0),
            'voltage1': round(float(telemetry.get('voltage1', 0.0)), 4),
            'voltage2': round(float(telemetry.get('voltage2', 0.0)), 4),
            'sensor1': telemetry.get('sensor1', 0),
            'rawSensor1': telemetry.get('rawSensor1', 0),
            'cycle': cycle_idx,
            'timestamp': telemetry.get('timestamp', time.strftime('%Y-%m-%d %H:%M:%S')),
            'unix_ts': round(time.time(), 3),
            'inference': inference or {
                'gas': 'Unknown',
                'confidence': 0.0,
                'ppm': 0.0,
                'riskLevel': 'Normal',
                'baseline': 0.0,
                'delta': 0.0
            }
        }

        try:
            # Drop older pending item if full to avoid lag
            if self._sample_queue.full():
                try:
                    self._sample_queue.get_nowait()
                except queue.Empty:
                    pass
            self._sample_queue.put_nowait(payload)
        except Exception:
            pass

    def push_cycle_summary(self, summary: Dict[str, Any]):
        """
        Enqueues a completed 250-point cycle summary to be written immediately to Firebase.
        """
        if not self.enabled or not self._running.is_set():
            return

        payload = dict(summary)
        payload['device'] = 'Raspberry Pi 3 Model B (Edge Gateway)'
        payload['unix_ts'] = round(time.time(), 3)
        if 'timestamp' not in payload:
            payload['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            self._cycle_queue.put_nowait(payload)
        except Exception:
            pass

    def _http_put(self, path: str, data: Dict[str, Any], timeout: float = 3.0) -> bool:
        """Helper to send HTTP PUT request to Firebase RTDB."""
        url = f"{self.base_url}/{self.branch}/{path}.json"
        if self.auth_secret:
            url += f"?auth={self.auth_secret}"

        body = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=body,
            method='PUT',
            headers={'Content-Type': 'application/json'}
        )

        tStart = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                latency = (time.perf_counter() - tStart) * 1000
                with self._lock:
                    self._last_latency_ms = round(latency, 1)
                    self._is_online = (status == 200)
                    self._last_push_ts = time.time()
                return status == 200
        except urllib.error.HTTPError as he:
            with self._lock:
                self._push_errors += 1
                self._is_online = False
                self._last_error = f"HTTP {he.code}: {he.reason}"
            return False
        except Exception as e:
            with self._lock:
                self._push_errors += 1
                self._is_online = False
                self._last_error = str(e)
            return False

    def _http_patch(self, path: str, data: Dict[str, Any], timeout: float = 3.0) -> bool:
        """Helper to send HTTP PATCH request to Firebase RTDB."""
        url = f"{self.base_url}/{self.branch}/{path}.json"
        if self.auth_secret:
            url += f"?auth={self.auth_secret}"

        body = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=body,
            method='PATCH',
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.getcode() == 200
        except Exception:
            return False

    def _worker_loop(self):
        """Worker thread processing queues with rate-limiting."""
        last_sample_time = 0.0
        last_heartbeat_time = 0.0

        # Initial device registration
        self._http_patch('device_status', {
            'status': 'ONLINE',
            'started_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'device': 'Raspberry Pi 3 Model B (Edge Gateway)',
            'branch': self.branch,
            'rs485_port': '/dev/ttyUSB0',
            'baudrate': 115200
        })

        while self._running.is_set():
            now = time.time()
            work_done = False

            # 1. Process Cycle Summaries (High priority, immediate push)
            try:
                cycle_data = self._cycle_queue.get_nowait()
                success = self._http_put('cycle_summary', cycle_data)
                if success:
                    with self._lock:
                        self._cycle_pushed += 1
                work_done = True
            except queue.Empty:
                pass

            # 2. Process Real-time Sample (Rate-limited to avoid spamming network)
            if (now - last_sample_time) >= self.min_push_interval_sec:
                try:
                    sample_data = self._sample_queue.get_nowait()
                    success = self._http_put('latest', sample_data)
                    if success:
                        with self._lock:
                            self._total_pushed += 1
                        last_sample_time = time.time()
                    work_done = True
                except queue.Empty:
                    pass

            # 3. Heartbeat & Health Check (every 30 seconds)
            if (now - last_heartbeat_time) >= 30.0:
                with self._lock:
                    total_pushed = self._total_pushed
                    cycle_pushed = self._cycle_pushed
                    errs = self._push_errors
                    lat = self._last_latency_ms

                self._http_patch('device_status', {
                    'status': 'ONLINE',
                    'last_heartbeat': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'total_points_published': total_pushed,
                    'total_cycles_published': cycle_pushed,
                    'push_errors': errs,
                    'last_latency_ms': lat
                })
                last_heartbeat_time = now

            if not work_done:
                time.sleep(0.05)

    def get_status(self) -> Dict[str, Any]:
        """Returns publisher status metrics for monitoring."""
        with self._lock:
            sec_ago = (time.time() - self._last_push_ts) if self._last_push_ts > 0 else None
            return {
                'enabled': self.enabled,
                'is_running': self._running.is_set(),
                'branch': self.branch,
                'base_url': self.base_url,
                'is_online': self._is_online,
                'total_points_published': self._total_pushed,
                'total_cycles_published': self._cycle_pushed,
                'push_errors': self._push_errors,
                'last_latency_ms': self._last_latency_ms,
                'last_push_seconds_ago': round(sec_ago, 1) if sec_ago is not None else None,
                'last_error': self._last_error
            }
