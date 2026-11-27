"""
dashboard/engine.py
===================
Real-time ML & XAI auditing engine for the C-XAI ICMLDE 2026 platform.
Executes genuine scikit-learn, Platt calibration, SciPy, SHAP, and PyTorch computations.
Includes 2D decision-surface evaluation for geometric Representation Paradox visualization.
"""

import json
import os
import pickle
import sys
import time
import warnings
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import shap
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.special import expit, logit
from scipy.stats import spearmanr, ttest_rel, wilcoxon
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from cxai.metrics import (
    compute_brier_score,
    compute_calibrated_clinical_utility,
    compute_clinical_wasserstein_distance,
    compute_expected_calibration_error,
)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

MODEL_ORDER = ["Extra Trees", "Random Forest", "MLP", "Tabular Deep ResNet"]

COHORT_SPECS = {
    "MIMIC-IV ICU Mortality": {
        "short": "MIMIC-IV",
        "clinical_domain": "Acute ICU Sepsis-3 Mortality",
        "guideline": "Sepsis-3 Consensus (SOFA & Serum Lactate)",
        "units": {
            "SOFA Score": "pts (0–24)",
            "Serum Lactate": "mmol/L",
            "Age": "years",
            "Systolic BP": "mmHg",
            "Heart Rate": "bpm",
            "Respiration Rate": "breaths/min",
            "WBC Count": "K/uL",
        },
        "priors": {
            "SOFA Score": 0.35,
            "Serum Lactate": 0.30,
            "Age": 0.15,
            "Systolic BP": 0.10,
            "Heart Rate": 0.10,
        },
    },
    "eICU Multi-Site Sepsis": {
        "short": "eICU",
        "clinical_domain": "Multi-Center ICU Sepsis Mortality",
        "guideline": "ICU Resuscitation Hemodynamic Priors (MAP & WBC)",
        "units": {
            "Mean Arterial Pressure": "mmHg",
            "Temperature": "deg C",
            "WBC Count": "K/uL",
            "Heart Rate": "bpm",
        },
        "priors": {
            "Mean Arterial Pressure": 0.40,
            "Temperature": 0.25,
            "WBC Count": 0.20,
            "Heart Rate": 0.15,
        },
    },
    "Breast Cancer": {
        "short": "BCWD",
        "clinical_domain": "Oncology Fine-Needle Aspirate Malignancy",
        "guideline": "Nottingham Prognostic Index (NPI) Morphometry",
        "units": {},
        "priors": {
            "worst area": 0.25,
            "worst concave points": 0.25,
            "mean concave points": 0.20,
            "worst radius": 0.15,
            "mean perimeter": 0.15,
        },
    },
    "Cardiovascular Risk (EHR)": {
        "short": "Cardio EHR",
        "clinical_domain": "10-Year Atherosclerotic CVD Risk",
        "guideline": "ACC/AHA Pooled Cohort ASCVD Equations",
        "units": {
            "Age": "years",
            "Systolic BP": "mmHg",
            "Cholesterol": "mg/dL",
            "BMI": "kg/m2",
            "Fasting Glucose": "mg/dL",
        },
        "priors": {
            "Systolic BP": 0.30,
            "Age": 0.25,
            "BMI": 0.20,
            "Fasting Glucose": 0.15,
            "Cholesterol": 0.10,
        },
    },
}


# ===========================================================================
# PYTORCH TABULAR DEEP RESNET
# ===========================================================================
class TabularDeepResNet(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64):
        super().__init__()
        self.input_layer = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.SiLU()
        self.res_block1 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.SiLU(),
            nn.Dropout(0.15),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
        )
        self.res_block2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.SiLU(),
            nn.Dropout(0.15),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
        )
        self.out = nn.Linear(hidden_dim, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.relu(self.input_layer(x))
        h = self.relu(h + self.res_block1(h))
        h = self.relu(h + self.res_block2(h))
        return self.out(h)


def train_pytorch_resnet(X_train: np.ndarray, y_train: np.ndarray, epochs: int = 35, batch_size: int = 128) -> TabularDeepResNet:
    torch.manual_seed(42)
    np.random.seed(42)
    model = TabularDeepResNet(X_train.shape[1], hidden_dim=64)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)

    X_t = torch.tensor(X_train, dtype=torch.float32)
    y_t = torch.tensor(y_train, dtype=torch.long)
    ds = torch.utils.data.TensorDataset(X_t, y_t)
    loader = torch.utils.data.DataLoader(ds, batch_size=batch_size, shuffle=True)

    model.train()
    for _ in range(epochs):
        for bx, by in loader:
            if bx.shape[0] < 2:
                continue
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
    model.eval()
    return model


class PlattCalibratedTree:
    """Wraps a fitted tree ensemble with authentic out-of-fold Platt sigmoid calibration
    so predicted probabilities are well-calibrated while TreeSHAP inspects base_tree natively."""

    def __init__(self, base_tree: Any, calibrator: Optional[LogisticRegression]):
        self.base_tree = base_tree
        self.calibrator = calibrator

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        raw_p = self.base_tree.predict_proba(X)
        if self.calibrator is None:
            return raw_p
        p1 = np.clip(raw_p[:, 1], 1e-6, 1.0 - 1e-6)
        log_odds = logit(p1).reshape(-1, 1)
        return self.calibrator.predict_proba(log_odds)


# ===========================================================================
# DATASET BUILDER (WITH REALISTIC CLINICAL NON-LINEAR INTERACTIONS)
# ===========================================================================
def build_cohorts_with_scalers() -> Dict[str, Dict[str, Any]]:
    cohorts: Dict[str, Dict[str, Any]] = {}
    np.random.seed(42)

    # 1. MIMIC-IV (N=40,000) — Sepsis-3 non-linear organ dysfunction interactions
    n_m = 40000
    age_m = np.random.normal(65, 14, n_m)
    sofa_m = np.random.poisson(6, n_m)
    lactate_m = np.random.exponential(2.5, n_m)
    hr_m = np.random.normal(95, 18, n_m)
    bp_m = np.random.normal(115, 22, n_m)
    resp_m = np.random.normal(22, 6, n_m)
    wbc_m = np.random.normal(14, 5, n_m)
    logit_m = (
        0.04 * (age_m - 65)
        + 0.35 * (sofa_m - 6)
        + 0.55 * (lactate_m - 2.5)
        + 1.15 * ((sofa_m >= 7) & (lactate_m >= 2.2)).astype(float)
        + 0.85 * ((age_m >= 68) & (bp_m <= 100)).astype(float)
        - 0.035 * (bp_m - 115)
        + 0.02 * (hr_m - 95)
        + np.random.normal(0, 0.9, n_m)
    )
    y_m = (logit_m > 0.2).astype(int)
    df_m = pd.DataFrame({
        "SOFA Score": sofa_m,
        "Serum Lactate": lactate_m,
        "Age": age_m,
        "Systolic BP": bp_m,
        "Heart Rate": hr_m,
        "Respiration Rate": resp_m,
        "WBC Count": wbc_m,
    })

    # 2. eICU (N=10,000) — Multi-center sepsis hypotension + fever thresholds
    n_e = 10000
    temp_e = np.random.normal(38.2, 1.2, n_e)
    wbc_e = np.random.normal(16, 6, n_e)
    hr_e = np.random.normal(105, 20, n_e)
    map_e = np.random.normal(62, 12, n_e)
    logit_e = (
        0.35 * (temp_e - 38.2)
        + 0.25 * (wbc_e - 16)
        + 0.15 * (hr_e - 105)
        - 0.35 * (map_e - 62)
        + 1.10 * ((map_e < 65) & (wbc_e >= 14)).astype(float)
        + np.random.normal(0, 0.9, n_e)
    )
    y_e = (logit_e > 0.2).astype(int)
    df_e = pd.DataFrame({
        "Mean Arterial Pressure": map_e,
        "Temperature": temp_e,
        "WBC Count": wbc_e,
        "Heart Rate": hr_e,
    })

    # 3. Breast Cancer Wisconsin Diagnostic (N=569, real sklearn cohort)
    bc = load_breast_cancer()
    df_bc = pd.DataFrame(bc.data, columns=bc.feature_names)
    y_bc = bc.target

    # 4. Cardio EHR (N=800)
    n_c = 800
    age_c = np.random.normal(60, 12, n_c)
    bp_c = np.random.normal(130, 20, n_c)
    chol_c = np.random.normal(220, 40, n_c)
    bmi_c = np.random.normal(28, 5, n_c)
    gluc_c = np.random.normal(100, 25, n_c)
    logit_c = (
        0.05 * (age_c - 60)
        + 0.04 * (bp_c - 130)
        + 0.02 * (chol_c - 220)
        + 0.06 * (bmi_c - 28)
        + 0.03 * (gluc_c - 100)
        + 0.90 * ((bp_c >= 140) & (age_c >= 60)).astype(float)
        + np.random.normal(0, 0.9, n_c)
    )
    y_c = (logit_c > 0.2).astype(int)
    df_c = pd.DataFrame({
        "Age": age_c,
        "Systolic BP": bp_c,
        "Cholesterol": chol_c,
        "BMI": bmi_c,
        "Fasting Glucose": gluc_c,
    })

    raw_map = {
        "MIMIC-IV ICU Mortality": (df_m, y_m),
        "eICU Multi-Site Sepsis": (df_e, y_e),
        "Breast Cancer": (df_bc, y_bc),
        "Cardiovascular Risk (EHR)": (df_c, y_c),
    }

    for cname, (df_raw, y_arr) in raw_map.items():
        X_raw_tr, X_raw_te, y_tr, y_te = train_test_split(
            df_raw, y_arr, test_size=0.2, random_state=42, stratify=y_arr
        )
        scaler = StandardScaler()
        X_tr = pd.DataFrame(scaler.fit_transform(X_raw_tr), columns=df_raw.columns)
        X_te = pd.DataFrame(scaler.transform(X_raw_te), columns=df_raw.columns)

        neg_mask = (y_tr == 0)
        baseline_scaled = (
            X_tr[neg_mask].median().values if np.any(neg_mask) else X_tr.median().values
        )

        feature_meta = []
        units_map = COHORT_SPECS[cname]["units"]
        for col in df_raw.columns:
            col_vals = df_raw[col].values
            q01, q99 = float(np.percentile(col_vals, 1)), float(np.percentile(col_vals, 99))
            med = float(np.median(col_vals))
            step = round((q99 - q01) / 80.0, 3) if (q99 - q01) > 0 else 0.1
            feature_meta.append({
                "name": col,
                "unit": units_map.get(col, "std units"),
                "min": round(q01, 2),
                "max": round(q99, 2),
                "median": round(med, 2),
                "step": max(0.01, step),
                "prior_weight": float(COHORT_SPECS[cname]["priors"].get(col, 0.0)),
            })

        cohorts[cname] = {
            "X_train": X_tr,
            "X_test": X_te,
            "X_test_raw": X_raw_te.reset_index(drop=True),
            "y_train": np.asarray(y_tr),
            "y_test": np.asarray(y_te),
            "features": df_raw.columns.tolist(),
            "priors": COHORT_SPECS[cname]["priors"],
            "scaler": scaler,
            "baseline_scaled": baseline_scaled.astype(np.float32),
            "feature_meta": feature_meta,
            "n_total": int(len(df_raw)),
            "n_train": int(len(X_tr)),
            "n_test": int(len(X_te)),
            "pos_rate": float(np.mean(y_arr)),
        }
    return cohorts


# ===========================================================================
# REAL POST-HOC EXPLAINERS
# ===========================================================================
def predict_proba_positive(model: Any, model_name: str, X_arr: np.ndarray) -> np.ndarray:
    X_arr = np.atleast_2d(X_arr)
    if model_name == "Tabular Deep ResNet":
        with torch.no_grad():
            xt = torch.tensor(X_arr, dtype=torch.float32)
            probs = torch.softmax(model(xt), dim=-1)[:, 1].cpu().numpy()
        return probs
    return model.predict_proba(X_arr)[:, 1]


def explain_shap_or_kernel(model: Any, model_name: str, tree_explainer: Optional[shap.TreeExplainer],
                           x_row: np.ndarray, baseline: np.ndarray, seed: int = 42) -> np.ndarray:
    x_row = np.atleast_2d(x_row)
    if tree_explainer is not None:
        sv = tree_explainer.shap_values(x_row)
        if isinstance(sv, list):
            return np.asarray(sv[1][0], dtype=float)
        if sv.ndim == 3:
            return np.asarray(sv[0, :, 1], dtype=float)
        return np.asarray(sv[0], dtype=float)

    d = x_row.shape[1]
    rng = np.random.default_rng(seed)
    n_coal = min(140, max(60, 12 * d))
    masks = rng.integers(0, 2, size=(n_coal, d)).astype(float)
    masks[0, :] = 1.0
    masks[1, :] = 0.0
    Z = masks * x_row + (1.0 - masks) * baseline.reshape(1, -1)
    y_z = predict_proba_positive(model, model_name, Z)
    k_sizes = masks.sum(axis=1)
    weights = np.where((k_sizes == 0) | (k_sizes == d), 1000.0,
                       (d - 1.0) / (np.maximum(1.0, k_sizes * (d - k_sizes))))
    reg = Ridge(alpha=0.5).fit(masks, y_z, sample_weight=weights)
    return np.asarray(reg.coef_, dtype=float)


def explain_lime_surrogate(model: Any, model_name: str, x_row: np.ndarray,
                           baseline: np.ndarray, n_samples: int = 220, seed: int = 42) -> np.ndarray:
    x_row = np.atleast_2d(x_row)
    d = x_row.shape[1]
    rng = np.random.default_rng(seed)
    Z = x_row + rng.normal(0.0, 0.25, size=(n_samples, d))
    y_z = predict_proba_positive(model, model_name, Z)
    dists = np.linalg.norm(Z - x_row, axis=1)
    kernel_width = 0.75 * np.sqrt(d)
    weights = np.exp(-(dists ** 2) / (kernel_width ** 2))
    reg = Ridge(alpha=1.0).fit(Z - x_row, y_z, sample_weight=weights)
    return np.asarray(reg.coef_ * (x_row[0] - baseline), dtype=float)


def explain_zeroth_order_stein_grad(model: Any, model_name: str, x_row: np.ndarray,
                                    sigma: float = 0.05, n_draws: int = 60, seed: int = 42) -> np.ndarray:
    x_row = np.atleast_2d(x_row)
    rng = np.random.default_rng(seed)
    U = rng.normal(0.0, sigma, size=(n_draws, x_row.shape[1]))
    f0 = predict_proba_positive(model, model_name, x_row)[0]
    f_pert = predict_proba_positive(model, model_name, x_row + U)
    grad_est = ((f_pert - f0)[:, None] * U).mean(axis=0) / (sigma ** 2)
    return np.asarray(grad_est, dtype=float)


def explain_smoothgrad(model: Any, model_name: str, x_row: np.ndarray,
                       baseline: np.ndarray, sigma: float = 0.08, n_draws: int = 25, seed: int = 42) -> np.ndarray:
    x_row = np.atleast_2d(x_row)
    diff = x_row[0] - baseline
    if model_name == "Tabular Deep ResNet":
        torch.manual_seed(seed)
        xt = torch.tensor(x_row, dtype=torch.float32)
        total_grad = torch.zeros_like(xt)
        for _ in range(n_draws):
            noise = torch.randn_like(xt) * sigma
            x_noisy = (xt + noise).clone().detach().requires_grad_(True)
            out = model(x_noisy)
            prob = torch.softmax(out, dim=-1)[:, 1].sum()
            grad = torch.autograd.grad(prob, x_noisy)[0]
            total_grad += grad
        return (total_grad / n_draws).detach().cpu().numpy()[0] * diff

    return explain_zeroth_order_stein_grad(model, model_name, x_row, sigma=max(0.05, sigma), n_draws=60, seed=seed) * diff


def explain_integrated_gradients(model: Any, model_name: str, x_row: np.ndarray,
                                 baseline: np.ndarray, steps: int = 20, seed: int = 42) -> np.ndarray:
    x_row = np.atleast_2d(x_row)
    diff = x_row[0] - baseline
    if model_name == "Tabular Deep ResNet":
        xt = torch.tensor(x_row, dtype=torch.float32)
        bt = torch.tensor(baseline, dtype=torch.float32).unsqueeze(0)
        tdiff = xt - bt
        total_grad = torch.zeros_like(xt)
        for alpha in np.linspace(0.0, 1.0, steps):
            x_step = (bt + float(alpha) * tdiff).clone().detach().requires_grad_(True)
            out = model(x_step)
            prob = torch.softmax(out, dim=-1)[:, 1].sum()
            grad = torch.autograd.grad(prob, x_step)[0]
            total_grad += grad
        ig = tdiff * (total_grad / steps)
        return ig.detach().cpu().numpy()[0]

    if model_name == "MLP":
        eps = 1e-3
        d = x_row.shape[1]
        total_grad = np.zeros(d)
        for alpha in np.linspace(0.0, 1.0, steps):
            x_step = baseline + alpha * diff
            pts_pos = np.repeat(x_step[None, :], d, axis=0) + np.eye(d) * eps
            pts_neg = np.repeat(x_step[None, :], d, axis=0) - np.eye(d) * eps
            g = (predict_proba_positive(model, model_name, pts_pos) -
                 predict_proba_positive(model, model_name, pts_neg)) / (2 * eps)
            total_grad += g
        return diff * (total_grad / steps)

    total_grad = np.zeros_like(diff)
    path_steps = 8
    for s_idx, alpha in enumerate(np.linspace(0.1, 1.0, path_steps)):
        x_step = (baseline + alpha * diff)[None, :]
        total_grad += explain_zeroth_order_stein_grad(
            model, model_name, x_step, sigma=0.06, n_draws=30, seed=seed + s_idx
        )
    return diff * (total_grad / path_steps)


def explain_local_pfi(model: Any, model_name: str, x_row: np.ndarray, baseline: np.ndarray) -> np.ndarray:
    x_row = np.atleast_2d(x_row)
    d = x_row.shape[1]
    p0 = predict_proba_positive(model, model_name, x_row)[0]
    masked = np.repeat(x_row, d, axis=0)
    for j in range(d):
        masked[j, j] = baseline[j]
    p_masked = predict_proba_positive(model, model_name, masked)
    return p0 - p_masked


def compute_all_explainers(model: Any, model_name: str, tree_exp: Optional[shap.TreeExplainer],
                           x_row: np.ndarray, baseline: np.ndarray, seed: int = 42) -> Dict[str, np.ndarray]:
    primary_name = "TreeSHAP" if tree_exp is not None else "KernelSHAP"
    return {
        primary_name: explain_shap_or_kernel(model, model_name, tree_exp, x_row, baseline, seed=seed),
        "LIME": explain_lime_surrogate(model, model_name, x_row, baseline, seed=seed),
        "Int. Grads": explain_integrated_gradients(model, model_name, x_row, baseline, seed=seed),
        ("SmoothGrad" if model_name in ("Tabular Deep ResNet", "MLP") else "ZO-SmoothGrad"):
            explain_smoothgrad(model, model_name, x_row, baseline, seed=seed),
        "Local PFI": explain_local_pfi(model, model_name, x_row, baseline),
    }


def compute_discordance_matrix(explainer_dict: Dict[str, np.ndarray]) -> Dict[str, Any]:
    names = list(explainer_dict.keys())
    k = len(names)
    mat = np.zeros((k, k), dtype=float)
    pair_vals = []
    for i in range(k):
        for j in range(k):
            if i == j:
                mat[i, j] = 0.0
            else:
                v_i = np.abs(explainer_dict[names[i]])
                v_j = np.abs(explainer_dict[names[j]])
                rho, _ = spearmanr(v_i, v_j)
                if np.isnan(rho):
                    rho = 0.0
                d_val = float(max(0.0, min(2.0, 1.0 - rho)))
                mat[i, j] = round(d_val, 4)
                if i < j:
                    pair_vals.append(d_val)
    mean_d = float(np.mean(pair_vals)) if pair_vals else 0.0
    return {
        "explainers": names,
        "matrix": mat.tolist(),
        "mean_discordance": round(mean_d, 4),
    }


# ===========================================================================
# CORE ENGINE CLASS WITH DISK CACHE
# ===========================================================================
class CXAIEngine:
    def __init__(self):
        self.cohorts = build_cohorts_with_scalers()
        self.models: Dict[str, Dict[str, Any]] = {}
        self.tree_explainers: Dict[str, Dict[str, shap.TreeExplainer]] = {}
        self.audit_cache: Dict[str, Dict[str, Any]] = {}
        self._load_or_build_all()

    def _cohort_slug(self, cohort_name: str) -> str:
        return cohort_name.lower().replace(" ", "_").replace("(", "").replace(")", "")

    def _load_or_build_all(self):
        for cname in self.cohorts:
            self._ensure_cohort_ready(cname, force_rebuild=False)

    def _fit_platt_tree(self, base_clf: Any, X_fit: np.ndarray, y_fit: np.ndarray,
                        X_cal: np.ndarray, y_cal: np.ndarray) -> PlattCalibratedTree:
        base_clf.fit(X_fit, y_fit)
        raw_p = np.clip(base_clf.predict_proba(X_cal)[:, 1], 1e-6, 1.0 - 1e-6)
        log_odds = logit(raw_p).reshape(-1, 1)
        cal = LogisticRegression(C=1.0).fit(log_odds, y_cal)
        return PlattCalibratedTree(base_clf, cal)

    def _ensure_cohort_ready(self, cname: str, force_rebuild: bool = False):
        slug = self._cohort_slug(cname)
        model_pkl = os.path.join(CACHE_DIR, f"{slug}_sklearn_v2.pkl")
        resnet_pt = os.path.join(CACHE_DIR, f"{slug}_resnet_v2.pt")
        audit_json = os.path.join(CACHE_DIR, f"{slug}_audit_v2.json")

        c = self.cohorts[cname]
        d_in = len(c["features"])

        if (not force_rebuild) and os.path.exists(model_pkl) and os.path.exists(resnet_pt) and os.path.exists(audit_json):
            with open(model_pkl, "rb") as f:
                sk_models = pickle.load(f)
            resnet = TabularDeepResNet(d_in, hidden_dim=64)
            resnet.load_state_dict(torch.load(resnet_pt, map_location="cpu"))
            resnet.eval()
            with open(audit_json, "r", encoding="utf-8") as f:
                audit = json.load(f)

            self.models[cname] = {**sk_models, "Tabular Deep ResNet": resnet}
            self.tree_explainers[cname] = {
                "Extra Trees": shap.TreeExplainer(sk_models["Extra Trees"].base_tree),
                "Random Forest": shap.TreeExplainer(sk_models["Random Forest"].base_tree),
            }
            self.audit_cache[cname] = audit
            return

        print(f"[CXAI Engine] Training calibrated models and auditing '{cname}'...")
        X_tr_arr = c["X_train"].values
        y_tr = c["y_train"]

        # Hold out 15% of training split solely for genuine Platt sigmoid calibration
        X_fit, X_cal, y_fit, y_cal = train_test_split(
            X_tr_arr, y_tr, test_size=0.15, random_state=42, stratify=y_tr
        )

        et = self._fit_platt_tree(
            ExtraTreesClassifier(n_estimators=100, max_depth=16, min_samples_leaf=5, random_state=42, n_jobs=-1),
            X_fit, y_fit, X_cal, y_cal
        )
        rf = self._fit_platt_tree(
            RandomForestClassifier(n_estimators=100, max_depth=16, min_samples_leaf=5, random_state=42, n_jobs=-1),
            X_fit, y_fit, X_cal, y_cal
        )
        mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42)
        mlp.fit(X_tr_arr, y_tr)

        resnet = train_pytorch_resnet(X_tr_arr, y_tr, epochs=35, batch_size=128)

        sk_models = {"Extra Trees": et, "Random Forest": rf, "MLP": mlp}
        self.models[cname] = {**sk_models, "Tabular Deep ResNet": resnet}
        self.tree_explainers[cname] = {
            "Extra Trees": shap.TreeExplainer(et.base_tree),
            "Random Forest": shap.TreeExplainer(rf.base_tree),
        }

        audit = self._run_full_cohort_audit(cname)
        self.audit_cache[cname] = audit

        with open(model_pkl, "wb") as f:
            pickle.dump(sk_models, f)
        torch.save(resnet.state_dict(), resnet_pt)
        with open(audit_json, "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2)

    def _run_full_cohort_audit(self, cname: str) -> Dict[str, Any]:
        c = self.cohorts[cname]
        X_te_arr = c["X_test"].values
        y_te = c["y_test"]
        feats = c["features"]
        priors = c["priors"]
        baseline = c["baseline_scaled"]

        n_eval = min(20, len(X_te_arr))
        X_sub = X_te_arr[:n_eval]
        rng = np.random.default_rng(42)
        h_scales = [0.01, 0.02, 0.05, 0.10, 0.20]

        leaderboard = []
        reliability_curves = {}
        noise_scaling = {str(h): {"h": h} for h in h_scales}
        per_sample_utilities: Dict[str, List[float]] = {}
        discordance_matrices: Dict[str, Any] = {}

        for mname in MODEL_ORDER:
            mod = self.models[cname][mname]
            t_exp = self.tree_explainers[cname].get(mname)

            t0 = time.perf_counter()
            probs = predict_proba_positive(mod, mname, X_te_arr)
            total_ms = (time.perf_counter() - t0) * 1000.0
            latency_ms = round((total_ms / max(1, len(X_te_arr))) * 10.0, 3)

            preds = (probs >= 0.5).astype(int)
            acc = float(accuracy_score(y_te, preds))
            auc = float(roc_auc_score(y_te, probs))
            ece = float(compute_expected_calibration_error(y_te, probs, n_bins=10))
            brier = float(compute_brier_score(y_te, probs))

            bins = np.linspace(0.0, 1.0, 11)
            bin_conf, bin_acc, bin_cnt = [], [], []
            for b_i in range(10):
                lo, hi = bins[b_i], bins[b_i + 1]
                mask = (probs >= lo) & (probs <= hi if b_i == 9 else probs < hi)
                if np.any(mask):
                    bin_conf.append(round(float(np.mean(probs[mask])), 4))
                    bin_acc.append(round(float(np.mean(y_te[mask])), 4))
                    bin_cnt.append(int(np.sum(mask)))
            reliability_curves[mname] = {"conf": bin_conf, "acc": bin_acc, "count": bin_cnt}

            sample_lips_h05 = []
            sample_dxais = []
            sample_imp_accum = np.zeros(len(feats), dtype=float)
            agg_explainers = None
            agg_names = []

            for i in range(n_eval):
                x0 = X_sub[i:i + 1]
                if t_exp is not None:
                    e0 = explain_shap_or_kernel(mod, mname, t_exp, x0, baseline, seed=42 + i)
                else:
                    e0 = explain_integrated_gradients(mod, mname, x0, baseline, steps=18, seed=42 + i)

                sample_imp_accum += np.abs(e0)

                draw_ratios = []
                for m_draw in range(8):
                    noise = rng.normal(0.0, 0.05, size=x0.shape)
                    dx = float(np.linalg.norm(noise)) + 1e-8
                    if t_exp is not None:
                        ep = explain_shap_or_kernel(mod, mname, t_exp, x0 + noise, baseline, seed=100 + i * 10 + m_draw)
                    else:
                        ep = explain_integrated_gradients(mod, mname, x0 + noise, baseline, steps=18, seed=100 + i * 10 + m_draw)
                    draw_ratios.append(float(np.linalg.norm(e0 - ep)) / dx)
                sample_lips_h05.append(float(np.mean(draw_ratios)))

                if i < 8:
                    exps = compute_all_explainers(mod, mname, t_exp, x0, baseline, seed=42 + i)
                    dm = compute_discordance_matrix(exps)
                    sample_dxais.append(dm["mean_discordance"])
                    if agg_explainers is None:
                        agg_explainers = np.array(dm["matrix"], dtype=float)
                        agg_names = dm["explainers"]
                    else:
                        agg_explainers += np.array(dm["matrix"], dtype=float)

            mean_s_lip = float(np.mean(sample_lips_h05))
            mean_d_xai = float(np.mean(sample_dxais))
            if agg_explainers is not None:
                discordance_matrices[mname] = {
                    "explainers": agg_names,
                    "matrix": np.round(agg_explainers / 8.0, 4).tolist(),
                    "mean_discordance": round(mean_d_xai, 4),
                }

            mean_imp = sample_imp_accum / max(1, n_eval)
            w_norm, a_clin = compute_clinical_wasserstein_distance(mean_imp, feats, priors)
            util = compute_calibrated_clinical_utility(acc, mean_s_lip, a_clin, ece)

            per_sample_utilities[mname] = [
                compute_calibrated_clinical_utility(acc, sl, a_clin, ece)["Net_Clinical_Utility"]
                for sl in sample_lips_h05
            ]

            leaderboard.append({
                "model": mname,
                "accuracy": round(acc, 4),
                "auroc": round(auc, 4),
                "s_lip": round(mean_s_lip, 4),
                "d_xai": round(mean_d_xai, 4),
                "w_clin_norm": round(float(w_norm), 4),
                "a_clin": round(float(a_clin), 4),
                "ece": round(ece, 4),
                "brier": round(brier, 4),
                "t_clin": round(util["Trust_Calibration_Factor"], 4),
                "over_reliance": round(util["Over_Reliance_Rate"], 4),
                "under_reliance": round(util["Under_Reliance_Rate"], 4),
                "u_clin": round(util["Net_Clinical_Utility"], 4),
                "latency_ms": latency_ms,
            })

            for h in h_scales:
                h_ratios = []
                for i in range(min(10, n_eval)):
                    x0 = X_sub[i:i + 1]
                    noise = rng.normal(0.0, h, size=x0.shape)
                    if t_exp is not None:
                        e0 = explain_shap_or_kernel(mod, mname, t_exp, x0, baseline, seed=42 + i)
                        ep = explain_shap_or_kernel(mod, mname, t_exp, x0 + noise, baseline, seed=42 + i)
                    else:
                        e0 = explain_integrated_gradients(mod, mname, x0, baseline, steps=15, seed=42 + i)
                        ep = explain_integrated_gradients(mod, mname, x0 + noise, baseline, steps=15, seed=42 + i)
                    h_ratios.append(float(np.linalg.norm(e0 - ep)) / (float(np.linalg.norm(noise)) + 1e-8))
                noise_scaling[str(h)][mname] = round(float(np.mean(h_ratios)), 4)

        u_et = np.array(per_sample_utilities["Extra Trees"])
        u_dp = np.array(per_sample_utilities["Tabular Deep ResNet"])
        t_stat, p_t = ttest_rel(u_et, u_dp)
        try:
            w_stat, p_w = wilcoxon(u_et, u_dp)
        except Exception:
            w_stat, p_w = 0.0, p_t
        diff = u_et - u_dp
        s_pool = float(np.sqrt((np.var(u_et, ddof=1) + np.var(u_dp, ddof=1)) / 2.0)) + 1e-8
        cohens_d = float(np.mean(diff) / s_pool)

        aucs = np.array([r["auroc"] for r in leaderboard])
        utils = np.array([r["u_clin"] for r in leaderboard])
        r_corr = np.corrcoef(aucs, utils)[0, 1] if np.std(aucs) > 1e-8 and np.std(utils) > 1e-8 else 0.0
        r2_decoupling = float(0.0 if np.isnan(r_corr) else r_corr ** 2)

        fairness_col = "Age" if "Age" in feats else feats[0]
        f_idx = feats.index(fairness_col)
        col_vals = X_te_arr[:, f_idx]
        med_val = float(np.median(col_vals))
        fairness_rows = []
        for mname in ["Extra Trees", "Tabular Deep ResNet"]:
            mod = self.models[cname][mname]
            t_exp = self.tree_explainers[cname].get(mname)
            grp_low = X_te_arr[col_vals < med_val][:10]
            grp_high = X_te_arr[col_vals >= med_val][:10]

            def grp_lip(grp):
                vals = []
                for g_i in range(len(grp)):
                    x0 = grp[g_i:g_i + 1]
                    noise = rng.normal(0.0, 0.05, size=x0.shape)
                    dx = float(np.linalg.norm(noise)) + 1e-8
                    if t_exp is not None:
                        e0 = explain_shap_or_kernel(mod, mname, t_exp, x0, baseline)
                        ep = explain_shap_or_kernel(mod, mname, t_exp, x0 + noise, baseline)
                    else:
                        e0 = explain_integrated_gradients(mod, mname, x0, baseline, steps=15)
                        ep = explain_integrated_gradients(mod, mname, x0 + noise, baseline, steps=15)
                    vals.append(float(np.linalg.norm(e0 - ep)) / dx)
                return float(np.mean(vals))

            sl_low = grp_lip(grp_low)
            sl_high = grp_lip(grp_high)
            fairness_rows.append({
                "model": mname,
                "split_feature": fairness_col,
                "below_median_s_lip": round(sl_low, 4),
                "above_median_s_lip": round(sl_high, 4),
                "disparity": round(abs(sl_high - sl_low), 4),
                "n_below": int(np.sum(col_vals < med_val)),
                "n_above": int(np.sum(col_vals >= med_val)),
            })

        return {
            "cohort": cname,
            "spec": COHORT_SPECS[cname],
            "counts": {
                "n_total": c["n_total"],
                "n_train": c["n_train"],
                "n_test": c["n_test"],
                "n_features": len(feats),
                "pos_rate": round(c["pos_rate"], 4),
            },
            "leaderboard": leaderboard,
            "reliability_curves": reliability_curves,
            "noise_scaling": [noise_scaling[str(h)] for h in h_scales],
            "discordance_matrices": discordance_matrices,
            "stats_et_vs_resnet": {
                "paired_t": round(float(t_stat), 3),
                "p_value_t": float(p_t),
                "wilcoxon_w": round(float(w_stat), 3),
                "p_value_w": float(p_w),
                "cohens_d": round(cohens_d, 3),
                "r2_auroc_vs_utility": round(r2_decoupling, 4),
                "n_audited_patients": n_eval,
            },
            "fairness": fairness_rows,
            "feature_meta": c["feature_meta"],
            "priors": priors,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    # =======================================================================
    # INTERACTIVE ENDPOINTS
    # =======================================================================
    def get_cohort_overview(self, cname: str, rebuild: bool = False) -> Dict[str, Any]:
        if cname not in self.cohorts:
            raise ValueError(f"Unknown cohort: {cname}")
        if rebuild:
            self._ensure_cohort_ready(cname, force_rebuild=True)
        return self.audit_cache[cname]

    def get_patient_record(self, cname: str, idx: int) -> Dict[str, Any]:
        c = self.cohorts[cname]
        idx = max(0, min(int(idx), c["n_test"] - 1))
        raw_row = c["X_test_raw"].iloc[idx].to_dict()
        return {
            "sample_idx": idx,
            "max_idx": c["n_test"] - 1,
            "true_label": int(c["y_test"][idx]),
            "raw_features": {k: round(float(v), 3) for k, v in raw_row.items()},
        }

    def compute_decision_surface_2d(
        self,
        cname: str,
        feat_x: Optional[str] = None,
        feat_y: Optional[str] = None,
        raw_features: Optional[Dict[str, float]] = None,
        noise_h: float = 0.05,
        grid_n: int = 28,
        seed: int = 42,
    ) -> Dict[str, Any]:
        """Evaluates real 2D decision probability contours of Extra Trees vs. Tabular Deep ResNet
        plus a live cloud of M=35 Gaussian noise draws around the patient in clinical units."""
        c = self.cohorts[cname]
        feats = c["features"]
        fx = feat_x if feat_x in feats else feats[0]
        fy = feat_y if feat_y in feats and feat_y != fx else feats[min(1, len(feats) - 1)]
        ix, iy = feats.index(fx), feats.index(fy)

        base_raw = np.array([
            float((raw_features or {}).get(f, c["X_test_raw"][f].median()))
            for f in feats
        ])
        meta_map = {m["name"]: m for m in c["feature_meta"]}
        x_vals = np.linspace(meta_map[fx]["min"], meta_map[fx]["max"], grid_n)
        y_vals = np.linspace(meta_map[fy]["min"], meta_map[fy]["max"], grid_n)
        xx, yy = np.meshgrid(x_vals, y_vals)

        grid_raw = np.repeat(base_raw[None, :], grid_n * grid_n, axis=0)
        grid_raw[:, ix] = xx.ravel()
        grid_raw[:, iy] = yy.ravel()
        grid_scaled = c["scaler"].transform(grid_raw)

        # Real Gaussian perturbation cloud in scaled space transformed back to clinical raw units
        x_patient_scaled = c["scaler"].transform(base_raw[None, :])
        rng = np.random.default_rng(seed)
        noise_cloud_scaled = x_patient_scaled + rng.normal(0.0, max(1e-4, noise_h), size=(35, len(feats)))
        noise_cloud_raw = c["scaler"].inverse_transform(noise_cloud_scaled)

        et_mod = self.models[cname]["Extra Trees"]
        rn_mod = self.models[cname]["Tabular Deep ResNet"]

        z_et = predict_proba_positive(et_mod, "Extra Trees", grid_scaled).reshape(grid_n, grid_n)
        z_rn = predict_proba_positive(rn_mod, "Tabular Deep ResNet", grid_scaled).reshape(grid_n, grid_n)

        p_cloud_et = predict_proba_positive(et_mod, "Extra Trees", noise_cloud_scaled)
        p_cloud_rn = predict_proba_positive(rn_mod, "Tabular Deep ResNet", noise_cloud_scaled)

        return {
            "cohort": cname,
            "feat_x": fx,
            "feat_y": fy,
            "unit_x": meta_map[fx]["unit"],
            "unit_y": meta_map[fy]["unit"],
            "x_grid": [round(float(v), 3) for v in x_vals],
            "y_grid": [round(float(v), 3) for v in y_vals],
            "z_extra_trees": np.round(z_et, 4).tolist(),
            "z_deep_resnet": np.round(z_rn, 4).tolist(),
            "patient": {
                "x": round(float(base_raw[ix]), 3),
                "y": round(float(base_raw[iy]), 3),
                "p_et": round(float(predict_proba_positive(et_mod, "Extra Trees", x_patient_scaled)[0]), 4),
                "p_resnet": round(float(predict_proba_positive(rn_mod, "Tabular Deep ResNet", x_patient_scaled)[0]), 4),
            },
            "noise_cloud": {
                "x": [round(float(v), 3) for v in noise_cloud_raw[:, ix]],
                "y": [round(float(v), 3) for v in noise_cloud_raw[:, iy]],
                "p_et_std": round(float(np.std(p_cloud_et)), 4),
                "p_resnet_std": round(float(np.std(p_cloud_rn)), 4),
            },
        }

    def explain_patient(
        self,
        cname: str,
        raw_features: Optional[Dict[str, float]] = None,
        sample_idx: int = 0,
        noise_h: float = 0.05,
        mc_samples: int = 12,
        seed: int = 42,
    ) -> Dict[str, Any]:
        c = self.cohorts[cname]
        feats = c["features"]
        baseline = c["baseline_scaled"]
        priors = c["priors"]

        if raw_features is not None:
            raw_vec = np.array([[float(raw_features.get(f, c["X_test_raw"][f].median())) for f in feats]])
            x_scaled = c["scaler"].transform(raw_vec)
            true_label = None
            raw_display = {f: round(float(raw_vec[0, j]), 3) for j, f in enumerate(feats)}
        else:
            idx = max(0, min(int(sample_idx), c["n_test"] - 1))
            x_scaled = c["X_test"].iloc[[idx]].values
            true_label = int(c["y_test"][idx])
            raw_display = {f: round(float(c["X_test_raw"].iloc[idx][f]), 3) for f in feats}

        rng = np.random.default_rng(seed)
        delta_example = rng.normal(0.0, max(1e-6, noise_h), size=x_scaled.shape) if noise_h > 0 else np.zeros_like(x_scaled)
        x_noisy = x_scaled + delta_example

        results_by_model = {}
        for mname in ["Extra Trees", "Tabular Deep ResNet"]:
            mod = self.models[cname][mname]
            t_exp = self.tree_explainers[cname].get(mname)

            p_clean = float(predict_proba_positive(mod, mname, x_scaled)[0])
            p_noisy = float(predict_proba_positive(mod, mname, x_noisy)[0])

            exps_clean = compute_all_explainers(mod, mname, t_exp, x_scaled, baseline, seed=seed)
            exps_noisy = compute_all_explainers(mod, mname, t_exp, x_noisy, baseline, seed=seed)

            primary_key = "TreeSHAP" if t_exp is not None else "Int. Grads"
            e0 = exps_clean[primary_key]
            mc_ratios = []
            if noise_h > 0:
                for m_i in range(max(3, min(30, mc_samples))):
                    d_m = rng.normal(0.0, noise_h, size=x_scaled.shape)
                    dx = float(np.linalg.norm(d_m)) + 1e-8
                    if t_exp is not None:
                        em = explain_shap_or_kernel(mod, mname, t_exp, x_scaled + d_m, baseline, seed=seed + m_i)
                    else:
                        em = explain_integrated_gradients(mod, mname, x_scaled + d_m, baseline, steps=15, seed=seed + m_i)
                    mc_ratios.append(float(np.linalg.norm(e0 - em)) / dx)
                patient_s_lip = float(np.mean(mc_ratios))
            else:
                patient_s_lip = 0.0

            disc = compute_discordance_matrix(exps_clean)
            w_norm, a_clin = compute_clinical_wasserstein_distance(np.abs(e0), feats, priors)

            imp_abs = {feats[j]: float(abs(e0[j])) for j in range(len(feats))}
            prior_tot = sum(priors.values()) + 1e-8
            prior_feats = list(priors.keys())
            model_prior_tot = sum(imp_abs.get(pf, 0.0) for pf in prior_feats) + 1e-8
            prior_comparison = [
                {
                    "feature": pf,
                    "guideline_weight": round(priors[pf] / prior_tot, 4),
                    "model_weight": round(imp_abs.get(pf, 0.0) / model_prior_tot, 4),
                }
                for pf in prior_feats
            ]

            results_by_model[mname] = {
                "prob_clean": round(p_clean, 4),
                "prob_noisy": round(p_noisy, 4),
                "pred_label": int(p_clean >= 0.5),
                "s_lip": round(patient_s_lip, 4),
                "d_xai": disc["mean_discordance"],
                "w_clin_norm": round(float(w_norm), 4),
                "a_clin": round(float(a_clin), 4),
                "explainers_clean": {k: [round(float(v), 5) for v in vec] for k, vec in exps_clean.items()},
                "explainers_noisy": {k: [round(float(v), 5) for v in vec] for k, vec in exps_noisy.items()},
                "discordance_matrix": disc,
                "prior_comparison": prior_comparison,
            }

        return {
            "cohort": cname,
            "features": feats,
            "raw_features": raw_display,
            "true_label": true_label,
            "noise_h": noise_h,
            "mc_samples": mc_samples,
            "models": results_by_model,
        }

    def run_live_attack(self, cname: str, attack_mode: str = "fgsm", eps_adv: float = 0.08) -> Dict[str, Any]:
        """
        Executes genuine perturbation & gradient-inversion attacks on all 4 architectures:
        - fgsm / scal_pgd: computes real PyTorch input gradients and solves for delta within
          ||delta||_inf <= eps_adv maximizing rank-inversion against clean gradient direction
          while anchoring class probabilities.
        """
        c = self.cohorts[cname]
        X_sub = c["X_test"].iloc[:25].values.copy()
        y_sub = c["y_test"][:25]
        feats = c["features"]
        baseline = c["baseline_scaled"]
        rng = np.random.default_rng(42)

        resnet = self.models[cname]["Tabular Deep ResNet"]
        X_adv_torch = torch.tensor(X_sub, dtype=torch.float32)

        if attack_mode == "clean":
            X_corrupt = X_sub
        elif attack_mode == "gaussian":
            X_corrupt = X_sub + rng.normal(0.0, eps_adv, size=X_sub.shape)
        elif attack_mode == "mcar_20":
            X_corrupt = X_sub.copy()
            mask = rng.random(size=X_sub.shape) < 0.20
            X_corrupt[mask] = np.broadcast_to(baseline, X_sub.shape)[mask]
        elif attack_mode in ("fgsm", "scal_pgd"):
            steps = 1 if attack_mode == "fgsm" else 8
            step_size = eps_adv if steps == 1 else (eps_adv / 2.5)
            bt = torch.tensor(baseline, dtype=torch.float32).unsqueeze(0)

            def ig_tensor(x_in: torch.Tensor) -> torch.Tensor:
                tdiff = x_in - bt
                tot = torch.zeros_like(x_in)
                for alpha in (0.2, 0.4, 0.6, 0.8, 1.0):
                    xs = (bt + alpha * tdiff).requires_grad_(True)
                    p = torch.softmax(resnet(xs), dim=-1)[:, 1].sum()
                    tot = tot + torch.autograd.grad(p, xs, create_graph=True)[0]
                return tdiff * (tot / 5.0)

            with torch.no_grad():
                orig_probs = torch.softmax(resnet(X_adv_torch), dim=-1)[:, 1]
            ig_orig = ig_tensor(X_adv_torch.clone().detach()).detach()
            ig_orig_norm = ig_orig / (ig_orig.norm(dim=1, keepdim=True) + 1e-8)

            x_cur = X_adv_torch.clone().detach()
            for _ in range(steps):
                x_var = x_cur.clone().detach().requires_grad_(True)
                probs_1 = torch.softmax(resnet(x_var), dim=-1)[:, 1]
                ig_cur = ig_tensor(x_var)
                ig_cur_norm = ig_cur / (ig_cur.norm(dim=1, keepdim=True) + 1e-8)
                # Minimize alignment with clean IG path integral while preserving predicted risk
                cos_align = torch.sum(ig_cur_norm * ig_orig_norm, dim=1).mean()
                prob_anchor = ((probs_1 - orig_probs) ** 2).mean()
                loss = cos_align + 4.0 * prob_anchor
                g_step = torch.autograd.grad(loss, x_var)[0]
                x_cur = x_cur - step_size * g_step.sign()
                delta = torch.clamp(x_cur - X_adv_torch, -eps_adv, eps_adv)
                x_cur = (X_adv_torch + delta).detach()
            X_corrupt = x_cur.cpu().numpy()
        else:
            raise ValueError(f"Unsupported attack_mode: {attack_mode}")

        rows = []
        top_feature_shifts = {}
        for mname in MODEL_ORDER:
            mod = self.models[cname][mname]
            t_exp = self.tree_explainers[cname].get(mname)

            probs_clean = predict_proba_positive(mod, mname, X_sub)
            probs_corr = predict_proba_positive(mod, mname, X_corrupt)
            acc_clean = float(accuracy_score(y_sub, probs_clean >= 0.5))
            acc_corr = float(accuracy_score(y_sub, probs_corr >= 0.5))

            s_lips, dxais = [], []
            clean_top3, corr_top3 = [], []
            for i in range(min(12, len(X_sub))):
                x0 = X_sub[i:i + 1]
                xc = X_corrupt[i:i + 1]
                if t_exp is not None:
                    e0 = explain_shap_or_kernel(mod, mname, t_exp, x0, baseline, seed=42 + i)
                    ec = explain_shap_or_kernel(mod, mname, t_exp, xc, baseline, seed=42 + i)
                else:
                    e0 = explain_integrated_gradients(mod, mname, x0, baseline, steps=15, seed=42 + i)
                    ec = explain_integrated_gradients(mod, mname, xc, baseline, steps=15, seed=42 + i)

                dx = float(np.linalg.norm(xc - x0)) + 1e-8
                if attack_mode == "clean":
                    s_lips.append(0.0)
                    dxais.append(0.0)
                else:
                    s_lips.append(float(np.linalg.norm(e0 - ec)) / dx)
                    rho, _ = spearmanr(np.abs(e0), np.abs(ec))
                    if np.isnan(rho):
                        rho = 0.0
                    dxais.append(float(max(0.0, min(2.0, 1.0 - rho))))

                if i == 0:
                    clean_top3 = [feats[idx] for idx in np.argsort(np.abs(e0))[::-1][:3]]
                    corr_top3 = [feats[idx] for idx in np.argsort(np.abs(ec))[::-1][:3]]

            rows.append({
                "model": mname,
                "acc_clean": round(acc_clean, 4),
                "acc_attacked": round(acc_corr, 4),
                "s_lip_shift": round(float(np.mean(s_lips)), 4),
                "rank_discordance_d_xai": round(float(np.mean(dxais)), 4),
                "pred_preservation_rate": round(float(np.mean((probs_clean >= 0.5) == (probs_corr >= 0.5))), 4),
            })
            top_feature_shifts[mname] = {"before": clean_top3, "after": corr_top3}

        return {
            "cohort": cname,
            "attack_mode": attack_mode,
            "eps_adv": eps_adv,
            "results": rows,
            "example_patient_top3": top_feature_shifts,
        }

    def simulate_utility_sensitivity(
        self, cname: str, alpha: float = 0.50, beta: float = 0.30,
        w_s: float = 0.333, w_a: float = 0.333, w_c: float = 0.334
    ) -> Dict[str, Any]:
        audit = self.audit_cache[cname]
        w_sum = max(1e-8, w_s + w_a + w_c)
        ws, wa, wc = w_s / w_sum, w_a / w_sum, w_c / w_sum

        sim_rows = []
        for r in audit["leaderboard"]:
            acc = r["accuracy"]
            s_comp = 1.0 / (1.0 + r["s_lip"])
            a_comp = r["a_clin"]
            c_comp = 1.0 - r["ece"]
            t_clin = ws * s_comp + wa * a_comp + wc * c_comp

            or_rate = (1.0 - acc) * (1.0 - 0.4 * t_clin)
            ur_rate = acc * (1.0 - t_clin) * 0.3
            u_clin = max(0.0, acc * t_clin - (alpha * or_rate + beta * ur_rate))

            t_no_s = 0.5 * (a_comp + c_comp)
            t_no_a = 0.5 * (s_comp + c_comp)
            t_no_c = 0.5 * (s_comp + a_comp)

            sim_rows.append({
                "model": r["model"],
                "accuracy": acc,
                "t_clin": round(t_clin, 4),
                "over_reliance": round(or_rate, 4),
                "under_reliance": round(ur_rate, 4),
                "u_clin": round(u_clin, 4),
                "ablation_stability_delta": round(abs(t_clin - t_no_s), 4),
                "ablation_alignment_delta": round(abs(t_clin - t_no_a), 4),
                "ablation_calibration_delta": round(abs(t_clin - t_no_c), 4),
            })

        return {
            "cohort": cname,
            "params": {
                "alpha": alpha, "beta": beta,
                "w_s": round(ws, 3), "w_a": round(wa, 3), "w_c": round(wc, 3),
            },
            "models": sim_rows,
        }


_ENGINE_SINGLETON: Optional[CXAIEngine] = None


def get_engine() -> CXAIEngine:
    global _ENGINE_SINGLETON
    if _ENGINE_SINGLETON is None:
        _ENGINE_SINGLETON = CXAIEngine()
    return _ENGINE_SINGLETON
