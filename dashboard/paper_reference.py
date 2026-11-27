"""
dashboard/paper_reference.py
Exact published benchmark results from ICMLDE 2026 accepted manuscript (Akshar_ICMLDE2026/Final.tex)
and presentation deck (CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857.pdf)
for transparent side-by-side reference during the conference presentation.
"""

PAPER_META = {
    "paper_id": "857",
    "title": "C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI",
    "conference": "5th Elsevier International Conference on Machine Learning and Data Engineering (ICMLDE 2026)",
    "proceedings": "Elsevier Procedia Computer Science",
    "location": "Dehradun, India",
    "authors": "Sheela Akshar Sakhi (Presenter), Ibbraheem Shaik, Settibattini Suhitha, Dr. Ramya G R*",
    "affiliation": "Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore, India",
    "repo": "https://github.com/aksharsakhi/c-xai-healthcare-predictions",
    "params": {
        "M_monte_carlo": 100,
        "h_default": 0.05,
        "alpha_over_reliance": 0.50,
        "beta_under_reliance": 0.30,
        "N_trials": 50,
        "total_encounters": 51369
    }
}

# Table 1 in Final.tex: Overall C-XAI benchmark results across 4 cohorts (N=50 trials)
PAPER_OVERALL_TABLE = [
    {"cohort": "MIMIC-IV", "n_records": 40000, "model": "Random Forest", "acc": 0.8845, "s_lip": 0.0821, "d_xai": 0.0812, "w_clin_norm": 0.0285, "u_clin": 0.8412},
    {"cohort": "MIMIC-IV", "n_records": 40000, "model": "Extra Trees", "acc": 0.8812, "s_lip": 0.0512, "d_xai": 0.0589, "w_clin_norm": 0.0312, "u_clin": 0.8485},
    {"cohort": "MIMIC-IV", "n_records": 40000, "model": "MLP", "acc": 0.8920, "s_lip": 0.4850, "d_xai": 0.4120, "w_clin_norm": 0.0389, "u_clin": 0.7120},
    {"cohort": "MIMIC-IV", "n_records": 40000, "model": "Tabular Deep ResNet", "acc": 0.8935, "s_lip": 0.4912, "d_xai": 0.4350, "w_clin_norm": 0.0375, "u_clin": 0.7105},

    {"cohort": "eICU", "n_records": 10000, "model": "Random Forest", "acc": 0.8510, "s_lip": 0.1120, "d_xai": 0.0920, "w_clin_norm": 0.0298, "u_clin": 0.7915},
    {"cohort": "eICU", "n_records": 10000, "model": "Extra Trees", "acc": 0.8485, "s_lip": 0.0785, "d_xai": 0.0715, "w_clin_norm": 0.0315, "u_clin": 0.7980},
    {"cohort": "eICU", "n_records": 10000, "model": "MLP", "acc": 0.8420, "s_lip": 0.4620, "d_xai": 0.3950, "w_clin_norm": 0.0412, "u_clin": 0.6850},
    {"cohort": "eICU", "n_records": 10000, "model": "Tabular Deep ResNet", "acc": 0.8540, "s_lip": 0.4820, "d_xai": 0.4210, "w_clin_norm": 0.0390, "u_clin": 0.6810},

    {"cohort": "BCWD", "n_records": 569, "model": "Random Forest", "acc": 0.9649, "s_lip": 0.0643, "d_xai": 0.0614, "w_clin_norm": 0.0307, "u_clin": 0.9062},
    {"cohort": "BCWD", "n_records": 569, "model": "Extra Trees", "acc": 0.9649, "s_lip": 0.0411, "d_xai": 0.0463, "w_clin_norm": 0.0371, "u_clin": 0.9139},
    {"cohort": "BCWD", "n_records": 569, "model": "MLP", "acc": 0.9737, "s_lip": 0.4500, "d_xai": 0.3800, "w_clin_norm": 0.0328, "u_clin": 0.7828},
    {"cohort": "BCWD", "n_records": 569, "model": "Tabular Deep ResNet", "acc": 0.9737, "s_lip": 0.4680, "d_xai": 0.3980, "w_clin_norm": 0.0315, "u_clin": 0.7780},

    {"cohort": "Cardio EHR", "n_records": 800, "model": "Random Forest", "acc": 0.8000, "s_lip": 0.3066, "d_xai": 0.1000, "w_clin_norm": 0.0306, "u_clin": 0.6191},
    {"cohort": "Cardio EHR", "n_records": 800, "model": "Extra Trees", "acc": 0.7875, "s_lip": 0.2491, "d_xai": 0.1000, "w_clin_norm": 0.0306, "u_clin": 0.6201},
    {"cohort": "Cardio EHR", "n_records": 800, "model": "MLP", "acc": 0.7750, "s_lip": 0.4500, "d_xai": 0.3800, "w_clin_norm": 0.0504, "u_clin": 0.5470},
    {"cohort": "Cardio EHR", "n_records": 800, "model": "Tabular Deep ResNet", "acc": 0.7812, "s_lip": 0.4706, "d_xai": 0.3920, "w_clin_norm": 0.0485, "u_clin": 0.5420},
]

# Table 2 in Final.tex: Empirical Local Lipschitz Stability across h
PAPER_H_SCALING = [
    {"h": 0.01, "label": "h = 0.01 (Micro-noise)", "Extra Trees": 0.0180, "Random Forest": 0.0250, "MLP": 0.2300, "Tabular Deep ResNet": 0.2800},
    {"h": 0.02, "label": "h = 0.02", "Extra Trees": 0.0248, "Random Forest": 0.0361, "MLP": 0.3698, "Tabular Deep ResNet": 0.4550},
    {"h": 0.05, "label": "h = 0.05 (Standard)", "Extra Trees": 0.0414, "Random Forest": 0.0644, "MLP": 0.7720, "Tabular Deep ResNet": 0.9715},
    {"h": 0.10, "label": "h = 0.10", "Extra Trees": 0.0642, "Random Forest": 0.1046, "MLP": 1.4169, "Tabular Deep ResNet": 1.8190},
    {"h": 0.20, "label": "h = 0.20 (Severe noise)", "Extra Trees": 0.1026, "Random Forest": 0.1748, "MLP": 2.6627, "Tabular Deep ResNet": 3.4906},
]

# Table 3 in Final.tex: Sensitivity of U_Clin across trust weight profiles (MIMIC-IV)
PAPER_WEIGHT_SENSITIVITY = [
    {"config": "Balanced (Baseline)", "weights": "(0.33, 0.33, 0.33)", "ET": 0.8135, "RF": 0.8076, "MLP": 0.7184, "Deep ResNet": 0.7206},
    {"config": "Stability-Focused", "weights": "(0.60, 0.20, 0.20)", "ET": 0.8077, "RF": 0.7951, "MLP": 0.6456, "Deep ResNet": 0.6463},
    {"config": "Prior-Focused", "weights": "(0.20, 0.60, 0.20)", "ET": 0.8146, "RF": 0.8138, "MLP": 0.7600, "Deep ResNet": 0.7623},
    {"config": "Calibration-Focused", "weights": "(0.20, 0.20, 0.60)", "ET": 0.8210, "RF": 0.8168, "MLP": 0.7524, "Deep ResNet": 0.7556},
    {"config": "Robust Clinical", "weights": "(0.40, 0.40, 0.20)", "ET": 0.8111, "RF": 0.8045, "MLP": 0.7028, "Deep ResNet": 0.7043},
]

# Table 4 in Final.tex: Adversarial robustness & missingness (MIMIC-IV)
PAPER_ADVERSARIAL = [
    {"mode": "Clean Baseline", "model": "Random Forest", "acc": 0.8845, "s_lip": 0.0821, "d_xai": 0.0812},
    {"mode": "Clean Baseline", "model": "MLP", "acc": 0.8920, "s_lip": 0.4850, "d_xai": 0.4120},
    {"mode": "Clean Baseline", "model": "Tabular Deep ResNet", "acc": 0.8935, "s_lip": 0.4912, "d_xai": 0.4350},
    {"mode": "Gaussian Noise (h=0.05)", "model": "Random Forest", "acc": 0.8790, "s_lip": 0.0845, "d_xai": 0.0910},
    {"mode": "Gaussian Noise (h=0.05)", "model": "MLP", "acc": 0.8710, "s_lip": 0.5210, "d_xai": 0.4680},
    {"mode": "Gaussian Noise (h=0.05)", "model": "Tabular Deep ResNet", "acc": 0.8750, "s_lip": 0.5340, "d_xai": 0.4820},
    {"mode": "Missingness (20% MCAR)", "model": "Random Forest", "acc": 0.8610, "s_lip": 0.0980, "d_xai": 0.1250},
    {"mode": "Missingness (20% MCAR)", "model": "MLP", "acc": 0.8120, "s_lip": 0.6120, "d_xai": 0.5840},
    {"mode": "Missingness (20% MCAR)", "model": "Tabular Deep ResNet", "acc": 0.8240, "s_lip": 0.6050, "d_xai": 0.5710},
    {"mode": "FGSM Attack (eps=0.02)", "model": "Random Forest", "acc": 0.8720, "s_lip": 0.1150, "d_xai": 0.2850},
    {"mode": "FGSM Attack (eps=0.02)", "model": "MLP", "acc": 0.7950, "s_lip": 0.8420, "d_xai": 1.8450},
    {"mode": "FGSM Attack (eps=0.02)", "model": "Tabular Deep ResNet", "acc": 0.8010, "s_lip": 0.8650, "d_xai": 1.8620},
    {"mode": "ScaL-PGD Attack (5 Steps)", "model": "Random Forest", "acc": 0.8650, "s_lip": 0.1320, "d_xai": 0.3120},
    {"mode": "ScaL-PGD Attack (5 Steps)", "model": "MLP", "acc": 0.7680, "s_lip": 0.9150, "d_xai": 1.9120},
    {"mode": "ScaL-PGD Attack (5 Steps)", "model": "Tabular Deep ResNet", "acc": 0.7720, "s_lip": 0.9380, "d_xai": 1.9280},
]

# Table 5 in Final.tex: Explainer Latency & Memory
PAPER_LATENCY = [
    {"explainer": "TreeSHAP", "complexity": "O(T L D²)", "latency_ms": 4.2, "ram_mb": 45},
    {"explainer": "KernelSHAP", "complexity": "O(2^D)", "latency_ms": 4210.0, "ram_mb": 512},
    {"explainer": "LIME", "complexity": "O(N D²)", "latency_ms": 850.0, "ram_mb": 120},
    {"explainer": "SmoothGrad", "complexity": "O(M |Θ|)", "latency_ms": 320.0, "ram_mb": 210},
    {"explainer": "Integrated Gradients", "complexity": "O(K |Θ|)", "latency_ms": 180.0, "ram_mb": 165},
]
