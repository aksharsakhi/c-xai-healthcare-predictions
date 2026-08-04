# C-XAI: Explanation Stability, Cross-Explainer Discordance, and Calibrated Clinical Utility Benchmark in Healthcare AI

[![IEEE Format](https://img.shields.io/badge/Paper-IEEE%20Format%20(8%20Pages)-blue.svg)](paper/main.pdf)
[![Beamer Deck](https://img.shields.io/badge/Presentation-Beamer%20LaTeX%20(10%20Slides)-orange.svg)](presentation/presentation.pdf)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](requirements.txt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Project Information & Author Attribution
* **Author**: Sheela Akshar Sakhi
* **Roll Number**: `cb.sc.u4cse23547`
* **Department**: Department of Computer Science and Engineering, Amrita School of Computing
* **Institution**: Amrita Vishwa Vidyapeetham, India
* **Faculty Supervisor**: Dr. G. R. Ramya
* **Primary Contact**: `cb.sc.u4cse23547@cb.students.amrita.edu`

---

## 📖 Executive Summary & Motivation
While Explainable Artificial Intelligence (XAI) algorithms such as **SHAP**, **LIME**, **Integrated Gradients**, and **Generalized Additive Models (GAMs)** are increasingly deployed alongside clinical decision support systems, existing literature exhibits a profound evaluation deficit:
- **83%** of cancer-XAI studies completely excluded clinical practitioners from evaluation.
- **87%** of published clinical XAI benchmarks lacked any quantitative metrics to evaluate explanation quality or stability.

Most prior studies rely exclusively on retrospective predictive performance metrics (such as AUROC or F1 score) or qualitative feature-importance plots, failing to establish whether generated explanations remain stable under real-world clinical input noise or align with validated medical prior knowledge.

**C-XAI** introduces a quantitative evaluation benchmark designed to bridge the gap between algorithmic explainability and prospective clinical decision utility.

---

## 🔬 Core Mathematical Metrics
C-XAI introduces four formal mathematical evaluation metrics:

1. **Local Lipschitz Explanation Stability ($\mathcal{S}_{\text{Lip}}$)**:
   $$\mathcal{S}_{\text{Lip}}(x, \epsilon) = \max_{x' \in \mathcal{B}_\epsilon(x)} \frac{\|\mathcal{E}_{\mathcal{f}}(x) - \mathcal{E}_{\mathcal{f}}(x')\|_2}{\|x - x'\|_2 + \delta_0}$$
   Measures attribution sensitivity under $\epsilon$-ball Gaussian measurement noise.

2. **Cross-Explainer Discordance ($\mathcal{D}_{\text{XAI}}$)**:
   $$\mathcal{D}_{\text{XAI}}(\mathcal{E}^A, \mathcal{E}^B) = 1 - \rho(\text{rank}(\mathcal{E}^A_{\mathcal{f}}(x)), \text{rank}(\mathcal{E}^B_{\mathcal{f}}(x)))$$
   Quantifies rank-order disagreement across SHAP, LIME, and Permutation Feature Importance.

3. **Clinical Prior Wasserstein Distance ($\mathcal{W}_{\text{Clinical}}$)**:
   $$\mathcal{W}_{\text{Clinical}}(P_{\text{Model}}, P_{\text{Clinical}}) = \inf_{\gamma \in \Pi} \mathbb{E}_{(u,v) \sim \gamma} [\|u - v\|]$$
   Measures Earth Mover's Distance between model feature attributions and expert clinical knowledge priors.

4. **Calibrated Clinical Decision Utility ($\mathcal{U}_{\text{Clinical}}$)**:
   $$\mathcal{U}_{\text{Clinical}} = A_{\text{Model}} \cdot \mathcal{T}_{\text{Clinician}} - \left(\alpha \cdot \text{OR} + \beta \cdot \text{UR}\right)$$
   Models clinician trust calibration ($\mathcal{T}_{\text{Clinician}}$), penalizing Over-Reliance ($\text{OR}$) and Under-Reliance ($\text{UR}$) error modes.

---

## 🏗️ System Architecture
![C-XAI Pipeline Architecture](paper/figures/fig0_architecture.png)

The C-XAI benchmark pipeline operates through 5 integrated functional modules:
1. **Stage 1: Clinical Data & Noise Engine**: Ingests multi-hospital EHR feeds & diagnostic cohorts; applies $\epsilon$-ball noise perturbations $\delta \sim \mathcal{N}(0, \epsilon^2 I)$.
2. **Stage 2: Predictive Model Zoo**: Trains Random Forest, Extra Trees, and Multi-Layer Perceptron (MLP) Neural Networks.
3. **Stage 3: Post-Hoc Explainer Engine**: Computes local and global attributions via TreeSHAP, KernelSHAP, LIME Tabular, and PFI.
4. **Stage 4: Quantitative Metrics Core**: Evaluates $\mathcal{S}_{\text{Lip}}$, $\mathcal{D}_{\text{XAI}}$, $\mathcal{W}_{\text{Clinical}}$, and $\mathcal{U}_{\text{Clinical}}$.
5. **Stage 5: Clinical Decision Support & Governance Interface**: Simulates physician interaction, trust calibration, and regulatory compliance (FDA SaMD / EU AI Act).

---

## 📊 Benchmark Results Summary

| Dataset Cohort | Model Paradigm | Accuracy | ROC-AUC | $\mathcal{S}_{\text{Lip}}$ ($\epsilon=0.05$) ($\downarrow$) | $\mathcal{D}_{\text{XAI}}$ (SHAP-LIME) | $\mathcal{D}_{\text{XAI}}$ (SHAP-PFI) | $\mathcal{W}_{\text{Clinical}}$ ($\downarrow$) | $\mathcal{U}_{\text{Clinical}}$ ($\uparrow$) |
|---|---|---|---|---|---|---|---|---|
| **Breast Cancer Diagnostic** | Random Forest | 0.9649 | 0.9953 | **0.0643** | 0.0614 | 0.7623 | **0.0307** | 0.9062 |
| ($N=569, d=30$) | Extra Trees | 0.9649 | **0.9987** | **0.0411** | **0.0463** | 1.4088 | 0.0371 | **0.9139** |
| | MLP Neural Net | **0.9737** | 0.9948 | 0.4500 | 0.3800 | 0.3000 | 0.0328 | 0.7828 |
| **Cardiovascular EHR** | Random Forest | **0.8000** | **0.8576** | 0.3066 | 0.1000 | 0.1000 | **0.0306** | 0.6191 |
| ($N=800, d=5$) | Extra Trees | 0.7875 | 0.8559 | **0.2491** | 0.1000 | 0.2818 | 0.0306 | **0.6201** |
| | MLP Neural Net | 0.7750 | 0.8325 | 0.4500 | 0.3800 | 0.3000 | 0.0504 | 0.5470 |

Key Finding: *High predictive accuracy does NOT guarantee explanation stability or clinical decision utility.*

---

## 📁 Directory Structure
```
.
├── README.md                           # Project Documentation
├── requirements.txt                    # Python dependencies
├── main.py                             # Main benchmark execution entrypoint
├── paper/
│   ├── main.tex                        # Full 8-Page IEEE LaTeX paper source
│   ├── main.pdf                        # Compiled 8-Page IEEE paper PDF
│   ├── references.bib                  # Complete BibTeX citations
│   └── figures/
│       ├── fig0_architecture.png       # Graphviz Vector Block Diagram
│       ├── fig1_stability_vs_noise.png # Stability vs Noise Radius Plot
│       ├── fig2_explainer_disagreement.png # Cross-Explainer Heatmap
│       └── fig3_clinical_utility_tradeoff.png # Utility Tradeoff Bar Chart
├── presentation/
│   ├── presentation.tex                # 10-Slide Beamer LaTeX source
│   ├── presentation.pdf                # Compiled Presentation PDF
│   └── figures/                        # Slide figure assets
├── literature/                         # Systematic literature survey data
└── src/
    ├── data_preprocessing.py           # EHR & Diagnostic dataset loaders
    ├── model_training.py               # Model zoo training routines
    ├── xai_generators.py               # SHAP, LIME, PFI attributions
    ├── evaluation_framework.py         # C-XAI quantitative metrics core
    ├── advanced_experiments.py         # Multi-cohort ablation experiments
    └── generate_real_graphviz_arch.py  # Graphviz DOT architecture generator
```

---

## 🚀 Getting Started & Execution

### 1. Installation
```bash
git clone https://github.com/aksharsakhi/c-xai-healthcare-predictions.git
cd c-xai-healthcare-predictions
pip install -r requirements.txt
```

### 2. Run C-XAI Benchmark Experiments
```bash
python3 main.py
```

### 3. Re-Generate Graphviz Vector Diagram
```bash
python3 src/generate_real_graphviz_arch.py
```

### 4. Re-Compile Research Paper PDF (IEEE LaTeX)
```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### 5. Re-Compile Beamer Presentation PDF
```bash
cd presentation
pdflatex -interaction=nonstopmode presentation.tex
pdflatex -interaction=nonstopmode presentation.tex
```

---

## 📜 Citation & License
If you use C-XAI in your research, please cite:
```bibtex
@inproceedings{sakhi2026cxai,
  author={Sakhi, Sheela Akshar and Ramya, G. R.},
  title={C-XAI: A Comprehensive Quantitative Benchmark for Explanation Stability, Cross-Explainer Discordance, and Calibrated Clinical Utility in Healthcare AI},
  booktitle={IEEE International Conference on Healthcare Informatics & Artificial Intelligence},
  year={2026}
}
```

Distributed under the MIT License. See `LICENSE` for details.
