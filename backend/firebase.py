import os
import csv
import json
import time
import math
import threading
import urllib.error
import urllib.request
from typing import Dict, Any, Optional, List, Callable

DEFAULT_RTDB_URL = 'https://enose-1aeb7-default-rtdb.asia-southeast1.firebasedatabase.app/sensor/latest.json?auth=qbtMtFdVKPlt5kBvQoD7ELUITrqs1qoPPuNmgQ0y'

class FirebaseService:
    def __init__(self, primary_url: str = DEFAULT_RTDB_URL, enable_sse: bool = False):
        self.dbUrls = {
            'CleanAir': primary_url,
            'H2S': 'https://enose-h2s-default-rtdb.asia-southeast1.firebasedatabase.app/sensor/latest.json?auth=qbtMtFdVKPlt5kBvQoD7ELUITrqs1qoPPuNmgQ0y',
            'NH3': 'https://enose-nh3-default-rtdb.asia-southeast1.firebasedatabase.app/sensor/latest.json?auth=qbtMtFdVKPlt5kBvQoD7ELUITrqs1qoPPuNmgQ0y',
            'MixedAir': primary_url
        }
        self.activeAir = 'CleanAir'
        self.enable_sse = enable_sse
        self.connectionStatus: Dict[str, Dict[str, Any]] = {}
        self.ramBuffers: Dict[str, List[Dict[str, Any]]] = {g: [] for g in self.dbUrls.keys()}
        self.csvFiles = {g: f'data/{g}_live.csv' for g in self.dbUrls.keys()}
        self.latest: Dict[str, Optional[Dict[str, Any]]] = {g: None for g in self.dbUrls.keys()}
        self.lastFlush = time.time()
        self.flushInterval = 60
        self.running = True
        self.lock = threading.Lock()
        self.subscribers: List[Callable[[Dict[str, Any]], None]] = []
        self.is_hardware_active: Optional[Callable[[], bool]] = None
        
        self.currentResp = None
        self.streamThread = None
        self.connThread = None

        if self.enable_sse:
            # Initial connection test
            self.checkAllConnections()
            self.streamThread = threading.Thread(target=self.sseStreamLoop, daemon=True)
            self.streamThread.start()
            # Periodic connection checker
            self.connThread = threading.Thread(target=self.connectionCheckLoop, daemon=True)
            self.connThread.start()

    def subscribe(self, callback: Callable[[Dict[str, Any]], None]):
        with self.lock:
            if callback not in self.subscribers:
                self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Dict[str, Any]], None]):
        with self.lock:
            if callback in self.subscribers:
                self.subscribers.remove(callback)

    def notifySubscribers(self, packet: Dict[str, Any]):
        with self.lock:
            subs = list(self.subscribers)
        for s in subs:
            try:
                s(packet)
            except Exception:
                pass

    def setAirType(self, airType: str):
        with self.lock:
            if airType in self.dbUrls and airType != self.activeAir:
                self.activeAir = airType
                # Close current stream to trigger immediate reconnection to new gas channel URL
                if self.currentResp:
                    try:
                        self.currentResp.close()
                    except Exception:
                        pass

    def getLatest(self, airType: Optional[str] = None) -> Optional[Dict[str, Any]]:
        with self.lock:
            target = airType if (airType and airType in self.dbUrls) else self.activeAir
            return self.latest.get(target)

    def checkConnection(self, gas: str) -> Dict[str, Any]:
        url = self.dbUrls.get(gas, '')
        if not url:
            return {'connected': False, 'code': 404, 'status': 'Offline - 404', 'url': '', 'latencyMs': 0.0}
        tStart = time.perf_counter()
        try:
            req = urllib.request.Request(url, headers={'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                code = resp.getcode()
                latency = round((time.perf_counter() - tStart) * 1000, 1)
                return {
                    'connected': code == 200,
                    'code': code,
                    'status': f'Connected - {code}' if code == 200 else f'HTTP {code}',
                    'url': url,
                    'latencyMs': latency
                }
        except urllib.error.HTTPError as err:
            latency = round((time.perf_counter() - tStart) * 1000, 1)
            return {'connected': False, 'code': err.code, 'status': f'Offline - {err.code}', 'url': url, 'latencyMs': latency}
        except Exception:
            latency = round((time.perf_counter() - tStart) * 1000, 1)
            return {'connected': False, 'code': 500, 'status': 'Offline - Timeout', 'url': url, 'latencyMs': latency}

    def checkAllConnections(self) -> Dict[str, Dict[str, Any]]:
        results = {}
        for gas in self.dbUrls.keys():
            results[gas] = self.checkConnection(gas)
        with self.lock:
            self.connectionStatus = results
        return results

    def connectionCheckLoop(self):
        while self.running:
            try:
                self.checkAllConnections()
            except Exception:
                pass
            time.sleep(60)

    def parseGasPacket(self, rawData: Dict[str, Any], gasName: str) -> Dict[str, Any]:
        v1 = float(rawData.get('voltage1', 0.0))
        v2 = float(rawData.get('voltage2', 0.0))
        pt = int(rawData.get('point', 0))
        pl = int(rawData.get('pulse', 0))
        dac = float(rawData.get('dac_voltage', 0.0))
        wt = int(rawData.get('wave_type', 0))
        s1 = int(rawData.get('sensor1', rawData.get('raw_sensor1', 0)))
        s2 = int(rawData.get('sensor2', rawData.get('raw_sensor2', 0)))
        raw_s1 = int(rawData.get('raw_sensor1', s1))
        raw_s2 = int(rawData.get('raw_sensor2', s2))
        ppmVal = float(rawData.get('ppm', 0.0))
        tNow = time.strftime('%Y-%m-%d %H:%M:%S')

        return {
            'point': pt,
            'voltage1': v1,
            'voltage2': v2,
            'sensor1': s1,
            'sensor2': s2,
            'rawSensor1': raw_s1,
            'rawSensor2': raw_s2,
            'pulse': pl,
            'dacVoltage': dac,
            'waveType': wt,
            'gasType': gasName,
            'ppm': ppmVal,
            'timestamp': tNow
        }

    def sseStreamLoop(self):
        """
        Uses persistent Server-Sent Events (SSE text/event-stream) to receive EVERY single
        point pushed in real-time from Firebase RTDB without dropped packets or polling lag.
        """
        last_pt = -1
        last_v1 = -1.0
        
        while self.running:
            gasName = self.activeAir
            url = self.dbUrls.get(gasName, DEFAULT_RTDB_URL)
            try:
                req = urllib.request.Request(url, headers={'Accept': 'text/event-stream'})
                with urllib.request.urlopen(req, timeout=15.0) as resp:
                    with self.lock:
                        self.currentResp = resp
                    curr_event = None

                    while self.running:
                        line_bytes = resp.readline()
                        if not line_bytes:
                            break
                        line = line_bytes.decode('utf-8', errors='ignore').strip()
                        if not line:
                            continue
                        if line.startswith('event:'):
                            curr_event = line.split(':', 1)[1].strip()
                        elif line.startswith('data:'):
                            data_str = line.split(':', 1)[1].strip()
                            if curr_event == 'put' and data_str and data_str != 'null':
                                try:
                                    payload = json.loads(data_str)
                                    path = payload.get('path', '')
                                    raw_data = payload.get('data')
                                    if path == '/' and isinstance(raw_data, dict) and 'voltage1' in raw_data:
                                        pt = int(raw_data.get('point', 0))
                                        v1 = float(raw_data.get('voltage1', 0.0))
                                        if pt != last_pt or abs(v1 - last_v1) > 1e-5:
                                            # If physical RS-485 hardware is actively streaming, don't mix cloud packets
                                            if self.is_hardware_active and self.is_hardware_active():
                                                continue
                                            last_pt = pt
                                            last_v1 = v1
                                            parsed = self.parseGasPacket(raw_data, gasName)
                                            with self.lock:
                                                self.latest[gasName] = parsed
                                                self.ramBuffers[gasName].append(parsed)
                                            
                                            self.notifySubscribers(parsed)
                                            
                                            if time.time() - self.lastFlush >= self.flushInterval:
                                                self.flushDisk()
                                except Exception:
                                    pass
            except Exception:
                # SSE connection dropped or reconnecting: short delay before retry
                time.sleep(1.0)

    def flushDisk(self):
        with self.lock:
            os.makedirs('data', exist_ok=True)
            for gas, buf in self.ramBuffers.items():
                if len(buf) > 0:
                    path = self.csvFiles[gas]
                    exists = os.path.exists(path)
                    keys = ['point', 'voltage1', 'voltage2', 'sensor1', 'sensor2', 'rawSensor1', 'rawSensor2', 'dacVoltage', 'pulse', 'waveType', 'gasType', 'ppm', 'timestamp']
                    try:
                        with open(path, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=keys)
                            if not exists or os.path.getsize(path) == 0:
                                writer.writeheader()
                            for r in buf:
                                row = {k: r.get(k, 0) for k in keys}
                                writer.writerow(row)
                        buf.clear()
                    except Exception:
                        pass
            self.lastFlush = time.time()

    def getStatus(self) -> Dict[str, Any]:
        with self.lock:
            return {
                'activeAir': self.activeAir,
                'latest': self.latest.get(self.activeAir),
                'ramCounts': {k: len(v) for k, v in self.ramBuffers.items()},
                'secondsUntilFlush': max(0, int(self.flushInterval - (time.time() - self.lastFlush))),
                'connections': self.connectionStatus
            }

    def stop(self):
        self.running = False
        self.flushDisk()

if __name__ == '__main__':
    service = FirebaseService()
    print("Testing FirebaseService...")
    time.sleep(1.5)
    st = service.getStatus()
    print(f"Status: {json.dumps(st, indent=2)}")
    service.stop()
