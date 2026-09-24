import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import json
import time
import pickle
import asyncio
import uvicorn
import numpy as np
import pandas as pd
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from backend.train import extract_window_features, extract_pulse_features, parse_pulse_num
from backend.calibration import BaselineTracker
from backend.firebase import FirebaseService

classesPath = 'backend/classes.json'
modelGasPath = 'backend/model_gas.pkl'
modelPpmPath = 'backend/model_ppm.pkl'
modelPulseGasPath = 'backend/model_pulse_gas.pkl'
modelPulsePpmPath = 'backend/model_pulse_ppm.pkl'

if not (os.path.exists(classesPath) and os.path.exists(modelGasPath) and os.path.exists(modelPpmPath)):
    from backend.train import trainModel
    trainModel()

firebaseService = FirebaseService()
baselineTracker = BaselineTracker(warmup_points=20)

app = FastAPI(title="Electronic Nose Edge AI Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/dashboard', StaticFiles(directory='dashboard', html=True), name='dashboard')
if os.path.exists('standee'):
    app.mount('/standee', StaticFiles(directory='standee', html=True), name='standee')

@app.get('/')
def getRoot():
    return RedirectResponse(url='/dashboard/index.html')

with open(classesPath, 'r', encoding='utf-8') as f:
    meta = json.load(f)

classes = meta['classes']

with open(modelGasPath, 'rb') as f:
    clf_win = pickle.load(f)
with open(modelPpmPath, 'rb') as f:
    reg_win = pickle.load(f)
with open(modelPulseGasPath, 'rb') as f:
    clf_pulse = pickle.load(f)
with open(modelPulsePpmPath, 'rb') as f:
    reg_pulse = pickle.load(f)


def buildScenarios():
    h2sDf = pd.read_csv('data/h2s_sensor_1_clean.csv')
    nh3Df = pd.read_csv('data/nh3_sensor_1_clean.csv')
    airDf = pd.read_csv('data/air_clean_sensor_1_clean.csv')

    point_cols = [c for c in airDf.columns if c.startswith('Point_')]

    # Pick representative pulses
    h2s_pulse = h2sDf[h2sDf['Pulse_Index'] == 'Pulse_95'][point_cols].values[0].tolist() if 'Pulse_95' in h2sDf['Pulse_Index'].values else h2sDf[point_cols].iloc[-1].values.tolist()
    nh3_pulse = nh3Df[nh3Df['Pulse_Index'] == 'Pulse_60'][point_cols].values[0].tolist() if 'Pulse_60' in nh3Df['Pulse_Index'].values else nh3Df[point_cols].iloc[20].values.tolist()
    air_pulse = airDf[point_cols].iloc[5].values.tolist()

    # Build sequence for Field Scenario: Baseline (Air) -> H2S Leak -> Recovery -> NH3 Exposure -> Purge
    fieldPoints = []

    # 1. Baseline Clean Air (25s)
    for idx, v in enumerate(air_pulse[:25]):
        noise = float(np.random.normal(0, 0.002))
        fieldPoints.append({
            's3': round(float(v), 4),
            's3Raw': round(float(v + noise), 4),
            'temperature': round(28.5 + 0.1 * np.sin(idx * 0.2), 1),
            'humidity': round(64.0 + 0.3 * np.cos(idx * 0.1), 1),
            'trueGas': 'Clean Air',
            'trueppm': 0.0,
            'phase': 'Baseline'
        })

    # 2. H2S Gas Leak Pulse (0s to 60s)
    for idx, v in enumerate(h2s_pulse):
        noise = float(np.random.normal(0, 0.003))
        ppm_est = 10.0 if (20 <= idx <= 125) else (10.0 * (v - 0.5) / 1.7 if v > 0.5 else 0.0)
        fieldPoints.append({
            's3': round(float(v), 4),
            's3Raw': round(float(v + noise), 4),
            'temperature': round(29.2 + 0.2 * np.sin(idx * 0.1), 1),
            'humidity': round(65.1 + 0.1 * np.cos(idx * 0.1), 1),
            'trueGas': 'H2S' if idx <= 140 else 'Clean Air',
            'trueppm': round(float(max(0.0, ppm_est)), 1),
            'phase': 'H2S Leakage' if idx <= 130 else 'Scrubber Purge'
        })

    # 3. Intermediate Recovery (20s)
    for idx, v in enumerate(air_pulse[20:40]):
        noise = float(np.random.normal(0, 0.002))
        fieldPoints.append({
            's3': round(float(v), 4),
            's3Raw': round(float(v + noise), 4),
            'temperature': 28.7,
            'humidity': 64.2,
            'trueGas': 'Clean Air',
            'trueppm': 0.0,
            'phase': 'Safe Baseline'
        })

    # 4. NH3 Gas Exposure Pulse (0s to 60s)
    for idx, v in enumerate(nh3_pulse):
        noise = float(np.random.normal(0, 0.003))
        ppm_est = 50.0 if (20 <= idx <= 125) else (50.0 * (v - 0.4) / 1.8 if v > 0.4 else 0.0)
        fieldPoints.append({
            's3': round(float(v), 4),
            's3Raw': round(float(v + noise), 4),
            'temperature': round(29.5 + 0.1 * np.cos(idx * 0.15), 1),
            'humidity': round(63.8 + 0.2 * np.sin(idx * 0.2), 1),
            'trueGas': 'NH3' if idx <= 140 else 'Clean Air',
            'trueppm': round(float(max(0.0, ppm_est)), 1),
            'phase': 'NH3 Detection' if idx <= 130 else 'Post-Purge Recovery'
        })

    # 5. Final Clean Air Recovery (25s)
    for idx, v in enumerate(air_pulse[50:75]):
        noise = float(np.random.normal(0, 0.002))
        fieldPoints.append({
            's3': round(float(v), 4),
            's3Raw': round(float(v + noise), 4),
            'temperature': 28.4,
            'humidity': 64.0,
            'trueGas': 'Clean Air',
            'trueppm': 0.0,
            'phase': 'Baseline Settled'
        })

    return {
        'fieldScenario': fieldPoints,
        'h2sRun': [{
            's3': round(float(v), 4),
            's3Raw': round(float(v + np.random.normal(0, 0.002)), 4),
            'temperature': 29.0,
            'humidity': 65.0,
            'trueGas': 'H2S' if idx <= 140 else 'Clean Air',
            'trueppm': 10.0 if (20 <= idx <= 125) else 0.0,
            'phase': 'H2S 10ppm Test'
        } for idx, v in enumerate(h2s_pulse)],
        'nh3Run': [{
            's3': round(float(v), 4),
            's3Raw': round(float(v + np.random.normal(0, 0.002)), 4),
            'temperature': 29.0,
            'humidity': 63.5,
            'trueGas': 'NH3' if idx <= 140 else 'Clean Air',
            'trueppm': 50.0 if (20 <= idx <= 125) else 0.0,
            'phase': 'NH3 50ppm Test'
        } for idx, v in enumerate(nh3_pulse)],
        'airRun': [{
            's3': round(float(v), 4),
            's3Raw': round(float(v + np.random.normal(0, 0.0015)), 4),
            'temperature': 28.5,
            'humidity': 64.0,
            'trueGas': 'Clean Air',
            'trueppm': 0.0,
            'phase': 'Clean Air Baseline'
        } for idx, v in enumerate(air_pulse)]
    }

scenarios = buildScenarios()


def computeRiskLevel(gas, ppmVal, deltaV):
    """
    Decoupled risk calculation: evaluates risk based on estimated PPM and differential ΔV.
    Eliminates false alarms caused by high static outdoor baseline voltages (0.35V - 0.70V).
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


def runInference(windowValues, compS3):
    tStart = time.perf_counter()
    w = list(windowValues)
    if len(w) < 20:
        fillVal = w[0] if w else float(compS3)
        w = [fillVal] * (20 - len(w)) + w

    w_20 = w[-20:]
    slope = float((w_20[-1] - w_20[0]) / max(len(w_20), 1))
    v0 = baselineTracker.v0 if baselineTracker.is_calibrated else float(np.median(w_20))
    deltaV = float(compS3 - v0)

    # Shift-invariant differential feature extraction
    feat = extract_window_features(w_20, base_v=v0)
    featArr = np.array([feat], dtype=np.float32)

    gasProbs = clf_win.predict_proba(featArr)[0]
    bestIdx = int(np.argmax(gasProbs))
    predGas = classes[bestIdx]
    conf = int(round(float(gasProbs[bestIdx]) * 100))
    probMap = {classes[i]: round(float(gasProbs[i]), 4) for i in range(len(classes))}

    estimatedppm = round(float(max(0.0, reg_win.predict(featArr)[0])), 2)

    # Kinematic Flatness & Slope Guard (Prevents outdoor false alarm)
    is_flat = baselineTracker.is_flat_baseline(w_20)
    if is_flat or abs(deltaV) <= 0.05:
        predGas = 'Clean Air'
        estimatedppm = 0.0
        conf = max(conf, 98)

    # Update baseline tracker (adapts slowly in clean air, locks during gas surge)
    baselineTracker.update(compS3, is_gas_detected=(predGas != 'Clean Air'), slope=slope)
    v0_updated = baselineTracker.v0

    risk = computeRiskLevel(predGas, estimatedppm, deltaV)
    latencyMs = round((time.perf_counter() - tStart) * 1000, 2)
    return {
        'gas': predGas,
        'confidence': conf,
        'probabilities': probMap,
        'estimatedppm': estimatedppm,
        'riskLevel': risk,
        'baseline': round(v0_updated, 4),
        'delta': round(deltaV, 4),
        'calibrationState': baselineTracker.state,
        'latencyMs': latencyMs
    }


def runPulseInference(points):
    if len(points) != 250:
        return None
    tStart = time.perf_counter()
    base_v = float(np.median(points[:10]))
    feat = extract_pulse_features(points, base_v=base_v)
    featArr = np.array([feat], dtype=np.float32)

    probs = clf_pulse.predict_proba(featArr)[0]
    bestIdx = int(np.argmax(probs))
    predGas = classes[bestIdx]
    conf = int(round(float(probs[bestIdx]) * 100))
    probMap = {classes[i]: round(float(probs[i]), 4) for i in range(len(classes))}

    estimatedppm = round(float(max(0.0, reg_pulse.predict(featArr)[0])), 2)
    latencyMs = round((time.perf_counter() - tStart) * 1000, 2)
    deltaV = float(np.max(points) - base_v)

    # Flat baseline check on pulse level
    if deltaV < 0.08 or float(np.std(points)) < 0.015:
        predGas = 'Clean Air'
        estimatedppm = 0.0
        conf = max(conf, 98)

    risk = computeRiskLevel(predGas, estimatedppm, deltaV)

    return {
        'gas': predGas,
        'confidence': conf,
        'probabilities': probMap,
        'estimatedppm': estimatedppm,
        'riskLevel': risk,
        'latencyMs': latencyMs,
        'baseline': round(base_v, 4),
        'delta': round(deltaV, 4),
        'features': {
            'min': round(float(np.min(points)), 4),
            'max': round(float(np.max(points)), 4),
            'delta': round(deltaV, 4),
            'auc': round(float(np.sum(points)), 2),
            'mean': round(float(np.mean(points)), 4),
            'std': round(float(np.std(points)), 4)
        }
    }


# =========================================================================
# REST API ENDPOINTS
# =========================================================================
@app.get('/health')
def health():
    return {'status': 'ok', 'model': 'RandomForest_EdgeAI_DualMode_ShiftInvariant'}

@app.get('/api/metrics')
def getMetrics():
    metricsPath = 'dashboard/model_metrics.json'
    if os.path.exists(metricsPath):
        with open(metricsPath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return meta

@app.get('/api/profiles')
def getProfiles():
    profPath = 'dashboard/gas_profiles.json'
    if os.path.exists(profPath):
        with open(profPath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@app.get('/api/pulse_samples')
def getPulseSamples():
    samplePath = 'dashboard/pulse_samples.json'
    if os.path.exists(samplePath):
        with open(samplePath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.post('/api/predict_pulse')
async def predictPulse(req: Request):
    data = await req.json()
    points = data.get('points', [])
    if len(points) != 250:
        return JSONResponse({'error': 'Expected 250 points array'}, status_code=400)
    res = runPulseInference(points)
    return res

@app.post('/api/calibrate/zero')
async def zeroCalibrate(req: Request = None):
    target_v = None
    if req:
        try:
            body = await req.json()
            target_v = body.get('targetVoltage')
        except Exception:
            pass
    latest = firebaseService.getLatest()
    recent = [float(latest.get('voltage1', 0.55))] if latest else None
    new_v0 = baselineTracker.recalibrate(recent_samples=recent, target_val=target_v)
    return {
        'status': 'ok',
        'baselineVoltage': round(new_v0, 4),
        'state': baselineTracker.state,
        'message': f'Zero calibration successful. Baseline anchored at {new_v0:.4f}V.'
    }

@app.get('/api/calibrate/status')
def getCalibrateStatus():
    return baselineTracker.get_status()

@app.get('/api/firebase/status')
def getFirebaseStatus():
    return firebaseService.getStatus()

@app.get('/api/firebase/latest')
def getFirebaseLatest():
    latest = firebaseService.getLatest()
    if latest:
        v1 = float(latest.get('voltage1', 1.0))
        inf = runInference([v1] * 20, v1)
        return {
            'telemetry': latest,
            'inference': inf
        }
    return {'telemetry': None, 'inference': None}

@app.post('/api/firebase/air_type')
async def setFirebaseAir(req: Request):
    data = await req.json()
    air = data.get('airType', 'CleanAir')
    firebaseService.setAirType(air)
    return {'status': 'ok', 'activeAir': air}

@app.post('/api/firebase/flush')
def flushFirebase():
    firebaseService.flushDisk()
    return {'status': 'ok', 'message': 'Buffer flushed to disk'}

@app.websocket('/ws/live_experiment')
async def liveExperimentWs(ws: WebSocket):
    await ws.accept()
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue(maxsize=200)

    def onPacket(packet):
        try:
            loop.call_soon_threadsafe(queue.put_nowait, packet)
        except Exception:
            pass

    firebaseService.subscribe(onPacket)

    state = {
        'recentWindow': [],
        'cyclePoints': [None] * 250,
        'cycleCount': 1,
        'lastPoint': -1
    }

    async def listenClient():
        try:
            while True:
                msg = await ws.receive_text()
                cmd = json.loads(msg)
                action = cmd.get('action')
                if action == 'setAirType':
                    firebaseService.setAirType(cmd.get('airType', 'CleanAir'))
                elif action == 'flush':
                    firebaseService.flushDisk()
                elif action == 'zeroCalibrate':
                    baselineTracker.recalibrate()
        except Exception:
            pass

    listenTask = asyncio.create_task(listenClient())

    try:
        init_st = firebaseService.getStatus()
        await ws.send_text(json.dumps({
            'type': 'connected',
            'status': init_st,
            'calibration': baselineTracker.get_status()
        }))

        while True:
            packet = await queue.get()
            pt = int(packet.get('point', 0))
            v1 = float(packet.get('voltage1', 0.0))
            v2 = float(packet.get('voltage2', 0.0))

            cycleSummary = None
            if state['lastPoint'] >= 200 and pt < 30:
                state['cycleCount'] += 1
                valid_pts = [p for p in state['cyclePoints'] if p is not None]
                if len(valid_pts) >= 150:
                    fill_val = float(np.mean(valid_pts))
                    full_p = [p if p is not None else fill_val for p in state['cyclePoints']]
                    cycleSummary = runPulseInference(full_p)
                state['cyclePoints'] = [None] * 250

            state['lastPoint'] = pt
            if 0 <= pt < 250:
                state['cyclePoints'][pt] = v1

            state['recentWindow'].append(v1)
            if len(state['recentWindow']) > 20:
                state['recentWindow'].pop(0)

            win_inf = runInference(state['recentWindow'], v1)

            response = {
                'type': 'telemetry',
                'cycle': state['cycleCount'],
                'point': pt,
                'voltage1': v1,
                'voltage2': v2,
                'telemetry': packet,
                'inference': win_inf,
                'baseline': win_inf.get('baseline'),
                'delta': win_inf.get('delta'),
                'calibrationState': win_inf.get('calibrationState'),
                'cycleSummary': cycleSummary,
                'timestamp': packet.get('timestamp')
            }
            await ws.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass
    finally:
        firebaseService.unsubscribe(onPacket)
        listenTask.cancel()


# =========================================================================
# WEBSOCKET STREAMING & INFERENCE
# =========================================================================
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
        'speedMs': 800,
        'window': [],
        'lastEma': None
    }

    async def listenCommands():
        try:
            while True:
                msg = await ws.receive_text()
                data = json.loads(msg)
                action = data.get('action')
                if action == 'pause':
                    state['isPlaying'] = False
                elif action == 'play':
                    state['isPlaying'] = True
                elif action == 'reset':
                    state['index'] = 0
                    state['window'] = []
                elif action == 'setMode':
                    m = data.get('mode', 'fieldScenario')
                    if m in scenarios:
                        state['mode'] = m
                        state['index'] = 0
                        state['window'] = []
                elif action == 'setSpeed':
                    mult = float(data.get('multiplier', 1.0))
                    state['speedMs'] = max(100, int(800 / mult))
                elif action == 'zeroCalibrate':
                    baselineTracker.recalibrate()
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

                inf = runInference(state['window'], compVal)
                gas = inf['gas']
                ppmVal = inf['estimatedppm']
                risk = inf['riskLevel']

                slopeVal = (state['window'][-1] - state['window'][0]) / max(len(state['window']), 1) if len(state['window']) > 1 else 0.0
                horizonSteps = [5, 10, 15, 20]
                traj = [round(float(compVal + slopeVal * s), 3) for s in horizonSteps]
                maxProj = max(compVal, *traj)
                isEmerg = (gas == 'H2S' and maxProj >= 2.45) or (gas == 'H2S' and slopeVal > 0.015)
                tte = None
                if isEmerg:
                    rate = max(0.002, slopeVal)
                    tte = max(3, min(25, round((2.45 - compVal) / rate)))

                packet = {
                    'timestamp': time.strftime('%I:%M:%S %p'),
                    's3': round(compVal, 4),
                    's3Raw': round(rawVal, 4),
                    's3Baseline': inf.get('baseline'),
                    's3Delta': inf.get('delta'),
                    'calibrationState': inf.get('calibrationState'),
                    'temperature': temp,
                    'humidity': hum,
                    'trueGas': pt['trueGas'],
                    'trueppm': pt['trueppm'],
                    'phase': pt.get('phase', 'Monitoring'),
                    'gas': gas,
                    'confidence': inf['confidence'],
                    'probabilities': inf['probabilities'],
                    'estimatedppm': ppmVal,
                    'riskLevel': risk,
                    'features': {
                        'mean': round(float(np.mean(state['window'])), 4),
                        'std': round(float(np.std(state['window'])), 4),
                        'max': round(float(np.max(state['window'])), 4),
                        'min': round(float(np.min(state['window'])), 4),
                        'range': round(float(np.max(state['window']) - np.min(state['window'])), 4),
                        'slope': round(float(slopeVal), 5)
                    },
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
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8001))
    print(f"Starting Electronic Nose Edge AI Gateway on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)