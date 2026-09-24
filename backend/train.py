import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix, classification_report, mean_absolute_error, r2_score
from sklearn.model_selection import StratifiedKFold, KFold

def parse_pulse_num(pulse_str):
    try:
        return int(str(pulse_str).replace('Pulse_', '').strip())
    except Exception:
        return 1

def extract_pulse_features(p):
    p = np.array(p, dtype=np.float32)
    v_min = float(np.min(p))
    v_max = float(np.max(p))
    delta_v = v_max - v_min
    auc = float(np.sum(p))
    mean_v = float(np.mean(p))
    std_v = float(np.std(p))
    peak_idx = int(np.argmax(p))
    rise_slope = float((v_max - p[0]) / max(peak_idx, 1))
    decay_slope = float((p[-1] - v_max) / max(len(p) - peak_idx, 1))
    
    # Key anchor samples along 60-second cycle
    anchors = [float(p[idx]) for idx in [15, 30, 50, 75, 100, 120, 140, 170, 200, 230]]
    
    feat = [v_min, v_max, delta_v, auc, mean_v, std_v, float(peak_idx), rise_slope, decay_slope] + anchors
    return feat

def extract_window_features(w, base_v=None):
    w = np.array(w, dtype=np.float32)
    n = len(w)
    mean_val = float(np.mean(w))
    std_val = float(np.std(w))
    min_val = float(np.min(w))
    max_val = float(np.max(w))
    rng_val = max_val - min_val
    delta_val = float(w[-1] - w[0])
    slope_val = float(delta_val / max(n, 1))
    q25 = float(np.percentile(w, 25))
    q75 = float(np.percentile(w, 75))
    diffs = np.diff(w)
    diff_mean = float(np.mean(diffs)) if len(diffs) > 0 else 0.0
    diff_std = float(np.std(diffs)) if len(diffs) > 0 else 0.0

    b = base_v if base_v is not None else min_val
    rel_amp = max_val - b
    ratio = max_val / max(b, 0.001)

    features = [mean_val, std_val, max_val, min_val, rng_val, delta_val, slope_val, diff_mean, diff_std, q75 - q25, rel_amp, ratio]
    features.extend([float(v) for v in w])
    return features


def trainModel():
    print("Loading cleaned sensor data...")
    air_df = pd.read_csv('data/air_clean_sensor_1_clean.csv')
    h2s_df = pd.read_csv('data/h2s_sensor_1_clean.csv')
    nh3_df = pd.read_csv('data/nh3_sensor_1_clean.csv')

    point_cols = [c for c in air_df.columns if c.startswith('Point_')]
    classes = ['Clean Air', 'H2S', 'NH3']
    label_map = {c: i for i, c in enumerate(classes)}

    # =========================================================================
    # 1. BUILD PULSE-LEVEL DATASET
    # =========================================================================
    pulse_X, pulse_gas, pulse_ppm, pulse_labels = [], [], [], []
    profiles = {
        'H2S': {'1ppm': [], '5ppm': [], '10ppm': []},
        'NH3': {'10ppm': [], '50ppm': [], '100ppm': []},
        'Clean Air': {'0ppm': []}
    }
    sample_pulses = []

    # Process H2S
    for _, row in h2s_df.iterrows():
        p_name = row['Pulse_Index']
        p_num = parse_pulse_num(p_name)
        points = row[point_cols].values.astype(np.float32)
        if p_num <= 37:
            ppm, conc = 1.0, '1ppm'
        elif p_num <= 74:
            ppm, conc = 5.0, '5ppm'
        else:
            ppm, conc = 10.0, '10ppm'

        profiles['H2S'][conc].append(points.tolist())
        pulse_X.append(extract_pulse_features(points))
        pulse_gas.append('H2S')
        pulse_ppm.append(ppm)
        pulse_labels.append(label_map['H2S'])

        if len([p for p in sample_pulses if p['gas'] == 'H2S' and p['ppm'] == ppm]) < 2:
            sample_pulses.append({
                'id': f"H2S_{p_name}_{int(ppm)}ppm",
                'name': f"H2S ({int(ppm)} ppm) - {p_name}",
                'gas': 'H2S',
                'ppm': ppm,
                'points': [round(float(v), 4) for v in points]
            })

    # Process NH3
    for _, row in nh3_df.iterrows():
        p_name = row['Pulse_Index']
        p_num = parse_pulse_num(p_name)
        points = row[point_cols].values.astype(np.float32)
        if p_num <= 42:
            ppm, conc = 10.0, '10ppm'
        elif p_num <= 84:
            ppm, conc = 50.0, '50ppm'
        else:
            ppm, conc = 100.0, '100ppm'

        profiles['NH3'][conc].append(points.tolist())
        pulse_X.append(extract_pulse_features(points))
        pulse_gas.append('NH3')
        pulse_ppm.append(ppm)
        pulse_labels.append(label_map['NH3'])

        if len([p for p in sample_pulses if p['gas'] == 'NH3' and p['ppm'] == ppm]) < 2:
            sample_pulses.append({
                'id': f"NH3_{p_name}_{int(ppm)}ppm",
                'name': f"NH3 ({int(ppm)} ppm) - {p_name}",
                'gas': 'NH3',
                'ppm': ppm,
                'points': [round(float(v), 4) for v in points]
            })

    # Process Clean Air
    for _, row in air_df.iterrows():
        p_name = row['Pulse_Index']
        points = row[point_cols].values.astype(np.float32)
        ppm = 0.0
        profiles['Clean Air']['0ppm'].append(points.tolist())
        pulse_X.append(extract_pulse_features(points))
        pulse_gas.append('Clean Air')
        pulse_ppm.append(ppm)
        pulse_labels.append(label_map['Clean Air'])

        if len([p for p in sample_pulses if p['gas'] == 'Clean Air']) < 2:
            sample_pulses.append({
                'id': f"Air_{p_name}_0ppm",
                'name': f"Clean Air (0 ppm) - {p_name}",
                'gas': 'Clean Air',
                'ppm': 0.0,
                'points': [round(float(v), 4) for v in points]
            })

    X_pulse = np.array(pulse_X, dtype=np.float32)
    y_pulse_gas = np.array(pulse_labels, dtype=np.int32)
    y_pulse_ppm = np.array(pulse_ppm, dtype=np.float32)

    # 1.1 Train Pulse Classifier & Regressor
    print("\n[Pulse Model] Training Random Forest Classifier & Regressor...")
    clf_pulse = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    reg_pulse = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_accs = []
    y_true_all, y_pred_all = [], []
    for train_idx, test_idx in skf.split(X_pulse, y_pulse_gas):
        clf_pulse.fit(X_pulse[train_idx], y_pulse_gas[train_idx])
        preds = clf_pulse.predict(X_pulse[test_idx])
        cv_accs.append(np.mean(preds == y_pulse_gas[test_idx]))
        y_true_all.extend(y_pulse_gas[test_idx])
        y_pred_all.extend(preds)

    pulse_acc = float(np.mean(cv_accs)) * 100.0
    cm_pulse = confusion_matrix(y_true_all, y_pred_all).tolist()
    cls_report_pulse = classification_report(y_true_all, y_pred_all, target_names=classes, output_dict=True)

    # Regressor CV
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    ppm_preds_all, ppm_true_all = [], []
    for train_idx, test_idx in kf.split(X_pulse, y_pulse_ppm):
        reg_pulse.fit(X_pulse[train_idx], y_pulse_ppm[train_idx])
        preds = reg_pulse.predict(X_pulse[test_idx])
        ppm_preds_all.extend(preds)
        ppm_true_all.extend(y_pulse_ppm[test_idx])

    pulse_mae = float(mean_absolute_error(ppm_true_all, ppm_preds_all))
    pulse_r2 = float(r2_score(ppm_true_all, ppm_preds_all))

    print(f"Pulse Classification Accuracy: {pulse_acc:.2f}%")
    print(f"Pulse Concentration MAE: {pulse_mae:.2f} ppm | R2: {pulse_r2:.4f}")

    # Fit pulse models on full dataset for inference
    clf_pulse.fit(X_pulse, y_pulse_gas)
    reg_pulse.fit(X_pulse, y_pulse_ppm)

    # =========================================================================
    # 2. BUILD WINDOW-LEVEL DATASET (For real-time streaming inference)
    # =========================================================================
    win_X, win_gas, win_ppm = [], [], []
    val_win_X, val_win_gas, val_win_ppm = [], [], []

    # Windows from H2S
    for _, row in h2s_df.iterrows():
        p_num = parse_pulse_num(row['Pulse_Index'])
        points = row[point_cols].values.astype(np.float32)
        ppm = 1.0 if p_num <= 37 else (5.0 if p_num <= 74 else 10.0)
        is_val = (p_num % 5 == 0)
        t_X = val_win_X if is_val else win_X
        t_g = val_win_gas if is_val else win_gas
        t_p = val_win_ppm if is_val else win_ppm

        base_v = float(points[0])
        # Active gas response window
        for st in range(20, 125, 2 if not is_val else 3):
            w = points[st:st + 20]
            t_X.append(extract_window_features(w, base_v))
            t_g.append(label_map['H2S'])
            t_p.append(ppm)

        # Baseline & tail windows
        for st in [0, 5, 200, 215, 225]:
            w = points[st:st + 20]
            t_X.append(extract_window_features(w, base_v))
            t_g.append(label_map['Clean Air'])
            t_p.append(0.0)

    # Windows from NH3
    for _, row in nh3_df.iterrows():
        p_num = parse_pulse_num(row['Pulse_Index'])
        points = row[point_cols].values.astype(np.float32)
        ppm = 10.0 if p_num <= 42 else (50.0 if p_num <= 84 else 100.0)
        is_val = (p_num % 5 == 0)
        t_X = val_win_X if is_val else win_X
        t_g = val_win_gas if is_val else win_gas
        t_p = val_win_ppm if is_val else win_ppm

        base_v = float(points[0])
        for st in range(20, 125, 2 if not is_val else 3):
            w = points[st:st + 20]
            t_X.append(extract_window_features(w, base_v))
            t_g.append(label_map['NH3'])
            t_p.append(ppm)

        for st in [0, 5, 200, 215, 225]:
            w = points[st:st + 20]
            t_X.append(extract_window_features(w, base_v))
            t_g.append(label_map['Clean Air'])
            t_p.append(0.0)

    # Windows from Clean Air
    for _, row in air_df.iterrows():
        p_num = parse_pulse_num(row['Pulse_Index'])
        points = row[point_cols].values.astype(np.float32)
        is_val = (p_num % 5 == 0)
        t_X = val_win_X if is_val else win_X
        t_g = val_win_gas if is_val else win_gas
        t_p = val_win_ppm if is_val else win_ppm

        base_v = float(points[0])
        for st in range(0, 230, 4 if not is_val else 6):
            w = points[st:st + 20]
            t_X.append(extract_window_features(w, base_v))
            t_g.append(label_map['Clean Air'])
            t_p.append(0.0)

    X_train_win = np.array(win_X, dtype=np.float32)
    y_train_win_gas = np.array(win_gas, dtype=np.int32)
    y_train_win_ppm = np.array(win_ppm, dtype=np.float32)

    X_val_win = np.array(val_win_X, dtype=np.float32)
    y_val_win_gas = np.array(val_win_gas, dtype=np.int32)
    y_val_win_ppm = np.array(val_win_ppm, dtype=np.float32)

    print(f"\n[Window Model] Training on {len(X_train_win)} windows, testing on {len(X_val_win)} windows...")
    clf_win = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    reg_win = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)

    clf_win.fit(X_train_win, y_train_win_gas)
    reg_win.fit(X_train_win, y_train_win_ppm)

    val_preds_gas = clf_win.predict(X_val_win)
    val_preds_ppm = reg_win.predict(X_val_win)

    win_acc = float(np.mean(val_preds_gas == y_val_win_gas)) * 100.0
    win_mae = float(mean_absolute_error(y_val_win_ppm, val_preds_ppm))
    win_r2 = float(r2_score(y_val_win_ppm, val_preds_ppm))
    print(f"Window Gas Accuracy: {win_acc:.2f}% | Window ppm MAE: {win_mae:.2f} ppm")

    # Feature Importance (Top 10 from Pulse Model)
    feature_names = ['Min_V', 'Max_V', 'Delta_V', 'AUC', 'Mean_V', 'Std_V', 'Peak_Time', 'Rise_Slope', 'Decay_Slope']
    feature_names += [f"Anchor_{s}s" for s in [4, 7, 12, 18, 24, 29, 34, 41, 48, 55]]
    importances = clf_pulse.feature_importances_
    top_indices = np.argsort(importances)[::-1][:10]
    top_features = [{'name': feature_names[i], 'importance': round(float(importances[i]), 4)} for i in top_indices]

    # Save summary curves (mean & std profiles)
    summary_profiles = {}
    for gas_name, sub in profiles.items():
        summary_profiles[gas_name] = {}
        for conc, pulse_list in sub.items():
            if len(pulse_list) > 0:
                arr = np.array(pulse_list)
                summary_profiles[gas_name][conc] = {
                    'count': int(len(pulse_list)),
                    'mean': [round(float(v), 4) for v in np.mean(arr, axis=0)],
                    'std': [round(float(v), 4) for v in np.std(arr, axis=0)],
                    'sample_pulse': [round(float(v), 4) for v in arr[0]]
                }

    os.makedirs('dashboard', exist_ok=True)
    os.makedirs('backend', exist_ok=True)

    with open('dashboard/gas_profiles.json', 'w', encoding='utf-8') as f:
        json.dump(summary_profiles, f, indent=2)

    with open('dashboard/pulse_samples.json', 'w', encoding='utf-8') as f:
        json.dump(sample_pulses, f, indent=2)

    # Save models
    with open('backend/model_gas.pkl', 'wb') as f:
        pickle.dump(clf_win, f)
    with open('backend/model_ppm.pkl', 'wb') as f:
        pickle.dump(reg_win, f)
    with open('backend/model_pulse_gas.pkl', 'wb') as f:
        pickle.dump(clf_pulse, f)
    with open('backend/model_pulse_ppm.pkl', 'wb') as f:
        pickle.dump(reg_pulse, f)

    meta = {
        'classes': classes,
        'windowSize': 20,
        'architecture': 'RandomForest_EdgeAI_DualMode',
        'validationMode': 'ZeroOverlapStratifiedPulseCV',
        'trainingMetrics': {
            'pulseAccuracy': round(pulse_acc, 2),
            'pulsePpmMae': round(pulse_mae, 2),
            'pulsePpmR2': round(pulse_r2, 4),
            'windowAccuracy': round(win_acc, 2),
            'windowPpmMae': round(win_mae, 2),
            'windowPpmR2': round(win_r2, 4),
            'confusionMatrix': cm_pulse,
            'classificationReport': cls_report_pulse,
            'topFeatures': top_features
        },
        'concentrationSpecs': {
            'H2S': [1.0, 5.0, 10.0],
            'NH3': [10.0, 50.0, 100.0],
            'Clean Air': [0.0]
        }
    }

    with open('backend/classes.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    with open('backend/metrics.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    with open('dashboard/model_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    with open('backend/scaler.pkl', 'wb') as f:
        pickle.dump({'modelType': 'RandomForest_EdgeAI', 'classes': classes}, f)

    print("\n==========================================")
    print(" TRAINING COMPLETED SUCCESSFULLY!")
    print(f" Pulse Classification Accuracy: {pulse_acc:.2f}%")
    print(f" Pulse Concentration MAE:      {pulse_mae:.2f} ppm (R2: {pulse_r2:.4f})")
    print(f" Window Real-Time Accuracy:    {win_acc:.2f}%")
    print(" Models and Web Artifacts saved to backend/ and dashboard/.")
    print("==========================================")
    return meta

if __name__ == '__main__':
    trainModel()