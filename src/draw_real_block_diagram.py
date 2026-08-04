import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_technical_block_diagram():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Color Palette - Professional Technical Schematic Style
    c_frame = '#1a365d'      # Deep Navy
    c_bg_sub = '#f7fafc'     # Crisp White-Gray Background
    c_box_1 = '#ebf8ff'      # Soft Blue
    c_box_2 = '#ebf8ff'      # Soft Cyan
    c_box_3 = '#faf5ff'      # Soft Purple
    c_box_4 = '#f0fff4'      # Soft Green
    c_box_5 = '#fff5f5'      # Soft Red/Coral
    
    c_border_1 = '#2b6cb0'
    c_border_2 = '#2c5282'
    c_border_3 = '#6b46c1'
    c_border_4 = '#276749'
    c_border_5 = '#c53030'

    # Outer Frame
    outer_box = patches.FancyBboxPatch((0.15, 0.15), 11.7, 6.7, boxstyle="round,pad=0.05", ec=c_frame, fc='#ffffff', lw=2)
    ax.add_patch(outer_box)
    
    # Title Block
    ax.text(6.0, 6.4, 'SYSTEM BLOCK DIAGRAM: C-XAI CLINICAL EVALUATION BENCHMARK PIPELINE', 
            ha='center', va='center', fontsize=11, fontweight='bold', color=c_frame)
    ax.text(6.0, 6.15, 'Author: Sheela Akshar Sakhi (Roll No: cb.sc.u4cse23547)  |  Supervisor: Dr. G. R. Ramya', 
            ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#4a5568')
    ax.plot([0.5, 11.5], [6.0, 6.0], color='#cbd5e0', lw=1.2)

    # BLOCK 1: Data Ingestion & Noise Perturbation Engine
    b1_outer = patches.Rectangle((0.4, 1.2), 2.1, 4.5, ec=c_border_1, fc=c_box_1, lw=1.5)
    ax.add_patch(b1_outer)
    ax.text(1.45, 5.4, 'BLOCK 1: DATA INGESTION &\nPERTURBATION ENGINE', ha='center', va='center', fontsize=8, fontweight='bold', color=c_border_1)
    
    # Sub-blocks inside Block 1
    s1_1 = patches.Rectangle((0.55, 4.3), 1.8, 0.7, ec=c_border_1, fc='#ffffff', lw=1)
    ax.add_patch(s1_1)
    ax.text(1.45, 4.65, 'Multi-Hospital EHR Vitals\n& Lab Feeds ($X \\in \\mathbb{R}^d$)', ha='center', va='center', fontsize=6.8)

    s1_2 = patches.Rectangle((0.55, 3.1), 1.8, 0.8, ec=c_border_1, fc='#ffffff', lw=1)
    ax.add_patch(s1_2)
    ax.text(1.45, 3.5, 'Noise Generator\n$\\delta \\sim \\mathcal{N}(0, \\epsilon^2 I)$', ha='center', va='center', fontsize=7, color='#c53030')

    s1_3 = patches.Rectangle((0.55, 1.6), 1.8, 0.8, ec=c_border_1, fc='#ffffff', lw=1)
    ax.add_patch(s1_3)
    ax.text(1.45, 2.0, 'Perturbed Patient Vector\n$x\' = x + \\delta \\in \\mathcal{B}_\\epsilon(x)$', ha='center', va='center', fontsize=6.8)

    ax.annotate('', xy=(1.45, 3.9), xytext=(1.45, 4.3), arrowprops=dict(arrowstyle="->", lw=1.2, color=c_border_1))
    ax.annotate('', xy=(1.45, 2.4), xytext=(1.45, 3.1), arrowprops=dict(arrowstyle="->", lw=1.2, color=c_border_1))

    # BLOCK 2: Model Training Zoo
    b2_outer = patches.Rectangle((2.8, 1.2), 2.1, 4.5, ec=c_border_2, fc=c_box_2, lw=1.5)
    ax.add_patch(b2_outer)
    ax.text(3.85, 5.4, 'BLOCK 2: PREDICTIVE\nMODEL ZOO', ha='center', va='center', fontsize=8, fontweight='bold', color=c_border_2)

    s2_1 = patches.Rectangle((2.95, 4.3), 1.8, 0.7, ec=c_border_2, fc='#ffffff', lw=1)
    ax.add_patch(s2_1)
    ax.text(3.85, 4.65, 'Random Forest (RF)\n$N_{trees} = 100$', ha='center', va='center', fontsize=6.8)

    s2_2 = patches.Rectangle((2.95, 3.1), 1.8, 0.8, ec=c_border_2, fc='#ffffff', lw=1)
    ax.add_patch(s2_2)
    ax.text(3.85, 3.5, 'Extra Trees Classifier\n(Ensemble Decision)', ha='center', va='center', fontsize=6.8)

    s2_3 = patches.Rectangle((2.95, 1.6), 1.8, 0.8, ec=c_border_2, fc='#ffffff', lw=1)
    ax.add_patch(s2_3)
    ax.text(3.85, 2.0, 'Multi-Layer Perceptron\nMLP NN (64x32)', ha='center', va='center', fontsize=6.8)

    # BLOCK 3: Post-Hoc Explainer Engine
    b3_outer = patches.Rectangle((5.2, 1.2), 2.1, 4.5, ec=c_border_3, fc=c_box_3, lw=1.5)
    ax.add_patch(b3_outer)
    ax.text(6.25, 5.4, 'BLOCK 3: POST-HOC\nEXPLAINER ENGINE', ha='center', va='center', fontsize=8, fontweight='bold', color=c_border_3)

    s3_1 = patches.Rectangle((5.35, 4.3), 1.8, 0.7, ec=c_border_3, fc='#ffffff', lw=1)
    ax.add_patch(s3_1)
    ax.text(6.25, 4.65, 'TreeSHAP Explainer\nShapley Value $\\phi_j$', ha='center', va='center', fontsize=6.8)

    s3_2 = patches.Rectangle((5.35, 3.1), 1.8, 0.8, ec=c_border_3, fc='#ffffff', lw=1)
    ax.add_patch(s3_2)
    ax.text(6.25, 3.5, 'LIME Tabular Explainer\nLocal Linear Surrogate', ha='center', va='center', fontsize=6.8)

    s3_3 = patches.Rectangle((5.35, 1.6), 1.8, 0.8, ec=c_border_3, fc='#ffffff', lw=1)
    ax.add_patch(s3_3)
    ax.text(6.25, 2.0, 'Permutation Feature\nImportance (PFI)', ha='center', va='center', fontsize=6.8)

    # BLOCK 4: C-XAI Quantitative Metrics Core
    b4_outer = patches.Rectangle((7.6, 1.2), 2.2, 4.5, ec=c_border_4, fc=c_box_4, lw=1.5)
    ax.add_patch(b4_outer)
    ax.text(8.7, 5.4, 'BLOCK 4: C-XAI QUANTITATIVE\nMETRICS CORE', ha='center', va='center', fontsize=8, fontweight='bold', color=c_border_4)

    s4_1 = patches.Rectangle((7.75, 4.4), 1.9, 0.65, ec=c_border_4, fc='#ffffff', lw=1)
    ax.add_patch(s4_1)
    ax.text(8.7, 4.725, 'Lipschitz Stability Index\n$\\mathcal{S}_{Lip} = \\max \\frac{||E(x)-E(x\')||}{||x-x\'||}$', ha='center', va='center', fontsize=6.3)

    s4_2 = patches.Rectangle((7.75, 3.4), 1.9, 0.65, ec=c_border_4, fc='#ffffff', lw=1)
    ax.add_patch(s4_2)
    ax.text(8.7, 3.725, 'Cross-Explainer Discordance\n$\\mathcal{D}_{XAI} = 1 - \\rho(r^A, r^B)$', ha='center', va='center', fontsize=6.3)

    s4_3 = patches.Rectangle((7.75, 2.4), 1.9, 0.65, ec=c_border_4, fc='#ffffff', lw=1)
    ax.add_patch(s4_3)
    ax.text(8.7, 2.725, 'Clinical Prior Distance\n$\\mathcal{W}_{Clinical} = EMD(P_M, P_C)$', ha='center', va='center', fontsize=6.3)

    s4_4 = patches.Rectangle((7.75, 1.4), 1.9, 0.65, ec=c_border_4, fc='#ffffff', lw=1)
    ax.add_patch(s4_4)
    ax.text(8.7, 1.725, 'Calibrated Clinical Utility\n$\\mathcal{U}_{Clinical} = A \\cdot \\mathcal{T} - (\\alpha OR + \\beta UR)$', ha='center', va='center', fontsize=6.3)

    # BLOCK 5: Clinical Decision Support & Feedback Loop
    b5_outer = patches.Rectangle((10.1, 1.2), 1.5, 4.5, ec=c_border_5, fc=c_box_5, lw=1.5)
    ax.add_patch(b5_outer)
    ax.text(10.85, 5.4, 'BLOCK 5: CLINICAL\nINTERFACE', ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_border_5)

    s5_1 = patches.Rectangle((10.2, 4.2), 1.3, 0.8, ec=c_border_5, fc='#ffffff', lw=1)
    ax.add_patch(s5_1)
    ax.text(10.85, 4.6, 'Physician Dashboard\n& Alerts', ha='center', va='center', fontsize=6.5)

    s5_2 = patches.Rectangle((10.2, 2.9), 1.3, 0.8, ec=c_border_5, fc='#ffffff', lw=1)
    ax.add_patch(s5_2)
    ax.text(10.85, 3.3, 'Trust Calibration\n$\\mathcal{T}_{Clinician}$ Score', ha='center', va='center', fontsize=6.5)

    s5_3 = patches.Rectangle((10.2, 1.6), 1.3, 0.8, ec=c_border_5, fc='#ffffff', lw=1)
    ax.add_patch(s5_3)
    ax.text(10.85, 2.0, 'Over-Reliance\nPrevention', ha='center', va='center', fontsize=6.5)

    # Main Connecting Flow Buses (Arrows between Blocks)
    ax.annotate('', xy=(2.8, 3.45), xytext=(2.5, 3.45), arrowprops=dict(arrowstyle="->", lw=2, color=c_frame))
    ax.annotate('', xy=(5.2, 3.45), xytext=(4.9, 3.45), arrowprops=dict(arrowstyle="->", lw=2, color=c_frame))
    ax.annotate('', xy=(7.6, 3.45), xytext=(7.3, 3.45), arrowprops=dict(arrowstyle="->", lw=2, color=c_frame))
    ax.annotate('', xy=(10.1, 3.45), xytext=(9.8, 3.45), arrowprops=dict(arrowstyle="->", lw=2, color=c_frame))

    # Feedback Loop (Bottom Bus Line from Block 5 back to Block 1)
    ax.plot([10.85, 10.85, 1.45, 1.45], [1.2, 0.6, 0.6, 1.2], color=c_border_5, linestyle='--', lw=1.5)
    ax.annotate('', xy=(1.45, 1.2), xytext=(1.45, 0.65), arrowprops=dict(arrowstyle="->", lw=1.5, color=c_border_5))
    ax.text(6.0, 0.45, 'Clinical Feedback & Model Calibration Loop', ha='center', va='center', fontsize=7.5, fontweight='bold', color=c_border_5)

    plt.tight_layout()
    plt.savefig('paper/figures/fig0_architecture.png', dpi=300)
    plt.savefig('presentation/figures/fig0_architecture.png', dpi=300)
    plt.close()
    print("Technical system block diagram generated and saved to paper/figures/fig0_architecture.png!")

if __name__ == '__main__':
    create_technical_block_diagram()
