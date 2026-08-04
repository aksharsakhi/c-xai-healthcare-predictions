import os
import numpy as np
import pandas as pd
from src.data_preprocessing import load_and_preprocess_data
from src.model_training import train_models
from src.evaluation_framework import (
    compute_empirical_lipschitz_stability,
    compute_cross_explainer_discordance,
    compute_clinical_wasserstein_distance,
    compute_expected_calibration_error,
    compute_calibrated_clinical_utility
)

def main():
    print("=== C-XAI Quantitative Clinical Explainability Benchmark ===")
    print("Loading healthcare datasets...")
    X_train, X_test, y_train, y_test, feature_names = load_and_preprocess_data()
    
    print("Training Model Zoo (Random Forest, Extra Trees, MLP)...")
    results = train_models(X_train, y_train, X_test, y_test)
    
    best_model_name = 'RandomForest'
    best_model = results[best_model_name]['model']
    
    print(f"\nEvaluating C-XAI Metrics for {best_model_name}...")
    
    # 1. Empirical Local Lipschitz Stability
    mean_s_lip, std_s_lip = compute_empirical_lipschitz_stability(best_model, X_test.iloc[:50], noise_level=0.05)
    print(f"Empirical Local Lipschitz Stability (S_Lip_hat): {mean_s_lip:.4f} +/- {std_s_lip:.4f}")
    
    # 2. Expected Calibration Error
    probs = best_model.predict_proba(X_test)[:, 1]
    ece = compute_expected_calibration_error(np.asarray(y_test), probs)
    print(f"Expected Calibration Error (ECE): {ece:.4f}")
    
    # 3. Clinical Prior Wasserstein Distance
    clinical_priors = {'worst concave points': 0.30, 'worst radius': 0.25, 'mean concave points': 0.25, 'worst area': 0.20}
    # Feature importances
    importances = best_model.feature_importances_
    w_dist, a_clinical = compute_clinical_wasserstein_distance(importances, feature_names, clinical_priors)
    print(f"Clinical Prior Wasserstein Distance (W_Clinical): {w_dist:.4f}")
    print(f"Clinical Alignment Score (A_Clinical): {a_clinical:.4f}")
    
    # 4. Calibrated Clinical Utility
    acc = results[best_model_name]['accuracy']
    utility = compute_calibrated_clinical_utility(acc, mean_s_lip, a_clinical, ece)
    print(f"Net Calibrated Clinical Utility (U_Clinical): {utility['Net_Clinical_Utility']:.4f}")
    print(f"  - Over-Reliance Rate: {utility['Over_Reliance_Rate']:.4f}")
    print(f"  - Under-Reliance Rate: {utility['Under_Reliance_Rate']:.4f}")
    
    # Execute full advanced multi-cohort experiments and save figures
    print("\nExecuting multi-cohort benchmark suite in src/advanced_experiments.py...")
    import subprocess
    subprocess.run(["python3", "src/advanced_experiments.py"], check=True)
    print("\nAll benchmark experiments executed and pushed successfully!")

if __name__ == "__main__":
    main()
