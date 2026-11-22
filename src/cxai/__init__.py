"""
C-XAI: Clinical Explainable AI Quantitative Benchmark Toolkit
Author: Sheela Akshar Sakhi, Dr. G. R. Ramya
Amrita Vishwa Vidyapeetham, India
"""

from .metrics import (
    compute_empirical_lipschitz_stability,
    compute_cross_explainer_discordance,
    compute_clinical_wasserstein_distance,
    compute_expected_calibration_error,
    compute_calibrated_clinical_utility
)
from .api import evaluate, benchmark, compare
from .attacks import fgsm_attribution_attack
from .fairness import evaluate_demographic_fairness
from .ablation import run_metric_ablation_study

__version__ = "1.0.0"
__all__ = [
    "compute_empirical_lipschitz_stability",
    "compute_cross_explainer_discordance",
    "compute_clinical_wasserstein_distance",
    "compute_expected_calibration_error",
    "compute_calibrated_clinical_utility",
    "evaluate",
    "benchmark",
    "compare",
    "fgsm_attribution_attack",
    "evaluate_demographic_fairness",
    "run_metric_ablation_study"
]
