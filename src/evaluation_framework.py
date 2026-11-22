import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wasserstein_distance
import shap

def compute_empirical_lipschitz_stability(model, X_subset, explainer=None, noise_level=0.05, n_samples=100, smoothing_const=1e-8):
    """
    Computes Empirical Local Lipschitz Explanation Stability Index (S_Lip_hat):
    S_Lip_hat(x, eps) = (1/M) * sum_{m=1}^M [ ||E(x) - E(x + delta_m)||_2 / (||delta_m||_2 + delta_0) ]
    """
    if explainer is None:
        explainer = shap.TreeExplainer(model)
        
    base_shap = explainer.shap_values(X_subset)
    if isinstance(base_shap, list):
        base_shap = base_shap[1]
    elif len(np.shape(base_shap)) == 3:
        base_shap = base_shap[:, :, 1]

    lipschitz_ratios = []
    for i in range(len(X_subset)):
        x_orig = X_subset.iloc[[i]].values
        e_orig = base_shap[i]
        
        # Monte Carlo Gaussian noise perturbation delta ~ N(0, eps^2 * I)
        noise = np.random.normal(0, noise_level, x_orig.shape)
        x_pert = x_orig + noise
        delta_x_norm = np.linalg.norm(noise) + smoothing_const
        
        pert_shap = explainer.shap_values(x_pert)
        if isinstance(pert_shap, list):
            pert_shap = pert_shap[1]
        elif len(np.shape(pert_shap)) == 3:
            pert_shap = pert_shap[0, :, 1]
        else:
            pert_shap = pert_shap[0]
            
        delta_e_norm = np.linalg.norm(e_orig - pert_shap)
        lipschitz_ratios.append(delta_e_norm / delta_x_norm)
        
    return np.mean(lipschitz_ratios), np.std(lipschitz_ratios)

def compute_cross_explainer_discordance(shap_importance, lime_importance):
    """
    Computes Cross-Explainer Discordance (D_XAI):
    D_XAI = 1 - Spearman_rho(rank(E^A), rank(E^B))
    """
    rho, _ = spearmanr(shap_importance, lime_importance)
    if np.isnan(rho):
        rho = 0.0
    discordance = 1.0 - rho
    return max(0.0, min(2.0, discordance))

def compute_clinical_wasserstein_distance(model_importance, feature_names, clinical_priors):
    """
    Computes 1D Earth Mover's / Wasserstein Distance between Model Attribution Distribution
    and Structured Clinical Prior Distribution (e.g. Framingham / APACHE-II).
    """
    imp_dict = dict(zip(feature_names, model_importance))
    tot_model = sum([abs(imp_dict.get(f, 0.0)) for f in clinical_priors.keys()]) + 1e-8
    
    prior_vec = []
    model_vec = []
    
    for f, p_weight in clinical_priors.items():
        prior_vec.append(p_weight)
        model_vec.append(abs(imp_dict.get(f, 0.0)) / tot_model)
        
    w_dist = float(wasserstein_distance(prior_vec, model_vec))
    d_feat = len(clinical_priors)
    w_norm = float(w_dist / max(1, (d_feat - 1))) if d_feat > 1 else float(w_dist)
    alignment_score = float(max(0.0, 1.0 - w_norm))
    return w_norm, alignment_score

def compute_expected_calibration_error(y_true, y_prob, n_bins=10):
    """
    Computes Expected Calibration Error (ECE):
    ECE = sum_{b=1}^B (|B_b| / N) * |acc(B_b) - conf(B_b)|
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        bin_lower, bin_upper = bin_boundaries[i], bin_boundaries[i+1]
        in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)
        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(y_true[in_bin])
            avg_confidence_in_bin = np.mean(y_prob[in_bin])
            ece += np.abs(accuracy_in_bin - avg_confidence_in_bin) * prop_in_bin
    return ece

def compute_calibrated_clinical_utility(acc, s_lip, a_clinical, ece, alpha=0.5, beta=0.3):
    """
    Computes Net Calibrated Clinical Decision Utility (U_Clinical):
    T_Clinician = (1/3) * [ (1 / (1 + S_Lip)) + A_Clinical + (1 - ECE) ]
    U_Clinical = Accuracy * T_Clinician - (alpha * OR + beta * UR)
    """
    trust_factor = (1.0 / 3.0) * ((1.0 / (1.0 + s_lip)) + a_clinical + (1.0 - ece))
    
    model_error = 1.0 - acc
    over_reliance_rate = model_error * (1.0 - 0.4 * trust_factor)
    under_reliance_rate = acc * (1.0 - trust_factor) * 0.3
    
    net_utility = acc * trust_factor - (alpha * over_reliance_rate + beta * under_reliance_rate)
    return {
        'Trust_Calibration_Factor': trust_factor,
        'Over_Reliance_Rate': over_reliance_rate,
        'Under_Reliance_Rate': under_reliance_rate,
        'Net_Clinical_Utility': max(0.0, net_utility)
    }
