#!/usr/bin/env python3
"""
build_technical_backup_presentation.py
Generates the comprehensive Technical Backup Presentation for ICMLDE 2026:
"C-XAI: Technical Defense & Backup Documentation"
Paper ID: Akshar_ICMLDE2026

Content:
- Four metric equations and derivations (Local Lipschitz, Cross-Explainer Discordance,
  Dimension-Normalized Wasserstein Prior Distance, Calibrated Decision Utility,
  and Zeroth-Order Gaussian Score Smoother).
- Detailed dataset characteristics & clinical prior guidelines across 4 cohorts (51.3K records).
- Predictive model architectures and exact hyperparameter zoo.
- Statistical significance tables (N=50 seeds, Wilcoxon W=0.0 p<0.001, Paired t=14.82 p<0.001).
- Additional experimental results: Perturbation scale sweep, Trust weight profiles, Adversarial stress-tests, Latency/RAM benchmarks.
- Comprehensive comparison with existing XAI frameworks (Captum, OpenXAI, Quantus, SENN).
- Regulatory compliance mapping (FDA SaMD & EU AI Act).
"""

import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# =============================================================================
# COLOR PALETTE (Matches ICMLDE 2026 Theme)
# =============================================================================
COLOR_DEEP_PURPLE = RGBColor(63, 14, 114)     # #3F0E72 - Primary Brand
COLOR_RICH_INDIGO = RGBColor(48, 10, 88)      # #300A58 - Deep Dark
COLOR_MID_PURPLE  = RGBColor(112, 48, 160)    # #7030A0 - Vibrant Accent
COLOR_CYAN        = RGBColor(0, 168, 204)     # #00A8CC - Accent Highlight
COLOR_CYAN_LIGHT  = RGBColor(80, 240, 255)    # #50F0FF - Bright Accent
COLOR_WHITE       = RGBColor(255, 255, 255)
COLOR_DARK_TEXT   = RGBColor(30, 35, 50)      # Heading / Table Text
COLOR_SLATE       = RGBColor(70, 75, 90)      # Body Text
COLOR_LIGHT_BG    = RGBColor(248, 249, 253)   # Card Fill
COLOR_BORDER      = RGBColor(218, 224, 240)   # Card / Table Border
COLOR_ROW_ALT     = RGBColor(243, 245, 252)   # Table Alt Row
COLOR_CALLOUT_BG  = RGBColor(238, 242, 255)   # Formula Callout Fill
COLOR_CALLOUT_BORDER = RGBColor(165, 180, 252)# Formula Callout Border
COLOR_BADGE_BG    = RGBColor(235, 230, 250)   # Category Badge Fill

def create_slide_header(slide, category, title, subtitle=None):
    """Creates a standardized professional header banner across content slides."""
    # Top Category Badge
    badge_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(4.5), Inches(0.35))
    tf_b = badge_box.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = f"■  {category.upper()}"
    p_b.font.name = "Times New Roman"
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_MID_PURPLE

    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.72), Inches(12.0), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = "Times New Roman"
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_DEEP_PURPLE

    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.35), Inches(12.0), Inches(0.4))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = "Times New Roman"
        p_s.font.size = Pt(11.5)
        p_s.font.color.rgb = COLOR_SLATE

def create_slide_footer(slide, current_slide, total_slides=16):
    """Creates the standardized bottom footer with paper and conference attribution."""
    footer_box = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(12.133), Inches(0.35))
    tf = footer_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"ICMLDE 2026  |  Paper ID: 857  |  Technical Defense & Backup Slides  |  Slide {current_slide} of {total_slides}"
    p.font.name = "Times New Roman"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_SLATE

def add_card(slide, left, top, width, height, bg_color=COLOR_LIGHT_BG, border_color=COLOR_BORDER):
    """Adds a rounded-corner container card shape."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def format_table(table, col_widths, headers, data, font_size=10, header_font_size=10.5):
    """Applies clean academic formatting to pptx tables."""
    for idx, width in enumerate(col_widths):
        table.columns[idx].width = width

    # Format Header Row
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_DEEP_PURPLE
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.04)
        cell.margin_bottom = Inches(0.04)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = "Times New Roman"
        p.font.size = Pt(header_font_size)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    # Format Data Rows
    for r_idx, row in enumerate(data):
        row_fill = COLOR_WHITE if r_idx % 2 == 0 else COLOR_ROW_ALT
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_fill
            cell.margin_left = Inches(0.06)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = "Times New Roman"
            p.font.size = Pt(font_size)
            p.font.color.rgb = COLOR_DARK_TEXT
            if c_idx > 1 and ("0." in str(val) or "%" in str(val) or str(val).isdigit()):
                p.alignment = PP_ALIGN.CENTER

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    # Background card
    add_card(s1, Inches(0.5), Inches(0.5), Inches(12.333), Inches(6.5), COLOR_LIGHT_BG, COLOR_BORDER)

    # Conference Ribbon
    tb_conf = s1.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.333), Inches(0.6))
    tf_conf = tb_conf.text_frame
    p_conf1 = tf_conf.paragraphs[0]
    p_conf1.text = "5th Elsevier International Conference on Machine Learning and Data Engineering (ICMLDE 2026)"
    p_conf1.font.name = "Times New Roman"
    p_conf1.font.size = Pt(14)
    p_conf1.font.bold = True
    p_conf1.font.color.rgb = COLOR_MID_PURPLE
    p_conf2 = tf_conf.add_paragraph()
    p_conf2.text = "27th–28th November 2026 · Dehradun, India · Procedia Computer Science"
    p_conf2.font.name = "Times New Roman"
    p_conf2.font.size = Pt(11.5)
    p_conf2.font.color.rgb = COLOR_SLATE

    # Main Presentation Title
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.333), Inches(1.6))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "C-XAI: Technical Defense & Backup Documentation"
    p_t1.font.name = "Times New Roman"
    p_t1.font.size = Pt(28)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_DEEP_PURPLE

    p_t2 = tf_title.add_paragraph()
    p_t2.text = "Comprehensive Metric Derivations, Dataset Characteristics, Model Zoo Architectures, Statistical Significance & Extended Experimental Audits"
    p_t2.font.name = "Times New Roman"
    p_t2.font.size = Pt(14)
    p_t2.font.color.rgb = COLOR_MID_PURPLE

    # Authors & Affiliations Box
    add_card(s1, Inches(1.0), Inches(3.7), Inches(11.333), Inches(2.2), COLOR_WHITE, COLOR_BORDER)
    tb_auth = s1.shapes.add_textbox(Inches(1.2), Inches(3.8), Inches(10.9), Inches(2.0))
    tf_auth = tb_auth.text_frame
    tf_auth.word_wrap = True

    p_a1 = tf_auth.paragraphs[0]
    r_a1 = p_a1.add_run()
    r_a1.text = "Sheela Akshar Sakhi¹ (Presenter)"
    r_a1.font.underline = True
    r_a1.font.bold = True
    r_a1.font.color.rgb = COLOR_DEEP_PURPLE
    r_a2 = p_a1.add_run()
    r_a2.text = ", Ibbraheem Shaik¹, Settibattini Suhitha¹, Ramya G R²*"
    r_a2.font.bold = True
    r_a2.font.color.rgb = COLOR_DEEP_PURPLE
    p_a1.font.name = "Times New Roman"
    p_a1.font.size = Pt(15)

    p_a2 = tf_auth.add_paragraph()
    p_a2.text = "¹Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore, Amrita Vishwa Vidyapeetham, India\n²Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore, Amrita Vishwa Vidyapeetham, India\n*Corresponding Author: Dr. Ramya G R (gr_ramya@cb.amrita.edu)"
    p_a2.font.name = "Times New Roman"
    p_a2.font.size = Pt(11.5)
    p_a2.font.color.rgb = COLOR_SLATE
    p_a2.space_before = Pt(4)

    p_a3 = tf_auth.add_paragraph()
    p_a3.text = "Paper ID: 857   |   Presentation Track: Technical Session & Award Committee Review"
    p_a3.font.name = "Times New Roman"
    p_a3.font.size = Pt(12)
    p_a3.font.bold = True
    p_a3.font.color.rgb = COLOR_CYAN
    p_a3.space_before = Pt(8)

    create_slide_footer(s1, 1)

    # =========================================================================
    # SLIDE 2: BACKUP DECK INDEX & STRUCTURE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    create_slide_header(s2, "Defense Roadmap", "Structure of Technical Defense & Backup Documentation",
                        "Organized across 6 thematic categories to support rigorous questioning from senior researchers and award evaluators.")

    cards_info = [
        ("Part I: Quantitative Formulations & Derivations",
         "• Metric 1: Empirical Local Lipschitz Stability (SbLip) & Proof of Axioms (Slide 3)\n• Metric 2: Cross-Explainer Discordance (DXAI) & Cognitive Dissonance (Slide 4)\n• Metric 3: Dimension-Normalized Wasserstein Prior Distance (W_Clin^norm) (Slide 5)\n• Metric 4: Net In-Silico Clinical Decision Utility (U_Clin) & Score Smoother (Slide 6)",
         Inches(0.6), Inches(1.8), Inches(6.0), Inches(2.35)),
        ("Part II: Healthcare Cohorts & Experimental Setup",
         "• Comprehensive Dataset Metadata: MIMIC-IV, eICU, BCWD, Cardio EHR (Slide 7)\n• Codified Clinical Prior Formulations: SOFA, Sepsis-3, NPI, ASCVD guidelines\n• Predictive Model Zoo: Random Forest, Extra Trees, MLP, Tabular Deep ResNet (Slide 8)\n• Explainer Suite: TreeSHAP, KernelSHAP, LIME, SmoothGrad, IntGrad, PFI",
         Inches(6.8), Inches(1.8), Inches(5.9), Inches(2.35)),
        ("Part III: Statistical Rigor & Hypothesis Testing",
         "• Full Table 1 Benchmark Results across 4 cohorts & 50 random trials (Slide 9)\n• Non-parametric Wilcoxon Signed-Rank Test (W = 0.0, p < 0.001)\n• Parametric Paired Two-Tailed t-Test (t = 14.82, p < 0.001, Cohen's d = 2.96)\n• Derivation of +19.6% Decision Utility Advantage (0.8485 vs 0.7095)",
         Inches(0.6), Inches(4.35), Inches(6.0), Inches(2.55)),
        ("Part IV: Extended Ablations & Operational Readiness",
         "• Perturbation Sensitivity Analysis across scale sweep h in [0.01, 0.20] (Slide 10)\n• Trust Weight Sensitivity across 5 clinical decision profiles (Slide 11)\n• Adversarial Stress-Tests under FGSM, ScaL-PGD, & 20% Missingness (Slide 12)\n• Latency/RAM Profiling (Slide 13) | Comparison (Slide 14) | Bibliography (Slide 15) | Q&A (Slide 16)",
         Inches(6.8), Inches(4.35), Inches(5.9), Inches(2.55))
    ]

    for title, body, left, top, width, height in cards_info:
        add_card(s2, left, top, width, height, COLOR_LIGHT_BG, COLOR_BORDER)
        tb = s2.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Times New Roman"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_DEEP_PURPLE

        p_b = tf.add_paragraph()
        p_b.text = body
        p_b.font.name = "Times New Roman"
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = COLOR_DARK_TEXT
        p_b.space_before = Pt(4)

    create_slide_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: METRIC 1: LOCAL LIPSCHITZ STABILITY & THEORETICAL DERIVATION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    create_slide_header(s3, "Mathematical Foundations", "Metric 1: Empirical Local Lipschitz Explanation Stability (SbLip)",
                        "Quantifies attribution robustness under physiological sensor noise via Monte Carlo expectation.")

    # Left Column: Equation & Clinical Motivation
    add_card(s3, Inches(0.6), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_eq = s3.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_eq = tb_eq.text_frame
    tf_eq.word_wrap = True

    p = tf_eq.paragraphs[0]
    p.text = "Mathematical Formulation:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    # Formula Callout
    p_f = tf_eq.add_paragraph()
    p_f.text = "S_bLip(x, h) = (1 / M) ∑_{m=1}^{M} [ ||E(x) - E(x + u_m)||_2 / (||u_m||_2 + τ) ]\nwhere u_m ~ N(0, h² I)"
    p_f.font.name = "Times New Roman"
    p_f.font.size = Pt(13)
    p_f.font.bold = True
    p_f.font.color.rgb = COLOR_RICH_INDIGO
    p_f.space_before = Pt(6)
    p_f.space_after = Pt(8)

    bullets_left = [
        ("• Physiological Noise Injection: ", "Clinical vitals and lab analytes naturally fluctuate. Rather than worst-case adversarial supremum bounds [Alvarez-Melis & Jaakkola, 2018], C-XAI models standard sensor uncertainty."),
        ("• Monte Carlo Approximation: ", "Evaluates M = 100 stochastic draws within a perturbation sphere of radius h = 0.05."),
        ("• Singularity Protection: ", "τ = 10⁻⁸ guarantees numerical stability when ||u_m||_2 → 0."),
        ("• Bounded Interpretation: ", "Lower values indicate superior stability. An ideal explainer satisfies S_bLip = 0.0 under local invariant shifts.")
    ]
    for b_title, b_desc in bullets_left:
        p_b = tf_eq.add_paragraph()
        r1 = p_b.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_b.font.name = "Times New Roman"
        p_b.font.size = Pt(10.5)
        p_b.space_before = Pt(4)

    # Right Column: Axiomatic Proofs & Derivation
    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_CALLOUT_BG, COLOR_CALLOUT_BORDER)
    tb_pr = s3.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True

    p = tf_pr.paragraphs[0]
    p.text = "Theorem 1: Metric Axioms & Convergence Proofs"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    proofs = [
        ("1. Non-Negativity: ", "Euclidean vector norms satisfy ||•||_2 ≥ 0. Since τ = 10⁻⁸ > 0 and ||u_m||_2 ≥ 0, every term in the Monte Carlo summation is strictly non-negative: S_bLip(x, h) ≥ 0, ∀ x, h."),
        ("2. Linear Stability Invariance: ", "For linear models f(x) = wᵀx + b, gradient and Shapley attributions satisfy E(x) = w. Under any perturbation u_m, E(x + u_m) = w. Hence ||E(x) - E(x + u_m)||_2 = ||w - w||_2 = 0, proving S_bLip ≡ 0 for linear models."),
        ("3. Monotonic Taylor Convergence: ", "Expanding E(x + u_m) via first-order Taylor expansion around x yields: E(x + u_m) = E(x) + J_E(x) u_m + O(||u_m||²), where J_E(x) is the explainer Jacobian matrix. Substituting into S_bLip and taking lim_{h → 0} yields ||J_E(x)||_F (the Frobenius norm of the Jacobian), guaranteeing deterministic convergence under infinitesimal perturbations."),
        ("4. Clinical Significance: ", "Deep neural models possess steep local gradients, resulting in 9.6× higher S_bLip (0.4912 vs 0.0512 for Extra Trees).")
    ]
    for p_title, p_desc in proofs:
        p_p = tf_pr.add_paragraph()
        r1 = p_p.add_run()
        r1.text = p_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_p.add_run()
        r2.text = p_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_p.font.name = "Times New Roman"
        p_p.font.size = Pt(10.5)
        p_p.space_before = Pt(5)

    create_slide_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: METRIC 2: CROSS-EXPLAINER DISCORDANCE & DERIVATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    create_slide_header(s4, "Mathematical Foundations", "Metric 2: Cross-Explainer Discordance (DXAI) & Conflict Resolution",
                        "Quantifies feature ranking conflict between distinct explainers on the identical patient encounter.")

    # Left Card: Formula and Derivation
    add_card(s4, Inches(0.6), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_d1 = s4.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_d1 = tb_d1.text_frame
    tf_d1.word_wrap = True

    p = tf_d1.paragraphs[0]
    p.text = "Formulation & Range Bounds:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p_f = tf_d1.add_paragraph()
    p_f.text = "D_XAI(E_A, E_B) = 1 - r_s(r_A, r_B)\nwhere r_s = 1 - [ 6 ∑_{j=1}^{d} (r_{A,j} - r_{B,j})² / (d(d² - 1)) ]"
    p_f.font.name = "Times New Roman"
    p_f.font.size = Pt(13)
    p_f.font.bold = True
    p_f.font.color.rgb = COLOR_RICH_INDIGO
    p_f.space_before = Pt(6)
    p_f.space_after = Pt(8)

    bullets_dxai = [
        ("• Rank Vector Transformation: ", "Continuous attribution vectors E_A(x), E_B(x) are converted into integer feature rank orderings r_A, r_B in {1, ..., d}."),
        ("• Spearman Rank Correlation (r_s): ", "Measures monotonic rank agreement across d features, naturally bounded in [-1.0, +1.0]."),
        ("• Exact Discordance Bounds: ", "D_XAI in [0, 2]:\n  - D_XAI = 0.0: Perfect concordance (r_s = +1.0) — explainers agree completely.\n  - D_XAI = 1.0: Orthogonal rankings (r_s = 0.0) — explainers rank features independently.\n  - D_XAI = 2.0: Complete rank inversion (r_s = -1.0) — acute contradiction!"),
        ("• Clinician Cognitive Dissonance: ", "When two explainers display contradictory rationales for the same ICU patient, clinicians discard both [Krishna et al., 2022; Mitrut et al., 2024].")
    ]
    for b_title, b_desc in bullets_dxai:
        p_b = tf_d1.add_paragraph()
        r1 = p_b.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_b.font.name = "Times New Roman"
        p_b.font.size = Pt(10.5)
        p_b.space_before = Pt(4)

    # Right Card: Resolution of the Tree vs. Deep Discordance Disconnect
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_WHITE, COLOR_BORDER)
    tb_d2 = s4.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_d2 = tb_d2.text_frame
    tf_d2.word_wrap = True

    p = tf_d2.paragraphs[0]
    p.text = "Explaining the 0.059 vs. 0.435 Numerical Results:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    disc_expl = [
        ("• Extra Trees (D_XAI = 0.059): ", "On tree ensembles, TreeSHAP and LIME evaluate partition frequency and axis-aligned splits. Their pairwise Spearman rank correlation is r_s = 0.941. Substituting into the equation:\n  D_XAI = 1 - 0.941 = 0.059 (Tight Concordance)."),
        ("• Tabular Deep ResNet (D_XAI = 0.435): ", "On neural architectures, Integrated Gradients integrates infinitesimal path gradients across latent representations, while LIME samples perturbations in input space. Their rank correlation drops to r_s = 0.565:\n  D_XAI = 1 - 0.565 = 0.435 (Severe Discordance)."),
        ("• Impact on Decision Making: ", "On Tabular Deep ResNet, LIME identifies Serum Lactate as the #1 mortality driver, while Integrated Gradients assigns top priority to MAP and places Lactate 4th. This contradiction triggers severe clinician confusion."),
        ("• Ensemble Stability Advantage: ", "Extra Trees constrains explainer variation, ensuring consistent clinical explanations across both perturbation-based and path-based explainer paradigms.")
    ]
    for d_title, d_desc in disc_expl:
        p_d = tf_d2.add_paragraph()
        r1 = p_d.add_run()
        r1.text = d_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_d.add_run()
        r2.text = d_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_d.font.name = "Times New Roman"
        p_d.font.size = Pt(10.5)
        p_d.space_before = Pt(5)

    create_slide_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: METRIC 3: DIMENSION-NORMALIZED WASSERSTEIN PRIOR DISTANCE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    create_slide_header(s5, "Mathematical Foundations", "Metric 3: Dimension-Normalized Wasserstein Prior Distance (W_Clin^norm)",
                        "Measures alignment with clinical guidelines via optimal transport, normalized across feature dimensions.")

    # Left Column: Formulation & Guideline Weighting
    add_card(s5, Inches(0.6), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_w1 = s5.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_w1 = tb_w1.text_frame
    tf_w1.word_wrap = True

    p = tf_w1.paragraphs[0]
    p.text = "Prior Construction & Wasserstein Metric:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p_f = tf_w1.add_paragraph()
    p_f.text = "W_Clin^{norm} = [1 / (d - 1)] ∑_{j=1}^{d} | ∑_{k=1}^{j} P_Model(k) - ∑_{k=1}^{j} P_Clinical(k) |\nClinical Alignment: A_Clinical = 1 - W_Clin^{norm} ∈ [0, 1]"
    p_f.font.name = "Times New Roman"
    p_f.font.size = Pt(12.5)
    p_f.font.bold = True
    p_f.font.color.rgb = COLOR_RICH_INDIGO
    p_f.space_before = Pt(6)
    p_f.space_after = Pt(8)

    bullets_w1 = [
        ("• Codified Clinical Prior (P_Clinical): ", "Formulated from established medical risk standards (SOFA, Sepsis-3, NPI, Framingham ASCVD). Guideline weights w_j are min-max standardized and normalized to sum to 1.0."),
        ("• Normalized Model Prior (P_Model): ", "Empirical mean absolute explainer attribution across cohort instances: P_Model(j) = ē_j / ∑_k ē_k."),
        ("• Optimal Transport Grounding: ", "Computes 1D Earth Mover's Distance between cumulative attribution distributions, penalizing displacement of probability mass away from validated clinical drivers [Villani, 2009]."),
        ("• Preventing Hospital Confounders: ", "Detects models exploiting non-causal confounding artifacts (e.g., protocol timestamps, billing codes) instead of core physiological biomarkers.")
    ]
    for b_title, b_desc in bullets_w1:
        p_b = tf_w1.add_paragraph()
        r1 = p_b.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_b.add_run()
        r2.text = b_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_b.font.name = "Times New Roman"
        p_b.font.size = Pt(10.5)
        p_b.space_before = Pt(4)

    # Right Column: Theorem & Mathematical Proof of (d-1) Normalization
    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_CALLOUT_BG, COLOR_CALLOUT_BORDER)
    tb_w2 = s5.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_w2 = tb_w2.text_frame
    tf_w2.word_wrap = True

    p = tf_w2.paragraphs[0]
    p.text = "Theorem 2: Proof of (d - 1) Supremum Normalization"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    proof_steps = [
        ("1. 1D Discrete Earth Mover's Distance: ", "On ordered discrete support {1, 2, ..., d}, the Wasserstein-1 distance between probability mass functions P and Q equals the L₁ norm of their cumulative distribution functions: W₁(P, Q) = ∑_{j=1}^{d-1} |F_P(j) - F_Q(j)|."),
        ("2. Cumulative Function Properties: ", "Since P and Q are valid probability distributions (∑ P(k) = 1, P(k) ≥ 0), their CDFs satisfy F_P(d) = F_Q(d) = 1.0, and 0 ≤ F_P(j), F_Q(j) ≤ 1.0 for all j."),
        ("3. Extremal Configuration Supremum: ", "The difference |F_P(j) - F_Q(j)| is upper bounded by 1.0 for each index j ∈ {1, ..., d-1}. The maximum divergence occurs when all probability mass of P is concentrated at index 1 (F_P(j) = 1, ∀ j ≥ 1) and all mass of Q is concentrated at index d (F_Q(j) = 0, ∀ j < d). Then:\n  |F_P(j) - F_Q(j)| = |1 - 0| = 1,   ∀ j ∈ {1, ..., d-1}.\nSumming over all d - 1 cutoff indices yields exactly d - 1."),
        ("4. Strict Invariance across Cohorts: ", "Dividing by (d - 1) guarantees W_Clin^{norm} ∈ [0.0, 1.0] for any dimensionality d > 1, enabling rigorous cross-cohort benchmarking between d = 5 (Cardio) and d = 30 (BCWD).")
    ]
    for s_title, s_desc in proof_steps:
        p_s = tf_w2.add_paragraph()
        r1 = p_s.add_run()
        r1.text = s_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_s.add_run()
        r2.text = s_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_s.font.name = "Times New Roman"
        p_s.font.size = Pt(10.5)
        p_s.space_before = Pt(4)

    create_slide_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: METRIC 4 & SMOOTHER: DECISION UTILITY & SCORE SMOOTHER
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    create_slide_header(s6, "Decision Theory & Methodology", "Metric 4: In-Silico Clinical Utility (U_Clin) & Zeroth-Order Smoother",
                        "Links statistical explanation fidelity to clinical decision payoffs, with Gaussian smoothing for step-function trees.")

    # Left Card: Calibrated Decision Utility Formulation
    add_card(s6, Inches(0.6), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_u = s6.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True

    p = tf_u.paragraphs[0]
    p.text = "In-Silico Decision Utility (U_Clin):"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p_f = tf_u.add_paragraph()
    p_f.text = "U_Clin_hat = Acc · T_Clinician - (α · OR + β · UR)\nT_Clinician = w_s [1 / (1 + S_bLip)] + w_a A_Clinical + w_c (1 - ECE)\nOR = P(y_hat ≠ y)(1 - κ_OR T_Clinician),  UR = P(y_hat = y)(1 - T_Clinician)κ_UR"
    p_f.font.name = "Times New Roman"
    p_f.font.size = Pt(11.5)
    p_f.font.bold = True
    p_f.font.color.rgb = COLOR_RICH_INDIGO
    p_f.space_before = Pt(4)
    p_f.space_after = Pt(6)

    util_points = [
        ("• Clinician Trust Index (T_Clinician): ", "Integrates explanation stability (w_s=0.33), prior alignment (w_a=0.33), and Expected Calibration Error (w_c=0.33)."),
        ("• Asymmetric Clinical Risk Penalties: ", "Grounded in Pauker-Kassirer threshold theory [1980]. False positive over-reliance (OR) carries α = 0.50 (inappropriate invasive intervention); false negative under-reliance (UR) carries β = 0.30 (missed diagnosis)."),
        ("• Human-AI Reliance Parameters: ", "κ_OR = 0.85, κ_UR = 0.70 model clinician heuristic adjustments based on explanation trust [Bussone et al., 2015; Jacobs et al., 2021]."),
        ("• Net Utility Advantage: ", "Extra Trees achieves U_Clin = 0.8485 vs. Tabular Deep ResNet = 0.7095 on MIMIC-IV (+19.6% relative improvement, p < 0.001).")
    ]
    for u_title, u_desc in util_points:
        p_u = tf_u.add_paragraph()
        r1 = p_u.add_run()
        r1.text = u_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_u.add_run()
        r2.text = u_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_u.font.name = "Times New Roman"
        p_u.font.size = Pt(10)
        p_u.space_before = Pt(4)

    # Right Card: Zeroth-Order Gaussian Score Smoother for Trees
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_CALLOUT_BG, COLOR_CALLOUT_BORDER)
    tb_sm = s6.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_sm = tb_sm.text_frame
    tf_sm.word_wrap = True

    p = tf_sm.paragraphs[0]
    p.text = "Zeroth-Order Gaussian Score Smoother:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p_f2 = tf_sm.add_paragraph()
    p_f2.text = "f_σ(x) = E_{ξ ~ N(0, σ² I)} [ f(x + ξ) ]\n∇_x f_σ(x) = (1 / σ²) E_ξ [ ξ f(x + ξ) ] ≈ [1 / (K σ²)] ∑_{k=1}^{K} ξ_k f(x + ξ_k)"
    p_f2.font.name = "Times New Roman"
    p_f2.font.size = Pt(12)
    p_f2.font.bold = True
    p_f2.font.color.rgb = COLOR_RICH_INDIGO
    p_f2.space_before = Pt(6)
    p_f2.space_after = Pt(8)

    smoother_points = [
        ("• Overcoming Tree Non-Differentiability: ", "Decision trees partition input space into axis-aligned piecewise constant steps. Standard gradients ∇_x f(x) are zero almost everywhere and undefined at split boundaries."),
        ("• Score-Function Gradient Estimator: ", "By convolving f with a Gaussian mollifier ξ ~ N(0, σ² I), f_σ becomes infinitely smooth (C^∞) without modifying trained tree weights."),
        ("• Monte Carlo Estimation: ", "Approximates gradients via K = 50 stochastic forward passes using variance parameter σ = 0.05."),
        ("• Unified Evaluation Architecture: ", "Enables gradient-based attribution explainers (Integrated Gradients, SmoothGrad) to evaluate tree ensembles on equal footing with deep neural networks.")
    ]
    for sm_title, sm_desc in smoother_points:
        p_sm = tf_sm.add_paragraph()
        r1 = p_sm.add_run()
        r1.text = sm_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_sm.add_run()
        r2.text = sm_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_sm.font.name = "Times New Roman"
        p_sm.font.size = Pt(10.5)
        p_sm.space_before = Pt(4)

    create_slide_footer(s6, 6)

    # =========================================================================
    # SLIDE 7: DETAILED DATASET CHARACTERISTICS & CLINICAL PRIORS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    create_slide_header(s7, "Experimental Infrastructure", "Detailed Healthcare Cohorts & Codified Clinical Prior Guidelines",
                        "Comprehensive overview of evaluated patient populations (51,369 records total) and medical consensus standards.")

    t_shape7 = s7.shapes.add_table(5, 7, Inches(0.6), Inches(1.85), Inches(12.133), Inches(3.2))
    table7 = t_shape7.table
    col_w7 = [Inches(1.5), Inches(1.8), Inches(1.1), Inches(0.8), Inches(1.2), Inches(2.2), Inches(3.533)]
    headers7 = ["Cohort Name", "Clinical Task", "Sample Size", "Features", "Imbalance", "Codified Guideline", "Key Prior Weights (P_Clinical)"]
    data7 = [
        ["MIMIC-IV", "ICU Mortality Prediction", "40,000", "24", "11.2% (Pos)", "SOFA Consensus & Surviving Sepsis", "SOFA (0.35), Lactate (0.30), Age (0.15), MAP (0.10), HR (0.10)"],
        ["eICU", "Multi-Center Sepsis Onset", "10,000", "18", "14.8% (Pos)", "Sepsis-3 & SIRS Criteria", "MAP (0.40), Body Temp (0.25), WBC Count (0.20), HR (0.15)"],
        ["BCWD", "Breast Cancer Histology", "569", "30", "37.3% (Mal)", "Nottingham Prognostic Index (NPI)", "Worst Area (0.25), Worst Concave (0.25), Mean Concave (0.20), Worst Rad (0.15)"],
        ["Cardio EHR", "10-Yr Cardiovascular Risk", "800", "5", "25.0% (High)", "ACC/AHA 10-Yr ASCVD Risk", "Systolic BP (0.30), Age (0.25), Cholesterol (0.20), Smoking (0.15), Glucose (0.10)"]
    ]
    format_table(table7, col_w7, headers7, data7, font_size=9.5, header_font_size=10)

    # Lower Information Cards
    add_card(s7, Inches(0.6), Inches(5.25), Inches(3.85), Inches(1.6), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_c1 = s7.shapes.add_textbox(Inches(0.7), Inches(5.35), Inches(3.65), Inches(1.4))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "51,369 Total Clinical Records"
    p.font.name = "Times New Roman"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE
    p2 = tf_c1.add_paragraph()
    p2.text = "Spans multi-center tertiary intensive care units (MIMIC-IV, Beth Israel; eICU, 208 Philips healthcare hospitals) and outpatient clinical diagnostic pathology feeds."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(3)

    add_card(s7, Inches(4.7), Inches(5.25), Inches(3.85), Inches(1.6), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_c2 = s7.shapes.add_textbox(Inches(4.8), Inches(5.35), Inches(3.65), Inches(1.4))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "Clinical Prior Construction"
    p.font.name = "Times New Roman"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE
    p2 = tf_c2.add_paragraph()
    p2.text = "Guidelines weights w_j are established from validated medical prognostic standards (e.g. SOFA multi-organ dysfunction score, NPI tumor morphometry) and strictly normalized to sum to 1.0."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(3)

    add_card(s7, Inches(8.8), Inches(5.25), Inches(3.933), Inches(1.6), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_c3 = s7.shapes.add_textbox(Inches(8.9), Inches(5.35), Inches(3.7), Inches(1.4))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "Stratified Evaluation Protocol"
    p.font.name = "Times New Roman"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE
    p2 = tf_c3.add_paragraph()
    p2.text = "Stratified 5-fold cross-validation repeated across 50 random seeds (seeds 42–91). Preprocessing pipelines fitted strictly within training folds to eliminate test-fold data leakage."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(3)

    create_slide_footer(s7, 7)

    # =========================================================================
    # SLIDE 8: MACHINE LEARNING ZOO: ARCHITECTURES & HYPERPARAMETERS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    create_slide_header(s8, "Experimental Infrastructure", "Predictive Model Zoo: Architectures & Hyperparameter Specifications",
                        "Exact architectural topologies, training parameters, and explainer configurations across all benchmarks.")

    t_shape8 = s8.shapes.add_table(5, 5, Inches(0.6), Inches(1.85), Inches(12.133), Inches(3.1))
    table8 = t_shape8.table
    col_w8 = [Inches(2.0), Inches(2.2), Inches(2.8), Inches(2.6), Inches(2.533)]
    headers8 = ["Model Paradigm", "Architecture / Base", "Optimization & Regularization", "Hyperparameter Configuration", "Explainer Compatibility"]
    data8 = [
        ["Random Forest (RF)", "Ensemble of 100 axis-aligned decision trees", "Gini impurity criterion, bootstrap aggregation", "n_estimators=100, max_depth=12, min_samples_split=5, random_state=42", "TreeSHAP (exact O(TLD²)), LIME, PFI, Score-Smoothed IntGrad"],
        ["Extra Trees (ET)", "Ensemble of 100 randomized orthogonal trees", "Extremely randomized splits, Gini criterion", "n_estimators=100, max_depth=12, min_samples_split=2, random_state=42", "TreeSHAP, KernelSHAP, LIME, PFI, Score-Smoothed SmoothGrad"],
        ["Multi-Layer Perceptron", "Fully connected feed-forward deep network", "ReLU activations, early stopping (patience=15)", "Input → 64 → 32 → 1, Adam (lr=10⁻³, β₁=0.9, β₂=0.999), batch_size=64, epochs=300", "Integrated Gradients, SmoothGrad, KernelSHAP, LIME, PFI"],
        ["Tabular Deep ResNet", "Deep residual tabular network with tokenization", "Feature token embeddings, BatchNorm, Dropout (p=0.10)", "2 residual blocks (Linear+BN+ReLU+Dropout), skip connections, Adam (lr=5×10⁻⁴, wd=10⁻⁵)", "Integrated Gradients (50 steps), SmoothGrad (50 noise draws), KernelSHAP, LIME"]
    ]
    format_table(table8, col_w8, headers8, data8, font_size=9, header_font_size=10)

    # Explainer Suite Details Card
    add_card(s8, Inches(0.6), Inches(5.15), Inches(12.133), Inches(1.7), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_ex = s8.shapes.add_textbox(Inches(0.8), Inches(5.25), Inches(11.7), Inches(1.5))
    tf_ex = tb_ex.text_frame
    tf_ex.word_wrap = True

    p = tf_ex.paragraphs[0]
    p.text = "Comprehensive 6-Explainer Auditing Suite (Mathematical Diversity):"
    p.font.name = "Times New Roman"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p2 = tf_ex.add_paragraph()
    p2.text = "1. TreeSHAP: Exact polynomial tree traversal algorithm (Lundberg et al., 2020), interventional feature perturbation.\n2. KernelSHAP: Model-agnostic weighted linear regression approximating Shapley values (N_samples = 500).\n3. LIME: Local surrogate linear model fitted with exponential distance kernel weights (N_samples = 1000, Ribeiro et al., 2016).\n4. SmoothGrad: Noise-augmented saliency averaging input gradients over M = 50 Gaussian perturbations (σ = 0.10, Smilkov et al., 2017).\n5. Integrated Gradients: Path-integral path-integrating gradients along straight line from zero baseline across K = 50 Gauss-Legendre quadrature steps (Sundararajan et al., 2017).\n6. Permutation Feature Importance (PFI): Empirical test-set feature permuting shuffling feature columns over N_repeats = 10."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(3)

    create_slide_footer(s8, 8)

    # =========================================================================
    # SLIDE 9: STATISTICAL SIGNIFICANCE & HYPOTHESIS TESTING (N=50 SEEDS)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    create_slide_header(s9, "Statistical Rigor", "Overall Benchmark Results & Hypothesis Testing (N = 50 Trials)",
                        "Full Table 1 empirical results across 4 healthcare cohorts with formal non-parametric and parametric significance tests.")

    t_shape9 = s9.shapes.add_table(17, 7, Inches(0.6), Inches(1.75), Inches(7.5), Inches(5.0))
    table9 = t_shape9.table
    col_w9 = [Inches(1.2), Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)]
    headers9 = ["Cohort", "Model", "Acc. ↑", "SbLip ↓", "DXAI ↓", "W_Clin ↓", "U_Clin ↑"]
    data9 = [
        ["MIMIC-IV", "Random Forest", "0.8845", "0.0821", "0.0812", "0.0285", "0.8412"],
        ["", "Extra Trees", "0.8812", "0.0512", "0.0589", "0.0312", "0.8485"],
        ["", "MLP", "0.8920", "0.4850", "0.4120", "0.0389", "0.7120"],
        ["", "Tabular ResNet", "0.8935", "0.4912", "0.4350", "0.0375", "0.7105"],
        ["eICU", "Random Forest", "0.8510", "0.1120", "0.0920", "0.0298", "0.7915"],
        ["", "Extra Trees", "0.8485", "0.0785", "0.0715", "0.0315", "0.7980"],
        ["", "MLP", "0.8420", "0.4620", "0.3950", "0.0412", "0.6850"],
        ["", "Tabular ResNet", "0.8540", "0.4820", "0.4210", "0.0390", "0.6810"],
        ["BCWD", "Random Forest", "0.9649", "0.0643", "0.0614", "0.0307", "0.9062"],
        ["", "Extra Trees", "0.9649", "0.0411", "0.0463", "0.0371", "0.9139"],
        ["", "MLP", "0.9737", "0.4500", "0.3800", "0.0328", "0.7828"],
        ["", "Tabular ResNet", "0.9737", "0.4680", "0.3980", "0.0315", "0.7780"],
        ["Cardio", "Random Forest", "0.8000", "0.3066", "0.1000", "0.0306", "0.6191"],
        ["", "Extra Trees", "0.7875", "0.2491", "0.1000", "0.0306", "0.6201"],
        ["", "MLP", "0.7750", "0.4500", "0.3800", "0.0504", "0.5470"],
        ["", "Tabular ResNet", "0.7812", "0.4706", "0.3920", "0.0485", "0.5420"]
    ]
    format_table(table9, col_w9, headers9, data9, font_size=8.5, header_font_size=9)

    # Right Column: Statistical Hypothesis Testing Breakdown
    add_card(s9, Inches(8.3), Inches(1.75), Inches(4.433), Inches(5.0), COLOR_CALLOUT_BG, COLOR_CALLOUT_BORDER)
    tb_st = s9.shapes.add_textbox(Inches(8.45), Inches(1.9), Inches(4.1), Inches(4.7))
    tf_st = tb_st.text_frame
    tf_st.word_wrap = True

    p = tf_st.paragraphs[0]
    p.text = "Rigorous Statistical Validation:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    stats_list = [
        ("• Formal Statistical Hypothesis: ", "H₀: U_Clin(ET) ≤ U_Clin(Deep ResNet) vs. H₁: U_Clin(ET) > U_Clin(Deep ResNet)."),
        ("• Non-Parametric Wilcoxon Signed-Rank: ", "Across N = 50 paired cross-validation trials, Extra Trees strictly outperformed Tabular Deep ResNet in all 50 seeds:\n  Wilcoxon W = 0.0, p = 2.4 × 10⁻⁷ < 0.001 (Extremely Significant)."),
        ("• Parametric Paired Two-Tailed t-Test: ", "Mean utility difference ΔU = +0.1390 (0.8485 vs 0.7095, SD = 0.0469):\n  t(49) = 14.82, p = 1.8 × 10⁻¹⁹ < 0.001.\n  Cohen's d = 2.96 (Exceeds standard threshold for massive clinical effect size)."),
        ("• Relative Gain (+19.6% Calculation): ", "Relative Gain = (0.8485 - 0.7095) / 0.7095 = +0.1390 / 0.7095 = +19.59% ≈ +19.6% (+13.9 percentage points absolute)."),
        ("• Decoupling Paradox Confirmed: ", "While Deep ResNet achieved +1.23% higher raw accuracy on MIMIC-IV (89.35% vs 88.12%), its 9.6× higher instability (0.4912 vs 0.0512) and severe discordance (0.4350 vs 0.0589) destroyed clinical decision utility.")
    ]
    for s_title, s_desc in stats_list:
        p_s = tf_st.add_paragraph()
        r1 = p_s.add_run()
        r1.text = s_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_s.add_run()
        r2.text = s_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_s.font.name = "Times New Roman"
        p_s.font.size = Pt(9.5)
        p_s.space_before = Pt(4)

    create_slide_footer(s9, 9)

    # =========================================================================
    # SLIDE 10: PERTURBATION SENSITIVITY ANALYSIS (h SWEEP)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    create_slide_header(s10, "Extended Experimental Results", "Perturbation Sensitivity Analysis across Scaling Sweep (h ∈ [0.01, 0.20])",
                        "Demonstrates sub-linear stability scaling in tree ensembles vs. catastrophic supra-linear explosion in deep networks.")

    t_shape10 = s10.shapes.add_table(6, 5, Inches(0.6), Inches(1.85), Inches(7.5), Inches(2.8))
    table10 = t_shape10.table
    col_w10 = [Inches(2.5), Inches(1.25), Inches(1.25), Inches(1.25), Inches(1.25)]
    headers10 = ["Perturbation Scale (h)", "Extra Trees", "Random Forest", "MLP", "Deep ResNet"]
    data10 = [
        ["h = 0.01 (Micro-noise)", "0.0180", "0.0250", "0.2300", "0.2800"],
        ["h = 0.02 (Low noise)", "0.0248", "0.0361", "0.3698", "0.4550"],
        ["h = 0.05 (Standard physiological)", "0.0414", "0.0644", "0.7720", "0.9715"],
        ["h = 0.10 (Elevated noise)", "0.0642", "0.1046", "1.4169", "1.8190"],
        ["h = 0.20 (Severe sensor noise)", "0.1026", "0.1748", "2.6627", "3.4906"]
    ]
    format_table(table10, col_w10, headers10, data10, font_size=9.5, header_font_size=10)

    # Right Card: Theoretical & Mathematical Interpretation
    add_card(s10, Inches(8.3), Inches(1.85), Inches(4.433), Inches(4.9), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_h = s10.shapes.add_textbox(Inches(8.45), Inches(1.95), Inches(4.1), Inches(4.6))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True

    p = tf_h.paragraphs[0]
    p.text = "Mathematical Scaling Dynamics:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    dyn_bullets = [
        ("• Sub-Linear Tree Growth: ", "As perturbation radius h expands 20-fold (0.01 → 0.20), Extra Trees SbLip grows from 0.0180 to 0.1026 — an increase of only 5.7×. Axis-aligned orthogonal partitions maintain stable leaf assignments under isotropic boundary noise."),
        ("• Supra-Linear Deep Explosion: ", "Tabular Deep ResNet surges from 0.2800 to 3.4906 — an increase of 12.5×! Deep continuous representations possess sharp, multi-dimensional decision manifolds where small perturbations displace embeddings across steep gradient boundaries."),
        ("• Explainer Fragility at Clinical Scales: ", "At standard physiological fluctuation (h = 0.05), neural instability is 23.5× higher than Extra Trees (0.9715 vs 0.0414)."),
        ("• Clinical Decision Safety: ", "ICU monitors cannot tolerate explanations that mutate wildly between consecutive sensor readings. Tree ensembles provide provably bounded attribution trajectories.")
    ]
    for d_title, d_desc in dyn_bullets:
        p_d = tf_h.add_paragraph()
        r1 = p_d.add_run()
        r1.text = d_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_d.add_run()
        r2.text = d_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_d.font.name = "Times New Roman"
        p_d.font.size = Pt(10)
        p_d.space_before = Pt(4)

    # Lower Left Card: Non-Gaussian Noise Sweep (Supplementary Study)
    add_card(s10, Inches(0.6), Inches(4.85), Inches(7.5), Inches(1.9), COLOR_WHITE, COLOR_BORDER)
    tb_ng = s10.shapes.add_textbox(Inches(0.75), Inches(4.95), Inches(7.2), Inches(1.7))
    tf_ng = tb_ng.text_frame
    tf_ng.word_wrap = True
    p = tf_ng.paragraphs[0]
    p.text = "Supplementary Study: Heavy-Tailed & Non-Gaussian Noise Distributions"
    p.font.name = "Times New Roman"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p2 = tf_ng.add_paragraph()
    p2.text = "To verify whether Gaussian assumptions biased stability findings, Supplementary Section 3 tested Student-t (ν = 3, heavy tails), Uniform U[-h√3, h√3], and Laplace (double exponential) perturbations. Extra Trees consistently preserved lowest SbLip across all distributions (Laplace: 0.0489 vs. Deep ResNet: 1.1240). This confirms that tree stability advantage is distribution-invariant."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(3)

    create_slide_footer(s10, 10)

    # =========================================================================
    # SLIDE 11: TRUST WEIGHT SENSITIVITY & ABLATION PROFILES
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    create_slide_header(s11, "Extended Experimental Results", "Trust Weight Sensitivity & Decision Utility Ablation (MIMIC-IV)",
                        "Evaluates net decision utility across 5 clinician operating profiles to verify robustness against subjective weighting.")

    t_shape11 = s11.shapes.add_table(6, 6, Inches(0.6), Inches(1.85), Inches(7.5), Inches(2.8))
    table11 = t_shape11.table
    col_w11 = [Inches(2.2), Inches(1.5), Inches(0.95), Inches(0.95), Inches(0.95), Inches(0.95)]
    headers11 = ["Configuration", "Weights (w_s, w_a, w_c)", "ET ↑", "RF ↑", "MLP ↑", "Deep ResNet ↑"]
    data11 = [
        ["Balanced (Baseline)", "(0.33, 0.33, 0.33)", "0.8135", "0.8076", "0.7184", "0.7206"],
        ["Stability-Focused", "(0.60, 0.20, 0.20)", "0.8077", "0.7951", "0.6456", "0.6463"],
        ["Prior-Focused", "(0.20, 0.60, 0.20)", "0.8146", "0.8138", "0.7600", "0.7623"],
        ["Calibration-Focused", "(0.20, 0.20, 0.60)", "0.8210", "0.8168", "0.7524", "0.7556"],
        ["Robust Clinical", "(0.40, 0.40, 0.20)", "0.8111", "0.8045", "0.7028", "0.7043"]
    ]
    format_table(table11, col_w11, headers11, data11, font_size=9.5, header_font_size=10)

    # Right Card: Profile Analysis & Clinical Findings
    add_card(s11, Inches(8.3), Inches(1.85), Inches(4.433), Inches(4.9), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_pr = s11.shapes.add_textbox(Inches(8.45), Inches(1.95), Inches(4.1), Inches(4.6))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True

    p = tf_pr.paragraphs[0]
    p.text = "Clinical Profile Analysis:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    prof_bullets = [
        ("• Uniform Dominance of Tree Ensembles: ", "Extra Trees achieves strictly superior decision utility (U_Clin) across every single evaluated weighting configuration. The ranking order (ET > RF > ResNet ≥ MLP) remains 100% invariant."),
        ("• Widest Utility Margin (+0.1614): ", "Under the Stability-Focused profile (w_s = 0.60), Extra Trees outperforms Deep ResNet by +0.1614 utility points (0.8077 vs 0.6463) — a +25.0% relative advantage."),
        ("• Narrowest Utility Margin (+0.0523): ", "Under the Prior-Focused profile (w_a = 0.60), Deep ResNet recovers slightly due to competitive global feature ranking, but Extra Trees still leads (0.8146 vs 0.7623)."),
        ("• Invariance to Subjective Bias: ", "Demonstrates that C-XAI's conclusions do not depend on fine-tuned loss weights, proving universal clinical validity across varying departmental risk tolerances.")
    ]
    for pr_title, pr_desc in prof_bullets:
        p_pr = tf_pr.add_paragraph()
        r1 = p_pr.add_run()
        r1.text = pr_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_pr.add_run()
        r2.text = pr_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_pr.font.name = "Times New Roman"
        p_pr.font.size = Pt(10)
        p_pr.space_before = Pt(4)

    # Lower Left Card: Penalty Asymmetry Sensitivity (alpha and beta sweep)
    add_card(s11, Inches(0.6), Inches(4.85), Inches(7.5), Inches(1.9), COLOR_WHITE, COLOR_BORDER)
    tb_pen = s11.shapes.add_textbox(Inches(0.75), Inches(4.95), Inches(7.2), Inches(1.7))
    tf_pen = tb_pen.text_frame
    tf_pen.word_wrap = True
    p = tf_pen.paragraphs[0]
    p.text = "Pauker-Kassirer Error Penalty Sweeps (α ∈ [0.1, 1.0], β ∈ [0.1, 1.0])"
    p.font.name = "Times New Roman"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p2 = tf_pen.add_paragraph()
    p2.text = "In high-stakes oncology and septic shock protocols, over-reliance penalty α is amplified (up to α = 1.0). As α increases from 0.10 to 1.00, Deep ResNet utility deteriorates by 38.4% due to high over-reliance under false positive uncalibrated predictions. In contrast, Extra Trees exhibits only a 12.1% drop, confirming superior fault tolerance."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(3)

    create_slide_footer(s11, 11)

    # =========================================================================
    # SLIDE 12: ADVERSARIAL ATTACKS & FEATURE MISSINGNESS STRESS-TESTS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    create_slide_header(s12, "Extended Experimental Results", "Adversarial Stress-Testing & Missingness Audits (MIMIC-IV)",
                        "Evaluates explainer degradation under gradient-crafted adversarial manipulation and Missing Completely At Random feeds.")

    t_shape12 = s12.shapes.add_table(16, 5, Inches(0.6), Inches(1.75), Inches(7.5), Inches(5.0))
    table12 = t_shape12.table
    col_w12 = [Inches(2.5), Inches(2.0), Inches(1.0), Inches(1.0), Inches(1.0)]
    headers12 = ["Corruption / Attack Mode", "Model Paradigm", "Acc. ↑", "SbLip ↓", "DXAI ↓"]
    data12 = [
        ["Clean Baseline", "Random Forest", "0.8845", "0.0821", "0.0812"],
        ["", "MLP", "0.8920", "0.4850", "0.4120"],
        ["", "Tabular Deep ResNet", "0.8935", "0.4912", "0.4350"],
        ["Gaussian Noise (h=0.05)", "Random Forest", "0.8790", "0.0845", "0.0910"],
        ["", "MLP", "0.8710", "0.5210", "0.4680"],
        ["", "Tabular Deep ResNet", "0.8750", "0.5340", "0.4820"],
        ["Missingness (20% MCAR)", "Random Forest", "0.8610", "0.0980", "0.1250"],
        ["", "MLP", "0.8120", "0.6120", "0.5840"],
        ["", "Tabular Deep ResNet", "0.8240", "0.6050", "0.5710"],
        ["FGSM Attack (ε_adv=0.02)", "Random Forest", "0.8720", "0.1150", "0.2850"],
        ["", "MLP", "0.7950", "0.8420", "1.8450"],
        ["", "Tabular Deep ResNet", "0.8010", "0.8650", "1.8620"],
        ["ScaL-PGD Attack (5 Steps)", "Random Forest", "0.8650", "0.1320", "0.3120"],
        ["", "MLP", "0.7680", "0.9150", "1.9120"],
        ["", "Tabular Deep ResNet", "0.7720", "0.9380", "1.9280"]
    ]
    format_table(table12, col_w12, headers12, data12, font_size=8.5, header_font_size=9)

    # Right Card: Adversarial Attribution Collapse Breakdown
    add_card(s12, Inches(8.3), Inches(1.75), Inches(4.433), Inches(5.0), COLOR_CALLOUT_BG, COLOR_CALLOUT_BORDER)
    tb_adv = s12.shapes.add_textbox(Inches(8.45), Inches(1.9), Inches(4.1), Inches(4.7))
    tf_adv = tb_adv.text_frame
    tf_adv.word_wrap = True

    p = tf_adv.paragraphs[0]
    p.text = "Catastrophic Attribution Collapse:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    adv_points = [
        ("• Fast Gradient Sign Method (FGSM): ", "Perturbing inputs by ε_adv = 0.02 along the loss gradient sign causes Tabular Deep ResNet explainer discordance to skyrocket from 0.4350 to 1.8620!"),
        ("• Scale-Bounded PGD (ScaL-PGD): ", "Under a 5-step iterative projected gradient attack, neural discordance reaches DXAI = 1.9280 — near complete rank inversion (theoretical maximum is 2.0). Explanations are completely hijacked while model accuracy drops only moderately (0.8935 → 0.7720)."),
        ("• Tree Resistance to Gradient Attacks: ", "Because tree ensembles possess zero gradients almost everywhere, gradient-crafted attacks cannot easily manipulate tree partition boundaries. Random Forest maintains DXAI = 0.3120 under identical ScaL-PGD attacks."),
        ("• 20% MCAR Missingness: ", "When 20% of EHR features are missing at random (common in real-time ICU feeds), tree stability degrades gracefully (SbLip = 0.0980 vs. 0.6050 for Deep ResNet).")
    ]
    for a_title, a_desc in adv_points:
        p_a = tf_adv.add_paragraph()
        r1 = p_a.add_run()
        r1.text = a_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_a.add_run()
        r2.text = a_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_a.font.name = "Times New Roman"
        p_a.font.size = Pt(9.5)
        p_a.space_before = Pt(4)

    create_slide_footer(s12, 12)

    # =========================================================================
    # SLIDE 13: COMPUTATIONAL LATENCY & PEAK MEMORY BENCHMARKS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    create_slide_header(s13, "Operational Benchmarking", "Computational Latency, Peak Memory & Dimensional Scalability",
                        "Profiles per-instance inference latency and peak memory footprint across explainers to evaluate point-of-care clinical feasibility.")

    t_shape13 = s13.shapes.add_table(6, 4, Inches(0.6), Inches(1.85), Inches(7.5), Inches(2.8))
    table13 = t_shape13.table
    col_w13 = [Inches(2.5), Inches(2.0), Inches(1.5), Inches(1.5)]
    headers13 = ["Explainer Method", "Computational Complexity", "Inference Latency (ms)", "Peak RAM (MB)"]
    data13 = [
        ["TreeSHAP", "O(T · L · D²)", "4.2 ms", "45 MB"],
        ["KernelSHAP", "O(2^D)", "4,210.0 ms", "512 MB"],
        ["LIME", "O(N · D²)", "850.0 ms", "120 MB"],
        ["SmoothGrad", "O(M · |Θ|)", "320.0 ms", "210 MB"],
        ["Integrated Gradients", "O(K · |Θ|)", "180.0 ms", "165 MB"]
    ]
    format_table(table13, col_w13, headers13, data13, font_size=9.5, header_font_size=10)

    # Right Card: Real-Time ICU Deployment Constraints
    add_card(s13, Inches(8.3), Inches(1.85), Inches(4.433), Inches(4.9), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_lat = s13.shapes.add_textbox(Inches(8.45), Inches(1.95), Inches(4.1), Inches(4.6))
    tf_lat = tb_lat.text_frame
    tf_lat.word_wrap = True

    p = tf_lat.paragraphs[0]
    p.text = "Point-of-Care Clinical Feasibility:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    lat_bullets = [
        ("• TreeSHAP Enables Real-Time ICU Triage: ", "TreeSHAP executes in 4.2 ms with 45 MB peak RAM. In emergency and septic shock workflows where physiological telemetry updates at 1 Hz, TreeSHAP easily supports continuous online explanation updates."),
        ("• KernelSHAP Intractability (1000× Slower): ", "KernelSHAP requires 4,210.0 ms (4.2 seconds) per patient encounter due to exponential coalition sampling O(2^D). Running KernelSHAP on a 100-bed ICU cohort requires >7 minutes per monitoring cycle, causing severe clinical bottleneck."),
        ("• Gradient Explainers Tradeoff: ", "Integrated Gradients (180 ms) and SmoothGrad (320 ms) offer reasonable speed on GPUs, but suffer from the catastrophic attribution instability uncovered in Table 1."),
        ("• Complete Deployment Synergy: ", "Extra Trees + TreeSHAP provides the optimal Pareto frontier: near-instant execution (4.2 ms), negligible memory footprint, lowest prior divergence, and highest decision utility.")
    ]
    for l_title, l_desc in lat_bullets:
        p_l = tf_lat.add_paragraph()
        r1 = p_l.add_run()
        r1.text = l_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_l.add_run()
        r2.text = l_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_l.font.name = "Times New Roman"
        p_l.font.size = Pt(10)
        p_l.space_before = Pt(4)

    # Lower Left Card: High-Dimensional Scaling (D Sweep up to 100 features)
    add_card(s13, Inches(0.6), Inches(4.85), Inches(7.5), Inches(1.9), COLOR_WHITE, COLOR_BORDER)
    tb_dim = s13.shapes.add_textbox(Inches(0.75), Inches(4.95), Inches(7.2), Inches(1.7))
    tf_dim = tb_dim.text_frame
    tf_dim.word_wrap = True
    p = tf_dim.paragraphs[0]
    p.text = "High-Dimensional Scalability (Supplementary Section 5: D Sweep up to 100 Features)"
    p.font.name = "Times New Roman"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p2 = tf_dim.add_paragraph()
    p2.text = "As feature dimensionality expands to D = 100 (genomic and multi-omic panel integration), TreeSHAP scales quadratically (latency increases to 14.8 ms), remaining fully clinical-grade. In stark contrast, KernelSHAP explodes beyond 60 seconds per instance, and LIME memory footprint climbs to 1.2 GB, demonstrating that C-XAI's recommended tree pipeline is future-proof."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(3)

    create_slide_footer(s13, 13)

    # =========================================================================
    # SLIDE 14: COMPREHENSIVE FRAMEWORK COMPARISON MATRIX
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    create_slide_header(s14, "Comparative Evaluation", "Comprehensive Comparison with Existing XAI Benchmarking Frameworks",
                        "Systematic capability matrix comparing C-XAI against Captum, OpenXAI, Quantus, and SENN across 7 core dimensions.")

    t_shape14 = s14.shapes.add_table(8, 6, Inches(0.6), Inches(1.85), Inches(12.133), Inches(3.6))
    table14 = t_shape14.table
    col_w14 = [Inches(3.133), Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.8), Inches(1.8)]
    headers14 = ["Capability / Evaluation Dimension", "Captum (PyTorch)", "OpenXAI (NeurIPS'22)", "Quantus (JMLR'23)", "SENN (NeurIPS'18)", "C-XAI (Proposed)"]
    data14 = [
        ["Local Perturbation Stability", "Partial (NoiseTunnel)", "Yes (Infidelity)", "Yes (Lipschitz)", "Yes (Supremum Bound)", "Yes (Physiological EHR Noise)"],
        ["Cross-Explainer Discordance (DXAI)", "No", "No", "No", "No", "Yes (Spearman Rank Conflict)"],
        ["Clinical Guideline Prior Alignment", "No", "No", "No", "No", "Yes (Normalized Wasserstein EMD)"],
        ["Calibration & Decision Utility (U_Clin)", "No", "No", "No", "No", "Yes (Pauker-Kassirer Model)"],
        ["Model Agnostic (Trees + Deep Networks)", "No (Neural Only)", "Partial", "Partial", "No (SENN Intrinsic Only)", "Yes (Zeroth-Order Score Smoother)"],
        ["Adversarial Attribution Auditing", "Partial", "No", "Partial", "No", "Yes (FGSM + ScaL-PGD Stress)"],
        ["Healthcare Cohort Integrations", "No", "No", "No", "No", "Yes (MIMIC-IV, eICU, BCWD, Cardio)"]
    ]
    format_table(table14, col_w14, headers14, data14, font_size=9.5, header_font_size=10)

    # Lower Card: Framework Synthesis & Why Existing Toolkits Fail in Healthcare
    add_card(s14, Inches(0.6), Inches(5.6), Inches(12.133), Inches(1.25), COLOR_CALLOUT_BG, COLOR_CALLOUT_BORDER)
    tb_syn = s14.shapes.add_textbox(Inches(0.8), Inches(5.68), Inches(11.7), Inches(1.1))
    tf_syn = tb_syn.text_frame
    tf_syn.word_wrap = True

    p = tf_syn.paragraphs[0]
    p.text = "Why Existing Frameworks are Insufficient for Healthcare AI Auditing:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    p2 = tf_syn.add_paragraph()
    p2.text = "1. Captum & SENN are strictly confined to differentiable neural networks, failing on step-function tree ensembles that dominate tabular clinical records.\n2. OpenXAI and Quantus evaluate mathematical infidelity against internal model weights, remaining completely blind to validated medical consensus (SOFA, ASCVD).\n3. No prior benchmark couples explanation stability with human clinician decision theory, omitting over-reliance and under-reliance error costs. C-XAI closes this critical gap."
    p2.font.name = "Times New Roman"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_DARK_TEXT
    p2.space_before = Pt(2)

    create_slide_footer(s14, 14)

    # =========================================================================
    # SLIDE 15: COMPLETE PAPER BIBLIOGRAPHY (All 28 References)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    create_slide_header(s15, "Literature & Citations", "Complete Paper Bibliography & Theoretical Foundations (All 28 References)",
                        "Full bibliographic catalogue of cited works across explainability stability, clinical priors, decision theory, and healthcare XAI.")

    # Left Column Card (References 1-14)
    add_card(s15, Inches(0.6), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_b1 = s15.shapes.add_textbox(Inches(0.75), Inches(1.9), Inches(5.6), Inches(4.85))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True
    tf_b1.margin_left = tf_b1.margin_top = tf_b1.margin_right = tf_b1.margin_bottom = 0

    refs_b1 = [
        "[1] S. M. Lundberg & S.-I. Lee, “A unified approach to interpreting model predictions,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 4765–4774, 2017.",
        "[2] M. T. Ribeiro, S. Singh, & C. Guestrin, “Why should I trust you?: Explaining predictions of any classifier,” in Proc. ACM SIGKDD, pp. 1135–1144, 2016.",
        "[3] M. Sundararajan, A. Taly, & Q. Yan, “Axiomatic attribution for deep networks,” in Proc. ICML, pp. 3319–3328, 2017.",
        "[4] D. Muhammad & M. Bendechache, “Unveiling the black box: Systematic review of XAI in medical imaging,” CSBJ, vol. 23, pp. 248–261, 2024.",
        "[5] K. Lamba & S. Rani, “BCI and Grad-CAM based explainable artificial intelligence for smart healthcare,” J. Neurosci. Methods, vol. 401, 2024.",
        "[6] R. Caruana, Y. Lou, P. Koch, et al., “Intelligible and interpretable machine learning in healthcare,” ACM Comput. Surv., vol. 55, no. 8, 2023.",
        "[7] C. Agarwal, S. Krishna, et al., “OpenXAI: Towards a unified benchmark of model explanations,” in Proc. NeurIPS, vol. 35, 2022.",
        "[8] A. Hedström, L. Weber, et al., “Quantus: An explainable AI evaluation toolkit,” J. Mach. Learn. Res. (JMLR), vol. 24, pp. 1–11, 2023.",
        "[9] S. Krishna, T. Han, A. Gu, et al., “The disagreement problem in explainable AI: Empirical studies,” in Proc. ACM CHI, pp. 1–16, 2022.",
        "[10] A. E. W. Johnson, L. Bulgarelli, et al., “MIMIC-IV, a freely accessible electronic health record dataset,” Sci. Data, vol. 10, no. 1, 2023.",
        "[11] T. J. Pollard, A. E. W. Johnson, et al., “The eICU collaborative research database benchmark pipeline,” Sci. Data, vol. 10, no. 1, 2023.",
        "[12] C.-K. Yeh, C.-K. Hsieh, et al., “Quantifying sensitivity and robustness of post-hoc explanations,” Nat. Mach. Intell., vol. 5, pp. 782–792, 2023.",
        "[13] G. Bansal, T. Wu, J. Zhou, et al., “Calibrating human-AI reliance in clinical decision support systems,” in Proc. ACM CHI, pp. 1–14, 2024.",
        "[14] Z. Buçinca, P. Malaya, et al., “Evaluating explanation stability and clinician trust in healthcare AI,” Artif. Intell. Med., vol. 138, 2023."
    ]
    for idx, ref in enumerate(refs_b1):
        p = tf_b1.paragraphs[0] if idx == 0 else tf_b1.add_paragraph()
        p.text = ref
        p.font.name = "Times New Roman"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(2.5)

    # Right Column Card (References 15-28)
    add_card(s15, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_WHITE, COLOR_BORDER)
    tb_b2 = s15.shapes.add_textbox(Inches(6.95), Inches(1.9), Inches(5.6), Inches(4.85))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True
    tf_b2.margin_left = tf_b2.margin_top = tf_b2.margin_right = tf_b2.margin_bottom = 0

    refs_b2 = [
        "[15] S. M. Lauritsen, M. Kalør, et al., “Early clinical prediction of sepsis using scalable ML protocols,” Lancet Digit. Health, vol. 6, 2024.",
        "[16] F. Bohlen, M. Mittermaier, et al., “Quantitative evaluation of explainable AI in intensive care risk,” IEEE JBHI, vol. 27, 2023.",
        "[17] J. Duell, G. Stiglic, & P. Kocbek, “Cross-explainer disagreement and instability in EHR analytics,” J. Biomed. Inform., vol. 142, 2023.",
        "[18] X. Niu, L. Wang, & J. Zhang, “Multi-level attention deep neural networks for patient risk prediction,” IEEE TNNLS, vol. 34, 2022.",
        "[19] T. Mahmood, Y. Chen, & X. Zhao, “Quantifying transparency in gradient boosted trees for EHR risk,” Nat. Mach. Intell., vol. 4, 2022.",
        "[20] J. Alderden, D. Drake, et al., “Clinical utility and usability auditing for interactive healthcare ML,” CIN, vol. 41, pp. 210–218, 2023.",
        "[21] K. Ihalapathirana & T. Silva, “ReliefF and SHAP feature selection for disease risk prediction,” IEEE Access, vol. 11, 2023.",
        "[22] P. Keyl, M. Becker, et al., “Multimodal deep neural networks for pan-cancer survival prognosis,” Lancet Digit. Health, vol. 6, 2024.",
        "[23] A. Mohamed, S. Ibrahim, et al., “Clinician exclusion and evaluation gaps in cancer XAI: Review,” Lancet Oncol., vol. 25, 2024.",
        "[24] Z. Shen, Y. Liu, & J. Wang, “Interpretable machine learning models for disease prognosis: A review,” Artif. Intell. Rev., vol. 57, 2024.",
        "[25] S. Vijay, G. R. Ramya, et al., “An Integrated Two Layered Voting (TLV) Framework for CAD Prediction,” IEEE Access, vol. 11, pp. 45120–45133, 2023.",
        "[26] G. R. Ramya, M. Senthil, et al., “Explainable Machine Learning Framework for Diabetes & CVD Risk,” LNCS, vol. 13840, Springer, 2023.",
        "[27] G. R. Ramya, S. V. Manoj, et al., “Understanding CNNs with Explainable AI & White Box AI,” in Proc. IJCACI, Springer Nature, pp. 139–153, 2025.",
        "[28] G. R. Ramya, R. Prabha, et al., “Predictive Machine Learning and Feature Selection for Clinical EHR,” CCIS, vol. 1780, Springer, 2023."
    ]
    for idx, ref in enumerate(refs_b2):
        p = tf_b2.paragraphs[0] if idx == 0 else tf_b2.add_paragraph()
        p.text = ref
        p.font.name = "Times New Roman"
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(2.5)

    create_slide_footer(s15, 15)

    # =========================================================================
    # SLIDE 16: CLINICAL GOVERNANCE, REGULATORY COMPLIANCE & Q&A
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    create_slide_header(s16, "Clinical Governance & Compliance", "Regulatory Alignment, Open-Source Release & Technical Defense Q&A",
                        "Mapping C-XAI quantitative auditing to FDA SaMD and EU AI Act mandates, with reproducible code repository.")

    # Left Column: Regulatory Alignment Matrix
    add_card(s16, Inches(0.6), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_LIGHT_BG, COLOR_BORDER)
    tb_reg = s16.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_reg = tb_reg.text_frame
    tf_reg.word_wrap = True

    p = tf_reg.paragraphs[0]
    p.text = "Compliance with Medical AI Regulations:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    reg_bullets = [
        ("• FDA Action Plan for AI/ML SaMD (2021): ", "Mandates pre-market algorithm transparency and post-market algorithmic surveillance. C-XAI's W_Clin^norm directly verifies that AI systems do not drift away from Good Machine Learning Practice (GMLP) clinical standards."),
        ("• EU AI Act (Regulation 2024/1689): ", "High-risk clinical diagnostic systems must comply with:\n  - Article 13 (Transparency): Verified by Cross-Explainer Discordance (DXAI ≤ 0.10).\n  - Article 14 (Human Oversight): Guaranteed by Pauker-Kassirer reliance modeling.\n  - Article 15 (Accuracy, Robustness & Cybersecurity): Audited by SbLip and ScaL-PGD stress-tests."),
        ("• Clinical Safety Gate: ", "Establishes quantitative go/no-go gating thresholds prior to hospital EHR deployment, preventing silent diagnostic failure.")
    ]
    for r_title, r_desc in reg_bullets:
        p_r = tf_reg.add_paragraph()
        r1 = p_r.add_run()
        r1.text = r_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_r.add_run()
        r2.text = r_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_r.font.name = "Times New Roman"
        p_r.font.size = Pt(10.5)
        p_r.space_before = Pt(5)

    # Right Column: Open Science, Artifacts & Q&A Invitation
    add_card(s16, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.05), COLOR_WHITE, COLOR_BORDER)
    tb_qa = s16.shapes.add_textbox(Inches(7.0), Inches(1.95), Inches(5.5), Inches(4.7))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True

    p = tf_qa.paragraphs[0]
    p.text = "Open Science & Technical Session Q&A:"
    p.font.name = "Times New Roman"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_DEEP_PURPLE

    qa_bullets = [
        ("• Open-Source Benchmark Repository: ", "Complete PyTorch/Scikit-learn pipeline, dataset downloaders, codified clinical prior guideline matrices, and synthetic noise generators available upon conference publication."),
        ("• Seed-Level Reproducibility: ", "All 50 random trial seeds (42–91), cross-validation folds, and model checkpoints fully serialized with fixed environmental configurations."),
        ("• Ready for Technical Committee Inquiry: ", "We welcome detailed questions from the session chairs, senior researchers, and the award evaluation committee on metric derivations, optimal transport proofs, clinical reliance modeling, and hospital deployment."),
        ("• Presenter Contact: ", "Sheela Akshar Sakhi (Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore, Amrita Vishwa Vidyapeetham)"),
        ("• Corresponding Author Contact: ", "Dr. Ramya G R (gr_ramya@cb.amrita.edu)")
    ]
    for q_title, q_desc in qa_bullets:
        p_q = tf_qa.add_paragraph()
        r1 = p_q.add_run()
        r1.text = q_title
        r1.font.bold = True
        r1.font.color.rgb = COLOR_DEEP_PURPLE
        r2 = p_q.add_run()
        r2.text = q_desc
        r2.font.color.rgb = COLOR_DARK_TEXT
        p_q.font.name = "Times New Roman"
        p_q.font.size = Pt(10)
        p_q.space_before = Pt(4)

    create_slide_footer(s16, 16)

    # =========================================================================
    # SAVE PRESENTATION
    # =========================================================================
    out_pptx = "CONF_PRESENTATION/templates/legacy_pptx_backup.pptx"
    prs.save(out_pptx)
    print(f"Successfully generated Technical Backup Presentation: {out_pptx}")

if __name__ == "__main__":
    build_presentation()
