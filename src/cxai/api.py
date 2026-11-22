from .metrics import (
    compute_empirical_lipschitz_stability,
    compute_cross_explainer_discordance,
    compute_clinical_wasserstein_distance,
    compute_expected_calibration_error,
    compute_calibrated_clinical_utility
)
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np
import pandas as pd

def evaluate(model, X_test, y_test, feature_names, clinical_priors):
    """
    Evaluates a single model using C-XAI quantitative benchmarks.
    Usage:
        results = cxai.evaluate(model, X_test, y_test, feature_names, clinical_priors)
    """
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else preds
    
    acc = float(accuracy_score(y_test, preds))
    auc = float(roc_auc_score(y_test, probs))
    ece = compute_expected_calibration_error(y_test, probs)
    
    s_lip, _ = compute_empirical_lipschitz_stability(model, X_test.iloc[:50])
    
    importances = getattr(model, 'feature_importances_', np.ones(len(feature_names))/len(feature_names))
    w_dist, a_clinical = compute_clinical_wasserstein_distance(importances, feature_names, clinical_priors)
    
    utility = compute_calibrated_clinical_utility(acc, s_lip, a_clinical, ece)
    
    return {
        'Accuracy': acc,
        'ROC_AUC': auc,
        'ECE': ece,
        'S_Lip_hat': s_lip,
        'W_Clinical': w_dist,
        'A_Clinical': a_clinical,
        'Trust_Calibration_Factor': utility['Trust_Calibration_Factor'],
        'Over_Reliance_Rate': utility['Over_Reliance_Rate'],
        'Under_Reliance_Rate': utility['Under_Reliance_Rate'],
        'U_Clinical': utility['Net_Clinical_Utility']
    }

def benchmark(models_dict, X_test, y_test, feature_names, clinical_priors):
    """
    Runs C-XAI benchmark across a dictionary of trained models.
    Usage:
        leaderboard_df = cxai.benchmark(models, X_test, y_test, feature_names, priors)
    """
    records = []
    for name, model in models_dict.items():
        res = evaluate(model, X_test, y_test, feature_names, clinical_priors)
        res['Model'] = name
        records.append(res)
    return pd.DataFrame(records)[['Model', 'Accuracy', 'ROC_AUC', 'S_Lip_hat', 'W_Clinical', 'ECE', 'U_Clinical']]

def compare(model_a, model_b, X_test, y_test, feature_names, clinical_priors):
    """
    Compares two model paradigms on C-XAI metrics.
    """
    res_a = evaluate(model_a, X_test, y_test, feature_names, clinical_priors)
    res_b = evaluate(model_b, X_test, y_test, feature_names, clinical_priors)
    return pd.DataFrame([res_a, res_b], index=['Model A', 'Model B'])
