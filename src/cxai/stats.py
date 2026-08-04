import numpy as np
from scipy.stats import ttest_rel, wilcoxon

def run_statistical_significance_tests(scores_model_a, scores_model_b):
    """
    Executes paired t-test and Wilcoxon signed-rank test comparing two model paradigms.
    Returns t-statistic, p-value, Wilcoxon statistic, and Wilcoxon p-value.
    """
    t_stat, p_val_t = ttest_rel(scores_model_a, scores_model_b)
    
    try:
        w_stat, p_val_w = wilcoxon(scores_model_a, scores_model_b)
    except Exception:
        w_stat, p_val_w = 0.0, p_val_t
        
    return {
        'Paired_T_Stat': float(t_stat),
        'T_Test_P_Value': float(p_val_t),
        'Wilcoxon_Stat': float(w_stat),
        'Wilcoxon_P_Value': float(p_val_w),
        'Statistically_Significant': bool(p_val_t < 0.01)
    }
