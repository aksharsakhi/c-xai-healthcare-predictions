import matplotlib.pyplot as plt
import numpy as np

def plot_reliability_diagram(y_true, y_prob, model_name="Model", save_path=None):
    """
    Plots Probability Calibration Reliability Diagram (Confidence vs Accuracy) with ECE annotation.
    """
    fig, ax = plt.subplots(figsize=(5, 4.5))
    n_bins = 10
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    
    bin_accs = []
    bin_confs = []
    
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    
    for i in range(n_bins):
        bin_lower, bin_upper = bin_boundaries[i], bin_boundaries[i+1]
        in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)
        if np.sum(in_bin) > 0:
            bin_accs.append(np.mean(y_true[in_bin]))
            bin_confs.append(np.mean(y_prob[in_bin]))
        else:
            bin_accs.append((bin_lower + bin_upper) / 2)
            bin_confs.append((bin_lower + bin_upper) / 2)
            
    ax.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
    ax.plot(bin_confs, bin_accs, 's-', color='#2ca02c', linewidth=2, label=f'{model_name}')
    ax.set_xlabel('Mean Predicted Probability (Confidence)')
    ax.set_ylabel('Empirical Accuracy')
    ax.set_title(f'Reliability Diagram: {model_name}')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.close()
