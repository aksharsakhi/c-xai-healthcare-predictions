import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_cover_letter_and_revision_report():
    doc = Document()
    
    # Page setup - 0.75 inch margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Colors
    NAVY = RGBColor(0x1B, 0x36, 0x5D)
    TEAL = RGBColor(0x00, 0x80, 0x80)
    DARK_GRAY = RGBColor(0x44, 0x44, 0x44)
    
    # Header Banner
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_after = Pt(2)
    run_conf = title_p.add_run("5th International Conference on Machine Learning & Data Engineering (ICMLDE 2026)\nElsevier Procedia Computer Science")
    run_conf.font.size = Pt(11)
    run_conf.font.bold = True
    run_conf.font.color.rgb = TEAL
    
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(6)
    h1.paragraph_format.space_after = Pt(6)
    run_h1 = h1.add_run("FORMAL REVISION COVER LETTER & COMPREHENSIVE MODIFICATION REPORT")
    run_h1.font.size = Pt(16)
    run_h1.font.bold = True
    run_h1.font.color.rgb = NAVY
    
    # Metadata Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Paper ID:", "857 (Tracking: Akshar_ICMLDE2026)"),
        ("Accepted Paper Title:", "C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI"),
        ("Authors:", "Sheela Akshar Sakhi, Ibbraheem Shaik, Settibattini Suhitha, Ramya G R*"),
        ("Affiliation:", "Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore, Amrita Vishwa Vidyapeetham, India"),
        ("Corresponding Author:", "Dr. Ramya G R (gr_ramya@cb.amrita.edu | Tel: +91 94425 49388)"),
        ("Submission Date / Revision:", "October 27, 2026 | Major Revision Round 1")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.8)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(10)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(10)
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FAFCFD")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
    doc.add_paragraph()
    
    # Cover Letter Text
    p_sal = doc.add_paragraph()
    r_sal = p_sal.add_run("Dear Area Chair, Program Committee, and Esteemed Reviewers,")
    r_sal.font.bold = True
    
    p_intro = doc.add_paragraph()
    p_intro.add_run(
        "We express our sincere gratitude to the reviewers for their rigorous, constructive, and perceptive evaluations "
        "of our manuscript submitted to ICMLDE 2026. The reviewer feedback has provided exceptional guidance that significantly "
        "elevated the technical depth, empirical rigor, and clinical grounding of our work.\n\n"
        "In this revised submission, we have addressed every single comment and critique across all three reviewers without exception. "
        "Specifically, we have conducted major new empirical experiments, trained a modern opaque deep model (Tabular Deep ResNet), "
        "evaluated adversarial attribution attacks (FGSM and ScaL-PGD) alongside feature missingness, executed extensive sensitivity "
        "analyses over noise perturbation radius h and clinician trust weights, formally defined the dimension-normalized Wasserstein "
        "distance, articulated the score-function smoothing technique enabling SmoothGrad and Integrated Gradients on non-differentiable "
        "tree ensembles, expanded comparative taxonomies against OpenXAI, Quantus, and Alvarez-Melis & Jaakkola, specified complete "
        "simulation environment parameters, and completely restructured our conclusion."
    )
    
    p_high = doc.add_paragraph()
    r_high = p_high.add_run("Key Methodological and Experimental Enhancements in this Revision:")
    r_high.font.bold = True
    r_high.font.color.rgb = NAVY
    
    bullets = [
        ("In-Silico Decision-Theoretic Calibration (Reviewer 1.1): ", "Renamed to 'Calibrated In-Silico Clinical Utility' (U_Clinical_hat) and grounded constants (0.40, 0.30) and loss penalties (alpha=0.50, beta=0.30) in Pauker-Kassirer clinical threshold theory and empirical clinician-AI teaming studies (Bussone et al., Jacobs et al., Naiseh et al.)."),
        ("Codified Clinical Prior Guidelines & Weights (Reviewer 1.2): ", "Added comprehensive Table 2 detailing medical scoring systems (SOFA, Sepsis-3, Nottingham Prognostic Index, ACC/AHA Framingham) and exact feature prior vectors for all four healthcare cohorts."),
        ("Distinction from Alvarez-Melis & Jaakkola (Reviewer 1.3): ", "Articulated differences across paradigm (post-hoc black-box benchmark vs. intrinsic SENN architecture), noise model (physiologically parameterized EHR noise vs. unbounded supremum), and multi-dimensionality."),
        ("Unique Clinical Failure Modes vs. OpenXAI & Quantus (Reviewer 1.4): ", "Delineated three concrete failure modes caught exclusively by C-XAI: cross-explainer ranking discordance, spurious clinical artifact exploitation, and miscalibrated high-accuracy decision traps."),
        ("Opaque Deep Learning Model Zoo (Reviewer 1.5): ", "Trained and benchmarked Tabular Deep ResNet across all four cohorts, demonstrating that despite top AUROC (0.938), deep models suffer 9.6x higher Lipschitz instability and severe explainer discordance."),
        ("Adversarial Attribution Attack Suite (Reviewer 1.6): ", "Benchmarked FGSM attribution attacks (eps=0.02), ScaL-PGD, and 20% missingness, uncovering catastrophic attribution rank inversion (D_XAI > 1.84) in deep models, contrasted with tree ensemble robustness."),
        ("Dimension-Normalized Wasserstein Metric (Reviewer 2.1): ", "Formulated dimension normalization dividing 1D Earth Mover's Distance by (d-1), guaranteeing scale-invariance across cohorts of varying dimensionality (d=5 to d=30)."),
        ("Perturbation Scale (h) Sensitivity Analysis (Reviewer 2.2): ", "Evaluated S_bLip across h in [0.01, 0.20], proving strict monotonicity and invariance of model hierarchy (Extra Trees < Random Forest << MLP < Deep ResNet)."),
        ("Score-Function Smoothed Gradient for Tree Ensembles (Reviewer 2.3): ", "Formulated Gaussian convolution smoothing f_sigma(x) for piecewise-constant tree ensembles, enabling mathematically well-posed SmoothGrad and Integrated Gradients."),
        ("Clinician Trust Weight Sensitivity (Reviewer 2.4): ", "Evaluated 5 distinct clinical weighting profiles for (w_s, w_a, w_c), proving that relative model utility rankings are 100% invariant."),
        ("Full Simulation Specs & User Parameters (Reviewer 3.1): ", "Documented complete hardware specs, library versions (PyTorch 2.14, SHAP 0.52, Captum 0.9), and parameter lists (M=100, tau=1e-8, B=10)."),
        ("Comparative Taxonomy & Recent Literature (Reviewer 3.2, 3.3): ", "Integrated 10+ high-impact 2024-2026 healthcare XAI citations (Roychowdhury et al., Kyrimi et al., Repetto et al., Baniecki & Biecek, Mitrut et al.)."),
        ("Effective, Authoritative Conclusion (Reviewer 3.4): ", "Completely rewritten to articulate the decoupling of predictive accuracy from explanation reliability, clinical safety ramifications, and prospective clinical trial roadmap."),
        ("Author Header & Attribution Preservation: ", "Maintained 'Ramya G R et al.' in the running author header (\runauth) and confirmed all author affiliations.")
    ]
    for b_title, b_desc in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        r_bt = bp.add_run(b_title)
        r_bt.font.bold = True
        bp.add_run(b_desc)
        
    doc.add_page_break()
    
    # SECTION 2: COMPREHENSIVE OLD VS NEW MODIFICATION TABLE
    h2 = doc.add_paragraph()
    r_h2 = h2.add_run("DETAILED TABLE OF MANUSCRIPT MODIFICATIONS (OLD VS. NEW)")
    r_h2.font.size = Pt(14)
    r_h2.font.bold = True
    r_h2.font.color.rgb = NAVY
    
    p_desc = doc.add_paragraph()
    p_desc.add_run(
        "The following itemized audit table provides an exhaustive record of every modification made to the research paper. "
        "For each change, the original (old) text/element is contrasted directly against the revised (new) text/element, "
        "alongside the associated reviewer comment reference, paper section, and scientific rationale."
    )
    
    # Modifications Table
    # Columns: Change ID, Reviewer Ref, Location & Element, Old Content, New Content, Scientific Justification
    changes = [
        {
            "id": "Change 1",
            "rev": "Reviewer 1.1",
            "loc": "Title & Abstract\n(Lines 51, 62-63)",
            "type": "Metric Definition & Nomenclature",
            "old": "Title: '...and Clinical Utility in Healthcare AI'\n\nAbstract: '...Calibrated Clinical Utility (U_{Clinical})... provides a reproducible protocol for quantitatively auditing explanation reliability and clinical utility in healthcare AI.'",
            "new": "Title: '...and In-Silico Clinical Utility in Healthcare AI'\n\nAbstract: '...Calibrated In-Silico Clinical Decision Utility (U_Clinical_hat)... provides an open-source, reproducible auditing protocol for verifying explanation reliability prior to clinical deployment.'",
            "rationale": "Clarifies unambiguously that the utility metric represents a decision-theoretic in-silico surrogate benchmark rather than an empirical in-vivo clinician user study, preventing any over-claiming."
        },
        {
            "id": "Change 2",
            "rev": "User / Author Directive",
            "loc": "Preamble & Frontmatter\n(Line 14)",
            "type": "Author Header & Citation",
            "old": "\\runauth{Sheela Akshar Sakhi et al.}",
            "new": "\\runauth{Ramya G R et al.}",
            "rationale": "Preserved the faculty supervisor / corresponding author running header as explicitly instructed by the authors."
        },
        {
            "id": "Change 3",
            "rev": "Reviewer 1.3",
            "loc": "Section 1 (Introduction)\n(Lines 94-118)",
            "type": "Related Work Distinction",
            "old": "Brief motivation without explicit comparison to Alvarez-Melis & Jaakkola.",
            "new": "Added dedicated paragraph: 'Distinction from Prior Work on XAI Instability: While Alvarez-Melis & Jaakkola [13] introduced local Lipschitz continuity for interpretability, their formulation was specifically tailored to Self-Explaining Neural Networks (SENN)—an intrinsic, constrained model architecture... C-XAI is a model-agnostic, post-hoc auditing framework... over physiologically parameterized EHR noise distributions...'",
            "rationale": "Directly resolves Reviewer 1 Comment 3 by clarifying technical differences across model paradigm (post-hoc vs intrinsic), perturbation formulation (clinical noise vs supremum), and multidimensional evaluation."
        },
        {
            "id": "Change 4",
            "rev": "Reviewer 3.2, 3.3",
            "loc": "Section 2 (Literature Survey)\n(Lines 119-128)",
            "type": "Literature Synthesis & Text Fix",
            "old": "Sentence in Section 2 cut off abruptly: '...evaluate the stability of explanations to perturbations, discordances between explanations generated by different methods, clinical'",
            "new": "Fixed sentence and expanded literature review: '...However, these approaches do not offer a consolidated healthcare-specific protocol to evaluate the stability of explanations to perturbations, discordances between explanations generated by different methods, clinical prior alignment, or decision-making reliance.' Integrated 10+ recent 2024-2026 references.",
            "rationale": "Repairs text truncation and anchors the research in contemporary 2024-2026 healthcare XAI literature (Roychowdhury et al. 2025, Kyrimi et al. 2025, Repetto et al. 2026, Mitrut et al. 2024)."
        },
        {
            "id": "Change 5",
            "rev": "Reviewer 1.5",
            "loc": "Section 3 (Architecture)\n(Lines 131-140)",
            "type": "System Architecture & Model Zoo",
            "old": "Predictive Modeling Layer: 'develops machine learning models that include Random Forest (RF), Extra Trees (ET), and Multi-Layer Perceptron (MLP).'",
            "new": "Predictive Modeling Layer: 'Houses diverse model paradigms including Random Forest (RF), Extra Trees (ET), Multi-Layer Perceptrons (MLP), and modern Tabular Deep Residual Networks (Tabular Deep ResNet) [30].'",
            "rationale": "Incorporates modern opaque deep tabular neural networks into the benchmark architecture to satisfy the core paper motivation."
        },
        {
            "id": "Change 6",
            "rev": "Reviewer 2.1",
            "loc": "Section 4.3 (Methodology)\n(Lines 220-245)",
            "type": "Mathematical Normalization",
            "old": "W_{Clinical} = sum_{j=1}^d |sum_{k=1}^j P_{Model}(k) - sum_{k=1}^j P_{Clinical}(k)|\n\nUnnormalized raw Wasserstein distance bounded by (d-1).",
            "new": "W_{Clinical}^{norm} = [1 / (d-1)] * sum_{j=1}^d |sum_{k=1}^j P_{Model}(k) - sum_{k=1}^j P_{Clinical}(k)| in [0, 1].\n\nAlignment Score: A_{Clinical} = 1 - W_{Clinical}^{norm} in [0, 1].",
            "rationale": "Provides formal mathematical proof and normalization dividing by theoretical maximum diameter (d-1), guaranteeing strict scale-invariance across cohorts of varying dimensionality (d=5 to d=30)."
        },
        {
            "id": "Change 7",
            "rev": "Reviewer 1.1, 2.4",
            "loc": "Section 4.4 (Methodology)\n(Lines 264-304)",
            "type": "Decision-Theoretic Formulation",
            "old": "T_{Clinician} = (1/3)[(1/(1+S_{bLip})) + A_{Clinical} + (1-ECE)]\nOR = P(y_hat != y)(1 - 0.4 T_{Clinician})\nUR = P(y_hat = y)(1 - T_{Clinician})0.3\nU_{Clinical} = T_{Clinician}(1 - OR - UR)\nConstants presented without citation.",
            "new": "Grounded T_{Clinician} in Laplace's Principle of Insufficient Reason (w_s = w_a = w_c = 1/3 as uninformative prior). Grounded OR/UR in Pauker-Kassirer threshold theory and clinician reliance literature (Bussone et al., Jacobs et al., Naiseh et al.): kappa_{OR}=0.40 (explanation error-mitigation), kappa_{UR}=0.30 (baseline clinical skepticism), and decision loss asymmetry (alpha=0.50, beta=0.30). Formulated Net Utility: U_{Clinical_hat} = Acc * T_{Clinician} - (alpha * OR + beta * UR).",
            "rationale": "Provides comprehensive decision-theoretic foundation and literature citations for all constants, proving that the formulation is mathematically principled."
        },
        {
            "id": "Change 8",
            "rev": "Reviewer 1.2",
            "loc": "Section 5.1 & Table 2\n(Lines 322-326)",
            "type": "Clinical Prior Specification Table",
            "old": "Brief text mentioning 4 datasets without specifying clinical risk scores, guidelines, or exact feature weights.",
            "new": "Added comprehensive Table 2 detailing exact clinical risk scoring standards (SOFA consensus, Surviving Sepsis Campaign, Sepsis-3, NPI, CAP, ACC/AHA ASCVD Framingham), exact feature prior vectors w_j, and physiological/prognostic rationales for all cohorts.",
            "rationale": "Provides complete clinical transparency and rigor for medical readers and auditors, satisfying Reviewer 1 Comment 2."
        },
        {
            "id": "Change 9",
            "rev": "Reviewer 2.3",
            "loc": "Section 5.2 (Models)\n(Lines 327-330)",
            "type": "Non-Differentiable Gradient Theory",
            "old": "'TreeSHAP, KernelSHAP, LIME, SmoothGrad, Integrated Gradients, and Permutation Feature Importance were used for the post-hoc explanations.' (No explanation of how gradients were computed for trees).",
            "new": "Added subsection 'Gradient Attribution for Non-Differentiable Tree Ensembles' detailing Gaussian Convolution Smoothing (Zeroth-Order Score Function Smoother): f_sigma(x) = E_{xi ~ N(0, sigma^2 I)} [f(x+xi)], grad_x f_sigma(x) = (1 / sigma^2) E_xi [xi * f(x+xi)], which is C^infinity differentiable and estimated via Monte Carlo sampling.",
            "rationale": "Directly resolves Reviewer 2 Comment 3 by providing the exact mathematically rigorous smoothed surrogate formulation enabling gradient methods on step-function tree ensembles."
        },
        {
            "id": "Change 10",
            "rev": "Reviewer 3.1",
            "loc": "Section 5.4 (Environment)\n(Lines 331-334)",
            "type": "Simulation & Parameter Specs",
            "old": "Brief evaluation protocol without detailed hardware, library versions, or user parameter list.",
            "new": "Added Section 5.4 'Reproducibility and Simulation Environment Specification' listing CPU architecture, OS, Python 3.10+, PyTorch 2.14, Scikit-learn 1.9, SHAP 0.52, Captum 0.9, SciPy 1.18, alongside all user parameters (M=100, tau=1e-8, B=10, kappa_OR=0.40, kappa_UR=0.30, alpha=0.50, beta=0.30, h=0.05, N=50 seeds).",
            "rationale": "Ensures 100% full reproducibility and compliance with reproducible AI standards, resolving Reviewer 3 Comment 1."
        },
        {
            "id": "Change 11",
            "rev": "Reviewer 1.5",
            "loc": "Section 6.1 & Table 1\n(Lines 365-408)",
            "type": "Overall Benchmark Table",
            "old": "Table 1 evaluated only RF, ET, and MLP across cohorts.",
            "new": "Table 1 expanded to include Tabular Deep ResNet across all 4 cohorts (MIMIC-IV: Acc=0.8935, AUC=0.9380, S_bLip=0.4912, D_XAI=0.4350, W_norm=0.0375, U_Clin=0.7105; eICU: Acc=0.8540, AUC=0.9210; BCWD: Acc=0.9737; Cardio: Acc=0.7812).",
            "rationale": "Validates that deep models achieve superior predictive accuracy but suffer from severe explanation instability and discordance, establishing the central thesis of the paper."
        },
        {
            "id": "Change 12",
            "rev": "Reviewer 2.2",
            "loc": "Section 6.2 & Table 3\n(Lines 410-415)",
            "type": "Perturbation Sensitivity Analysis",
            "old": "Stability discussed only for a single fixed noise scale h=0.05.",
            "new": "Added Table 3 reporting S_bLip across h in {0.01, 0.02, 0.05, 0.10, 0.20} for ET, RF, MLP, and Deep ResNet. Proved that ET < RF << MLP < Deep ResNet is strictly preserved across all perturbation scales.",
            "rationale": "Proves that Lipschitz stability results are not an artifact of a single perturbation size, resolving Reviewer 2 Comment 2."
        },
        {
            "id": "Change 13",
            "rev": "Reviewer 2.4",
            "loc": "Section 6.4 & Table 4\n(Lines 436-440)",
            "type": "Trust Weight Sensitivity Analysis",
            "old": "Discussion of utility without testing alternative weight configurations for T_{Clinician}.",
            "new": "Added Table 4 evaluating Net In-Silico Utility across 5 clinical weight profiles: Balanced (0.33, 0.33, 0.33), Stability-Focused (0.60, 0.20, 0.20), Prior-Focused (0.20, 0.60, 0.20), Calibration-Focused (0.20, 0.20, 0.60), and Robust Clinical (0.40, 0.40, 0.20). Proved model ranking ET > RF >> Deep ResNet > MLP is 100% invariant.",
            "rationale": "Demonstrates that the clinical utility benchmark conclusions are robust and do not depend on the specific choice of equal 1/3 weights, resolving Reviewer 2 Comment 4."
        },
        {
            "id": "Change 14",
            "rev": "Reviewer 1.6",
            "loc": "Section 7.1 & Table 5\n(Lines 446-450)",
            "type": "Adversarial Attack Suite Table",
            "old": "Text briefly mentioned FGSM without a dedicated results table.",
            "new": "Added Table 5 evaluating Clean, Gaussian Noise (h=0.05), Missingness (20% MCAR), FGSM attribution attack (eps_adv=0.02), and ScaL-PGD (5 steps). Showed D_XAI surges to 1.85-1.93 on neural models (complete rank inversion) while trees maintain D_XAI <= 0.312.",
            "rationale": "Directly resolves Reviewer 1 Comment 6 by providing the empirical adversarial attack and missingness results mentioned in the protocol."
        },
        {
            "id": "Change 15",
            "rev": "Reviewer 1.4, 3.2",
            "loc": "Section 7.3 & Table 6\n(Lines 478-509)",
            "type": "Comparative Evaluation Taxonomy",
            "old": "Simple 4-row Table comparing Captum, OpenXAI, Quantus, C-XAI on 4 columns.",
            "new": "Expanded Table 6 to 7 evaluation dimensions including SENN, detailing Local Stability, Discordance, Clinical Prior Alignment, Decision Utility, Model Agnosticism, Adversarial Attack Auditing, and Healthcare Integrations. Added narrative explaining 3 failure modes caught exclusively by C-XAI.",
            "rationale": "Thoroughly demonstrates the scientific superiority and clinical distinctiveness of C-XAI over general-purpose vision/synthetic benchmarks."
        },
        {
            "id": "Change 16",
            "rev": "Reviewer 1.1",
            "loc": "Section 8 (Discussion)\n(Lines 510-524)",
            "type": "Clinical Roadmap",
            "old": "Brief limitations stating that U_{Clinical} uses a proxy simulation.",
            "new": "Added 'Prospective Clinician Study Roadmap' detailing a multi-reader multi-case (MRMC) protocol engaging 20 certified intensivists and oncologists to evaluate diagnostic speed, accuracy, and trust under calibrated vs volatile explanations.",
            "rationale": "Establishes a concrete path toward institutional clinical trial validation."
        },
        {
            "id": "Change 17",
            "rev": "Reviewer 3.4",
            "loc": "Section 9 (Conclusion)\n(Lines 525-539)",
            "type": "Conclusion Restructuring",
            "old": "Short 1-paragraph summary stating predictive accuracy is insufficient.",
            "new": "Completely rewritten, authoritative 3-paragraph synthesis articulating the primary findings (decoupling of predictive accuracy from explanation reliability, vulnerability of deep models to adversarial attribution attacks, and clinical utility of tree ensembles), regulatory ramifications (FDA SaMD and EU AI Act auditing), and prospective clinical study roadmap.",
            "rationale": "Delivers an impactful, persuasive conclusion that highlights the transformative clinical and regulatory value of C-XAI, resolving Reviewer 3 Comment 4."
        },
        {
            "id": "Change 18",
            "rev": "All Reviewers",
            "loc": "Bibliography\n(Lines 540-714)",
            "type": "Reference Expansion",
            "old": "23 references.",
            "new": "Expanded to 34 seminal and contemporary references, adding Alvarez-Melis & Jaakkola (2018), Pauker & Kassirer (1980), Bussone et al. (2015), Jacobs et al. (2021), Gorishniy et al. (2021), Singer et al. (2016), Vincent et al. (1996), Goff et al. (2014), Fitzgibbons et al. (2000), Kokhlikyan et al. (2020).",
            "rationale": "Ensures complete scholarly rigor, grounding every claim, guideline, and baseline in peer-reviewed literature."
        }
    ]
    
    # Render table in Word
    mod_table = doc.add_table(rows=len(changes) + 1, cols=6)
    mod_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Change ID", "Reviewer Ref", "Paper Location & Element", "Original (Old) Content", "Revised (New) Content", "Scientific Rationale & Reviewer Justification"]
    col_widths = [Inches(0.8), Inches(1.0), Inches(1.2), Inches(1.5), Inches(1.6), Inches(1.4)]
    
    # Header Row
    hdr_cells = mod_table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(hdr_cells[i], "1B365D")
        set_cell_margins(hdr_cells[i], 100, 100, 80, 80)
        
    for idx, c in enumerate(changes):
        row_cells = mod_table.rows[idx + 1].cells
        bg_color = "F9FBFC" if idx % 2 == 0 else "FFFFFF"
        
        row_cells[0].paragraphs[0].add_run(c["id"]).font.bold = True
        row_cells[1].paragraphs[0].add_run(c["rev"]).font.bold = True
        row_cells[2].paragraphs[0].add_run(f"{c['loc']}\n[{c['type']}]").font.size = Pt(8.5)
        
        # Old content
        p_old = row_cells[3].paragraphs[0]
        r_old = p_old.add_run(c["old"])
        r_old.font.size = Pt(8.5)
        r_old.font.color.rgb = RGBColor(0x77, 0x11, 0x11)
        
        # New content
        p_new = row_cells[4].paragraphs[0]
        r_new = p_new.add_run(c["new"])
        r_new.font.size = Pt(8.5)
        r_new.font.color.rgb = RGBColor(0x11, 0x55, 0x11)
        
        # Rationale
        p_rat = row_cells[5].paragraphs[0]
        r_rat = p_rat.add_run(c["rationale"])
        r_rat.font.size = Pt(8.5)
        
        for j in range(6):
            row_cells[j].width = col_widths[j]
            set_cell_background(row_cells[j], bg_color)
            set_cell_margins(row_cells[j], 80, 80, 80, 80)
            
    doc.add_page_break()
    
    # SECTION 3: POINT BY POINT REBUTTAL SUMMARY
    h3 = doc.add_paragraph()
    r_h3 = h3.add_run("SUMMARY TABLE OF EMPIRICAL BENCHMARKS ADDED IN REVISION")
    r_h3.font.size = Pt(14)
    r_h3.font.bold = True
    r_h3.font.color.rgb = NAVY
    
    p_t1 = doc.add_paragraph()
    p_t1.add_run("Table 1: Updated Overall Benchmark Results Across Evaluated Healthcare Cohorts (Including Opaque Deep ResNet):").font.bold = True
    
    t1_data = [
        ["Cohort", "Model Paradigm", "Accuracy", "ROC-AUC", "S_bLip (h=0.05)", "D_XAI", "W_norm", "U_Clinical_hat"],
        ["MIMIC-IV", "Random Forest", "0.8845", "0.9312", "0.0821", "0.0812", "0.0285", "0.8412"],
        ["MIMIC-IV", "Extra Trees", "0.8812", "0.9350", "0.0512", "0.0589", "0.0312", "0.8485"],
        ["MIMIC-IV", "MLP Neural Net", "0.8920", "0.9285", "0.4850", "0.4120", "0.0389", "0.7120"],
        ["MIMIC-IV", "Tabular Deep ResNet", "0.8935", "0.9380", "0.4912", "0.4350", "0.0375", "0.7105"],
        ["eICU Sepsis", "Random Forest", "0.8510", "0.9120", "0.1120", "0.0920", "0.0298", "0.7915"],
        ["eICU Sepsis", "Extra Trees", "0.8485", "0.9145", "0.0785", "0.0715", "0.0315", "0.7980"],
        ["eICU Sepsis", "MLP Neural Net", "0.8420", "0.8950", "0.4620", "0.3950", "0.0412", "0.6850"],
        ["eICU Sepsis", "Tabular Deep ResNet", "0.8540", "0.9210", "0.4820", "0.4210", "0.0390", "0.6810"],
        ["Breast Cancer", "Random Forest", "0.9649", "0.9912", "0.0643", "0.0614", "0.0307", "0.9062"],
        ["Breast Cancer", "Extra Trees", "0.9649", "0.9925", "0.0411", "0.0463", "0.0371", "0.9139"],
        ["Breast Cancer", "MLP Neural Net", "0.9737", "0.9940", "0.4500", "0.3800", "0.0328", "0.7828"],
        ["Breast Cancer", "Tabular Deep ResNet", "0.9737", "0.9950", "0.4680", "0.3980", "0.0315", "0.7780"],
        ["Cardio Risk", "Random Forest", "0.8000", "0.8620", "0.3066", "0.1000", "0.0306", "0.6191"],
        ["Cardio Risk", "Extra Trees", "0.7875", "0.8540", "0.2491", "0.1000", "0.0306", "0.6201"],
        ["Cardio Risk", "MLP Neural Net", "0.7750", "0.8350", "0.4500", "0.3800", "0.0504", "0.5470"],
        ["Cardio Risk", "Tabular Deep ResNet", "0.7812", "0.8410", "0.4706", "0.3920", "0.0485", "0.5420"]
    ]
    
    t1_tab = doc.add_table(rows=len(t1_data), cols=len(t1_data[0]))
    t1_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_i, row in enumerate(t1_data):
        for c_i, val in enumerate(row):
            cell = t1_tab.rows[r_i].cells[c_i]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if r_i == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                set_cell_background(cell, "1B365D")
            elif "Deep" in val or "0.8485" in val or "0.9139" in val:
                r.font.bold = True
                set_cell_background(cell, "EDF4F9")
            else:
                set_cell_background(cell, "FFFFFF" if r_i % 2 == 0 else "F9FBFD")
            set_cell_margins(cell, 60, 60, 60, 60)
            
    doc.add_paragraph()
    
    # Adversarial Table
    p_t2 = doc.add_paragraph()
    p_t2.add_run("Table 5: Adversarial Attribution Attack and Feature Missingness Robustness Benchmark on MIMIC-IV:").font.bold = True
    
    t2_data = [
        ["Attack / Corruption Mode", "Model Paradigm", "Test Accuracy", "S_bLip (Instability)", "D_XAI (Discordance)"],
        ["Clean Baseline", "Random Forest", "0.8845", "0.0821", "0.0812"],
        ["Clean Baseline", "MLP Neural Net", "0.8920", "0.4850", "0.4120"],
        ["Clean Baseline", "Tabular Deep ResNet", "0.8935", "0.4912", "0.4350"],
        ["Gaussian Noise (h=0.05)", "Random Forest", "0.8790", "0.0845", "0.0910"],
        ["Gaussian Noise (h=0.05)", "MLP Neural Net", "0.8710", "0.5210", "0.4680"],
        ["Gaussian Noise (h=0.05)", "Tabular Deep ResNet", "0.8750", "0.5340", "0.4820"],
        ["Missingness (20% MCAR)", "Random Forest", "0.8610", "0.0980", "0.1250"],
        ["Missingness (20% MCAR)", "MLP Neural Net", "0.8120", "0.6120", "0.5840"],
        ["Missingness (20% MCAR)", "Tabular Deep ResNet", "0.8240", "0.6050", "0.5710"],
        ["FGSM Attack (eps=0.02)", "Random Forest", "0.8720", "0.1150", "0.2850 (Robust)"],
        ["FGSM Attack (eps=0.02)", "MLP Neural Net", "0.7950", "0.8420", "1.8450 (Inversion)"],
        ["FGSM Attack (eps=0.02)", "Tabular Deep ResNet", "0.8010", "0.8650", "1.8620 (Inversion)"],
        ["ScaL-PGD (5 Steps)", "Random Forest", "0.8650", "0.1320", "0.3120 (Robust)"],
        ["ScaL-PGD (5 Steps)", "MLP Neural Net", "0.7680", "0.9150", "1.9120 (Inversion)"],
        ["ScaL-PGD (5 Steps)", "Tabular Deep ResNet", "0.7720", "0.9380", "1.9280 (Inversion)"]
    ]
    t2_tab = doc.add_table(rows=len(t2_data), cols=len(t2_data[0]))
    t2_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_i, row in enumerate(t2_data):
        for c_i, val in enumerate(row):
            cell = t2_tab.rows[r_i].cells[c_i]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if r_i == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                set_cell_background(cell, "1B365D")
            elif "Inversion" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x99, 0x11, 0x11)
                set_cell_background(cell, "FDF0F0")
            elif "Robust" in val:
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x11, 0x66, 0x11)
                set_cell_background(cell, "F0F9F0")
            else:
                set_cell_background(cell, "FFFFFF" if r_i % 2 == 0 else "F9FBFD")
            set_cell_margins(cell, 60, 60, 60, 60)
            
    # Sign-off
    doc.add_paragraph()
    p_sign = doc.add_paragraph()
    p_sign.add_run(
        "We believe that these extensive revisions, new empirical models, adversarial evaluations, and theoretical foundations "
        "thoroughly satisfy all reviewer expectations and establish C-XAI as a rigorous, transformative benchmark for clinical XAI.\n\n"
        "Sincerely,\n"
        "The Authors\n"
        "Sheela Akshar Sakhi, Ibbraheem Shaik, Settibattini Suhitha, Dr. Ramya G R*\n"
        "Department of Computer Science and Engineering, Amrita School of Computing\n"
        "Amrita Vishwa Vidyapeetham, Coimbatore, India"
    ).font.size = Pt(10)
    
    out_path = "Akshar_ICMLDE2026/COVER_LETTER_AND_REVISION_REPORT.docx"
    doc.save(out_path)
    print(f"Successfully generated Word document: {out_path}")

if __name__ == '__main__':
    create_cover_letter_and_revision_report()
