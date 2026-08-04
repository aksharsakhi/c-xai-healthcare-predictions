import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Colors
    c_blue = '#1f77b4'
    c_orange = '#ff7f0e'
    c_green = '#2ca02c'
    c_red = '#d62728'
    c_purple = '#9467bd'
    c_bg = '#f8f9fa'

    # Background canvas
    rect_bg = patches.FancyBboxPatch((0.2, 0.2), 9.6, 5.6, boxstyle="round,pad=0.1", ec="#cccccc", fc=c_bg, lw=1.5)
    ax.add_patch(rect_bg)
    
    # Title
    ax.text(5, 5.5, 'C-XAI Architecture: Quantitative Clinical Explainability Benchmark Pipeline', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#333333')

    # Box 1: Data & Perturbation Module
    b1 = patches.FancyBboxPatch((0.5, 3.5), 2.2, 1.5, boxstyle="round,pad=0.1", ec=c_blue, fc='#e8f4f8', lw=2)
    ax.add_patch(b1)
    ax.text(1.6, 4.6, 'Data & Perturbation\nModule', ha='center', va='center', fontweight='bold', fontsize=9, color=c_blue)
    ax.text(1.6, 3.9, '• Clinical EHR / Cohorts\n• Noise Injection ($\\epsilon$-ball)\n• Multi-Hospital Features', ha='center', va='center', fontsize=7.5)

    # Box 2: Predictive Model Layer
    b2 = patches.FancyBboxPatch((3.4, 3.5), 2.2, 1.5, boxstyle="round,pad=0.1", ec=c_orange, fc='#fff3e0', lw=2)
    ax.add_patch(b2)
    ax.text(4.5, 4.6, 'Predictive Models\nLayer', ha='center', va='center', fontweight='bold', fontsize=9, color=c_orange)
    ax.text(4.5, 3.9, '• Random Forest / ET\n• Deep Neural Net (MLP)\n• XGBoost / Gradient Boost', ha='center', va='center', fontsize=7.5)

    # Box 3: Multi-Explainer Engine
    b3 = patches.FancyBboxPatch((6.3, 3.5), 2.2, 1.5, boxstyle="round,pad=0.1", ec=c_purple, fc='#f3e5f5', lw=2)
    ax.add_patch(b3)
    ax.text(7.4, 4.6, 'Post-Hoc Explainer\nEngine', ha='center', va='center', fontweight='bold', fontsize=9, color=c_purple)
    ax.text(7.4, 3.9, '• TreeSHAP / KernelSHAP\n• LIME Tabular Explainer\n• Permutation Importance', ha='center', va='center', fontsize=7.5)

    # Arrows (Top Row)
    ax.annotate('', xy=(3.3, 4.25), xytext=(2.8, 4.25), arrowprops=dict(arrowstyle="->", lw=2, color='#555555'))
    ax.annotate('', xy=(6.2, 4.25), xytext=(5.7, 4.25), arrowprops=dict(arrowstyle="->", lw=2, color='#555555'))

    # Box 4: Quantitative Evaluation Metrics Suite (Center Bottom)
    b4 = patches.FancyBboxPatch((1.5, 0.8), 5.0, 2.0, boxstyle="round,pad=0.1", ec=c_green, fc='#e8f5e9', lw=2)
    ax.add_patch(b4)
    ax.text(4.0, 2.5, 'C-XAI Quantitative Evaluation Metrics Suite', ha='center', va='center', fontweight='bold', fontsize=10, color=c_green)
    ax.text(4.0, 1.6, '1. Local Lipschitz Stability ($\\mathcal{S}_{Lip}$): $\\max_{x\' \\in \\mathcal{B}_\\epsilon(x)} \\frac{||E(x)-E(x\')||}{||x-x\'||}$\n'
                      '2. Cross-Explainer Discordance ($\\mathcal{D}_{XAI}$): $1 - \\rho(\\text{SHAP}, \\text{LIME})$\n'
                      '3. Clinical Prior Wasserstein Distance ($\\mathcal{W}_{Clinical}$): $\\text{EMD}(P_{Model}, P_{Clinical})$\n'
                      '4. Calibrated Decision Utility ($\\mathcal{U}_{Clinical}$): $A_{Model} \\cdot \\mathcal{T} - (\\alpha \\text{OR} + \\beta \\text{UR})$', 
            ha='center', va='center', fontsize=7.5)

    # Box 5: Clinical Decision Support & Reliance (Bottom Right)
    b5 = patches.FancyBboxPatch((7.0, 0.8), 2.3, 2.0, boxstyle="round,pad=0.1", ec=c_red, fc='#ffebee', lw=2)
    ax.add_patch(b5)
    ax.text(8.15, 2.5, 'Clinical Decision\nSupport', ha='center', va='center', fontweight='bold', fontsize=9, color=c_red)
    ax.text(8.15, 1.5, '• Physician Workflow\n• Error Detection\n• Over/Under-Reliance\n• Trust Calibration', ha='center', va='center', fontsize=7.5)

    # Arrows (Connecting to Metrics & Support)
    ax.annotate('', xy=(4.0, 2.9), xytext=(7.4, 3.4), arrowprops=dict(arrowstyle="->", lw=2, color='#555555', connectionstyle="arc3,rad=0.2"))
    ax.annotate('', xy=(6.6, 1.8), xytext=(6.9, 1.8), arrowprops=dict(arrowstyle="<-", lw=2, color='#555555'))

    plt.tight_layout()
    plt.savefig('paper/figures/fig0_architecture.png', dpi=300)
    plt.savefig('presentation/figures/fig0_architecture.png', dpi=300)
    plt.close()
    print("Architecture diagram saved to paper/figures/fig0_architecture.png!")

if __name__ == '__main__':
    draw_architecture_diagram()
