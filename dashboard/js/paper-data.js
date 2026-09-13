// Paper Metadata and Ground Truth Benchmark from mst_37_3_035109.pdf
export const PAPER_INFO = {
  title: "High-fidelity embedded gas sensing: a unified deep learning framework for simultaneous identification and quantification",
  journal: "Measurement Science and Technology 37 (2026) 035109",
  doi: "https://doi.org/10.1088/1361-6501/ae3252",
  authors: "Xuanque Nguyen, Ngoc Viet Nguyen, Chien Nguyen Viet, Van Su Luong, Quang Vuong Pham, Viet Thong Le, Van Hieu Nguyen, Minhhuy Le",
  affiliation: "Phenikaa University, Hanoi, Vietnam",
  hardwareSetup: {
    sensorChips: "4 x MiCS-4514 (SGX Sensortech) = 8 independent MOS sensing channels (S1-S8)",
    flowControl: "MFCs (Mass Flow Controllers) with constant flow delivery",
    normalization: "Rg / Ra (Resistance ratio under gas vs. baseline clean air)",
    parametersCount: "180,534 parameters (1.03 MFLOPS, 0.514 MMACS)",
    benchmarkMcu: "10 STM32 MCUs (7.11 ms on STM32H735G down to 60.35 ms on STM32L4R9I)"
  },
  modelArchitecture: {
    name: "Dual-Branch Attention Multitask Deep Learning (MT-DL)",
    classificationHead: "1D-CNN + Global Pooling + Dense (Softmax 9 classes: 8 gases + Air) -> 100% Accuracy",
    regressionHead: "1D-CNN + Attention-conditioned weights -> Quantification (MAPE 6.61%)",
    lossFunction: "Concentration-Adaptive Custom Loss (k = 0.4, ε = 1e-3) vs standard MAE"
  },
  gasPerformance: {
    "H2S": {
      name: "Hydrogen Sulfide",
      formula: "H₂S",
      mape: "6.64%",
      rsd: "0.14 ppm",
      range: "0 - 10 ppm",
      sensorsImpact: "S7, S5 (Moderate positive correlation r=0.37, 0.33; S2 sharp drop)",
      hazardLevel: "Highly Toxic / Respiratory Paralysis (PEL: 10 ppm, IDLH: 50 ppm)"
    },
    "CO": {
      name: "Carbon Monoxide",
      formula: "CO",
      mape: "9.02%",
      rsd: "1.70 ppm",
      range: "0 - 100 ppm",
      sensorsImpact: "S2, S6, S8 (Strong positive response)",
      hazardLevel: "Asphyxiant, Silent Killer (PEL: 50 ppm)"
    },
    "NH3": {
      name: "Ammonia",
      formula: "NH₃",
      mape: "2.84%",
      rsd: "0.81 ppm",
      range: "0 - 100 ppm",
      sensorsImpact: "S8 (r=0.53), S6 (r=0.45) strong correlation",
      hazardLevel: "Corrosive to eyes and respiratory tract"
    },
    "SO2": {
      name: "Sulfur Dioxide",
      formula: "SO₂",
      mape: "5.93%",
      rsd: "0.18 ppm",
      range: "0 - 10 ppm",
      sensorsImpact: "S8, S7 (High precision absolute RSD 0.18 ppm)",
      hazardLevel: "Toxic irritant from oil refinery desulfurization"
    },
    "NO2": {
      name: "Nitrogen Dioxide",
      formula: "NO₂",
      mape: "15.38%",
      rsd: "0.48 ppm",
      range: "0 - 10 ppm",
      sensorsImpact: "Strong oxidizing gas, highly nonlinear sensor response",
      hazardLevel: "Severe pulmonary irritant (PEL: 5 ppm)"
    },
    "CH3OCH3": {
      name: "Dimethyl Ether",
      formula: "CH₃OCH₃",
      mape: "7.15%",
      rsd: "1.25 ppm",
      range: "0 - 100 ppm",
      sensorsImpact: "Volatile organic ether",
      hazardLevel: "Flammable gas"
    },
    "C2H5OH": {
      name: "Ethanol",
      formula: "C₂H₅OH",
      mape: "6.80%",
      rsd: "1.40 ppm",
      range: "0 - 100 ppm",
      sensorsImpact: "VOC alcohol interference",
      hazardLevel: "Solvent / Flammable vapor"
    },
    "H2": {
      name: "Hydrogen",
      formula: "H₂",
      mape: "5.21%",
      rsd: "1.10 ppm",
      range: "0 - 100 ppm",
      sensorsImpact: "Reducing gas with rapid diffusion",
      hazardLevel: "Highly explosive (LEL: 4%)"
    }
  }
};
