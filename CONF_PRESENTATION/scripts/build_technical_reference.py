#!/usr/bin/env python3
"""
build_technical_reference.py
============================
Generates the formal, slide-by-slide Technical Reference Document for
ICMLDE 2026 Paper ID 857 (C-XAI).

Outputs (in CONF_PRESENTATION/SUBMISSION_READY/):
- ICMLDE-2026-857_Slide_by_Slide_Technical_Reference.md
- ICMLDE-2026-857_Slide_by_Slide_Technical_Reference.docx
- ICMLDE-2026-857_Slide_by_Slide_Technical_Reference.pdf
"""

import os
import re
import sys
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
from technical_reference_data import SLIDES_DATA

OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "SUBMISSION_READY"))
BASE_NAME = "ICMLDE-2026-857_Slide_by_Slide_Technical_Reference"
MD_PATH = os.path.join(OUTPUT_DIR, f"{BASE_NAME}.md")
DOCX_PATH = os.path.join(OUTPUT_DIR, f"{BASE_NAME}.docx")
PDF_PATH = os.path.join(OUTPUT_DIR, f"{BASE_NAME}.pdf")

# Palette
COLOR_PRIMARY = RGBColor(27, 54, 93)      # Deep Navy (#1B365D)
COLOR_SECONDARY = RGBColor(46, 92, 138)   # Slate Blue (#2E5C8A)
COLOR_TEAL = RGBColor(0, 109, 119)        # Clinical Teal (#006D77)
COLOR_DARK = RGBColor(34, 34, 34)         # Charcoal (#222222)
COLOR_MUTED = RGBColor(85, 85, 85)        # Muted Gray (#555555)

HEX_PRIMARY = "1B365D"
HEX_SECONDARY = "2E5C8A"
HEX_BOX_BG = "F4F7FA"
HEX_ROW_ALT = "EBF1F8"
HEX_RULE = "B8C9DC"

PRINTABLE_WIDTH_IN = 7.0
PRINTABLE_WIDTH_DXA = int(PRINTABLE_WIDTH_IN * 1440)  # 10080 dxa


# ===========================================================================
# XML / RICH TEXT HELPERS
# ===========================================================================
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))


def set_cell_margins(cell, top=90, bottom=90, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)


def set_table_fixed_width(tbl, total_dxa, col_widths_dxa):
    tblPr = tbl._tbl.tblPr
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="{total_dxa}" w:type="dxa"/>'))
    tblPr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))
    for row in tbl.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        for idx, w_dxa in enumerate(col_widths_dxa):
            cell = row.cells[idx]
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:tcW {nsdecls("w")} w:w="{w_dxa}" w:type="dxa"/>'))


def add_bottom_border(paragraph, hex_color=HEX_RULE, sz="6"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(f'''
        <w:pBdr {nsdecls("w")}>
            <w:bottom w:val="single" w:sz="{sz}" w:space="4" w:color="{hex_color}"/>
        </w:pBdr>
    ''')
    pPr.append(pBdr)


def add_rich_runs(paragraph, text, font_name="Arial", font_size=Pt(8.8),
                  color=COLOR_DARK, bold=False, italic=False):
    """Parses <b>, <i>, <sub>, <sup> inline tags into native Word runs."""
    pattern = re.compile(r'(<b>.*?</b>|<i>.*?</i>|<sub>.*?</sub>|<sup>.*?</sup>)', re.DOTALL)
    tokens = pattern.split(text)
    for tok in tokens:
        if not tok:
            continue
        is_b, is_i, is_sub, is_sup = bold, italic, False, False
        content = tok
        if tok.startswith("<b>") and tok.endswith("</b>"):
            is_b = True
            content = tok[3:-4]
        elif tok.startswith("<i>") and tok.endswith("</i>"):
            is_i = True
            content = tok[3:-4]
        elif tok.startswith("<sub>") and tok.endswith("</sub>"):
            is_sub = True
            content = tok[5:-6]
        elif tok.startswith("<sup>") and tok.endswith("</sup>"):
            is_sup = True
            content = tok[5:-6]

        # Support nested <sub>/<sup> inside <b> if present
        if is_b and ("<sub>" in content or "<sup>" in content):
            add_rich_runs(paragraph, content, font_name=font_name, font_size=font_size,
                          color=color, bold=True, italic=is_i)
            continue

        run = paragraph.add_run(content)
        run.font.name = font_name
        run.font.size = font_size
        run.font.color.rgb = color
        run.font.bold = is_b
        run.font.italic = is_i
        if is_sub:
            run.font.subscript = True
        if is_sup:
            run.font.superscript = True


def html_to_markdown(text):
    """Converts inline markup tags to clean Markdown."""
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text)
    return text


def add_formula_box(doc, formulas):
    """Renders the 4 core mathematical formulations inside a crisp bordered box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_fixed_width(tbl, PRINTABLE_WIDTH_DXA, [PRINTABLE_WIDTH_DXA])

    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_BOX_BG)
    set_cell_margins(cell, top=110, bottom=110, left=150, right=150)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_RULE}"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_PRIMARY}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_RULE}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_RULE}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    for idx, (f_name, f_expr, f_notes) in enumerate(formulas):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0 if idx == 0 else 4)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.18
        add_rich_runs(p, f"<b>{f_name}:</b> ", font_size=Pt(8.8), color=COLOR_PRIMARY)
        add_rich_runs(p, f_expr, font_name="Arial", font_size=Pt(8.8), color=COLOR_DARK)
        if f_notes:
            p_n = cell.add_paragraph()
            p_n.paragraph_format.space_before = Pt(0)
            p_n.paragraph_format.space_after = Pt(2 if idx < len(formulas) - 1 else 0)
            p_n.paragraph_format.left_indent = Inches(0.18)
            add_rich_runs(p_n, f_notes, font_size=Pt(8.2), color=COLOR_MUTED, italic=True)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)


def add_rationale_box(doc, rationales):
    """Renders Methodological Rationales & Technical Notes in an unbreakable block."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_fixed_width(tbl, PRINTABLE_WIDTH_DXA, [PRINTABLE_WIDTH_DXA])

    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_BOX_BG)
    set_cell_margins(cell, top=95, bottom=95, left=140, right=140)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_SECONDARY}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    for idx, (topic, explanation) in enumerate(rationales):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0 if idx == 0 else 4)
        p.paragraph_format.space_after = Pt(1 if idx < len(rationales) - 1 else 0)
        p.paragraph_format.line_spacing = 1.15
        add_rich_runs(p, f"<b>{topic}:</b> ", font_size=Pt(8.7), color=COLOR_PRIMARY)
        add_rich_runs(p, explanation, font_size=Pt(8.7), color=COLOR_DARK)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)


# ===========================================================================
# 1. MARKDOWN GENERATION
# ===========================================================================
def generate_markdown():
    print(f"Writing Markdown technical reference to {MD_PATH}...")
    lines = []
    lines.append("# C-XAI: Slide-by-Slide Technical Reference Document")
    lines.append("### 5th Elsevier International Conference on Machine Learning and Data Engineering (ICMLDE 2026)")
    lines.append("**Procedia Computer Science · Paper ID: 857 · Technical Session**\n")
    lines.append("> **Presenting Author**: Sheela Akshar Sakhi (`aksharsakhi@gmail.com`)  ")
    lines.append("> **Co-Authors**: Ibbraheem Shaik, Settibattini Suhitha, Dr. Ramya G R* (`gr_ramya@cb.amrita.edu`)  ")
    lines.append("> **Affiliation**: Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore, India  ")
    lines.append("> **Repository**: [github.com/aksharsakhi/c-xai-healthcare-predictions](https://github.com/aksharsakhi/c-xai-healthcare-predictions)\n")
    lines.append("---\n")

    lines.append("## Executive Summary: Benchmark Metrics & Core Formulations\n")
    lines.append("| Metric / Dimension | Reported Empirical Value | Cohort & Statistical Interpretation |")
    lines.append("|:---|:---|:---|")
    lines.append("| **Total Records Audited** | **51,369 encounters** | MIMIC-IV (40,000), eICU (10,000), BCWD (569), Cardio EHR (800) |")
    lines.append("| **Clinical Decision Utility** | **+19.6% relative (+13.9% abs)** | Extra Trees (0.8485) vs. Tabular Deep ResNet (0.7095–0.7107) on MIMIC-IV |")
    lines.append("| **Statistical Significance** | **p < 0.001, W = 0.0, d = 2.96** | Wilcoxon signed-rank W = 0.0 (50/50 wins), paired t = 14.82, Cohen's d = 2.96 |")
    lines.append("| **Explanation Instability** | **9.6× higher in Deep ResNet** | Deep ResNet Ŝ<sub>Lip</sub> = 0.4912 vs. Extra Trees 0.0512 (h = 0.05) |")
    lines.append("| **Explainer Discordance** | **7.4× higher in Deep ResNet** | Deep ResNet D<sub>XAI</sub> = 0.435 vs. Extra Trees 0.059 (94.1% rank consensus) |")
    lines.append("| **Accuracy Decoupling** | **R² = 0.04 across cohorts** | AUROC explains less than 4% of clinical utility variance (p = 0.42) |")
    lines.append("| **Calibration Error (ECE)** | **0.015 vs. 0.055** | Extra Trees calibration error is 3.7× lower than Tabular Deep ResNet |")
    lines.append("| **Inference Latency** | **4.2 ms vs. 48.5 ms** | Extra Trees scoring is 11.5× faster than Deep ResNet per encounter |\n")

    lines.append("### Core C-XAI Mathematical Formulations\n")
    lines.append("1. **Local Lipschitz Explanation Stability ($\\widehat{\\mathcal{S}}_{\\text{Lip}}$)**:")
    lines.append("   $$\\widehat{\\mathcal{S}}_{\\text{Lip}}(x; f, \\mathcal{E}, h) = \\frac{1}{M} \\sum_{m=1}^{M} \\frac{\\|\\mathcal{E}_f(x + \\delta_m) - \\mathcal{E}_f(x)\\|_2}{\\|\\delta_m\\|_2 + \\delta_0}, \\quad \\delta_m \\sim \\mathcal{N}(0, h^2 I), \\; M = 100, \\; h = 0.05, \\; \\delta_0 = 10^{-8}$$")
    lines.append("2. **Cross-Explainer Discordance ($\\mathcal{D}_{\\text{XAI}}$)**:")
    lines.append("   $$\\mathcal{D}_{\\text{XAI}}(x; f) = 1 - \\frac{2}{K(K - 1)} \\sum_{j < k} r_s(\\mathcal{E}_j(x), \\mathcal{E}_k(x)) \\in [0, 2]$$")
    lines.append("3. **Dimension-Normalized Clinical Prior Alignment ($\\mathcal{W}_{\\text{Clin}}^{\\text{norm}}$ & $A_{\\text{Clin}}$)**:")
    lines.append("   $$\\mathcal{W}_{\\text{Clin}}^{\\text{norm}}(x) = \\frac{\\mathcal{W}_1(\\mathcal{E}_{\\text{norm}}(x), P_{\\text{clin}})}{d - 1} \\in [0, 1], \\qquad A_{\\text{Clin}} = 1 - \\mathcal{W}_{\\text{Clin}}^{\\text{norm}}$$")
    lines.append("4. **Trust Calibration Factor ($\\widehat{T}_{\\text{Clin}}$) & Net Clinical Utility ($\\widehat{\\mathcal{U}}_{\\text{Clin}}$)**:")
    lines.append("   $$\\widehat{T}_{\\text{Clin}} = \\frac{1}{3}\\left[\\frac{1}{1 + \\widehat{\\mathcal{S}}_{\\text{Lip}}} + A_{\\text{Clin}} + (1 - \\text{ECE})\\right], \\qquad \\widehat{\\mathcal{U}}_{\\text{Clin}} = \\text{Acc}\\cdot\\widehat{T}_{\\text{Clin}} - (\\alpha\\cdot\\text{OR} + \\beta\\cdot\\text{UR})$$")
    lines.append("   *Parameters*: $\\text{OR} = (1 - \\text{Acc})(1 - 0.4\\,\\widehat{T}_{\\text{Clin}})$, $\\text{UR} = \\text{Acc}(1 - \\widehat{T}_{\\text{Clin}})(0.3)$, $\\alpha = 0.50$, $\\beta = 0.30$.\n")
    lines.append("---\n")

    for s in SLIDES_DATA:
        lines.append(f"## Slide {s['slide_num']}: {s['title']}\n")
        lines.append(f"**Overview**: {html_to_markdown(s['overview'])}\n")

        lines.append("### Key Terminology & Definitions")
        for term, definition in s["terminology"]:
            lines.append(f"- **{html_to_markdown(term)}**: {html_to_markdown(definition)}")
        lines.append("")

        lines.append("### Mathematical Formulations & Technical Details")
        for head, details in s["mechanics"]:
            lines.append(f"- **{html_to_markdown(head)}**:")
            for sub in details.split("\n"):
                lines.append(f"  {html_to_markdown(sub)}")
        lines.append("")

        lines.append("### Clinical & Regulatory Context")
        for head, details in s["clinical_context"]:
            lines.append(f"- **{html_to_markdown(head)}**: {html_to_markdown(details)}")
        lines.append("")

        lines.append("### Methodological Rationales & Technical Notes")
        for topic, explanation in s["rationales"]:
            lines.append(f"> **{html_to_markdown(topic)}**: {html_to_markdown(explanation)}\n")
        lines.append("---\n")

    lines.append("---\n")
    lines.append("## Appendix: Quick-Lookup Glossary of Symbols, Acronyms & Specialized Terms\n")
    lines.append("| Symbol / Term | Domain | Meaning |")
    lines.append("|:---|:---|:---|")
    glossary_rows = [
        ("Ŝ<sub>Lip</sub>", "Stability Metric", "Empirical Local Lipschitz Stability Index measuring attribution sensitivity under Gaussian noise (h = 0.05, M = 100). Lower is more stable."),
        ("D<sub>XAI</sub>", "Discordance Metric", "Cross-Explainer Discordance (1 − r<sub>s</sub>) ∈ [0, 2]; measures rank-order conflict between pairs of post-hoc explainers. Lower is better."),
        ("W<sub>Clin</sub><sup>norm</sup> / A<sub>Clin</sub>", "Clinical Alignment", "Dimension-normalized 1D Wasserstein distance to medical priors ∈ [0, 1]; Alignment A<sub>Clin</sub> = 1 − W<sub>Clin</sub><sup>norm</sup>."),
        ("T<sub>Clin</sub> / Û<sub>Clin</sub>", "Decision Utility", "Clinician Trust Calibration Factor T<sub>Clin</sub> and Net Calibrated Decision Utility Û<sub>Clin</sub> incorporating accuracy and reliance loss."),
        ("ECE / Brier Score", "Calibration", "Expected Calibration Error and mean squared probability error measuring how faithfully predicted probabilities match true risk."),
        ("OR / UR (α = 0.50, β = 0.30)", "Decision Theory", "Over-Reliance (accepting false predictions; penalty α = 0.50) and Under-Reliance (ignoring true alerts; penalty β = 0.30)."),
        ("r<sub>s</sub>", "Statistics", "Spearman rank correlation coefficient ∈ [−1, +1] measuring ordinal rank consistency between two attribution vectors."),
        ("W = 0.0 / t = 14.82 / d = 2.96", "Hypothesis Testing", "Wilcoxon signed-rank statistic (0.0 = 50/50 wins), paired t-statistic, and Cohen's d standardized effect size (> 0.8 = large)."),
        ("SOFA / Sepsis-3", "Clinical ICU", "Sequential Organ Failure Assessment (0–24) and international consensus criteria defining acute sepsis organ dysfunction."),
        ("MAP / Lactate / WBC / Creatinine", "Clinical Biomarkers", "Mean Arterial Pressure (perfusion), Serum Lactate (hypoxia), White Blood Cell count (inflammation), Creatinine (kidney injury)."),
        ("NPI / ASCVD", "Clinical Oncology / Cardio", "Nottingham Prognostic Index (breast pathology) and ACC/AHA 10-year Atherosclerotic Cardiovascular Disease risk score."),
        ("MCAR", "Missing Data", "Missing Completely At Random: missingness independent of observed or unobserved patient clinical states (20% stress-test)."),
        ("TreeSHAP / KernelSHAP / LIME", "XAI Explainers", "Game-theoretic Shapley attribution methods (tree-exact vs. kernel-approximated) and local sparse linear surrogate explainer."),
        ("IG / SmoothGrad / PFI", "XAI Explainers", "Integrated Gradients (path integral from survivor median), SmoothGrad (noisy gradient averaging), Permutation Feature Importance."),
        ("Zeroth-Order Smoother", "Optimization", "Gaussian convolution + Stein's lemma score estimator enabling gradient attribution on discontinuous decision-tree step functions."),
        ("FGSM / ScaL-PGD", "Adversarial ML", "Fast Gradient Sign Method and Scaled Projected Gradient Descent attacks perturbing attributions while preserving predictions."),
        ("SENN / Captum / OpenXAI / Quantus", "Prior Benchmarks", "Self-Explaining Neural Networks and existing vision/NLP/synthetic XAI evaluation toolkits lacking clinical guideline utility models."),
        ("FDA SaMD / GMLP / EU AI Act", "Governance", "Software as a Medical Device, Good Machine Learning Practice Principle 7, and EU AI Act Articles 13 (transparency) & 14 (human oversight).")
    ]
    for sym, dom, desc in glossary_rows:
        lines.append(f"| **{sym}** | {dom} | {desc} |")
    lines.append("")

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Markdown written: {MD_PATH}")


# ===========================================================================
# 2. DOCX GENERATION
# ===========================================================================
def generate_docx():
    print(f"Building Word document at {DOCX_PATH}...")
    doc = docx.Document()

    # Configure Page Geometry (US Letter 8.5 x 11 in, 0.75 in margins => 7.0 in width)
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        r_h = p_head.add_run("ICMLDE 2026 (Paper ID: 857) · C-XAI Slide-by-Slide Technical Reference")
        r_h.font.name = "Arial"
        r_h.font.size = Pt(8.0)
        r_h.font.color.rgb = COLOR_MUTED

        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        r_f = p_foot.add_run("Amrita School of Computing, Amrita Vishwa Vidyapeetham · Department of Computer Science & Engineering")
        r_f.font.name = "Arial"
        r_f.font.size = Pt(8.0)
        r_f.font.color.rgb = COLOR_MUTED

    # Title Block
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("C-XAI: Slide-by-Slide Technical Reference Document")
    r_t.font.name = "Arial"
    r_t.font.size = Pt(16.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(5)
    r_s = p_sub.add_run("5th Elsevier International Conference on Machine Learning and Data Engineering (ICMLDE 2026)\nProcedia Computer Science · Paper ID: 857 · Technical Session")
    r_s.font.name = "Arial"
    r_s.font.size = Pt(10.0)
    r_s.font.italic = True
    r_s.font.color.rgb = COLOR_SECONDARY

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(10)
    p_meta.paragraph_format.line_spacing = 1.15
    add_bottom_border(p_meta, hex_color=HEX_PRIMARY, sz="12")
    r_m = p_meta.add_run(
        "Presenting Author: Sheela Akshar Sakhi (aksharsakhi@gmail.com)\n"
        "Co-Authors: Ibbraheem Shaik, Settibattini Suhitha, Dr. Ramya G R* (Corresponding Author: gr_ramya@cb.amrita.edu)\n"
        "Affiliation: Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore, India\n"
        "Public Repository: https://github.com/aksharsakhi/c-xai-healthcare-predictions"
    )
    r_m.font.name = "Arial"
    r_m.font.size = Pt(8.5)
    r_m.font.color.rgb = COLOR_MUTED

    # Executive Benchmark Summary
    h_exec = doc.add_heading("Executive Summary: Benchmark Metrics & Core Formulations", level=1)
    h_exec.paragraph_format.space_before = Pt(6)
    h_exec.paragraph_format.space_after = Pt(4)
    h_exec.paragraph_format.keep_with_next = True
    for r in h_exec.runs:
        r.font.name = "Arial"
        r.font.size = Pt(12.0)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY

    table_stats = [
        ("Metric / Dimension", "Reported Empirical Value", "Cohort & Statistical Interpretation"),
        ("Total Records Audited", "51,369 encounters", "MIMIC-IV (40,000), eICU (10,000), BCWD (569), Cardio EHR (800)"),
        ("Clinical Decision Utility", "+19.6% relative (+13.9% abs)", "Extra Trees (0.8485) vs. Tabular Deep ResNet (0.7095–0.7107) on MIMIC-IV"),
        ("Statistical Significance", "p < 0.001, W = 0.0, d = 2.96", "Wilcoxon W = 0.0 (50/50 wins), paired t = 14.82, Cohen's d = 2.96"),
        ("Explanation Instability", "9.6× higher in Deep ResNet", "Deep ResNet Ŝ<sub>Lip</sub> = 0.4912 vs. Extra Trees 0.0512 (h = 0.05)"),
        ("Explainer Discordance", "7.4× higher in Deep ResNet", "Deep ResNet D<sub>XAI</sub> = 0.435 vs. Extra Trees 0.059 (94.1% rank consensus)"),
        ("Accuracy Decoupling", "R² = 0.04 across cohorts", "AUROC explains less than 4% of clinical utility variance (p = 0.42)"),
        ("Calibration Error (ECE)", "0.015 vs. 0.055", "Extra Trees calibration error is 3.7× lower than Tabular Deep ResNet"),
        ("Inference Latency", "4.2 ms vs. 48.5 ms", "Extra Trees scoring is 11.5× faster than Deep ResNet per encounter")
    ]

    col_widths_dxa = [2592, 3024, 4464]  # 1.8 in + 2.1 in + 3.1 in = 7.0 in (10080 dxa)
    tbl = doc.add_table(rows=len(table_stats), cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_fixed_width(tbl, PRINTABLE_WIDTH_DXA, col_widths_dxa)

    for r_idx, row in enumerate(table_stats):
        is_header = (r_idx == 0)
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            set_cell_margins(cell, top=65, bottom=65, left=95, right=95)
            if is_header:
                set_cell_background(cell, HEX_PRIMARY)
            else:
                set_cell_background(cell, HEX_ROW_ALT if r_idx % 2 == 1 else "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            if is_header:
                add_rich_runs(p, val, font_size=Pt(8.5), color=RGBColor(255, 255, 255), bold=True)
            elif c_idx == 1:
                add_rich_runs(p, val, font_size=Pt(8.5), color=COLOR_PRIMARY, bold=True)
            else:
                add_rich_runs(p, val, font_size=Pt(8.5), color=COLOR_DARK)

    # Core Mathematical Formulations
    h_math = doc.add_heading("Core C-XAI Mathematical Formulations", level=2)
    h_math.paragraph_format.space_before = Pt(10)
    h_math.paragraph_format.space_after = Pt(4)
    h_math.paragraph_format.keep_with_next = True
    for r in h_math.runs:
        r.font.name = "Arial"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_SECONDARY

    formulas = [
        ("1. Local Lipschitz Explanation Stability (Ŝ<sub>Lip</sub>)",
         "Ŝ<sub>Lip</sub>(x; f, E, h) = (1 / M) ∑<sub>m=1</sub><sup>M</sup> [ ‖E<sub>f</sub>(x + δ<sub>m</sub>) − E<sub>f</sub>(x)‖<sub>2</sub> / (‖δ<sub>m</sub>‖<sub>2</sub> + δ<sub>0</sub>) ]",
         "where δ<sub>m</sub> ∼ N(0, h²I), M = 100 Monte Carlo draws, h = 0.05 physiological noise radius, δ<sub>0</sub> = 10⁻⁸."),
        ("2. Cross-Explainer Discordance (D<sub>XAI</sub>)",
         "D<sub>XAI</sub>(x; f) = 1 − [ 2 / K(K − 1) ] ∑<sub>j < k</sub> r<sub>s</sub>(E<sub>j</sub>(x), E<sub>k</sub>(x)) ∈ [0, 2]",
         "where r<sub>s</sub> is pairwise Spearman rank correlation across K = 6 post-hoc explainers."),
        ("3. Dimension-Normalized Clinical Prior Alignment (W<sub>Clin</sub><sup>norm</sup>)",
         "W<sub>Clin</sub><sup>norm</sup>(x) = W<sub>1</sub>(E<sub>norm</sub>(x), P<sub>clin</sub>) / (d − 1) ∈ [0, 1],    A<sub>Clin</sub> = 1 − W<sub>Clin</sub><sup>norm</sup>",
         "where W<sub>1</sub> is 1D Wasserstein (Earth Mover's) distance over d ordered clinical prior features."),
        ("4. Trust Factor & Net Clinical Decision Utility (T<sub>Clin</sub>, Û<sub>Clin</sub>)",
         "T<sub>Clin</sub> = (1 / 3) [ 1 / (1 + Ŝ<sub>Lip</sub>) + A<sub>Clin</sub> + (1 − ECE) ],    Û<sub>Clin</sub> = Acc · T<sub>Clin</sub> − (α · OR + β · UR)",
         "where OR = (1 − Acc)(1 − 0.4 T<sub>Clin</sub>), UR = Acc(1 − T<sub>Clin</sub>)(0.3), α = 0.50 (over-reliance), β = 0.30 (under-reliance).")
    ]
    add_formula_box(doc, formulas)

    # Slide-by-Slide Reference Sections
    for s in SLIDES_DATA:
        s_num = s["slide_num"]
        s_title = s["title"]

        h1 = doc.add_heading(f"Slide {s_num}: {s_title}", level=1)
        h1.paragraph_format.space_before = Pt(12)
        h1.paragraph_format.space_after = Pt(4)
        h1.paragraph_format.keep_with_next = True
        add_bottom_border(h1, hex_color=HEX_RULE, sz="6")
        for r in h1.runs:
            r.font.name = "Arial"
            r.font.size = Pt(12.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_PRIMARY

        # Overview
        p_ov = doc.add_paragraph()
        p_ov.paragraph_format.space_before = Pt(2)
        p_ov.paragraph_format.space_after = Pt(4)
        p_ov.paragraph_format.line_spacing = 1.15
        p_ov.paragraph_format.widow_control = True
        add_rich_runs(p_ov, "<b>Overview:</b> ", font_size=Pt(8.8), color=COLOR_SECONDARY)
        add_rich_runs(p_ov, s["overview"], font_size=Pt(8.8), color=COLOR_DARK, italic=True)

        # Terminology & Definitions
        h2_terms = doc.add_heading("Key Terminology & Definitions", level=2)
        h2_terms.paragraph_format.space_before = Pt(5)
        h2_terms.paragraph_format.space_after = Pt(2)
        h2_terms.paragraph_format.keep_with_next = True
        for r in h2_terms.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.8)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY

        for term, definition in s["terminology"]:
            p_b = doc.add_paragraph(style='List Bullet')
            p_b.paragraph_format.space_before = Pt(0)
            p_b.paragraph_format.space_after = Pt(2)
            p_b.paragraph_format.line_spacing = 1.15
            p_b.paragraph_format.widow_control = True
            add_rich_runs(p_b, f"<b>{term}:</b> {definition}", font_size=Pt(8.6), color=COLOR_DARK)

        # Mathematical Formulations & Technical Details
        h2_tech = doc.add_heading("Mathematical Formulations & Technical Details", level=2)
        h2_tech.paragraph_format.space_before = Pt(5)
        h2_tech.paragraph_format.space_after = Pt(2)
        h2_tech.paragraph_format.keep_with_next = True
        for r in h2_tech.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.8)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY

        for head, details in s["mechanics"]:
            p_t = doc.add_paragraph(style='List Bullet')
            p_t.paragraph_format.space_before = Pt(0)
            p_t.paragraph_format.space_after = Pt(2)
            p_t.paragraph_format.line_spacing = 1.15
            p_t.paragraph_format.widow_control = True
            add_rich_runs(p_t, f"<b>{head}:</b> ", font_size=Pt(8.6), color=COLOR_PRIMARY)
            add_rich_runs(p_t, details, font_size=Pt(8.6), color=COLOR_DARK)

        # Clinical & Regulatory Context
        h2_clin = doc.add_heading("Clinical & Regulatory Context", level=2)
        h2_clin.paragraph_format.space_before = Pt(5)
        h2_clin.paragraph_format.space_after = Pt(2)
        h2_clin.paragraph_format.keep_with_next = True
        for r in h2_clin.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.8)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY

        for head, details in s["clinical_context"]:
            p_c = doc.add_paragraph(style='List Bullet')
            p_c.paragraph_format.space_before = Pt(0)
            p_c.paragraph_format.space_after = Pt(2)
            p_c.paragraph_format.line_spacing = 1.15
            p_c.paragraph_format.widow_control = True
            add_rich_runs(p_c, f"<b>{head}:</b> ", font_size=Pt(8.6), color=COLOR_TEAL)
            add_rich_runs(p_c, details, font_size=Pt(8.6), color=COLOR_DARK)

        # Methodological Rationales & Technical Notes
        h2_rat = doc.add_heading("Methodological Rationales & Technical Notes", level=2)
        h2_rat.paragraph_format.space_before = Pt(5)
        h2_rat.paragraph_format.space_after = Pt(3)
        h2_rat.paragraph_format.keep_with_next = True
        for r in h2_rat.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.8)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY

        add_rationale_box(doc, s["rationales"])

    # Appendix: Quick-Lookup Glossary Table
    h_app = doc.add_heading("Appendix: Quick-Lookup Glossary of Symbols, Acronyms & Specialized Terms", level=1)
    h_app.paragraph_format.space_before = Pt(12)
    h_app.paragraph_format.space_after = Pt(4)
    h_app.paragraph_format.keep_with_next = True
    add_bottom_border(h_app, hex_color=HEX_RULE, sz="6")
    for r in h_app.runs:
        r.font.name = "Arial"
        r.font.size = Pt(12.0)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY

    glossary_table = [
        ("Symbol / Term", "Category", "Definition & Technical Meaning"),
        ("Ŝ<sub>Lip</sub>", "Stability Metric", "Empirical Local Lipschitz Stability Index measuring attribution sensitivity under Gaussian noise (h = 0.05, M = 100). Lower is more stable."),
        ("D<sub>XAI</sub>", "Discordance Metric", "Cross-Explainer Discordance (1 − r<sub>s</sub>) ∈ [0, 2]; quantifies rank-order conflict across competing post-hoc explainers. Lower is better."),
        ("W<sub>Clin</sub><sup>norm</sup> / A<sub>Clin</sub>", "Clinical Alignment", "Dimension-normalized 1D Wasserstein distance to medical priors ∈ [0, 1]; Alignment A<sub>Clin</sub> = 1 − W<sub>Clin</sub><sup>norm</sup>."),
        ("T<sub>Clin</sub> / Û<sub>Clin</sub>", "Decision Utility", "Clinician Trust Calibration Factor T<sub>Clin</sub> and Net Calibrated Clinical Decision Utility Û<sub>Clin</sub> combining accuracy and reliance loss."),
        ("ECE / Brier Score", "Calibration", "Expected Calibration Error and mean squared probability error measuring how faithfully predicted risks match observed outcomes."),
        ("OR / UR (α = 0.50, β = 0.30)", "Decision Theory", "Over-Reliance (following false predictions; penalty α = 0.50) and Under-Reliance (dismissing true alerts; penalty β = 0.30)."),
        ("r<sub>s</sub> / R²", "Statistics", "Spearman rank correlation ∈ [−1, +1] across feature ranks; R² is variance explained in OLS regression (R² = 0.04 decoupling)."),
        ("W = 0.0 / t = 14.82 / d = 2.96", "Hypothesis Tests", "Wilcoxon signed-rank statistic (0.0 = 50/50 wins), paired t-statistic, and Cohen's d standardized effect size (> 0.8 = large)."),
        ("SOFA / Sepsis-3", "Clinical ICU", "Sequential Organ Failure Assessment (0–24) and consensus criteria defining acute sepsis organ dysfunction."),
        ("MAP / Lactate / WBC / Creatinine", "Clinical Biomarkers", "Mean Arterial Pressure (perfusion), Serum Lactate (hypoxia), White Blood Cell count (infection), Creatinine (kidney function)."),
        ("NPI / ASCVD", "Oncology / Cardio", "Nottingham Prognostic Index (breast pathology) and ACC/AHA 10-year Atherosclerotic Cardiovascular Disease risk score."),
        ("MCAR", "Missing Data", "Missing Completely At Random: missing values independent of observed or unobserved patient states (20% stress-test)."),
        ("TreeSHAP / KernelSHAP / LIME", "XAI Explainers", "Game-theoretic Shapley attribution (tree-exact vs. kernel-approximated) and local sparse linear surrogate explainer."),
        ("IG / SmoothGrad / PFI", "XAI Explainers", "Integrated Gradients (path integral from survivor median), SmoothGrad (noisy gradient averaging), Permutation Feature Importance."),
        ("Zeroth-Order Smoother", "Optimization", "Gaussian convolution + Stein's lemma score estimator enabling gradient attribution on discontinuous tree step functions."),
        ("FGSM / ScaL-PGD", "Adversarial ML", "Fast Gradient Sign Method and Scaled Projected Gradient Descent attacks distorting explanations while preserving predictions."),
        ("SENN / Captum / OpenXAI / Quantus", "Prior Toolkits", "Self-Explaining Neural Networks and existing vision/NLP/synthetic XAI libraries lacking clinical guideline utility models."),
        ("FDA SaMD / GMLP / EU AI Act", "Governance", "Software as a Medical Device, Good Machine Learning Practice Principle 7, and EU AI Act Articles 13 (transparency) & 14 (oversight).")
    ]

    g_widths_dxa = [2304, 1584, 6192]  # 1.6 + 1.1 + 4.3 = 7.0 in
    g_tbl = doc.add_table(rows=len(glossary_table), cols=3)
    g_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    g_tbl.autofit = False
    set_table_fixed_width(g_tbl, PRINTABLE_WIDTH_DXA, g_widths_dxa)
    g_tbl.rows[0]._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    for r_idx, row in enumerate(glossary_table):
        is_header = (r_idx == 0)
        for c_idx, val in enumerate(row):
            cell = g_tbl.cell(r_idx, c_idx)
            set_cell_margins(cell, top=55, bottom=55, left=85, right=85)
            if is_header:
                set_cell_background(cell, HEX_PRIMARY)
            else:
                set_cell_background(cell, HEX_ROW_ALT if r_idx % 2 == 1 else "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            if is_header:
                add_rich_runs(p, val, font_size=Pt(8.3), color=RGBColor(255, 255, 255), bold=True)
            elif c_idx == 0:
                add_rich_runs(p, val, font_size=Pt(8.2), color=COLOR_PRIMARY, bold=True)
            elif c_idx == 1:
                add_rich_runs(p, val, font_size=Pt(8.2), color=COLOR_TEAL, bold=True)
            else:
                add_rich_runs(p, val, font_size=Pt(8.2), color=COLOR_DARK)

    doc.save(DOCX_PATH)
    print(f"DOCX written: {DOCX_PATH}")


# ===========================================================================
# 3. PDF CONVERSION
# ===========================================================================
def convert_to_pdf():
    print(f"Converting {DOCX_PATH} to PDF via LibreOffice...")
    cmd = [
        "soffice",
        "--headless",
        "--convert-to", "pdf",
        DOCX_PATH,
        "--outdir", OUTPUT_DIR
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and os.path.exists(PDF_PATH):
        print(f"PDF compiled: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
    else:
        raise RuntimeError(f"LibreOffice conversion failed: {res.stderr}\n{res.stdout}")


if __name__ == "__main__":
    generate_markdown()
    generate_docx()
    convert_to_pdf()
