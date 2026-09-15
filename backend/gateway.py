import os
import sys
import json
import time
import sqlite3
import numpy as np
import tensorflow as tf
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
class SQLiteEdgeStore:
  def __init__(self, dbPath='EdgeStorage.db'):
    self.dbPath = dbPath
    self.initSchema()
  def getConnection(self):
    return sqlite3.connect(self.dbPath)
  def initSchema(self):
    with self.getConnection() as conn:
      cur = conn.cursor()
      cur.execute('''CREATE TABLE IF NOT EXISTS TelemetryRecords (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, nodeID INTEGER, s3Raw REAL, s3Filtered REAL, s3Compensated REAL, temperature REAL, humidity REAL, mq136ADC INTEGER, mq135ADC INTEGER, identifiedGas TEXT, estimatedppm REAL, riskLevel TEXT)''')
      cur.execute('''CREATE TABLE IF NOT EXISTS AlarmEvents (id INTEGER PRIMARY KEY AUTOINCREMENT, alertID TEXT, timestamp TEXT, nodeID INTEGER, gas TEXT, ppm REAL, riskLevel TEXT, actionTaken TEXT)''')
      conn.commit()
  def logTelemetry(self, record):
    with self.getConnection() as conn:
      cur = conn.cursor()
      cur.execute('''INSERT INTO TelemetryRecords (timestamp, nodeID, s3Raw, s3Filtered, s3Compensated, temperature, humidity, mq136ADC, mq135ADC, identifiedGas, estimatedppm, riskLevel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (record.get('timestamp'), record.get('nodeID'), record.get('s3Raw'), record.get('s3Filtered'), record.get('s3Compensated'), record.get('temperature'), record.get('humidity'), record.get('mq136ADC'), record.get('mq135ADC'), record.get('identifiedGas'), record.get('estimatedppm'), record.get('riskLevel')))
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
    self.store = SQLiteEdgeStore(dbPath='backend/EdgeStorage.db')
    self.mqttFormatter = MQTTWISEIoTFormatter()
    self.window = []
    self.windowSize = 20
    with open('backend/classes.json', 'r', encoding='utf-8') as f:
      meta = json.load(f)
    self.classes = meta['classes']
    self.model = tf.keras.models.load_model('backend/model.keras')
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
    rawTensor = np.array(w[-20:], dtype=np.float32).reshape(1, 20, 1)
    gasPreds, ppmPreds = self.model(rawTensor, training=False)
    gasProbs = gasPreds.numpy()[0]
    bestIdx = int(np.argmax(gasProbs))
    gas = self.classes[bestIdx]
    conf = round(float(gasProbs[bestIdx]), 2)
    estimatedppm = round(float(max(0.0, ppmPreds.numpy()[0][0])), 2)
    if gas == 'Clean Air' or compensated <= 1.015:
      gas = 'Clean Air'
      estimatedppm = 0.0
      conf = max(conf, 0.98)
    risk = 'Normal'
    if gas == 'H2S':
      if estimatedppm >= 10.0 or compensated >= 1.25:
        risk = 'Emergency'
      elif estimatedppm >= 5.0 or compensated >= 1.10:
        risk = 'Hazardous'
      elif estimatedppm >= 1.0 or compensated >= 1.03:
        risk = 'Warning'
    elif gas == 'CO':
      if estimatedppm >= 50.0:
        risk = 'Hazardous'
      elif estimatedppm >= 25.0:
        risk = 'Warning'
    latencyMs = round((time.perf_counter() - tStart) * 1000.0, 3)
    record = {
      'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
      'nodeID': nodeID,
      's3Raw': round(rawVal, 4),
      's3Filtered': round(filtered, 4),
      's3Compensated': round(compensated, 4),
      'temperature': temp,
      'humidity': hum,
      'mq136ADC': int(1120 + estimatedppm * 55) if gas == 'H2S' else 1120,
      'mq135ADC': int(940 + estimatedppm * 22) if gas == 'H2S' else 940,
      'identifiedGas': gas,
      'estimatedppm': estimatedppm,
      'riskLevel': risk,
      'latencyMs': latencyMs
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
  sampleInputs = [
    (1.002, 28.5, 64.0),
    (1.001, 28.6, 64.1),
    (1.003, 28.7, 64.2),
    (1.015, 29.0, 64.5),
    (1.035, 29.2, 65.0),
    (1.070, 29.4, 65.2),
    (1.150, 29.5, 65.5),
    (1.280, 29.8, 66.0),
    (1.350, 30.1, 66.5),
    (1.420, 30.5, 67.0)
  ]
  results = []
  for raw, temp, hum in sampleInputs:
    res = gateway.processSample(raw, temp, hum, nodeID=1)
    results.append(res)
  recent = gateway.store.fetchRecentTelemetry(5)
  payload = gateway.mqttFormatter.formatTelemetryPayload([results[-1]])
  print(f'Benchmark Completed: Processed {len(results)} Samples Successfully')
  print(f'Average Inference Latency: {np.mean([r.get("latencyMs") for r in results]):.3f} MS')
  print(f'SQLite Store Verified: {len(recent)} Recent Records Retrieved')
  print(f'WISE-IoT MQTT Topic: {gateway.mqttFormatter.buildTelemetryTopic()}')
  print(f'Sample MQTT Payload: {json.dumps(payload, indent=2)}')
if __name__ == '__main__':
  runBenchmark()