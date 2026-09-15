import json
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
def buildBlockDataset():
  h2sDf = pd.read_csv('data/H2S.csv')
  coDf = pd.read_csv('data/CO.csv')
  h2s = h2sDf['S3'].values
  co = coDf['S3'].values
  trainWindows, trainGas, trainppm = [], [], []
  valWindows, valGas, valppm = [], [], []
  for start in range(0, 300, 5):
    w = co[start:start + 20]
    if np.max(np.abs(w - 1.0)) < 0.02:
      trainWindows.append(w)
      trainGas.append('Clean Air')
      trainppm.append(0.0)
  for base in np.linspace(0.970, 1.015, 40):
    trainWindows.append(base + np.random.normal(0, 0.0015, 20))
    trainGas.append('Clean Air')
    trainppm.append(0.0)
  for start in range(1550, 1580, 2):
    valWindows.append(h2s[start:start + 20])
    valGas.append('Clean Air')
    valppm.append(0.0)
  for base in np.linspace(0.975, 1.010, 15):
    valWindows.append(base + np.random.normal(0, 0.002, 20))
    valGas.append('Clean Air')
    valppm.append(0.0)
  for start in range(940, 990, 2):
    w = co[start:start + 20]
    ppmVal = float(max(0.0, (w[-1] - 1.0) * 820.0))
    trainWindows.append(w)
    trainGas.append('CO')
    trainppm.append(ppmVal)
  for start in range(1180, 1230, 2):
    w = co[start:start + 20]
    ppmVal = float(max(0.0, (w[-1] - 1.0) * 820.0))
    trainWindows.append(w)
    trainGas.append('CO')
    trainppm.append(ppmVal)
  for start in range(1415, 1475, 2):
    w = co[start:start + 20]
    ppmVal = float(max(0.0, (w[-1] - 1.0) * 820.0))
    valWindows.append(w)
    valGas.append('CO')
    valppm.append(ppmVal)
  for start in range(400, 460, 2):
    w = h2s[start:start + 20]
    ppmVal = float(max(0.0, (w[-1] - 1.0) * 7.8))
    trainWindows.append(w)
    trainGas.append('H2S')
    trainppm.append(ppmVal)
  for start in range(930, 990, 2):
    w = h2s[start:start + 20]
    ppmVal = float(max(0.0, (w[-1] - 1.0) * 7.8))
    trainWindows.append(w)
    trainGas.append('H2S')
    trainppm.append(ppmVal)
  for start in range(1405, 1475, 2):
    w = h2s[start:start + 20]
    ppmVal = float(max(0.0, (w[-1] - 1.0) * 7.8))
    valWindows.append(w)
    valGas.append('H2S')
    valppm.append(ppmVal)
  classes = ['Clean Air', 'CO', 'H2S']
  labelMap = {c: i for i, c in enumerate(classes)}
  XTrain = np.expand_dims(np.array(trainWindows, dtype=np.float32), axis=-1)
  yGasTrain = np.array([labelMap[g] for g in trainGas], dtype=np.int32)
  yppmTrain = np.array(trainppm, dtype=np.float32)
  XVal = np.expand_dims(np.array(valWindows, dtype=np.float32), axis=-1)
  yGasVal = np.array([labelMap[g] for g in valGas], dtype=np.int32)
  yppmVal = np.array(valppm, dtype=np.float32)
  return XTrain, yGasTrain, yppmTrain, XVal, yGasVal, yppmVal, classes
def trainModel():
  XTrain, yGasTrain, yppmTrain, XVal, yGasVal, yppmVal, classes = buildBlockDataset()
  rawInput = tf.keras.layers.Input(shape=(20, 1), name='rawInput')
  x = tf.keras.layers.Conv1D(filters=16, kernel_size=3, padding='same', activation='relu')(rawInput)
  x = tf.keras.layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu')(x)
  x = tf.keras.layers.GlobalAveragePooling1D()(x)
  x = tf.keras.layers.Dense(32, activation='relu')(x)
  gasOutput = tf.keras.layers.Dense(len(classes), activation='softmax', name='gasOutput')(x)
  ppmOutput = tf.keras.layers.Dense(1, activation='softplus', name='ppmOutput')(x)
  model = tf.keras.Model(inputs=rawInput, outputs=[gasOutput, ppmOutput])
  model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),
    loss={'gasOutput': 'sparse_categorical_crossentropy', 'ppmOutput': 'huber'},
    loss_weights={'gasOutput': 1.0, 'ppmOutput': 0.1},
    metrics={'gasOutput': 'accuracy', 'ppmOutput': 'mae'}
  )
  model.fit(
    XTrain,
    [yGasTrain, yppmTrain],
    validation_data=(XVal, [yGasVal, yppmVal]),
    epochs=120,
    batch_size=16,
    verbose=0
  )
  cleanRes = model.evaluate(XVal, [yGasVal, yppmVal], verbose=0)
  print(f'Block Accuracy: {cleanRes[3] * 100:.2f}% ppmMae: {cleanRes[4]:.2f}')
  XValNoisy = XVal + np.random.normal(0, 0.01, XVal.shape).astype(np.float32)
  noiseRes = model.evaluate(XValNoisy, [yGasVal, yppmVal], verbose=0)
  print(f'Noise Stress Accuracy: {noiseRes[3] * 100:.2f}% ppmMae: {noiseRes[4]:.2f}')
  XValDrift = XVal + 0.025
  driftRes = model.evaluate(XValDrift, [yGasVal, yppmVal], verbose=0)
  print(f'Drift Stress Accuracy: {driftRes[3] * 100:.2f}% ppmMae: {driftRes[4]:.2f}')
  model.save('backend/model.keras')
  with open('backend/classes.json', 'w', encoding='utf-8') as f:
    json.dump({'classes': classes, 'windowSize': 20, 'architecture': 'MultiTask1DCNN', 'validationMode': 'ZeroOverlapBlockSplit'}, f, indent=2)
  with open('backend/scaler.pkl', 'wb') as f:
    pickle.dump({'modelType': 'MultiTask1DCNN'}, f)
  print('Completed Successfully!')
if __name__ == '__main__':
  trainModel()