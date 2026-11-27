#!/usr/bin/env python3
"""
build_defense_document.py
=========================
Builds the complete slide-by-slide technical reference & defense guide
in Markdown, DOCX, and PDF formats for ICMLDE 2026 Paper ID: 857.
"""

import os
import sys
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sys.path.append(os.path.dirname(__file__))
from slide_defense_data import SLIDES_DATA

OUTPUT_DIR = "CONF_PRESENTATION/SUBMISSION_READY"
os.makedirs(OUTPUT_DIR, exist_ok=True)
MD_PATH = os.path.join(OUTPUT_DIR, "ICMLDE-2026-857_Slide_by_Slide_Defense_Guide.md")
DOCX_PATH = os.path.join(OUTPUT_DIR, "ICMLDE-2026-857_Slide_by_Slide_Defense_Guide.docx")
PDF_PATH = os.path.join(OUTPUT_DIR, "ICMLDE-2026-857_Slide_by_Slide_Defense_Guide.pdf")

# Styling Constants
COLOR_PRIMARY = RGBColor(27, 54, 93)      # #1B365D Deep Navy
COLOR_SECONDARY = RGBColor(51, 102, 153)  # #336699 Slate Blue
COLOR_DARK = RGBColor(34, 34, 34)         # #222222 Charcoal
COLOR_MUTED = RGBColor(89, 89, 89)        # #595959 Grey
COLOR_GREEN = RGBColor(30, 126, 52)       # #1E7E34 Emerald
COLOR_AMBER = RGBColor(180, 83, 9)        # #B45309 Warm Amber

HEX_PRIMARY = "1B365D"
HEX_SECONDARY = "336699"
HEX_LIGHT_BG = "F4F6F9"
HEX_CALLOUT_BG = "EBF3FA"
HEX_BORDER = "B0C4DE"

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def add_callout(doc, question, answer):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{HEX_PRIMARY}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run_q = p.add_run(f"❓ DEFENSE QUESTION: {question}\n")
    run_q.font.name = "Arial"
    run_q.font.size = Pt(9.5)
    run_q.font.bold = True
    run_q.font.color.rgb = COLOR_PRIMARY
    
    run_lbl = p.add_run("🎯 SAY EXACTLY THIS:\n")
    run_lbl.font.name = "Arial"
    run_lbl.font.size = Pt(8.5)
    run_lbl.font.bold = True
    run_lbl.font.color.rgb = COLOR_AMBER
    
    run_a = p.add_run(answer)
    run_a.font.name = "Arial"
    run_a.font.size = Pt(9.0)
    run_a.font.color.rgb = COLOR_DARK
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)


# ===========================================================================
# 1. GENERATE MARKDOWN GUIDE
# ===========================================================================
def generate_markdown():
    print(f"Writing Markdown guide to {MD_PATH}...")
    lines = []
    
    lines.append("# C-XAI: Master Slide-by-Slide Technical Reference & Conference Defense Guide")
    lines.append("### 5th Elsevier International Conference on Machine Learning and Data Engineering (ICMLDE 2026)")
    lines.append("**Paper ID: 857** · Procedia Computer Science · Dehradun, India\n")
    lines.append("> **Presenter**: Sheela Akshar Sakhi¹ (`aksharsakhi@gmail.com`)  ")
    lines.append("> **Co-Authors**: Ibbraheem Shaik¹, Settibattini Suhitha¹, Dr. Ramya G. R.²* (Supervisor & Corresponding Author: `gr_ramya@cb.amrita.edu`)  ")
    lines.append("> **Affiliation**: Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore, Tamil Nadu, India  ")
    lines.append("> **Public Repository**: [github.com/aksharsakhi/c-xai-healthcare-predictions](https://github.com/aksharsakhi/c-xai-healthcare-predictions)\n")
    lines.append("---\n")
    
    # Executive Cheat Sheet Section
    lines.append("## ⚡ Executive Defense Cheat Sheet: Vital Numbers & Formulations to Know Cold\n")
    lines.append("If you get asked any sudden numbers, consult this instant reference table:\n")
    lines.append("| Metric / Parameter | Value to State | Clinical / Mathematical Meaning |")
    lines.append("|:---|:---|:---|")
    lines.append("| **Total Records Audited** | **51,369 encounters** | MIMIC-IV (40k), eICU (10k), BCWD (569), Cardio EHR (800) |")
    lines.append("| **Clinical Utility Gain** | **+19.6% relative (+13.9% abs)** | Extra Trees ($0.849$) vs. Tabular Deep ResNet ($0.711$) on MIMIC-IV |")
    lines.append("| **Statistical Significance** | **p < 0.001, W = 0.0, d = 2.96** | Wilcoxon signed-rank $W=0.0$ (50/50 wins), Paired $t=14.82$, Cohen's $d=2.96$ |")
    lines.append("| **Explanation Instability** | **9.6× worse in Deep Nets** | ResNet $\\widehat{\\mathcal{S}}_{\\text{Lip}} = 0.4912$ vs. Extra Trees $0.0512$ under $h=0.05$ |")
    lines.append("| **Explainer Discordance** | **7.4× higher in Deep Nets** | ResNet $\\mathcal{D}_{\\text{XAI}} = 0.435$ vs. Extra Trees $0.059$ (94.1% consensus) |")
    lines.append("| **Accuracy Decoupling** | **R² = 0.04 across cohorts** | Linear regression between AUROC and Utility proves zero predictive correlation |")
    lines.append("| **Sensor Noise Radius** | **h = 0.05 (Gaussian)** | 5% standard deviation drift, matching routine ICU telemetry fluctuation |")
    lines.append("| **Reliance Error Weights** | **α = 0.50, β = 0.30** | Asymmetric decision penalties: Over-reliance (fatal omission) > Under-reliance |")
    lines.append("| **Inference Latency** | **4.2 ms vs. 48.5 ms** | Extra Trees is 11.5× faster than Tabular Deep ResNet in real-time scoring |\n")
    
    lines.append("### 📐 The 4 Core C-XAI Mathematical Formulas\n")
    lines.append("1. **Local Lipschitz Explanation Stability ($\\widehat{\\mathcal{S}}_{\\text{Lip}}$)**:")
    lines.append("   $$\\widehat{\\mathcal{S}}_{\\text{Lip}}(x; f, \\mathcal{E}, h) = \\frac{1}{M} \\sum_{m=1}^M \\frac{\\|\\mathcal{E}_f(x + \\delta_m) - \\mathcal{E}_f(x)\\|_2}{\\|\\delta_m\\|_2 + \\epsilon_0}, \\quad \\delta_m \\sim \\mathcal{N}(0, h^2 I), \\quad M = 100, \\; h = 0.05$$")
    lines.append("2. **Cross-Explainer Discordance ($\\mathcal{D}_{\\text{XAI}}$)**:")
    lines.append("   $$\\mathcal{D}_{\\text{XAI}}(x; f) = 1 - \\frac{2}{K(K - 1)} \\sum_{j < k} r_s(\\mathcal{E}_j(x), \\mathcal{E}_k(x)) \\in [0, 2], \\quad K = 6 \\text{ explainers}$$")
    lines.append("3. **Dimension-Normalized Clinical Prior Alignment ($\\mathcal{W}_{\\text{Clin}}^{\\text{norm}}$)**:")
    lines.append("   $$\\mathcal{W}_{\\text{Clin}}^{\\text{norm}}(x) = \\frac{\\mathcal{W}_1(\\mathcal{E}_{\\text{norm}}(x), P_{\\text{clin}})}{d - 1} = \\frac{1}{d - 1} \\sum_{j=1}^{d-1} |F_{\\mathcal{E}}(j) - F_{\\text{clin}}(j)| \\in [0, 1]$$")
    lines.append("4. **Calibrated In-Silico Clinical Utility ($\\widehat{\\mathcal{U}}_{\\text{Clin}}$)**:")
    lines.append("   $$\\widehat{\\mathcal{U}}_{\\text{Clin}} = w_s (1 - \\widehat{\\mathcal{S}}_{\\text{Lip}}) + w_d (1 - \\mathcal{D}_{\\text{XAI}}) + w_p (1 - \\mathcal{W}_{\\text{Clin}}^{\\text{norm}}) + w_c (1 - \\text{Loss}_{\\text{rel}})$$")
    lines.append("   *Weights*: $w_s = 0.30$, $w_d = 0.25$, $w_p = 0.25$, $w_c = 0.20$.\n")
    lines.append("---\n")
    
    # Slide by Slide Walkthrough
    for s in SLIDES_DATA:
        s_num = s["slide_num"]
        s_title = s["title"]
        lines.append(f"## Slide {s_num}: {s_title}\n")
        lines.append(f"**Core Message for Presenter**: *{s['core_message']}*\n")
        
        lines.append("### 🔑 Key Concepts, Acronyms & Terminology Explained")
        for term, definition in s["key_terms"]:
            lines.append(f"- **{term}**: {definition}")
        lines.append("")
        
        lines.append("### ⚙️ Deep Technical & Mathematical Mechanics")
        for head, details in s["technical_mechanics"]:
            lines.append(f"- **{head}**:")
            for sub in details.split("\n"):
                lines.append(f"  {sub}")
        lines.append("")
        
        lines.append("### 🏥 Clinical Context & Real-World Decision Impact")
        for head, details in s["clinical_relevance"]:
            lines.append(f"- **{head}**: {details}")
        lines.append("")
        
        lines.append("### 🎯 Tough Examiner/Reviewer Questions & Instant Defense Answers")
        for q, a in s["tough_questions"]:
            lines.append(f"> **❓ Question: {q}**  ")
            lines.append(f"> **🎯 Say Exactly This**: {a}\n")
        
        lines.append("---\n")
    
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Markdown guide written successfully: {MD_PATH}")


# ===========================================================================
# 2. GENERATE STYLED DOCX GUIDE
# ===========================================================================
def generate_docx():
    print(f"Building styled Word document at {DOCX_PATH}...")
    doc = docx.Document()
    
    # Set standard 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Document Title Block
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("C-XAI: Master Slide-by-Slide Technical Reference & Conference Defense Guide")
    r_t.font.name = "Arial"
    r_t.font.size = Pt(18)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_s = p_sub.add_run("5th Elsevier International Conference on Machine Learning and Data Engineering (ICMLDE 2026)\nProcedia Computer Science · Paper ID: 857 · Technical Session Presentation")
    r_s.font.name = "Arial"
    r_s.font.size = Pt(11)
    r_s.font.italic = True
    r_s.font.color.rgb = COLOR_SECONDARY
    
    # Metadata Block
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(12)
    p_meta.paragraph_format.line_spacing = 1.15
    r_m = p_meta.add_run(
        "Presenter: Sheela Akshar Sakhi (aksharsakhi@gmail.com)\n"
        "Authors: Sheela Akshar Sakhi, Ibbraheem Shaik, Settibattini Suhitha, Dr. Ramya G. R.* (Supervisor: gr_ramya@cb.amrita.edu)\n"
        "Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, India\n"
        "Public Code Repository: https://github.com/aksharsakhi/c-xai-healthcare-predictions"
    )
    r_m.font.name = "Arial"
    r_m.font.size = Pt(9)
    r_m.font.color.rgb = COLOR_MUTED
    
    # Executive Cheat Sheet Section
    h_exec = doc.add_heading("⚡ Executive Defense Cheat Sheet: Vital Numbers to Know Cold", level=1)
    h_exec.paragraph_format.space_before = Pt(14)
    h_exec.paragraph_format.space_after = Pt(6)
    for r in h_exec.runs:
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        
    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_after = Pt(4)
    r_d = p_desc.add_run("Keep these exact empirical numbers and formulas in mind for instant, authoritative responses to judges:")
    r_d.font.name = "Arial"
    r_d.font.size = Pt(9.5)
    r_d.font.italic = True
    
    # Summary Stats Table
    table_stats = [
        ("Metric / Dimension", "Exact Value", "Scientific / Clinical Interpretation"),
        ("Total Clinical Records", "51,369 encounters", "MIMIC-IV (40k, ICU Sepsis), eICU (10k, multi-center), BCWD (569), Cardio EHR (800)"),
        ("Clinical Decision Utility", "+19.6% relative (+13.9% abs)", "Extra Trees (0.849) vs. Tabular Deep ResNet (0.711) on MIMIC-IV"),
        ("Statistical Significance", "p < 0.001, W = 0.0, d = 2.96", "Wilcoxon W=0.0 (50/50 wins across seeds), Paired t=14.82, Cohen's d=2.96 (huge effect)"),
        ("Explanation Instability", "9.6× higher in Deep Nets", "ResNet SbLip = 0.4912 vs. Extra Trees 0.0512 under physiological noise (h = 0.05)"),
        ("Explainer Discordance", "7.4× higher in Deep Nets", "ResNet DXAI = 0.435 vs. Extra Trees 0.059 (94.1% consensus across SHAP, LIME, IG)"),
        ("Accuracy Decoupling", "R² = 0.04 across cohorts", "Linear regression shows AUROC has zero correlation with explanation reliability"),
        ("Inference Latency", "4.2 ms vs. 48.5 ms", "Extra Trees is 11.5× faster than Tabular Deep ResNet in real-time bedside triage")
    ]
    
    tbl = doc.add_table(rows=len(table_stats), cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(1.8)
    tbl.columns[1].width = Inches(2.0)
    tbl.columns[2].width = Inches(2.7)
    
    for r_idx, row in enumerate(table_stats):
        is_header = (r_idx == 0)
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            if is_header:
                set_cell_background(cell, HEX_PRIMARY)
            else:
                set_cell_background(cell, HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF")
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(8.5)
            if is_header:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 1:
                run.font.bold = True
                run.font.color.rgb = COLOR_PRIMARY
            else:
                run.font.color.rgb = COLOR_DARK
                
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(6)

    # Walkthrough each slide
    for s in SLIDES_DATA:
        s_num = s["slide_num"]
        s_title = s["title"]
        
        # Slide Heading
        h1 = doc.add_heading(f"Slide {s_num}: {s_title}", level=1)
        h1.paragraph_format.space_before = Pt(16)
        h1.paragraph_format.space_after = Pt(4)
        h1.paragraph_format.keep_with_next = True
        for r in h1.runs:
            r.font.name = "Arial"
            r.font.size = Pt(13.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_PRIMARY
            
        # Core Message
        p_core = doc.add_paragraph()
        p_core.paragraph_format.space_after = Pt(6)
        p_core.paragraph_format.line_spacing = 1.15
        r_cm_lbl = p_core.add_run("📢 PUNCHY CORE MESSAGE: ")
        r_cm_lbl.font.name = "Arial"
        r_cm_lbl.font.size = Pt(9.5)
        r_cm_lbl.font.bold = True
        r_cm_lbl.font.color.rgb = COLOR_SECONDARY
        r_cm_txt = p_core.add_run(s["core_message"])
        r_cm_txt.font.name = "Arial"
        r_cm_txt.font.size = Pt(9.5)
        r_cm_txt.font.italic = True
        r_cm_txt.font.color.rgb = COLOR_DARK
        
        # Key Terms
        h2_terms = doc.add_heading("Key Concepts, Acronyms & Terminology", level=2)
        h2_terms.paragraph_format.space_before = Pt(8)
        h2_terms.paragraph_format.space_after = Pt(3)
        h2_terms.paragraph_format.keep_with_next = True
        for r in h2_terms.runs:
            r.font.name = "Arial"
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY
            
        for term, definition in s["key_terms"]:
            p_b = doc.add_paragraph(style='List Bullet')
            p_b.paragraph_format.space_after = Pt(2)
            p_b.paragraph_format.line_spacing = 1.15
            r_t = p_b.add_run(f"{term}: ")
            r_t.font.name = "Arial"
            r_t.font.size = Pt(9.0)
            r_t.font.bold = True
            r_t.font.color.rgb = COLOR_DARK
            r_d = p_b.add_run(definition)
            r_d.font.name = "Arial"
            r_d.font.size = Pt(9.0)
            r_d.font.color.rgb = COLOR_DARK
            
        # Technical Mechanics
        h2_tech = doc.add_heading("Deep Technical & Mathematical Mechanics", level=2)
        h2_tech.paragraph_format.space_before = Pt(8)
        h2_tech.paragraph_format.space_after = Pt(3)
        h2_tech.paragraph_format.keep_with_next = True
        for r in h2_tech.runs:
            r.font.name = "Arial"
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY
            
        for head, details in s["technical_mechanics"]:
            p_t = doc.add_paragraph(style='List Bullet')
            p_t.paragraph_format.space_after = Pt(2)
            p_t.paragraph_format.line_spacing = 1.15
            r_h = p_t.add_run(f"{head}: ")
            r_h.font.name = "Arial"
            r_h.font.size = Pt(9.0)
            r_h.font.bold = True
            r_h.font.color.rgb = COLOR_PRIMARY
            r_det = p_t.add_run(details)
            r_det.font.name = "Arial"
            r_det.font.size = Pt(9.0)
            r_det.font.color.rgb = COLOR_DARK
            
        # Clinical Relevance
        h2_clin = doc.add_heading("Clinical Context & Real-World Impact", level=2)
        h2_clin.paragraph_format.space_before = Pt(8)
        h2_clin.paragraph_format.space_after = Pt(3)
        h2_clin.paragraph_format.keep_with_next = True
        for r in h2_clin.runs:
            r.font.name = "Arial"
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY
            
        for head, details in s["clinical_relevance"]:
            p_c = doc.add_paragraph(style='List Bullet')
            p_c.paragraph_format.space_after = Pt(2)
            p_c.paragraph_format.line_spacing = 1.15
            r_ch = p_c.add_run(f"{head}: ")
            r_ch.font.name = "Arial"
            r_ch.font.size = Pt(9.0)
            r_ch.font.bold = True
            r_ch.font.color.rgb = COLOR_GREEN
            r_cd = p_c.add_run(details)
            r_cd.font.name = "Arial"
            r_cd.font.size = Pt(9.0)
            r_cd.font.color.rgb = COLOR_DARK
            
        # Tough Questions
        h2_q = doc.add_heading("Tough Reviewer / Audience Questions & Defense Answers", level=2)
        h2_q.paragraph_format.space_before = Pt(8)
        h2_q.paragraph_format.space_after = Pt(4)
        h2_q.paragraph_format.keep_with_next = True
        for r in h2_q.runs:
            r.font.name = "Arial"
            r.font.size = Pt(10.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_SECONDARY
            
        for q, a in s["tough_questions"]:
            add_callout(doc, q, a)
            
    doc.save(DOCX_PATH)
    print(f"Word document generated successfully: {DOCX_PATH}")


# ===========================================================================
# 3. CONVERT DOCX TO PDF VIA LIBREOFFICE
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
        print(f"PDF compiled successfully: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
    else:
        print(f"PDF conversion warning/error: {res.stderr}\n{res.stdout}")


if __name__ == "__main__":
    generate_markdown()
    generate_docx()
