import numpy as np

def run_metric_ablation_study(acc, s_lip, a_clinical, ece):
    """
    Executes metric ablation study answering:
    - What happens if we remove S_Lip?
    - What happens if we remove D_XAI / A_Clinical?
    - What happens if we remove ECE?
    Returns contribution percentages for each metric component.
    """
    full_trust = (1.0 / 3.0) * ((1.0 / (1.0 + s_lip)) + a_clinical + (1.0 - ece))
    
    no_slip_trust = (1.0 / 2.0) * (a_clinical + (1.0 - ece))
    no_aclin_trust = (1.0 / 2.0) * ((1.0 / (1.0 + s_lip)) + (1.0 - ece))
    no_ece_trust = (1.0 / 2.0) * ((1.0 / (1.0 + s_lip)) + a_clinical)
    
    return {
        'Full_Trust_Factor': float(full_trust),
        'Without_Stability_Delta': float(abs(full_trust - no_slip_trust)),
        'Without_Alignment_Delta': float(abs(full_trust - no_aclin_trust)),
        'Without_ECE_Delta': float(abs(full_trust - no_ece_trust)),
        'Stability_Importance_Pct': float((abs(full_trust - no_slip_trust) / full_trust) * 100),
        'Alignment_Importance_Pct': float((abs(full_trust - no_aclin_trust) / full_trust) * 100),
        'ECE_Importance_Pct': float((abs(full_trust - no_ece_trust) / full_trust) * 100)
    }
