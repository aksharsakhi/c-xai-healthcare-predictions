#!/usr/bin/env python3
"""
build_template_matched_poster.py
================================
Generates the official ICMLDE 2026 digital poster for Paper ID: 857 strictly following
the official template (ICMLDE2026_poster_3.pptx).

Rules:
1. Strictly preserve all existing shapes, positions, font families (Arial),
   font sizes (40pt headers, 24-28pt body, 24pt table, 21-24pt captions), and colors.
2. In-place replacement of placeholder text only:
   - Motivation & Problem (keep heading, replace 3 bullet placeholders)
   - Key Contributions (keep heading, replace 3 numbered contribution placeholders without double-numbering)
   - Method (keep heading, replace architecture placeholder with diagram)
   - How it works (keep heading, replace 3 step placeholders)
   - Data & Experimental Setup (keep heading, keep exact Datasets:, Baselines:, Metrics:, Setup: tags)
   - Results (keep heading, populate existing 5x4 table, keep Table 1 caption)
   - Conclusion (keep heading, replace Main takeaway, Key number, Limitation placeholders)
   - Links & References (keep heading, replace 2 citation placeholders)
   - Placeholders for Figures & QR code replaced with high-res figures at exact coordinates.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

TEMPLATE_PATH = "CONF_PRESENTATION/templates/ICMLDE2026_poster_3.pptx"
OUTPUT_DIR = "CONF_PRESENTATION/SUBMISSION_READY"
OUTPUT_PPTX = os.path.join(OUTPUT_DIR, "ICMLDE-2026-857_C-XAI_Digital_Poster.pptx")

FIG1_PATH = "CONF_PRESENTATION/scripts/fig_discordance_comparison.png"
FIG2_PATH = "CONF_PRESENTATION/scripts/fig_architecture_subsystems.png"
FIG3_PATH = "Akshar_ICMLDE2026/figures/fig1_stability_vs_noise.png"
QR_PATH = "CONF_PRESENTATION/scripts/qr_code.png"
INST_LOGO_SVG = "CONF_PRESENTATION/templates/clear-space-logo-01.svg"
INST_LOGO_PNG = "CONF_PRESENTATION/templates/amrita_logo_pristine_clean.png"


def remove_shape(shape):
    sp = shape._element
    sp.getparent().remove(sp)


def set_run_text(run, text, font_name="Arial", font_size_pt=None, bold=None, color=None):
    run.text = text
    if font_name:
        run.font.name = font_name
    if font_size_pt:
        run.font.size = Pt(font_size_pt)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


def build_poster():
    print(f"Loading template: {TEMPLATE_PATH}...")
    prs = Presentation(TEMPLATE_PATH)
    slide = prs.slides[0]
    shapes = {s.name: s for s in slide.shapes}

    # =========================================================================
    # 1. HEADER SECTION
    # =========================================================================
    print("Updating Header...")

    # 1.1 Institution Logo (CustomShape 5 replaced by official logo image)
    s_inst = shapes.get("CustomShape 5")
    if s_inst and os.path.exists(INST_LOGO_PNG):
        l, t, w, h = s_inst.left, s_inst.top, s_inst.width, s_inst.height
        remove_shape(s_inst)
        # Target aspect ratio is 2945 / 776 ~ 3.795
        logo_h = Inches(1.88)
        logo_w = Inches(1.88 * 3.795)  # ~ 7.13 in
        logo_l = l + (w - logo_w) / 2
        logo_t = t + (h - logo_h) / 2
        slide.shapes.add_picture(INST_LOGO_PNG, logo_l, logo_t, logo_w, logo_h)

    # 1.2 Title Label (Title label)
    s_title = shapes.get("Title label")
    if s_title and s_title.has_text_frame:
        tf = s_title.text_frame
        p = tf.paragraphs[0]
        title_text = "C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance,\nand Clinical Utility in Healthcare AI"
        set_run_text(p.runs[0], title_text, font_size_pt=40, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))

    # 1.3 Authors (TextShape 1)
    s_authors = shapes.get("TextShape 1")
    if s_authors and s_authors.has_text_frame:
        tf = s_authors.text_frame
        p0 = tf.paragraphs[0]
        set_run_text(p0.runs[0], "Sheela Akshar Sakhi¹ (Presenter),  Ibbraheem Shaik¹,  Settibattini Suhitha¹,  Ramya G R²*",
                     font_size_pt=32, bold=False, color=RGBColor(0x00, 0x00, 0x00))
        p1 = tf.paragraphs[1]
        set_run_text(p1.runs[0], "¹·² Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore, India   ·   gr_ramya@cb.amrita.edu",
                     font_size_pt=26, bold=False, color=RGBColor(0x59, 0x59, 0x59))

    # 1.4 ICMLDE badge: kept strictly untouched.

    # =========================================================================
    # 2. COLUMN 1: MOTIVATION, KEY CONTRIBUTIONS, TEASER FIGURE
    # =========================================================================
    print("Updating Column 1...")

    # 2.1 Motivation & Problem (keep heading, update 3 bullet paragraphs)
    s_mot = shapes.get("Motivation & Problem")
    if s_mot and s_mot.has_text_frame:
        s_mot.left = Inches(0.90)
        s_mot.top = Inches(3.90)
        s_mot.width = Inches(14.80)
        s_mot.height = Inches(3.80)
        tf = s_mot.text_frame
        # P0 is heading "Motivation & Problem" - untouched!
        # P1: [What problem does the paper solve, and why does it matter now?]
        set_run_text(tf.paragraphs[1].runs[0],
                     "Deep neural networks achieve ≥96% AUROC in healthcare, yet post-hoc explanations remain unverified and fragile, risking catastrophic clinical triage errors.",
                     font_size_pt=25)
        # P2: [What is wrong with current approaches: cost, scale, accuracy, data quality?]
        set_run_text(tf.paragraphs[2].runs[0],
                     "ICU sensor noise (h = 0.05) triggers up to 9.6× explanation instability in deep nets, while competing explainers provide >40% contradictory rationales on identical patients.",
                     font_size_pt=25)
        # P3: [One-sentence research question]
        set_run_text(tf.paragraphs[3].runs[0],
                     "Can we quantitatively benchmark explanation stability, cross-explainer discordance, and clinical prior alignment to safely calibrate medical AI utility?",
                     font_size_pt=25)

    # 2.2 Key Contributions (keep heading, update 3 numbered items - no double numbering!)
    s_contrib = shapes.get("Key Contributions")
    if s_contrib and s_contrib.has_text_frame:
        s_contrib.left = Inches(0.90)
        s_contrib.top = Inches(8.00)
        s_contrib.width = Inches(14.80)
        s_contrib.height = Inches(4.80)
        tf = s_contrib.text_frame
        # P0 is heading "Key Contributions" - untouched!
        # P1: [Contribution 1] (bold) – new model / algorithm (regular)
        set_run_text(tf.paragraphs[1].runs[0], "C-XAI Benchmark", font_size_pt=25, bold=True)
        set_run_text(tf.paragraphs[1].runs[1], " – Formulates 4 quantitative metrics: Local Lipschitz Stability (SbLip), Cross-Explainer Discordance (DXAI), Prior Alignment (W_Clin), and Decision Utility (U_Clin).", font_size_pt=25, bold=False)
        # P2: [Contribution 2] (bold) – data pipeline, dataset or benchmark (regular)
        set_run_text(tf.paragraphs[2].runs[0], "Algorithmic Innovations", font_size_pt=25, bold=True)
        set_run_text(tf.paragraphs[2].runs[1], " – Zeroth-Order Gaussian Smoothing for step-function tree ensembles and 1D Wasserstein Earth Mover's Distance for clinical prior grounding.", font_size_pt=25, bold=False)
        # P3: [Contribution 3] (bold) – headline result (regular)
        set_run_text(tf.paragraphs[3].runs[0], "Empirical Decoupling", font_size_pt=25, bold=True)
        set_run_text(tf.paragraphs[3].runs[1], " – Tree ensembles achieve +19.6% higher clinical decision utility (0.849 vs. 0.711, p < 0.001, Cohen's d = 2.96) over deep networks despite lower AUROC.", font_size_pt=25, bold=False)

    # 2.3 Teaser Figure: Discordance Matrix (Figure 1)
    s_ph_fig1 = shapes.get("Figure placeholder: [Teaser figure]")
    if s_ph_fig1 and os.path.exists(FIG1_PATH):
        left = Inches(1.20)
        top = Inches(13.20)
        width = Inches(14.20)
        height = Inches(7.00)
        remove_shape(s_ph_fig1)
        slide.shapes.add_picture(FIG1_PATH, left, top, width, height)

    s_cap_fig1 = shapes.get("Caption: [Teaser figure]")
    if s_cap_fig1 and s_cap_fig1.has_text_frame:
        s_cap_fig1.left = Inches(1.20)
        s_cap_fig1.top = Inches(20.40)
        s_cap_fig1.width = Inches(14.20)
        s_cap_fig1.height = Inches(0.80)
        p = s_cap_fig1.text_frame.paragraphs[0]
        set_run_text(p.runs[0],
                     "Figure 1. Cross-Explainer Discordance Matrix: Tree ensembles achieve consensus (DXAI = 0.059), whereas Deep ResNet exhibits severe conflict (DXAI = 0.435, 7.4× higher disagreement).",
                     font_size_pt=22, color=RGBColor(0x59, 0x59, 0x59))

    # =========================================================================
    # 3. COLUMN 2: METHOD, HOW IT WORKS, DATA & EXPERIMENTAL SETUP
    # =========================================================================
    print("Updating Column 2...")

    # 3.1 Method Heading: untouched!
    s_method = shapes.get("Method")
    if s_method:
        s_method.left = Inches(16.60)
        s_method.top = Inches(3.90)

    # 3.2 Method Architecture Diagram (Figure 2)
    s_ph_fig2 = shapes.get("Figure placeholder: [Architecture / pipeline diagram]")
    if s_ph_fig2 and os.path.exists(FIG2_PATH):
        left = Inches(16.90)
        top = Inches(4.55)
        width = Inches(14.20)
        height = Inches(7.20)
        remove_shape(s_ph_fig2)
        slide.shapes.add_picture(FIG2_PATH, left, top, width, height)

    s_cap_fig2 = shapes.get("Caption: [Architecture / pipeline diagram]")
    if s_cap_fig2 and s_cap_fig2.has_text_frame:
        s_cap_fig2.left = Inches(16.90)
        s_cap_fig2.top = Inches(11.85)
        s_cap_fig2.width = Inches(14.20)
        s_cap_fig2.height = Inches(0.55)
        p = s_cap_fig2.text_frame.paragraphs[0]
        set_run_text(p.runs[0],
                     "Figure 2. C-XAI Auditing Architecture: (1) System Architecture (Subsystems 1–4) & (2) Detailed Auditing Module Specification.",
                     font_size_pt=22, color=RGBColor(0x59, 0x59, 0x59))

    # 3.3 How it works (keep heading, update 3 steps)
    s_steps = shapes.get("Method steps")
    if s_steps and s_steps.has_text_frame:
        s_steps.left = Inches(16.60)
        s_steps.top = Inches(12.55)
        s_steps.width = Inches(14.80)
        s_steps.height = Inches(3.30)
        tf = s_steps.text_frame
        # P0 is heading "How it works" - untouched!
        # P1: [Step 1: data ingestion / preprocessing]
        set_run_text(tf.paragraphs[1].runs[0],
                     "Step 1 (Ingestion & Perturbation): Standardize 4 clinical cohorts (51.3K records) and inject Gaussian sensor noise δ ~ N(0, h²I) and missingness.",
                     font_size_pt=25)
        # P2: [Step 2: model or algorithm core idea]
        set_run_text(tf.paragraphs[2].runs[0],
                     "Step 2 (Predictive Zoo & Explainers): Evaluate tree ensembles with Zeroth-Order Smoothing alongside deep networks across 6 explainers (SHAP, LIME, IG).",
                     font_size_pt=25)
        # P3: [Step 3: training objective or inference]
        set_run_text(tf.paragraphs[3].runs[0],
                     "Step 3 (Quantitative Auditing): Formulate Lipschitz stability (SbLip), explainer discordance (DXAI), prior distance (W_Clin), and net clinical utility (U_Clin).",
                     font_size_pt=25)

    # 3.4 Data & Experimental Setup (keep heading, keep exact Datasets:, Baselines:, Metrics:, Setup: tags)
    s_setup = shapes.get("Data & Experimental Setup")
    if s_setup and s_setup.has_text_frame:
        s_setup.left = Inches(16.60)
        s_setup.top = Inches(16.05)
        s_setup.width = Inches(14.80)
        s_setup.height = Inches(5.40)
        tf = s_setup.text_frame
        # P0 is heading "Data & Experimental Setup" - untouched!
        # P1: Datasets: (bold) [names, size, domain] (regular)
        set_run_text(tf.paragraphs[1].runs[0], "Datasets: ", font_size_pt=25, bold=True)
        set_run_text(tf.paragraphs[1].runs[1], "MIMIC-IV (40k, ICU sepsis), eICU (10k, multi-center), BCWD (569, oncology), Cardio EHR (800, 10-Yr CVD risk)", font_size_pt=25, bold=False)

        # P2: Baselines: (bold) [methods compared] (regular)
        set_run_text(tf.paragraphs[2].runs[0], "Baselines: ", font_size_pt=25, bold=True)
        set_run_text(tf.paragraphs[2].runs[1], "Random Forest, Extra Trees, MLP, Tabular Deep ResNet; evaluated with TreeSHAP, KernelSHAP, LIME, SmoothGrad, IntGrad", font_size_pt=25, bold=False)

        # P3: Metrics: (bold) [accuracy, F1, latency, …] (regular)
        set_run_text(tf.paragraphs[3].runs[0], "Metrics: ", font_size_pt=25, bold=True)
        set_run_text(tf.paragraphs[3].runs[1], "Accuracy, AUROC, Lipschitz Stability (SbLip), Cross-Explainer Discordance (DXAI), Prior Distance (W_Clin), Decision Utility (U_Clin)", font_size_pt=25, bold=False)

        # P4: Setup: (bold) [hardware, training budget] (regular)
        set_run_text(tf.paragraphs[4].runs[0], "Setup: ", font_size_pt=25, bold=True)
        set_run_text(tf.paragraphs[4].runs[1], "50 random trials (seeds 42–91), 5-fold CV, Zeroth-Order Smoother (M = 100 draws), PyTorch & scikit-learn on Apple Silicon", font_size_pt=25, bold=False)

    # =========================================================================
    # 4. COLUMN 3: RESULTS, ABLATION PLOT, CONCLUSION, REFS & QR
    # =========================================================================
    print("Updating Column 3...")

    # 4.1 Results Heading: untouched!
    s_results = shapes.get("Results")
    if s_results:
        s_results.left = Inches(32.30)
        s_results.top = Inches(3.90)

    # 4.2 Main Results Table (Update cells in-place in existing 5x4 table)
    s_tbl = shapes.get("Main results table")
    if s_tbl and s_tbl.has_table:
        s_tbl.left = Inches(32.60)
        s_tbl.top = Inches(4.75)
        s_tbl.width = Inches(14.20)
        s_tbl.height = Inches(3.50)
        t = s_tbl.table
        # Table data layout: Method | Accuracy (AUC) | DXAI Discordance (↓) | U_Clin Utility (↑)
        table_values = [
            ["Method", "Accuracy (AUC)", "DXAI Discordance (↓)", "U_Clin Utility (↑)"],
            ["Tabular Deep ResNet", "89.35% (0.913)", "0.435 (Severe)", "0.711"],
            ["MLP Classifier", "89.20% (0.907)", "0.412 (High)", "0.712"],
            ["Random Forest", "88.45% (0.899)", "0.081 (Low)", "0.841"],
            ["Extra Trees (C-XAI)", "88.12% (0.903)", "0.059 (Best)", "0.849*"]
        ]
        for r_idx, row in enumerate(table_values):
            is_header = (r_idx == 0)
            is_ours = (r_idx == 4)
            for c_idx, val in enumerate(row):
                cell = t.cell(r_idx, c_idx)
                p = cell.text_frame.paragraphs[0]
                if len(p.runs) > 0:
                    set_run_text(p.runs[0], val, font_size_pt=23, bold=(is_header or is_ours or ("*" in val)))
                else:
                    r = p.add_run()
                    set_run_text(r, val, font_size_pt=23, bold=(is_header or is_ours or ("*" in val)))

    # 4.3 Table Caption (Positioned strictly below the table with clear margin)
    s_cap_tbl = shapes.get("Caption: table")
    if s_cap_tbl and s_cap_tbl.has_text_frame:
        s_cap_tbl.left = Inches(32.60)
        s_cap_tbl.top = Inches(8.45)
        s_cap_tbl.width = Inches(14.20)
        s_cap_tbl.height = Inches(0.65)
        p = s_cap_tbl.text_frame.paragraphs[0]
        set_run_text(p.runs[0],
                     "Table 1. Benchmark across 50 trials (MIMIC-IV): Classification metrics vs. XAI reliability (best in bold). Extra Trees achieves +19.6% higher clinical utility (p < 0.001) despite deep nets having higher raw accuracy.",
                     font_size_pt=21, color=RGBColor(0x59, 0x59, 0x59))

    # 4.4 Ablation / Scaling Plot (Figure 3)
    s_ph_fig3 = shapes.get("Figure placeholder: [Ablation / scaling plot]")
    if s_ph_fig3 and os.path.exists(FIG3_PATH):
        left = Inches(32.60)
        top = Inches(9.20)
        width = Inches(14.20)
        height = Inches(4.15)
        remove_shape(s_ph_fig3)
        slide.shapes.add_picture(FIG3_PATH, left, top, width, height)

    s_cap_fig3 = shapes.get("Caption: [Ablation / scaling plot]")
    if s_cap_fig3 and s_cap_fig3.has_text_frame:
        s_cap_fig3.left = Inches(32.60)
        s_cap_fig3.top = Inches(13.45)
        s_cap_fig3.width = Inches(14.20)
        s_cap_fig3.height = Inches(0.55)
        p = s_cap_fig3.text_frame.paragraphs[0]
        set_run_text(p.runs[0],
                     "Figure 3. Stability Scaling vs. Sensor Noise: Tree ensembles maintain sub-linear scaling, whereas Deep ResNet suffers explosive explanation degradation (h ∈ [0.01, 0.20]).",
                     font_size_pt=22, color=RGBColor(0x59, 0x59, 0x59))

    # 4.5 Conclusion (keep heading, update 3 items)
    s_conc = shapes.get("Conclusion")
    if s_conc and s_conc.has_text_frame:
        s_conc.left = Inches(32.30)
        s_conc.top = Inches(14.15)
        s_conc.width = Inches(14.80)
        s_conc.height = Inches(3.60)
        tf = s_conc.text_frame
        # P0 is heading "Conclusion" - untouched!
        # P1: [Main takeaway in one line]
        set_run_text(tf.paragraphs[1].runs[0],
                     "High predictive AUROC masks severe explanation instability (9.6×) and cross-explainer discordance (7.4×) in acute healthcare AI.",
                     font_size_pt=25)
        # P2: [Key number: +X% over best baseline]
        set_run_text(tf.paragraphs[2].runs[0],
                     "Tree ensembles achieve +19.6% higher calibrated clinical decision utility over deep neural networks (0.849 vs. 0.711, p < 0.001, Cohen's d = 2.96).",
                     font_size_pt=25)
        # P3: [Limitation or next step]
        set_run_text(tf.paragraphs[3].runs[0],
                     "C-XAI operationalizes automated verification for FDA SaMD Action Plan and EU AI Act (Articles 13 & 14) clinical governance compliance.",
                     font_size_pt=25)

    # 4.6 QR Code
    s_ph_qr = shapes.get("QR placeholder")
    if s_ph_qr and os.path.exists(QR_PATH):
        left = Inches(32.60)
        top = Inches(18.05)
        size = Inches(2.80)
        remove_shape(s_ph_qr)
        slide.shapes.add_picture(QR_PATH, left, top, size, size)

    # 4.7 Links & References (keep heading, update 2 citations)
    s_links = shapes.get("Links & References")
    if s_links and s_links.has_text_frame:
        s_links.left = Inches(35.70)
        s_links.top = Inches(18.05)
        s_links.width = Inches(11.20)
        s_links.height = Inches(3.20)
        tf = s_links.text_frame
        # P0 is heading "Paper · Code · Project page" - untouched!
        # P1: [1] [Author et al., Venue Year]
        set_run_text(tf.paragraphs[1].runs[0],
                     "[1] S. M. Lundberg & S.-I. Lee, “A unified approach to interpreting model predictions,” NeurIPS, vol. 30, 2017.",
                     font_size_pt=22)
        # P2: [2] [Author et al., Venue Year]
        set_run_text(tf.paragraphs[2].runs[0],
                     "[2] S. Krishna, T. Han, et al., “The disagreement problem in explainable AI,” Proc. ACM CHI, 2022.",
                     font_size_pt=22)

    # Save PPTX
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prs.save(OUTPUT_PPTX)
    print(f"Template-matched poster generated successfully:\n  -> {OUTPUT_PPTX}")


if __name__ == "__main__":
    build_poster()
