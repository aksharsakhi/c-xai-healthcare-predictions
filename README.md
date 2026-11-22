# C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI

[![Conference Acceptance](https://img.shields.io/badge/ICMLDE%202026-Accepted%20(Elsevier)-success.svg)](https://www.elsevier.com/locate/procedia)
[![Paper ID](https://img.shields.io/badge/Paper%20ID-857-blue.svg)](https://github.com/aksharsakhi/c-xai-healthcare-predictions)
[![Proceedings](https://img.shields.io/badge/Proceedings-Procedia%20Computer%20Science-orange.svg)](PROCS_ICMLDE2024/PROCS_ICMLDE2024.pdf)
[![Digital Poster](https://img.shields.io/badge/Digital%20Poster-PDF%20%7C%20PPTX-purple.svg)](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857_C-XAI_Digital_Poster.pdf)
[![Presentation Slides](https://img.shields.io/badge/Presentation-Slides%20(PDF%20%7C%20PPTX)-red.svg)](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857.pdf)
[![Python Package](https://img.shields.io/badge/Python%20Package-cxai--1.0.0-informational.svg)](setup.py)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Paper Information & Author Attribution

* **Paper Title**: **C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI**
* **Conference**: **International Conference on Machine Learning and Data Engineering (ICMLDE 2026)**
* **Publisher / Journal**: **Elsevier *Procedia Computer Science***
* **Paper ID**: `857`

### Authors
* **Sheela Akshar Sakhi¹ (Presenter)** — [`aksharsakhi@gmail.com`](mailto:aksharsakhi@gmail.com) / [`cb.sc.u4cse23547@cb.students.amrita.edu`](mailto:cb.sc.u4cse23547@cb.students.amrita.edu)
* **Ibbraheem Shaik¹**
* **Settibattini Suhitha¹**
* **Dr. Ramya G. R.²\*** *(Supervisor & Corresponding Author)* — [`gr_ramya@cb.amrita.edu`](mailto:gr_ramya@cb.amrita.edu)

### Affiliation
¹·² **Department of Computer Science and Engineering, Amrita School of Computing**,  
**Amrita Vishwa Vidyapeetham, Coimbatore, Tamil Nadu, India**

---

## 📖 Executive Summary & Clinical Motivation

Clinical decision support systems increasingly rely on machine learning models, yet rigorous evaluation of post-hoc explanations remains limited. Surveys reveal that:
- **83%** of healthcare explainable AI (XAI) studies omit clinical experts during validation.
- **87%** lack quantitative metrics for attribution reliability.

Standard benchmarks focus primarily on predictive accuracy or static attribution maps, providing little insight into explanation stability under routine sensor noise.

```
                           THE CLINICAL EXPLAINABILITY GAP
┌──────────────────────────┐                      ┌──────────────────────────┐
│   Deep Neural Networks   │                      │  Clinical Decision Risk  │
│  (≥96% Raw AUROC Score)  │                      │ (Fragile Rationales)     │
└────────────┬─────────────┘                      └────────────▲─────────────┘
             │                                                 │
             ▼                                                 │
   Routine Sensor Noise (h = 0.05) ────────────────────────────┤
   triggers up to 9.6× explanation instability                 │
                                                               │
   Competing Explainers (SHAP vs. LIME vs. IG) ────────────────┘
   disagree by >40% on identical patient encounters!
```

**C-XAI (v1.0)** is an open-source auditing framework designed to quantify **explanation stability**, **inter-explainer concordance**, **clinical prior alignment**, and **calibrated decision utility** across algorithms including SHAP, LIME, Integrated Gradients, and SmoothGrad. Evaluated across **51.3K records** spanning MIMIC-IV, eICU, BCWD, and diagnostic cohorts, our findings show that even when classifiers achieve over 96% diagnostic accuracy, post-hoc attributions exhibit substantial local instability ($\widehat{\mathcal{S}}_{\text{Lip}} > 0.45$) and rank disagreement ($\mathcal{D}_{\text{XAI}} > 0.43$, Cohen's $d = 4.82, p < 0.001$). 

> **Key Finding (Accuracy-Explainability Decoupling)**: Tree ensembles (Extra Trees, Random Forest) achieve **+19.6% higher calibrated clinical decision utility** ($0.849$ vs. $0.711$, $p < 0.001$, Cohen's $d = 2.96$) over deep neural networks despite deep models achieving slightly higher raw AUROC.

---

## 💡 Key Contributions

1. **Unified Quantitative Benchmarking Suite (C-XAI)**: Formulates four clinically grounded, mathematically rigorous evaluation metrics: Local Lipschitz Stability ($\widehat{\mathcal{S}}_{\text{Lip}}$), Cross-Explainer Discordance ($\mathcal{D}_{\text{XAI}}$), Clinical Prior Alignment ($\mathcal{W}_{\text{Clin}}$), and Net Clinical Decision Utility ($\mathcal{U}_{\text{Clin}}$).
2. **Zeroth-Order Gaussian Smoothing**: Extends continuous Lipschitz sensitivity auditing to non-differentiable step boundaries of clinical tree ensembles via Monte Carlo score expectation ($M = 100$ draws).
3. **Clinical Prior Grounding via 1D Wasserstein Earth Mover's Distance**: First benchmark grounding post-hoc feature attributions against codified medical guidelines (SOFA, Sepsis-3, NPI, ASCVD).
4. **Empirical Decoupling Proof**: Demonstrates that raw predictive AUROC masks severe explanation fragility and explainer conflict, providing an automated audit mechanism aligned with the FDA SaMD Action Plan and EU AI Act (Articles 13 & 14).

---

## 🔬 Core Mathematical Formulations

### 1. Local Lipschitz Explanation Stability ($\widehat{\mathcal{S}}_{\text{Lip}}$)
Measures the vulnerability of feature attribution $\mathcal{E}_f(x)$ under Gaussian measurement perturbations $\delta \sim \mathcal{N}(0, h^2 I)$ over $M$ Monte Carlo iterations:

$$\widehat{\mathcal{S}}_{\text{Lip}}(x; f, \mathcal{E}, h) = \mathbb{E}_{\delta} \left[ \frac{\|\mathcal{E}_f(x + \delta) - \mathcal{E}_f(x)\|_2}{\|\delta\|_2} \right] \approx \frac{1}{M} \sum_{m=1}^M \frac{\|\mathcal{E}_f(x + \delta_m) - \mathcal{E}_f(x)\|_2}{\|\delta_m\|_2 + \epsilon_0}$$

### 2. Cross-Explainer Discordance ($\mathcal{D}_{\text{XAI}}$)
Captures pairwise rank dissonance among $K$ competing explainers (e.g., TreeSHAP, KernelSHAP, LIME, SmoothGrad, Integrated Gradients):

$$\mathcal{D}_{\text{XAI}}(x; f) = 1 - \frac{2}{K(K - 1)} \sum_{j < k} r_s(\mathcal{E}_j(x), \mathcal{E}_k(x))$$

where $r_s$ denotes the Spearman rank correlation coefficient.

### 3. Clinical Prior Alignment ($\mathcal{W}_{\text{Clin}}$)
Quantifies divergence between empirical feature attribution distributions $\mathcal{E}_{\text{norm}}(x)$ and established medical risk score weightings $P_{\text{clin}}$ via 1D Wasserstein Earth Mover's Distance:

$$\mathcal{W}_{\text{Clin}}^{\text{norm}}(x) = \frac{\mathcal{W}_1(\mathcal{E}_{\text{norm}}(x), P_{\text{clin}})}{\mathcal{W}_{\max}} = \frac{1}{\mathcal{W}_{\max}} \int_{-\infty}^{\infty} |F_{\mathcal{E}}(t) - F_{\text{clin}}(t)| \, dt$$

### 4. Calibrated Clinical Decision Utility ($\mathcal{U}_{\text{Clin}}$)
A decision-theoretic utility metric penalizing high-risk reliance on unstable or discordant rationales:

$$\mathcal{U}_{\text{Clin}} = w_s (1 - \widehat{\mathcal{S}}_{\text{Lip}}) + w_d (1 - \mathcal{D}_{\text{XAI}}) + w_p (1 - \mathcal{W}_{\text{Clin}}^{\text{norm}}) + w_c (1 - \text{Loss}_{\text{rel}})$$

---

## 🏗️ 4-Subsystem Auditing Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       1. C-XAI SYSTEM ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  Subsystem 1: Data & Noise Ingestion                                        │
│  ┌─────────────────────────┐          ┌──────────────────────────────────┐  │
│  │    Clinical Datasets    ├─────────►│     Preprocessing + Noise        │  │
│  │ (MIMIC-IV, eICU, BCWD)  │          │ Injection δ ~ N(0, h²I)          │  │
│  └─────────────────────────┘          └────────────────┬─────────────────┘  │
│                                                        │                    │
│  Subsystem 2: Predictive Model Zoo                     ▼                    │
│  ┌───────────────┐   ┌─────────────┐   ┌─────────────┐   ┌───────────────┐  │
│  │ Random Forest ├──►│ Extra Trees ├──►│     MLP     ├──►│ Tabular Deep  │  │
│  │               │   │             │   │ Classifier  │   │ ResNet        │  │
│  └───────────────┘   └─────────────┘   └─────────────┘   └───────┬───────┘  │
│                                                                  │          │
│  Subsystem 3: Post-Hoc Explainer Suite                           ▼          │
│  ┌──────────┐   ┌────────────┐   ┌──────┐   ┌────────────┐   ┌───────────┐  │
│  │ TreeSHAP ├──►│ KernelSHAP ├──►│ LIME ├──►│ SmoothGrad ├──►│ Int. Grads│  │
│  └──────────┘   └────────────┘   └──────┘   └────────────┘   └─────┬─────┘  │
│                                                                    │        │
│  Subsystem 4: Quantitative Auditing & Decision Support             ▼        │
│  ┌───────────────┐   ┌──────────────┐   ┌───────────────┐   ┌────────────┐  │
│  │   Stability   ├──►│  Discordance ├──►│Prior Alignment├──►│  Utility   │  │
│  │    (SbLip)    │   │    (DXAI)    │   │    (W_Clin)   │   │  (U_Clin)  │  │
│  └───────────────┘   └──────────────┘   └───────────────┘   └────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Comprehensive Benchmark Results

### 1. Multi-Cohort Benchmark Leaderboard across 50 Trials ($N = 50$ Seeds)

| Clinical Cohort | Model Architecture | Accuracy | ROC-AUC | $\widehat{\mathcal{S}}_{\text{Lip}}$ ($h=0.05$) ($\downarrow$) | $\mathcal{D}_{\text{XAI}}$ ($\downarrow$) | $\mathcal{W}_{\text{Clin}}$ ($\downarrow$) | $\mathcal{U}_{\text{Clin}}$ ($\uparrow$) |
|---|---|---|---|---|---|---|---|
| **MIMIC-IV ICU Sepsis** | **Extra Trees (C-XAI)** | 88.12% | 0.903 | **0.051** | **0.059** | 0.031 | **0.849\*** |
| ($N=40,000$, SOFA/Lactate) | Random Forest | 88.45% | 0.899 | 0.082 | 0.081 | **0.029** | 0.841 |
| | MLP Classifier | 89.20% | 0.907 | 0.485 | 0.412 | 0.039 | 0.712 |
| | Tabular Deep ResNet | **89.35%** | **0.913** | 0.491 | 0.435 | 0.044 | 0.711 |
| **eICU Multi-Center** | **Extra Trees (C-XAI)** | 84.85% | 0.897 | **0.078** | **0.072** | 0.032 | **0.798\*** |
| ($N=10,000$, MAP/WBC) | Random Forest | 85.10% | 0.899 | 0.112 | 0.092 | **0.030** | 0.792 |
| | Tabular Deep ResNet | **85.60%** | **0.905** | 0.472 | 0.418 | 0.041 | 0.690 |
| **Breast Cancer (BCWD)** | **Extra Trees (C-XAI)** | 96.49% | **0.999** | **0.041** | **0.046** | 0.037 | **0.914\*** |
| ($N=569$, NPI Tumor) | Random Forest | 96.49% | 0.995 | 0.064 | 0.061 | **0.031** | 0.906 |
| | Tabular Deep ResNet | **97.37%** | 0.995 | 0.450 | 0.380 | 0.033 | 0.783 |
| **Cardiovascular EHR** | **Extra Trees (C-XAI)** | 78.75% | 0.856 | **0.249** | **0.100** | **0.031** | **0.620\*** |
| ($N=800$, ASCVD Risk) | Random Forest | **80.00%** | **0.858** | 0.307 | 0.100 | **0.031** | 0.619 |
| | Tabular Deep ResNet | 78.50% | 0.842 | 0.460 | 0.395 | 0.050 | 0.542 |

*\*Statistically significant clinical utility improvement ($p < 0.001$, Wilcoxon signed-rank test, Cohen's $d = 2.96$).*

### 2. Cross-Explainer Discordance Matrix ($\mathcal{D}_{\text{XAI}}$)

Tree ensembles achieve high consensus across explainers ($\mathcal{D}_{\text{XAI}} = 0.059$), whereas Tabular Deep ResNet exhibits severe cross-explainer conflict ($\mathcal{D}_{\text{XAI}} = 0.435$, a **7.4× higher disagreement rate**):

```
       Extra Trees (Consensus)                     Tabular Deep ResNet (Severe Conflict)
          TreeSHAP   KernSHAP    LIME                    IntGrad   SmoothGrad    LIME
TreeSHAP   0.000      0.042     0.059         IntGrad     0.000      0.312      0.435
KernSHAP   0.042      0.000     0.075         SmoothGrad  0.312      0.000      0.458
LIME       0.059      0.075     0.000         LIME        0.435      0.458      0.000
    Mean DXAI = 0.059 (Agreement: 94.1%)            Mean DXAI = 0.435 (Agreement: 56.5%)
```

---

## 💻 Quickstart Python Package API (`cxai`)

### Installation
```bash
git clone https://github.com/aksharsakhi/c-xai-healthcare-predictions.git
cd c-xai-healthcare-predictions
pip install -e .
```

### Python API Usage
```python
import cxai

# 1. Audit single model across all C-XAI metrics
metrics = cxai.evaluate(model, X_test, y_test, feature_names=features, clinical_priors=priors)
print(f"Explanation Stability (SbLip): {metrics['SbLip']:.4f}")
print(f"Explainer Discordance (DXAI):  {metrics['DXAI']:.4f}")
print(f"Net Clinical Decision Utility: {metrics['U_Clin']:.4f}")

# 2. Generate multi-model benchmark leaderboard
models = {'RandomForest': rf, 'ExtraTrees': et, 'DeepResNet': resnet}
leaderboard = cxai.benchmark(models, X_test, y_test, feature_names=features, clinical_priors=priors)
print(leaderboard)

# 3. Head-to-head paradigm comparison with Wilcoxon hypothesis testing
comparison = cxai.compare(model_trees, model_deep, X_test, y_test, feature_names=features, clinical_priors=priors)
print(f"Utility Advantage: +{comparison['delta_utility']:.2f}% (p = {comparison['p_value']:.4e})")
```

---

## 📦 Conference Deliverables & Artifacts

All final presentation and submission artifacts are organized in `CONF_PRESENTATION/SUBMISSION_READY/`:

| Deliverable | File Path | Format / Description |
|:---|:---|:---|
| **Digital Poster (Required)** | [`ICMLDE-2026-857_C-XAI_Digital_Poster.pdf`](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857_C-XAI_Digital_Poster.pdf) | 48 × 24 in landscape PDF (printable at 96 × 48 in @ 200%) |
| **Digital Poster (Editable)** | [`ICMLDE-2026-857_C-XAI_Digital_Poster.pptx`](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857_C-XAI_Digital_Poster.pptx) | Editable PPTX matching official ICMLDE 2026 template |
| **Digital Poster Package** | [`ICMLDE-2026-857_C-XAI_Digital_Poster_Package.zip`](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857_C-XAI_Digital_Poster_Package.zip) | Combined ZIP archive containing both PDF & PPTX |
| **Technical PPT Deck** | [`ICMLDE-2026-857.pptx`](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857.pptx) | 16:9 Presentation Slides for Technical Session |
| **Technical PDF Deck** | [`ICMLDE-2026-857.pdf`](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857.pdf) | PDF export of presentation slides |
| **Technical Backup Doc** | [`ICMLDE-2026-857_Technical_Backup_Documentation.pdf`](CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857_Technical_Backup_Documentation.pdf) | Supplementary proof & extended tables |
| **Camera-Ready Paper** | [`PROCS_ICMLDE2024/PROCS_ICMLDE2024.pdf`](PROCS_ICMLDE2024/PROCS_ICMLDE2024.pdf) | Elsevier Procedia Computer Science camera-ready PDF |

---

## 📁 Repository Directory Structure

```
c-xai-healthcare-predictions/
├── README.md                                  # Main Documentation & Overview
├── setup.py                                   # PyPI / cxai package setup script
├── Dockerfile                                 # Reproducible Docker container definition
├── requirements.txt                           # Python package dependencies
├── run_master_cxai_benchmark.py               # End-to-end benchmark execution driver
├── CONFERENCE_DETAILS.md                      # Official ICMLDE 2026 acceptance metadata
│
├── CONF_PRESENTATION/                         # Conference Presentation Suite
│   ├── SUBMISSION_READY/                      # Final submission deliverables
│   │   ├── ICMLDE-2026-857_C-XAI_Digital_Poster.pdf
│   │   ├── ICMLDE-2026-857_C-XAI_Digital_Poster.pptx
│   │   ├── ICMLDE-2026-857_C-XAI_Digital_Poster_Package.zip
│   │   ├── ICMLDE-2026-857.pdf
│   │   ├── ICMLDE-2026-857.pptx
│   │   └── ICMLDE-2026-857_Technical_Backup_Documentation.pdf
│   ├── previews/                              # High-resolution figure & poster renders
│   ├── scripts/                               # Poster & presentation generation scripts
│   └── templates/                             # Official conference templates & logos
│
├── PROCS_ICMLDE2024/                          # Elsevier Camera-Ready Paper Sources
│   ├── PROCS_ICMLDE2024.tex                   # Main LaTeX manuscript
│   ├── PROCS_ICMLDE2024.pdf                   # Compiled Elsevier camera-ready PDF
│   ├── references.bib                         # BibTeX reference database
│   └── figures/                               # Vector & high-res paper figures
│
└── src/                                       # Core Source Code & Package
    ├── cxai/                                  # Top-level cxai Python package
    │   ├── __init__.py                        # Package init
    │   ├── api.py                             # High-level API (evaluate, benchmark, compare)
    │   ├── metrics.py                         # SbLip, DXAI, W_Clin, U_Clin formulations
    │   ├── attacks.py                         # Attribution perturbation attacks
    │   ├── fairness.py                        # Subgroup calibration & fairness auditing
    │   ├── ablation.py                        # Metric component ablation study
    │   ├── stats.py                           # Paired t-tests & Wilcoxon signed-rank
    │   └── visualization.py                   # Plotting utilities & heatmaps
    ├── data_preprocessing.py                  # Clinical EHR dataset loaders
    ├── model_training.py                      # Tree & neural net training zoo
    └── xai_generators.py                      # Post-hoc explainer implementations
```

---

## 🚀 Reproduction & Execution

### 1. Run Complete Benchmark
```bash
python3 run_master_cxai_benchmark.py
```

### 2. Docker Containerized Execution
```bash
docker build -t cxai:latest .
docker run --rm cxai:latest
```

---

## 📜 Citation & Reference

If you find C-XAI useful in your research, please cite our paper:

```bibtex
@article{sakhi2026cxai,
  title={{C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI}},
  author={Sakhi, Sheela Akshar and Shaik, Ibbraheem and Suhitha, Settibattini and Ramya, G. R.},
  journal={Procedia Computer Science},
  volume={xx},
  pages={xx--xx},
  year={2026},
  publisher={Elsevier},
  note={International Conference on Machine Learning and Data Engineering (ICMLDE 2026), Paper ID: 857}
}
```

---

## 📄 License
This repository is licensed under the [MIT License](LICENSE).
