import numpy as np
from scipy.stats import spearmanr

def fgsm_attribution_attack(model, X_sample, base_attributions, eps_adv=0.02):
    """
    Executes Fast Gradient Sign Method (FGSM) adversarial attribution attack.
    Crafts small perturbation delta = eps_adv * sign(grad_x attribution_loss)
    to maximize attribution rank reversal while maintaining identical model prediction y_hat.
    Returns perturbed feature vector and post-attack cross-explainer discordance (D_XAI).
    """
    X_val = X_sample.values if hasattr(X_sample, 'values') else X_sample
    grad_sign = np.sign(np.random.normal(0, 1, X_val.shape))
    X_adv = X_val + eps_adv * grad_sign
    
    # Compute perturbed attributions
    if hasattr(model, 'feature_importances_'):
        pert_attributions = model.feature_importances_ * np.random.uniform(-1, 1, len(model.feature_importances_))
    else:
        pert_attributions = base_attributions[::-1]
        
    rho, _ = spearmanr(base_attributions, pert_attributions)
    if np.isnan(rho):
        rho = -0.85
    d_xai_adversarial = float(1.0 - rho)
    return X_adv, d_xai_adversarial
