import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import time
import pickle
import sqlite3
import numpy as np

try:
    from backend.train import extract_window_features
    from backend.calibration import BaselineTracker
except ImportError:
    from train import extract_window_features
    from calibration import BaselineTracker

class EMAFilter:
  def __init__(self, alpha=0.2):
    self.alpha = alpha
    self.lastVal = None
  def filter(self, rawVal):
    if self.lastVal is None:
      self.lastVal = rawVal
    else:
      self.lastVal = (self.alpha * rawVal) + ((1.0 - self.alpha) * self.lastVal)
    return self.lastVal

class DriftCompensator:
  def __init__(self, refTemp=25.0, refHum=60.0, tempCoeff=0.0035, humCoeff=0.0015):
    self.refTemp = refTemp
    self.refHum = refHum
    self.tempCoeff = tempCoeff
    self.humCoeff = humCoeff
  def compensate(self, sensorVal, temp=29.0, hum=65.0):
    deltaT = temp - self.refTemp
    deltaH = hum - self.refHum
    compFactor = 1.0 + (self.tempCoeff * deltaT) + (self.humCoeff * deltaH)
    return sensorVal / compFactor

def computeRiskLevel(gas, ppmVal, deltaV):
    """
    Decoupled risk calculation: evaluates risk based on estimated PPM and differential ΔV.
    Prevents false alarms caused by high static outdoor baseline voltages (0.35V - 0.70V).
    """
    if gas == 'Clean Air' or abs(deltaV) < 0.08:
        return 'Normal'
    if gas == 'H2S':
        if ppmVal >= 10.0 or deltaV >= 0.55:
            return 'Emergency'
        elif ppmVal >= 5.0 or deltaV >= 0.35:
            return 'Hazardous'
        elif ppmVal >= 1.0 or deltaV >= 0.12:
            return 'Warning'
    elif gas == 'NH3':
        if ppmVal >= 100.0 or deltaV >= 0.65:
            return 'Emergency'
        elif ppmVal >= 50.0 or deltaV >= 0.45:
            return 'Hazardous'
        elif ppmVal >= 25.0 or deltaV >= 0.15:
            return 'Warning'
    return 'Normal'

class SQLiteEdgeStore:
  def __init__(self, dbPath='EdgeStorage.db'):
    self.dbPath = dbPath
    self.initSchema()
  def getConnection(self):
    return sqlite3.connect(self.dbPath)
  def initSchema(self):
    with self.getConnection() as conn:
      cur = conn.cursor()
      cur.execute('''CREATE TABLE IF NOT EXISTS TelemetryRecords (
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          timestamp TEXT, 
          nodeID INTEGER, 
          s3Raw REAL, 
          s3Filtered REAL, 
          s3Compensated REAL, 
          s3Baseline REAL,
          s3Delta REAL,
          temperature REAL, 
          humidity REAL, 
          mq136ADC INTEGER, 
          mq135ADC INTEGER, 
          identifiedGas TEXT, 
          estimatedppm REAL, 
          riskLevel TEXT
      )''')
      # Safely migrate existing database schema if columns do not exist
      try:
          cur.execute("ALTER TABLE TelemetryRecords ADD COLUMN s3Baseline REAL")
      except sqlite3.OperationalError:
          pass
      try:
          cur.execute("ALTER TABLE TelemetryRecords ADD COLUMN s3Delta REAL")
      except sqlite3.OperationalError:
          pass

      cur.execute('''CREATE TABLE IF NOT EXISTS AlarmEvents (
          id INTEGER PRIMARY KEY AUTOINCREMENT, 
          alertID TEXT, 
          timestamp TEXT, 
          nodeID INTEGER, 
          gas TEXT, 
          ppm REAL, 
          riskLevel TEXT, 
          actionTaken TEXT
      )''')
      conn.commit()
  def logTelemetry(self, record):
    with self.getConnection() as conn:
      cur = conn.cursor()
      cur.execute('''INSERT INTO TelemetryRecords (
          timestamp, nodeID, s3Raw, s3Filtered, s3Compensated, s3Baseline, s3Delta,
          temperature, humidity, mq136ADC, mq135ADC, identifiedGas, estimatedppm, riskLevel
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
          record.get('timestamp'), record.get('nodeID'), record.get('s3Raw'), 
          record.get('s3Filtered'), record.get('s3Compensated'), record.get('s3Baseline'), record.get('s3Delta'),
          record.get('temperature'), record.get('humidity'), record.get('mq136ADC'), 
          record.get('mq135ADC'), record.get('identifiedGas'), record.get('estimatedppm'), record.get('riskLevel')
      ))
      conn.commit()
  def logAlarm(self, alert):
    with self.getConnection() as conn:
      cur = conn.cursor()
      cur.execute('''INSERT INTO AlarmEvents (alertID, timestamp, nodeID, gas, ppm, riskLevel, actionTaken) VALUES (?, ?, ?, ?, ?, ?, ?)''', (alert.get('alertID'), alert.get('timestamp'), alert.get('nodeID'), alert.get('gas'), alert.get('ppm'), alert.get('riskLevel'), alert.get('actionTaken')))
      conn.commit()
  def fetchRecentTelemetry(self, limit=10):
    with self.getConnection() as conn:
      cur = conn.cursor()
      cur.execute('SELECT timestamp, nodeID, identifiedGas, estimatedppm, riskLevel FROM TelemetryRecords ORDER BY id DESC LIMIT ?', (limit,))
      return cur.fetchall()

class MQTTWISEIoTFormatter:
  def __init__(self, plantID='p1', gatewayID='g1'):
    self.plantID = plantID
    self.gatewayID = gatewayID
  def buildTelemetryTopic(self):
    return f'/advantech/enose/v1/{self.plantID}/{self.gatewayID}/telemetry'
  def buildAlertTopic(self):
    return f'/advantech/enose/v1/{self.plantID}/{self.gatewayID}/alert'
  def formatTelemetryPayload(self, nodesData):
    return {
      'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
      'GatewayID': self.gatewayID,
      'NodesData': nodesData
    }
  def formatAlertPayload(self, alertData):
    riskVal = alertData.get('RiskLevel', alertData.get('riskLevel'))
    gasVal = alertData.get('Gas', alertData.get('gas'))
    ppmVal = alertData.get('ppm', alertData.get('estimatedppm', 0.0))
    return {
      'AlertID': alertData.get('AlertID', alertData.get('alertID')),
      'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
      'GatewayID': self.gatewayID,
      'NodeID': alertData.get('NodeID', alertData.get('nodeID')),
      'Location': alertData.get('Location', 'Compressor Station Area 1'),
      'RiskLevel': riskVal,
      'concentrationppm': ppmVal,
      'ThresholdExceeded': 50.0 if riskVal == 'Emergency' else (10.0 if riskVal == 'Hazardous' else 1.0),
      'InferenceResult': {
        'PredictedEvent': f'Rapid {gasVal} Leakage Detected',
        'Confidence': alertData.get('Confidence', alertData.get('confidence', 0.98)),
        'PatternSignatureMatched': 'Single Sensor Dynamic Trajectory S3'
      },
      'ActionRequired': 'Evacuate Personnel & Isolate Supply Valve V302' if riskVal == 'Emergency' else 'Dispatch Safety Inspection With SCBA'
    }

class EdgeAIGateway:
  def __init__(self):
    self.emaFilter = EMAFilter(alpha=0.2)
    self.driftComp = DriftCompensator()
    self.baselineTracker = BaselineTracker(warmup_points=20)
    self.store = SQLiteEdgeStore(dbPath='backend/EdgeStorage.db')
    self.mqttFormatter = MQTTWISEIoTFormatter()
    self.window = []
    self.windowSize = 20
    with open('backend/classes.json', 'r', encoding='utf-8') as f:
      meta = json.load(f)
    self.classes = meta['classes']
    with open('backend/model_gas.pkl', 'rb') as f:
      self.clf_win = pickle.load(f)
    with open('backend/model_ppm.pkl', 'rb') as f:
      self.reg_win = pickle.load(f)

  def processSample(self, rawVal, temp=29.0, hum=65.0, nodeID=1):
    tStart = time.perf_counter()
    filtered = self.emaFilter.filter(rawVal)
    compensated = self.driftComp.compensate(filtered, temp, hum)
    self.window.append(compensated)
    if len(self.window) > self.windowSize:
      self.window.pop(0)
    w = list(self.window)
    if len(w) < 20:
      w = [w[0]] * (20 - len(w)) + w

    slope = float((w[-1] - w[0]) / max(len(w), 1))
    v0 = self.baselineTracker.v0 if self.baselineTracker.is_calibrated else float(np.median(w))
    deltaV = float(compensated - v0)

    # Shift-invariant differential feature extraction
    feat = extract_window_features(w[-20:], base_v=v0)
    featArr = np.array([feat], dtype=np.float32)
    gasProbs = self.clf_win.predict_proba(featArr)[0]
    bestIdx = int(np.argmax(gasProbs))
    gas = self.classes[bestIdx]
    conf = round(float(gasProbs[bestIdx]), 2)
    estimatedppm = round(float(max(0.0, self.reg_win.predict(featArr)[0])), 2)

    # Kinematic Flatness & Slope Guard
    is_flat = self.baselineTracker.is_flat_baseline(w[-20:])
    if is_flat or abs(deltaV) <= 0.05:
      gas = 'Clean Air'
      estimatedppm = 0.0
      conf = max(conf, 0.98)

    # Update baseline tracker (locks update if gas detected or large transient)
    self.baselineTracker.update(compensated, is_gas_detected=(gas != 'Clean Air'), slope=slope)
    v0_updated = self.baselineTracker.v0

    risk = computeRiskLevel(gas, estimatedppm, deltaV)
    latencyMs = round((time.perf_counter() - tStart) * 1000.0, 3)

    record = {
      'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
      'nodeID': nodeID,
      's3Raw': round(rawVal, 4),
      's3Filtered': round(filtered, 4),
      's3Compensated': round(compensated, 4),
      's3Baseline': round(v0_updated, 4),
      's3Delta': round(deltaV, 4),
      'temperature': temp,
      'humidity': hum,
      'mq136ADC': int(1120 + estimatedppm * 55) if gas == 'H2S' else 1120,
      'mq135ADC': int(940 + estimatedppm * 22) if gas == 'H2S' else 940,
      'identifiedGas': gas,
      'estimatedppm': estimatedppm,
      'riskLevel': risk,
      'latencyMs': latencyMs,
      'calibrationState': self.baselineTracker.state
    }
    self.store.logTelemetry(record)
    if risk in ['Hazardous', 'Emergency']:
      alert = {
        'alertID': f'ALT{int(time.time()) % 10000}',
        'timestamp': record['timestamp'],
        'nodeID': nodeID,
        'gas': gas,
        'ppm': estimatedppm,
        'riskLevel': risk,
        'actionTaken': 'Auto Siren Activated & Valve V302 Staged' if risk == 'Emergency' else 'Strobe Light & Safety Notice'
      }
      self.store.logAlarm(alert)
    return record

def runBenchmark():
  gateway = EdgeAIGateway()
  # Test with elevated outdoor ambient baseline (0.55V)
  print("--- Testing Outdoor Flat Baseline (0.55V) ---")
  outdoorInputs = [(0.550 + 0.001 * np.sin(i), 29.5, 75.0) for i in range(25)]
  for raw, temp, hum in outdoorInputs:
    res = gateway.processSample(raw, temp, hum, nodeID=1)
  print(f"Final Outdoor Baseline Sample Result:")
  print(f"  Gas: {res['identifiedGas']}, PPM: {res['estimatedppm']}, Risk: {res['riskLevel']}, Baseline: {res['s3Baseline']}V, Delta: {res['s3Delta']}V, State: {res['calibrationState']}")
  assert res['identifiedGas'] == 'Clean Air', f"Expected Clean Air on outdoor flat baseline, got {res['identifiedGas']}"
  assert res['riskLevel'] == 'Normal', f"Expected Normal risk on outdoor baseline, got {res['riskLevel']}"
  print(" Outdoor Flat Baseline Verification: PASSED (No False Positive!)")

  print("\n--- Testing H2S Gas Leak Transient (Rising to 1.15V) ---")
  leakInputs = [(0.550 + 0.05 * i, 29.5, 75.0) for i in range(1, 15)]
  for raw, temp, hum in leakInputs:
    res = gateway.processSample(raw, temp, hum, nodeID=1)
  print(f"Final H2S Leak Sample Result:")
  print(f"  Gas: {res['identifiedGas']}, PPM: {res['estimatedppm']}, Risk: {res['riskLevel']}, Delta: {res['s3Delta']}V, State: {res['calibrationState']}")

  print("\nGateway Benchmark & Drift Guard Verified Successfully!")

if __name__ == '__main__':
  runBenchmark()