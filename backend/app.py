import os
import json
import time
import pickle
import asyncio
import uvicorn
import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
classesPath = 'backend/classes.json'
modelPath = 'backend/model.keras'
scalerPath = 'backend/scaler.pkl'
if not (os.path.exists(classesPath) and os.path.exists(scalerPath) and os.path.exists(modelPath)):
  from backend.train import trainModel
  trainModel()
app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)
app.mount('/dashboard', StaticFiles(directory='dashboard', html=True), name='dashboard')
@app.get('/')
def getRoot():
  return RedirectResponse(url='/dashboard/index.html')
with open(classesPath, 'r', encoding='utf-8') as f:
  meta = json.load(f)
classes = meta['classes']
model = tf.keras.models.load_model(modelPath)
def buildScenarios():
  h2sDf = pd.read_csv('data/H2S.csv')
  coDf = pd.read_csv('data/CO.csv')
  h2sRaw = h2sDf['S3'].values
  coRaw = coDf['S3'].values
  h2sSlice = h2sRaw[1400:1520].tolist()
  coSlice = coRaw[1420:1510].tolist()
  np.random.seed(42)
  airSlice = [round(float(1.000 + np.random.normal(0, 0.0012)), 4) for _ in range(40)]
  fieldPoints = []
  for idx, v in enumerate(airSlice[:15]):
    noise = float(np.random.normal(0, 0.002))
    rawVal = round(float(v + noise), 4)
    temp = round(28.5 + 0.1 * np.sin(idx * 0.2), 1)
    hum = round(64.0 + 0.3 * np.cos(idx * 0.1), 1)
    fieldPoints.append({'s3': round(float(v), 4), 's3Raw': rawVal, 'temperature': temp, 'humidity': hum, 'trueGas': 'Air', 'ppm': 0.0, 'phase': 'Baseline'})
  for idx, v in enumerate(coSlice[:40]):
    noise = float(np.random.normal(0, 0.003))
    rawVal = round(float(v + noise), 4)
    ppmVal = round(float(max(0.0, (v - 1.0) * 820.0)), 1)
    temp = round(29.0 + 0.2 * np.sin(idx * 0.3), 1)
    hum = round(63.5 - 0.1 * idx, 1)
    fieldPoints.append({'s3': round(float(v), 4), 's3Raw': rawVal, 'temperature': temp, 'humidity': hum, 'trueGas': 'CO', 'ppm': ppmVal, 'phase': 'COPuff'})
  for idx, v in enumerate(airSlice[:15]):
    noise = float(np.random.normal(0, 0.002))
    rawVal = round(float(v + noise), 4)
    temp = round(28.7 + 0.05 * idx, 1)
    hum = round(64.2, 1)
    fieldPoints.append({'s3': round(float(v), 4), 's3Raw': rawVal, 'temperature': temp, 'humidity': hum, 'trueGas': 'Air', 'ppm': 0.0, 'phase': 'Recovery'})
  for idx, v in enumerate(h2sSlice[:60]):
    noise = float(np.random.normal(0, 0.004))
    rawVal = round(float(v + noise), 4)
    ppmVal = round(float(max(0.0, (v - 1.0) * 7.8)), 2)
    temp = round(29.4 + 0.15 * np.cos(idx * 0.2), 1)
    hum = round(65.0 + 0.2 * np.sin(idx * 0.1), 1)
    fieldPoints.append({'s3': round(float(v), 4), 's3Raw': rawVal, 'temperature': temp, 'humidity': hum, 'trueGas': 'H2S', 'ppm': ppmVal, 'phase': 'H2SLeak'})
  for idx, v in enumerate(airSlice[:15]):
    noise = float(np.random.normal(0, 0.002))
    rawVal = round(float(v + noise), 4)
    temp = round(28.6, 1)
    hum = round(64.5, 1)
    fieldPoints.append({'s3': round(float(v), 4), 's3Raw': rawVal, 'temperature': temp, 'humidity': hum, 'trueGas': 'Air', 'ppm': 0.0, 'phase': 'Purge'})
  return {
    'fieldScenario': fieldPoints,
    'H2SRun': [{'s3': round(float(v), 4), 's3Raw': round(float(v + np.random.normal(0, 0.003)), 4), 'temperature': 29.5, 'humidity': 65.2, 'trueGas': 'H2S', 'ppm': round(float(max(0.0, (v - 1.0) * 7.8)), 2), 'phase': 'H2SLeak'} for v in h2sSlice],
    'CORun': [{'s3': round(float(v), 4), 's3Raw': round(float(v + np.random.normal(0, 0.003)), 4), 'temperature': 29.1, 'humidity': 63.8, 'trueGas': 'CO', 'ppm': round(float(max(0.0, (v - 1.0) * 820.0)), 1), 'phase': 'COPuff'} for v in coSlice],
    'airRun': [{'s3': round(float(v), 4), 's3Raw': round(float(v + np.random.normal(0, 0.0015)), 4), 'temperature': 28.5, 'humidity': 64.0, 'trueGas': 'Air', 'ppm': 0.0, 'phase': 'Baseline'} for v in airSlice]
  }
scenarios = buildScenarios()
def extractFeatures(w):
  n = len(w)
  meanVal = float(np.mean(w))
  stdVal = float(np.std(w))
  slopeVal = float((w[-1] - w[0]) / n)
  minVal = float(np.min(w))
  maxVal = float(np.max(w))
  rngVal = maxVal - minVal
  deltaVal = float(w[-1] - w[0])
  sortedW = np.sort(w)
  q25 = float(sortedW[int(n * 0.25)])
  q75 = float(sortedW[int(n * 0.75)])
  diffs = [w[i] - w[i - 1] for i in range(1, n)]
  diffMean = float(np.mean(diffs)) if diffs else 0.0
  diffStd = float(np.std(diffs)) if diffs else 0.0
  return [meanVal, stdVal, maxVal, minVal, rngVal, deltaVal, slopeVal, diffMean, diffStd, q75 - q25]
def runInference(windowValues, compS3):
  tStart = time.perf_counter()
  w = list(windowValues)
  if len(w) < 20:
    fillVal = w[0] if w else float(compS3)
    w = [fillVal] * (20 - len(w)) + w
  rawTensor = np.array(w[-20:], dtype=np.float32).reshape(1, 20, 1)
  gasPreds, ppmPreds = model(rawTensor, training=False)
  gasProbs = gasPreds.numpy()[0]
  bestIdx = int(np.argmax(gasProbs))
  predGas = classes[bestIdx]
  conf = int(round(float(gasProbs[bestIdx]) * 100))
  probMap = {classes[i]: round(float(gasProbs[i]), 4) for i in range(len(classes))}
  compVal = float(compS3)
  estimatedppm = round(float(max(0.0, ppmPreds.numpy()[0][0])), 2)
  if predGas == 'Clean Air' or compVal <= 1.015:
    predGas = 'Clean Air'
    estimatedppm = 0.0
    conf = max(conf, 98)
  latencyMs = round((time.perf_counter() - tStart) * 1000, 2)
  return {
    'gas': predGas,
    'confidence': conf,
    'probabilities': probMap,
    'estimatedppm': estimatedppm,
    'latencyMs': latencyMs
  }
@app.get('/health')
def health():
  return {'status': 'ok', 'model': 'MultiTask1DCNN'}
@app.websocket('/predict')
async def predictWs(ws: WebSocket):
  await ws.accept()
  try:
    while True:
      msg = await ws.receive_text()
      payload = json.loads(msg)
      win = payload.get('window', payload.get('features', []))
      compVal = payload.get('compS3', 1.0)
      result = runInference(win, compVal)
      await ws.send_text(json.dumps(result))
  except WebSocketDisconnect:
    pass
@app.websocket('/stream')
async def streamWs(ws: WebSocket):
  await ws.accept()
  state = {
    'mode': 'fieldScenario',
    'index': 0,
    'isPlaying': True,
    'speedMs': 1000,
    'window': [],
    'lastEma': None
  }
  async def listenCommands():
    try:
      while True:
        msg = await ws.receive_text()
        data = json.loads(msg)
        action = data.get('action')
        if action == 'setMode':
          newMode = data.get('mode', 'fieldScenario')
          if newMode in scenarios:
            state['mode'] = newMode
            state['index'] = 0
            state['window'] = []
            state['lastEma'] = None
        elif action == 'togglePlay':
          state['isPlaying'] = not state['isPlaying']
        elif action == 'pause':
          state['isPlaying'] = False
        elif action == 'play':
          state['isPlaying'] = True
        elif action == 'setSpeed':
          mult = float(data.get('multiplier', 1.0))
          state['speedMs'] = max(100, int(1000 / mult))
    except Exception:
      pass
  cmdTask = asyncio.create_task(listenCommands())
  try:
    while True:
      if state['isPlaying']:
        series = scenarios.get(state['mode'], scenarios['fieldScenario'])
        idx = state['index'] % len(series)
        pt = series[idx]
        state['index'] = (idx + 1) % len(series)
        rawVal = float(pt['s3Raw'])
        temp = float(pt['temperature'])
        hum = float(pt['humidity'])
        if state['lastEma'] is None:
          state['lastEma'] = rawVal
        else:
          state['lastEma'] = 0.2 * rawVal + 0.8 * state['lastEma']
        compFactor = 1.0 + 0.0035 * (temp - 25.0) + 0.0015 * (hum - 60.0)
        compVal = state['lastEma'] / compFactor
        state['window'].append(compVal)
        if len(state['window']) > 20:
          state['window'].pop(0)
        feat = extractFeatures(state['window']) if len(state['window']) >= 3 else None
        if len(state['window']) >= 3:
          inf = runInference(state['window'], compVal)
        else:
          inf = {
            'gas': 'Clean Air',
            'confidence': 98,
            'probabilities': {'Clean Air': 0.98, 'CO': 0.01, 'H2S': 0.01},
            'estimatedppm': 0.0,
            'latencyMs': 0.5
          }
        gas = inf['gas']
        ppmVal = inf['estimatedppm']
        risk = 'Normal'
        if gas == 'H2S':
          if ppmVal >= 10.0 or compVal >= 1.25:
            risk = 'Emergency'
          elif ppmVal >= 5.0 or compVal >= 1.10:
            risk = 'Hazardous'
          elif ppmVal >= 1.0 or compVal >= 1.03:
            risk = 'Warning'
        elif gas == 'CO':
          if ppmVal >= 50.0:
            risk = 'Hazardous'
          elif ppmVal >= 25.0:
            risk = 'Warning'
        slopeVal = feat[6] if feat else 0.0
        horizonSteps = [5, 10, 15, 20]
        traj = [round(float(compVal + slopeVal * s), 3) for s in horizonSteps]
        maxProj = max(compVal, *traj)
        isEmerg = (gas == 'H2S' and maxProj >= 1.25) or (gas == 'H2S' and slopeVal > 0.008)
        tte = None
        if isEmerg:
          rate = max(0.002, slopeVal)
          tte = max(3, min(25, round((1.25 - compVal) / rate)))
        packet = {
          'timestamp': time.strftime('%I:%M:%S %p'),
          's3': round(compVal, 4),
          's3Raw': round(rawVal, 4),
          'temperature': temp,
          'humidity': hum,
          'trueGas': pt['trueGas'],
          'trueppm': pt['ppm'],
          'phase': pt.get('phase', 'Monitoring'),
          'gas': gas,
          'confidence': inf['confidence'],
          'probabilities': inf['probabilities'],
          'estimatedppm': ppmVal,
          'riskLevel': risk,
          'features': {
            'mean': round(feat[0], 5),
            'std': round(feat[1], 5),
            'max': round(feat[2], 5),
            'min': round(feat[3], 5),
            'range': round(feat[4], 5),
            'delta': round(feat[5], 5),
            'slope': round(feat[6], 5),
            'diffmean': round(feat[7], 5),
            'diffstd': round(feat[8], 5),
            'iqr': round(feat[9], 5)
          } if feat else None,
          'prognostics': {
            'trajectoryPoints': traj,
            'maxProjectedS3': round(maxProj, 3),
            'isImminentEmergency': isEmerg,
            'timeToEmergencySec': tte
          },
          'latencyMs': inf['latencyMs'],
          'frameIndex': idx,
          'totalFrames': len(series),
          'mode': state['mode'],
          'isPlaying': state['isPlaying']
        }
        await ws.send_text(json.dumps(packet))
      await asyncio.sleep(state['speedMs'] / 1000.0)
  except WebSocketDisconnect:
    pass
  finally:
    cmdTask.cancel()
if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8001)