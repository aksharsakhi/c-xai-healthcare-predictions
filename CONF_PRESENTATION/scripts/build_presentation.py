import os
import shutil
import pptx
from pptx.util import Pt, Inches
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml import parse_xml
from pptx.chart.data import CategoryChartData

def create_presentation():
    src_template = "CONF_PRESENTATION/templates/ICMLDE_2026_Paper_Presentation_Template_ORIGINAL_BACKUP.pptx"
    prs = pptx.Presentation(src_template)

    # =========================================================================
    # 0. UPDATE MASTER & LAYOUT FOOTERS ACROSS ENTIRE PRESENTATION
    # =========================================================================
    for layout in prs.slide_layouts:
        for s in layout.shapes:
            if s.has_text_frame and ("ICMLDE-2026-XXX" in s.text_frame.text or "Akshar_ICMLDE2026" in s.text_frame.text):
                for p in s.text_frame.paragraphs:
                    p.text = p.text.replace("ICMLDE-2026-XXX", "857").replace("Akshar_ICMLDE2026", "857")
    for master in prs.slide_masters:
        for s in master.shapes:
            if s.has_text_frame and ("ICMLDE-2026-XXX" in s.text_frame.text or "Akshar_ICMLDE2026" in s.text_frame.text):
                for p in s.text_frame.paragraphs:
                    p.text = p.text.replace("ICMLDE-2026-XXX", "857").replace("Akshar_ICMLDE2026", "857")

    # =========================================================================
    # HELPER FUNCTIONS
    # =========================================================================
    def get_shape_by_name(slide, name):
        for s in slide.shapes:
            if s.name == name:
                return s
        return None

    def remove_shape_by_name(slide, name):
        s = get_shape_by_name(slide, name)
        if s is not None:
            el = s._element
            el.getparent().remove(el)

    def clear_paragraph_bullets_and_indents(p):
        pPr = p._p.get_or_add_pPr()
        for child in list(pPr):
            tag = child.tag.split("}")[-1]
            if tag.startswith("bu"):
                pPr.remove(child)
        pPr.insert(0, parse_xml('<a:buNone xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
        pPr.set('marL', '0')
        pPr.set('indent', '0')

    def set_shape_text(shape, paragraphs_data, align=PP_ALIGN.LEFT, default_space_after=4):
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True

        for i, p_data in enumerate(paragraphs_data):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.level = 0
            clear_paragraph_bullets_and_indents(p)

            if isinstance(p_data, tuple):
                text, size, bold, color, space_after = p_data
                p.space_after = Pt(space_after if space_after is not None else default_space_after)
                run = p.add_run()
                run.text = text
                run.font.name = "Times New Roman"
                run.font.size = Pt(size)
                run.font.bold = bold
                if isinstance(color, RGBColor):
                    run.font.color.rgb = color
                elif color is not None:
                    run.font.color.theme_color = color
            elif isinstance(p_data, list):
                space_after = default_space_after
                runs_to_process = p_data
                if len(p_data) > 0 and isinstance(p_data[-1], (int, float)):
                    space_after = p_data[-1]
                    runs_to_process = p_data[:-1]

                p.space_after = Pt(space_after)

                for r_info in runs_to_process:
                    r_text, r_size, r_bold, r_color = r_info[:4]
                    run = p.add_run()
                    run.text = r_text
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(r_size)
                    run.font.bold = r_bold
                    if len(r_info) > 4 and r_info[4] is True:
                        run.font.underline = True
                    if isinstance(r_color, RGBColor):
                        run.font.color.rgb = r_color
                    elif r_color is not None:
                        run.font.color.theme_color = r_color

    # COLOR PALETTE
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_CYAN = RGBColor(80, 240, 255)
    COLOR_LIGHT_BLUE = RGBColor(215, 240, 255)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides[0]
    s_title = get_shape_by_name(slide1, "Google Shape;33;p1")
    if s_title:
        set_shape_text(s_title, [
            ("C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI", 28, True, MSO_THEME_COLOR.DARK_2, 0)
        ], align=PP_ALIGN.CENTER)

    s_author = get_shape_by_name(slide1, "Google Shape;34;p1")
    if s_author:
        s_author.top = 3720000
        s_author.height = 1500000
        tf = s_author.text_frame
        tf.clear()
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        p0.space_after = Pt(3)
        clear_paragraph_bullets_and_indents(p0)
        
        # Presenter underlined
        r0_1 = p0.add_run()
        r0_1.text = "Sheela Akshar Sakhi¹"
        r0_1.font.name = "Times New Roman"
        r0_1.font.size = Pt(16.5)
        r0_1.font.bold = True
        r0_1.font.underline = True
        r0_1.font.color.theme_color = MSO_THEME_COLOR.DARK_1

        r0_2 = p0.add_run()
        r0_2.text = " (Presenter), Ibbraheem Shaik¹, Settibattini Suhitha¹, Ramya G R²*"
        r0_2.font.name = "Times New Roman"
        r0_2.font.size = Pt(16.5)
        r0_2.font.bold = True
        r0_2.font.color.theme_color = MSO_THEME_COLOR.DARK_1

        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(4)
        clear_paragraph_bullets_and_indents(p1)
        r1 = p1.add_run()
        r1.text = "¹Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore\nAmrita Vishwa Vidyapeetham, India  ·  *Corresponding Author: gr_ramya@cb.amrita.edu"
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(13)
        r1.font.color.theme_color = MSO_THEME_COLOR.DARK_1

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        clear_paragraph_bullets_and_indents(p2)
        r2 = p2.add_run()
        r2.text = "Paper ID: 857   ·   Track: Technical Session"
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(14.5)
        r2.font.bold = True
        r2.font.color.theme_color = MSO_THEME_COLOR.ACCENT_2

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    slide2 = prs.slides[1]
    s_intro_title = get_shape_by_name(slide2, "Google Shape;44;p2")
    if s_intro_title:
        s_intro_title.text_frame.text = "Introduction & Research Context"
        s_intro_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    s_intro_body = get_shape_by_name(slide2, "Google Shape;45;p2")
    if s_intro_body:
        s_intro_body.width = 4650000
        set_shape_text(s_intro_body, [
            [
                ("• Healthcare AI & Black-Box Dilemma: ", 13.5, True, MSO_THEME_COLOR.DARK_2),
                ("High-performing deep tabular networks and complex ensembles are deployed in ICU triage and clinical CDS, yet operate as opaque black boxes, limiting clinician adoption [Muhammad & Bendechache, 2024].", 13, False, MSO_THEME_COLOR.DARK_1),
                5
            ],
            [
                ("• Auditing Void in Clinical XAI: ", 13.5, True, MSO_THEME_COLOR.DARK_2),
                ("Over 85% of published clinical XAI studies lack quantitative evaluation of explanation quality, relying purely on anecdotal visual heatmaps [Roychowdhury et al., npj Digit. Med. 2025; Kyrimi et al., 2025].", 13, False, MSO_THEME_COLOR.DARK_1),
                5
            ],
            [
                ("• Decoupling of Accuracy & Reliability: ", 13.5, True, MSO_THEME_COLOR.DARK_2),
                ("Superior predictive ROC-AUC does not guarantee explanation reliability; models often fit non-causal confounding artifacts while generating volatile attributions under clinical noise [Jin et al., 2023].", 13, False, MSO_THEME_COLOR.DARK_1),
                5
            ],
            [
                ("• The C-XAI Framework: ", 13.5, True, MSO_THEME_COLOR.DARK_2),
                ("First quantitative auditing foundation formulating 4 metrics: Local Lipschitz Stability (SbLip), Cross-Explainer Discordance (DXAI), Prior Alignment (W_Clin^norm), & Simulated Decision Utility (U_Clin_hat).", 13, False, MSO_THEME_COLOR.DARK_1),
                5
            ],
            [
                ("• Presentation Outline: ", 13.5, True, MSO_THEME_COLOR.DARK_2),
                ("Research Novelty  →  Auditing Methodology  →  Experimental Protocol  →  Benchmark Results & Auditing  →  Clinical Decision Impact.", 13, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    remove_shape_by_name(slide2, "Google Shape;47;p2")
    remove_shape_by_name(slide2, "Google Shape;48;p2")
    card2 = get_shape_by_name(slide2, "Google Shape;46;p2")
    if card2:
        img_w = int(card2.width * 0.92)
        img_left = card2.left + int(card2.width * 0.04)
        img_top = card2.top + int(card2.height * 0.04)
        pic2 = slide2.shapes.add_picture("Akshar_ICMLDE2026/figures/cxai_architecture.png", img_left, img_top, width=img_w)

        cap_top = img_top + pic2.height + int(card2.height * 0.03)
        cap_h = card2.top + card2.height - cap_top - int(card2.height * 0.03)
        tb_cap = slide2.shapes.add_textbox(img_left, cap_top, img_w, cap_h)
        set_shape_text(tb_cap, [
            ("Fig. 1: C-XAI 5-Layer Auditing Architecture", 12.5, True, MSO_THEME_COLOR.DARK_2, 3),
            ("Ingests multi-hospital EHR feeds  →  Injects physiological noise & adversarial attacks  →  Audits tree & deep neural models across 4 metrics (SbLip, DXAI, W_Clin, U_Clin)  →  Simulates calibrated clinician reliance.", 11.5, False, MSO_THEME_COLOR.DARK_1, 0)
        ], align=PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT (Fixed framing, card bounds & footer clearance!)
    # =========================================================================
    slide3 = prs.slides[2]
    s_ps_title = get_shape_by_name(slide3, "Google Shape;55;p3")
    if s_ps_title:
        s_ps_title.text_frame.text = "Problem Statement: The Clinical Explainability Gap"
        s_ps_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    s_banner = get_shape_by_name(slide3, "Google Shape;59;p3")
    if s_banner:
        set_shape_text(s_banner, [
            ("High predictive accuracy fails to guarantee explanation reliability in healthcare AI: post-hoc explanations remain fragile under physiological noise, exhibit severe cross-explainer conflict, and fail to align with established clinical guidelines, risking catastrophic decision errors.", 15, False, COLOR_WHITE, 0)
        ])

    # Card 1: Who is Affected
    s_card1 = get_shape_by_name(slide3, "Google Shape;60;p3")
    if s_card1:
        s_card1.top = 3000000
        s_card1.height = 3050000
    s_c1_icon = get_shape_by_name(slide3, "Google Shape;61;p3")
    if s_c1_icon:
        s_c1_icon.top = 3120000
        s_c1_icon.left = 1460220
        s_c1_icon.width = 600000
        s_c1_icon.height = 600000
    s_c1_pic = get_shape_by_name(slide3, "Google Shape;62;p3")
    if s_c1_pic:
        s_c1_pic.top = 3230000
        s_c1_pic.left = 1570220
        s_c1_pic.width = 380000
        s_c1_pic.height = 380000
    s_card1_title = get_shape_by_name(slide3, "Google Shape;63;p3")
    if s_card1_title:
        s_card1_title.top = 3800000
        s_card1_title.height = 350000
        s_card1_title.text_frame.text = "Who is Affected"
        p = s_card1_title.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(14)
        p.font.bold = True
    s_card1_body = get_shape_by_name(slide3, "Google Shape;64;p3")
    if s_card1_body:
        s_card1_body.top = 4220000
        s_card1_body.height = 1750000
        set_shape_text(s_card1_body, [
            [
                ("• ICU Clinicians: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Uncalibrated explanations increase inappropriate over-reliance on false predictions by up to 45% [Bussone, 2015; Jacobs, 2021].", 9, False, MSO_THEME_COLOR.DARK_1),
                2.5
            ],
            [
                ("• Healthcare Regulators: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Auditing mandates (FDA SaMD, EU AI Act) lack objective verification benchmarks.", 9, False, MSO_THEME_COLOR.DARK_1),
                2.5
            ],
            [
                ("• Patients: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Exposed to harm when triage models rely on non-causal confounding artifacts.", 9, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    # Card 2: Scale of the Issue
    s_card2 = get_shape_by_name(slide3, "Google Shape;65;p3")
    if s_card2:
        s_card2.top = 3000000
        s_card2.height = 3050000
    s_c2_icon = get_shape_by_name(slide3, "Google Shape;66;p3")
    if s_c2_icon:
        s_c2_icon.top = 3120000
        s_c2_icon.left = 4249140
        s_c2_icon.width = 600000
        s_c2_icon.height = 600000
    s_c2_pic = get_shape_by_name(slide3, "Google Shape;67;p3")
    if s_c2_pic:
        s_c2_pic.top = 3230000
        s_c2_pic.left = 4359140
        s_c2_pic.width = 380000
        s_c2_pic.height = 380000
    s_card2_title = get_shape_by_name(slide3, "Google Shape;68;p3")
    if s_card2_title:
        s_card2_title.top = 3800000
        s_card2_title.height = 350000
        s_card2_title.text_frame.text = "Scale of the Issue"
        p = s_card2_title.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(14)
        p.font.bold = True
    s_card2_body = get_shape_by_name(slide3, "Google Shape;69;p3")
    if s_card2_body:
        s_card2_body.top = 4220000
        s_card2_body.height = 1750000
        set_shape_text(s_card2_body, [
            [
                ("• >85% Lacks Auditing: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Clinical studies rely predominantly on anecdotal visual saliency without quantitative evaluation [Roychowdhury, 2025].", 9, False, MSO_THEME_COLOR.DARK_1),
                2.5
            ],
            [
                ("• 9.6× Instability: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Deep neural models exhibit up to 9.6× higher explanation instability under standard sensor noise (h=0.05).", 9, False, MSO_THEME_COLOR.DARK_1),
                2.5
            ],
            [
                ("• >40% Disagreement: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Post-hoc explainers produce conflicting clinical rationales on identical patient encounters (DXAI ≈ 0.435).", 9, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    # Card 3: Current Gaps
    s_card3 = get_shape_by_name(slide3, "Google Shape;70;p3")
    if s_card3:
        s_card3.top = 3000000
        s_card3.height = 3050000
    s_c3_icon = get_shape_by_name(slide3, "Google Shape;71;p3")
    if s_c3_icon:
        s_c3_icon.top = 3120000
        s_c3_icon.left = 7038060
        s_c3_icon.width = 600000
        s_c3_icon.height = 600000
    s_c3_pic = get_shape_by_name(slide3, "Google Shape;72;p3")
    if s_c3_pic:
        s_c3_pic.top = 3230000
        s_c3_pic.left = 7148060
        s_c3_pic.width = 380000
        s_c3_pic.height = 380000
    s_card3_title = get_shape_by_name(slide3, "Google Shape;73;p3")
    if s_card3_title:
        s_card3_title.top = 3800000
        s_card3_title.height = 350000
        s_card3_title.text_frame.text = "Current Gaps"
        p = s_card3_title.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(14)
        p.font.bold = True
    s_card3_body = get_shape_by_name(slide3, "Google Shape;74;p3")
    if s_card3_body:
        s_card3_body.top = 4220000
        s_card3_body.height = 1750000
        set_shape_text(s_card3_body, [
            [
                ("• Blind to Medical Priors: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Toolkits (Captum, OpenXAI) test against internal weights, ignoring clinical consensus (SOFA, ASCVD).", 9, False, MSO_THEME_COLOR.DARK_1),
                2.5
            ],
            [
                ("• Synthetic Data Focus: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Prior benchmarks omit realistic EHR noise models and clinical tabular architectures.", 9, False, MSO_THEME_COLOR.DARK_1),
                2.5
            ],
            [
                ("• No Utility Modeling: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Fails to link explanation fidelity to physician decision-theoretic error penalties.", 9, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    # =========================================================================
    # SLIDE 4: RESEARCH NOVELTY (Updated per Dr. Ramya's feedback!)
    # =========================================================================
    slide4 = prs.slides[3]
    s_bg_title = get_shape_by_name(slide4, "Google Shape;81;p4")
    if s_bg_title:
        s_bg_title.text_frame.text = "Research Novelty: Why C-XAI is Necessary"
        s_bg_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    s_table = get_shape_by_name(slide4, "Google Shape;82;p4")
    if s_table and s_table.has_table:
        t = s_table.table
        headers = ["Existing Frameworks Evaluate", "What They Fail to Evaluate", "What C-XAI Introduces (Novelty)"]
        rows_data = [
            ["Internal attribution fidelity against model weights (Captum, OpenXAI, Quantus)", "Zero clinical guideline integration; blind to medical consensus (SOFA, ASCVD)", "Dimension-Normalized Wasserstein Prior Distance (W_Clin^norm) grounded in clinical guidelines"],
            ["Pixel / token saliency and synthetic Gaussian noise on vision / NLP benchmarks", "Omit cross-explainer ranking conflict on individual patient encounters", "Cross-Explainer Discordance (DXAI = 1 - r_s) with adversarial stress-testing"],
            ["Theoretical supremum Lipschitz bounds in toy / synthetic settings (SENN)", "Fail on step-function tree ensembles; no clinical decision utility modeling", "Empirical Lipschitz Stability (SbLip) with Zeroth-Order Smoothing + Calibrated Utility (U_Clin)"]
        ]
        for c_idx, h in enumerate(headers):
            cell = t.cell(0, c_idx)
            cell.text = h
            cell.margin_left = Inches(0.06)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Times New Roman"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_WHITE
        for r_idx, r in enumerate(rows_data):
            for c_idx, val in enumerate(r):
                cell = t.cell(r_idx + 1, c_idx)
                cell.text = val
                cell.margin_left = Inches(0.06)
                cell.margin_right = Inches(0.06)
                cell.margin_top = Inches(0.04)
                cell.margin_bottom = Inches(0.04)
                p = cell.text_frame.paragraphs[0]
                p.font.name = "Times New Roman"
                p.font.size = Pt(9.5)
                p.font.color.theme_color = MSO_THEME_COLOR.DARK_1

    s_thy_t = get_shape_by_name(slide4, "Google Shape;86;p4")
    if s_thy_t:
        s_thy_t.text_frame.text = "Theoretical Novelty"
        p = s_thy_t.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.theme_color = MSO_THEME_COLOR.DARK_2

    s_thy = get_shape_by_name(slide4, "Google Shape;95;p4")
    if s_thy:
        s_thy.top = 4220000
        s_thy.height = 1300000
        set_shape_text(s_thy, [
            [
                ("• Local Lipschitz Stability: ", 10, True, MSO_THEME_COLOR.DARK_2),
                ("Monte Carlo expectation under physiological noise draws u_m ~ N(0, h²I).", 9.5, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Optimal Transport: ", 10, True, MSO_THEME_COLOR.DARK_2),
                ("Proven (d-1) upper-bound normalization for 1D Earth Mover's Distance.", 9.5, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Decision Theory: ", 10, True, MSO_THEME_COLOR.DARK_2),
                ("Pauker-Kassirer threshold reliance model with asymmetric error penalties.", 9.5, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    s_gap_title = get_shape_by_name(slide4, "Google Shape;90;p4")
    if s_gap_title:
        s_gap_title.text_frame.text = "Methodological Novelty"
        p = s_gap_title.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    s_gap = get_shape_by_name(slide4, "Google Shape;96;p4")
    if s_gap:
        s_gap.top = 4220000
        s_gap.height = 1300000
        set_shape_text(s_gap, [
            [
                ("• Zeroth-Order Smoother: ", 10, True, COLOR_LIGHT_BLUE),
                ("Gaussian score smoother enables gradient explainers on step-function trees.", 9.5, False, COLOR_WHITE),
                2
            ],
            [
                ("• Explainer Discordance: ", 10, True, COLOR_LIGHT_BLUE),
                ("Formulates DXAI (1 - r_s) to capture clinician cognitive dissonance.", 9.5, False, COLOR_WHITE),
                2
            ],
            [
                ("• Adversarial Stress-Tests: ", 10, True, COLOR_LIGHT_BLUE),
                ("Evaluates attribution collapse under FGSM and multi-step ScaL-PGD attacks.", 9.5, False, COLOR_WHITE),
                0
            ]
        ])

    s_contrib_t = get_shape_by_name(slide4, "Google Shape;94;p4")
    if s_contrib_t:
        s_contrib_t.text_frame.text = "Clinical Governance"
        p = s_contrib_t.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.theme_color = MSO_THEME_COLOR.DARK_2

    s_contrib = get_shape_by_name(slide4, "Google Shape;97;p4")
    if s_contrib:
        s_contrib.top = 4220000
        s_contrib.height = 1300000
        set_shape_text(s_contrib, [
            [
                ("• Uncovers Paradox: ", 10, True, MSO_THEME_COLOR.DARK_2),
                ("High predictive accuracy masks severe attribution instability (9.6x higher).", 9.5, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Multi-Cohort Audit: ", 10, True, MSO_THEME_COLOR.DARK_2),
                ("Audits MIMIC-IV (40k), eICU (10k), BCWD (569), & Cardio EHR (800).", 9.5, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Regulatory Readiness: ", 10, True, MSO_THEME_COLOR.DARK_2),
                ("Establishes pre-deployment auditing fulfilling FDA SaMD & EU AI Act.", 9.5, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    # =========================================================================
    # SLIDE 5: PROPOSED METHODOLOGY
    # =========================================================================
    slide5 = prs.slides[4]
    s_pm_title = get_shape_by_name(slide5, "Google Shape;104;p5")
    if s_pm_title:
        s_pm_title.text_frame.text = "Proposed Methodology: The C-XAI Auditing Framework"
        s_pm_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    step_labels = [
        ("Google Shape;108;p5", "Data & Noise Layer", MSO_THEME_COLOR.DARK_2),
        ("Google Shape;113;p5", "Predictive Modeling", MSO_THEME_COLOR.DARK_2),
        ("Google Shape;118;p5", "Post-Hoc Explainers", COLOR_WHITE),
        ("Google Shape;123;p5", "Quantitative Auditing", MSO_THEME_COLOR.DARK_2)
    ]
    for s_name, label, col in step_labels:
        s_box = get_shape_by_name(slide5, s_name)
        if s_box:
            s_box.text_frame.text = label
            p = s_box.text_frame.paragraphs[0]
            p.font.name = "Times New Roman"
            p.font.size = Pt(16)
            p.font.bold = True
            if isinstance(col, RGBColor):
                p.font.color.rgb = col
            else:
                p.font.color.theme_color = col

    s_pm_body = get_shape_by_name(slide5, "Google Shape;124;p5")
    if s_pm_body:
        s_pm_body.top = 3520000
        s_pm_body.height = 2200000
        set_shape_text(s_pm_body, [
            [
                ("1. Data & Perturbation Layer: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Standardizes multi-center EHR feeds across 4 cohorts (MIMIC-IV, eICU, BCWD, Cardio). Injects physiologically parameterized Gaussian noise u_m ~ N(0, h²I), 20% MCAR feature missingness, and gradient-crafted adversarial shifts (FGSM, ScaL-PGD).", 10.5, False, MSO_THEME_COLOR.DARK_1),
                3
            ],
            [
                ("2. Predictive Modeling Layer: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Evaluates tree ensembles (Random Forest, Extra Trees) with Zeroth-Order Gaussian Smoothing for gradient estimation on non-differentiable step boundaries, alongside deep neural models (MLP, Tabular Deep ResNet with feature tokenization).", 10.5, False, MSO_THEME_COLOR.DARK_1),
                3
            ],
            [
                ("3. Post-Hoc Explainer Layer: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Computes local feature attribution vectors across diverse mathematical foundations: TreeSHAP, KernelSHAP, LIME, SmoothGrad, Integrated Gradients, and Permutation Feature Importance (PFI).", 10.5, False, MSO_THEME_COLOR.DARK_1),
                3
            ],
            [
                ("4. Quantitative Auditing Layer: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Formulates 4 rigorous metrics: Empirical Lipschitz Stability (SbLip), Cross-Explainer Discordance (DXAI), Dimension-Normalized Clinical Prior Alignment (W_Clin^norm), and Calibrated In-Silico Decision Utility (U_Clin_hat).", 10.5, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    # =========================================================================
    # SLIDE 6: EXPERIMENTAL SETUP (Updated per Dr. Ramya's feedback & framing!)
    # =========================================================================
    slide6 = prs.slides[5]
    s_es_title = get_shape_by_name(slide6, "Google Shape;131;p6")
    if s_es_title:
        s_es_title.text_frame.text = "Experimental Setup & Auditing Protocol"
        s_es_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    top_stats = [
        ("Google Shape;133;p6", "4", COLOR_WHITE, "Google Shape;134;p6", "Healthcare Cohorts", COLOR_WHITE, 457200),
        ("Google Shape;136;p6", "51.3 K", MSO_THEME_COLOR.DARK_2, "Google Shape;137;p6", "Total Clinical Records", MSO_THEME_COLOR.DARK_1, 2560320),
        ("Google Shape;139;p6", "4 · 6", MSO_THEME_COLOR.DARK_2, "Google Shape;140;p6", "Models · Explainers", MSO_THEME_COLOR.DARK_1, 4663440),
        ("Google Shape;142;p6", "4", MSO_THEME_COLOR.DARK_2, "Google Shape;143;p6", "C-XAI Audit Metrics", MSO_THEME_COLOR.DARK_1, 6766560)
    ]
    card_w = 1920240
    for num_name, num_val, num_col, lbl_name, lbl_val, lbl_col, c_left_pos in top_stats:
        s_num = get_shape_by_name(slide6, num_name)
        if s_num:
            s_num.left = c_left_pos
            s_num.width = card_w
            s_num.top = 1500000
            s_num.height = 550000
            s_num.text_frame.text = num_val
            p = s_num.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Times New Roman"
            p.font.size = Pt(34)
            p.font.bold = True
            if isinstance(num_col, RGBColor):
                p.font.color.rgb = num_col
            else:
                p.font.color.theme_color = num_col

        s_lbl = get_shape_by_name(slide6, lbl_name)
        if s_lbl:
            s_lbl.left = c_left_pos
            s_lbl.width = card_w
            s_lbl.top = 2120000
            s_lbl.height = 700000
            s_lbl.text_frame.text = lbl_val
            p = s_lbl.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Times New Roman"
            p.font.size = Pt(12)
            p.font.bold = True
            if isinstance(lbl_col, RGBColor):
                p.font.color.rgb = lbl_col
            else:
                p.font.color.theme_color = lbl_col

    # Bottom 4 sections: 2 rows of 2 cards shifted up to guarantee generous footer margin!
    r1_circle_top = 3180000
    r1_icon_top = 3314000
    r1_title_top = 3180000
    r1_body_top = 3520000

    r2_circle_top = 4600000
    r2_icon_top = 4734000
    r2_title_top = 4600000
    r2_body_top = 4940000

    # Adjust Row 1 shapes
    for s_id, s_pos in [
        ("Google Shape;144;p6", (457200, r1_circle_top, 520000, 520000)),
        ("Google Shape;145;p6", (591200, r1_icon_top, 252000, 252000)),
        ("Google Shape;146;p6", (1100000, r1_title_top, 3450000, 350000)),
        ("Google Shape;147;p6", (1100000, r1_body_top, 3450000, 750000)),
        ("Google Shape;148;p6", (4663440, r1_circle_top, 520000, 520000)),
        ("Google Shape;149;p6", (4797440, r1_icon_top, 252000, 252000)),
        ("Google Shape;150;p6", (5300000, r1_title_top, 3450000, 350000)),
        ("Google Shape;151;p6", (5300000, r1_body_top, 3450000, 750000))
    ]:
        sh = get_shape_by_name(slide6, s_id)
        if sh:
            sh.left, sh.top, sh.width, sh.height = s_pos

    # Adjust Row 2 shapes
    for s_id, s_pos in [
        ("Google Shape;152;p6", (457200, r2_circle_top, 520000, 520000)),
        ("Google Shape;153;p6", (591200, r2_icon_top, 252000, 252000)),
        ("Google Shape;154;p6", (1100000, r2_title_top, 3450000, 350000)),
        ("Google Shape;155;p6", (1100000, r2_body_top, 3450000, 750000)),
        ("Google Shape;156;p6", (4663440, r2_circle_top, 520000, 520000)),
        ("Google Shape;157;p6", (4797440, r2_icon_top, 252000, 252000)),
        ("Google Shape;158;p6", (5300000, r2_title_top, 3450000, 350000)),
        ("Google Shape;159;p6", (5300000, r2_body_top, 3450000, 750000))
    ]:
        sh = get_shape_by_name(slide6, s_id)
        if sh:
            sh.left, sh.top, sh.width, sh.height = s_pos

    b_cards = [
        ("Google Shape;146;p6", "Cohorts & 51.3K Breakdown", "Google Shape;147;p6", [
            [("• MIMIC-IV (40k) & eICU (10k): ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("SOFA (0.35), Lactate (0.30); MAP (0.40), WBC (0.20).", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• BCWD (569) & Cardio (800): ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("Tumor Area & Concavity (0.25); Systolic BP (0.30), Age (0.25).", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• Total Clinical Encounters: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("51,369 records across multi-center ICU & outpatient feeds.", 9, False, MSO_THEME_COLOR.DARK_1), 0]
        ]),
        ("Google Shape;150;p6", "Software, Hardware & Protocol", "Google Shape;151;p6", [
            [("• Environment: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("Python 3.10+, PyTorch 2.14, Scikit-learn, Captum, SHAP, SciPy.", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• Hardware: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("Apple Silicon / Linux x86_64, 16 GB RAM. Fully reproducible pipeline.", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• Validation Protocol: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("Stratified 5-fold cross-validation repeated across 50 random seeds.", 9, False, MSO_THEME_COLOR.DARK_1), 0]
        ]),
        ("Google Shape;154;p6", "4 Models · 6 Explainers Evaluated", "Google Shape;155;p6", [
            [("• Predictive Models: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("Random Forest & Extra Trees (Smoothed); MLP, Tabular Deep ResNet.", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• Post-Hoc Explainers: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("TreeSHAP, KernelSHAP, LIME, SmoothGrad, Integrated Gradients, PFI.", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• Score Smoother: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("Zeroth-order Gaussian smoother renders step boundaries differentiable.", 9, False, MSO_THEME_COLOR.DARK_1), 0]
        ]),
        ("Google Shape;158;p6", "C-XAI Audit Metrics & Loss Weights", "Google Shape;159;p6", [
            [("• Stability & Discordance: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("SbLip (Local Lipschitz, M=100, h=0.05); DXAI (Spearman rank distance in [0, 2]).", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• Clinical Prior Alignment: ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("W_Clin^norm (Dimension-normalized discrete 1D Earth Mover's Distance).", 9, False, MSO_THEME_COLOR.DARK_1), 1.5],
            [("• Decision Utility (U_Clin): ", 9.5, True, MSO_THEME_COLOR.DARK_2), ("Net utility with over-reliance α=0.50 and under-reliance β=0.30.", 9, False, MSO_THEME_COLOR.DARK_1), 0]
        ])
    ]

    for title_name, title_txt, body_name, body_paragraphs in b_cards:
        s_t = get_shape_by_name(slide6, title_name)
        if s_t:
            s_t.text_frame.text = title_txt
            p = s_t.text_frame.paragraphs[0]
            p.font.name = "Times New Roman"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.theme_color = MSO_THEME_COLOR.DARK_2
        s_b = get_shape_by_name(slide6, body_name)
        if s_b:
            set_shape_text(s_b, body_paragraphs)

    # =========================================================================
    # SLIDE 7: RESULTS (Updated per Dr. Ramya's feedback!)
    # =========================================================================
    slide7 = prs.slides[6]
    s_r_title = get_shape_by_name(slide7, "Google Shape;166;p7")
    if s_r_title:
        s_r_title.text_frame.text = "Results: Accuracy vs. Clinical Explanation Reliability"
        s_r_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    for s in slide7.shapes:
        if s.has_chart:
            chart = s.chart
            chart_data = CategoryChartData()
            chart_data.categories = ['Tabular ResNet', 'MLP', 'Random Forest', 'Extra Trees (C-XAI)']
            chart_data.add_series('Predictive Acc (%)', (89.4, 89.2, 88.5, 88.1))
            chart_data.add_series('Clinical Utility (%)', (71.0, 71.2, 84.1, 84.9))
            chart.replace_data(chart_data)
            chart.has_title = True
            chart.chart_title.text_frame.text = "Predictive Accuracy vs. Calibrated Decision Utility (MIMIC-IV)"
            for p in chart.chart_title.text_frame.paragraphs:
                p.font.name = "Times New Roman"
                p.font.size = Pt(13)
                p.font.bold = True
            chart.has_legend = True
            chart.legend.position = pptx.enum.chart.XL_LEGEND_POSITION.TOP
            chart.legend.include_in_layout = False
            chart.legend.font.name = "Times New Roman"
            chart.legend.font.size = Pt(11)

    s_stat = get_shape_by_name(slide7, "Google Shape;169;p7")
    if s_stat:
        s_stat.top = 1500000
        s_stat.text_frame.text = "+19.6%"
        p = s_stat.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(40)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN

    s_stat_lbl = get_shape_by_name(slide7, "Google Shape;170;p7")
    if s_stat_lbl:
        s_stat_lbl.top = 2250000
        s_stat_lbl.height = 600000
        set_shape_text(s_stat_lbl, [
            ("Clinical Decision Utility Advantage: Extra Trees vs. Tabular Deep ResNet (MIMIC-IV)", 11, False, COLOR_WHITE, 0)
        ])

    s_findings = get_shape_by_name(slide7, "Google Shape;171;p7")
    if s_findings:
        s_findings.top = 2950000
        s_findings.height = 2900000
        set_shape_text(s_findings, [
            [
                ("• Improvement Calculation & Significance: ", 9.5, True, COLOR_CYAN),
                ("Gain of +0.1390 absolute (+13.9 percentage points, 0.8485 vs 0.7095); relative gain +19.6% (p < 0.001, Wilcoxon W=0.0, Paired t=14.82 over N=50 seeds).", 9, False, COLOR_WHITE),
                2
            ],
            [
                ("• 9.6× Instability in Deep Architectures: ", 9.5, True, COLOR_CYAN),
                ("Tabular Deep ResNet attains state-of-the-art accuracy (89.4%) but yields severe explanation instability (SbLip = 0.4912 vs. 0.0512 for ET).", 9, False, COLOR_WHITE),
                2
            ],
            [
                ("• Acute Cross-Explainer Conflict: ", 9.5, True, COLOR_CYAN),
                ("Neural models produce severe discordance (DXAI ≈ 0.435), where SHAP and LIME present contradictory clinical rationales on the identical patient encounter.", 9, False, COLOR_WHITE),
                2
            ],
            [
                ("• Tree Ensembles Maximize Safety: ", 9.5, True, COLOR_CYAN),
                ("Extra Trees maintains top utility (U_Clin = 0.8485), lowest prior divergence (W_Clin^norm = 0.0312), and near-instant latency (4.2 ms).", 9, False, COLOR_WHITE),
                0
            ]
        ])

    # =========================================================================
    # SLIDE 8: RESULTS - COMPARATIVE ANALYSIS (Updated per Dr. Ramya's feedback & framing!)
    # =========================================================================
    slide8 = prs.slides[7]
    s_ca_title = get_shape_by_name(slide8, "Google Shape;178;p8")
    if s_ca_title:
        s_ca_title.text_frame.text = "Results: Explainer Discordance & Accuracy Decoupling"
        s_ca_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    remove_shape_by_name(slide8, "Google Shape;181;p8")
    remove_shape_by_name(slide8, "Google Shape;182;p8")
    remove_shape_by_name(slide8, "Google Shape;184;p8")
    remove_shape_by_name(slide8, "Google Shape;185;p8")

    c_left = get_shape_by_name(slide8, "Google Shape;179;p8")
    c_right = get_shape_by_name(slide8, "Google Shape;180;p8")

    if c_left:
        # fig_discordance_comparison: side-by-side heatmaps (Extra Trees vs Tabular Deep ResNet)
        pic_w = int(c_left.width * 0.94)
        pic_h = int(pic_w * 1220 / 2919)
        pic_l = c_left.left + (c_left.width - pic_w) // 2
        pic_t = c_left.top + int(c_left.height * 0.04)
        slide8.shapes.add_picture("CONF_PRESENTATION/scripts/fig_discordance_comparison.png", pic_l, pic_t, width=pic_w, height=pic_h)

        # Key takeaway and derivation box inside left card per Dr. Ramya's request!
        tb_l_top = pic_t + pic_h + 100000
        tb_l_h = c_left.top + c_left.height - tb_l_top - 50000
        tb_l = slide8.shapes.add_textbox(pic_l, tb_l_top, pic_w, tb_l_h)
        set_shape_text(tb_l, [
            [
                ("• Metric Formulation: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("DXAI(E1, E2) = 1 - r_s in [0, 2], quantifying Spearman rank discordance between attribution vectors.", 9, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Tree Disagreement = 0.059: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("TreeSHAP and LIME achieve high concordance (mean r_s = 0.941 -> DXAI = 1 - 0.941 = 0.059; tight consensus).", 9, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Neural Disagreement = 0.435: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Deep ResNet explainers severely diverge (r_s = 0.565 -> DXAI = 0.435; 7.4× higher conflict on identical patients).", 9, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    if c_right:
        pic_w = int(c_right.width * 0.90)
        pic_h = int(pic_w * 1166 / 1810)
        pic_l = c_right.left + (c_right.width - pic_w) // 2
        pic_t = c_right.top + int(c_right.height * 0.04)
        slide8.shapes.add_picture("Akshar_ICMLDE2026/figures/accuracy_vs_clinical_utility.png", pic_l, pic_t, width=pic_w, height=pic_h)

        tb_r_top = pic_t + pic_h + 100000
        tb_r_h = c_right.top + c_right.height - tb_r_top - 50000
        tb_r = slide8.shapes.add_textbox(pic_l, tb_r_top, pic_w, tb_r_h)
        set_shape_text(tb_r, [
            [
                ("• Accuracy Decoupling: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("AUROC fails to predict clinical explanation reliability (R² = 0.04 across cohorts); accuracy masks fragile rationales.", 9, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Clinical Decision Winner: ", 9.5, True, MSO_THEME_COLOR.DARK_2),
                ("Extra Trees maintains top utility (U_Clin = 84.9%) over Tabular ResNet (71.0%) due to calibrated risk weighting.", 9, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    s_cap1 = get_shape_by_name(slide8, "Google Shape;183;p8")
    if s_cap1:
        s_cap1.top = 5400000
        s_cap1.height = 450000
        set_shape_text(s_cap1, [
            ("Fig. 2: Pairwise explainer discordance matrix (DXAI = 1 - rs) across explainers on MIMIC-IV", 9.5, True, MSO_THEME_COLOR.DARK_2, 0)
        ], align=PP_ALIGN.CENTER)

    s_cap2 = get_shape_by_name(slide8, "Google Shape;186;p8")
    if s_cap2:
        s_cap2.top = 5400000
        s_cap2.height = 450000
        set_shape_text(s_cap2, [
            ("Fig. 3: Predictive accuracy vs. simulated clinical decision utility (U_Clin_hat) across 4 cohorts", 9.5, True, MSO_THEME_COLOR.DARK_2, 0)
        ], align=PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 9: DISCUSSION
    # =========================================================================
    slide9 = prs.slides[8]
    s_disc_title = get_shape_by_name(slide9, "Google Shape;193;p9")
    if s_disc_title:
        s_disc_title.text_frame.text = "Discussion: Insights, Robustness & Regulatory Impact"
        s_disc_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    s_hyp_t = get_shape_by_name(slide9, "Google Shape;197;p9")
    if s_hyp_t:
        s_hyp_t.top = 1520000
        s_hyp_t.text_frame.text = "Theoretical Hypothesis & The Representation Paradox"
        p = s_hyp_t.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.theme_color = MSO_THEME_COLOR.DARK_2

    s_hyp_b = get_shape_by_name(slide9, "Google Shape;198;p9")
    if s_hyp_b:
        s_hyp_b.top = 1950000
        s_hyp_b.height = 680000
        set_shape_text(s_hyp_b, [
            [
                ("• Initial Hypothesis: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Continuous neural representations were expected to produce smoother, more stable explanations than step-function tree partitions.", 11, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Empirical Reality: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Hypothesis rejected. Deep networks construct complex, chaotic decision manifolds with steep local gradients, inducing high attribution volatility under clinical noise.", 11, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    s_evi_t = get_shape_by_name(slide9, "Google Shape;202;p9")
    if s_evi_t:
        s_evi_t.top = 3080000
        s_evi_t.text_frame.text = "Empirical Evidence & Adversarial Vulnerability"
        p = s_evi_t.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    s_evi_b = get_shape_by_name(slide9, "Google Shape;203;p9")
    if s_evi_b:
        s_evi_b.top = 3510000
        s_evi_b.height = 680000
        set_shape_text(s_evi_b, [
            [
                ("• Sub-Linear vs. Supra-Linear Scaling: ", 11.5, True, COLOR_CYAN),
                ("Across noise radii (h=0.01 to 0.20), Extra Trees exhibits sub-linear growth (SbLip=0.018 to 0.103), while deep models scale supra-linearly (>12× degradation).", 11, False, COLOR_WHITE),
                2
            ],
            [
                ("• Adversarial Collapse: ", 11.5, True, COLOR_CYAN),
                ("Under FGSM/ScaL-PGD attacks, neural explainers completely collapse (DXAI > 1.84, near-total rank inversion), whereas tree ensembles remain robust (DXAI ≤ 0.312).", 11, False, COLOR_WHITE),
                0
            ]
        ])

    s_sig_t = get_shape_by_name(slide9, "Google Shape;207;p9")
    if s_sig_t:
        s_sig_t.top = 4640000
        s_sig_t.text_frame.text = "Clinical Governance & Regulatory Compliance"
        p = s_sig_t.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.theme_color = MSO_THEME_COLOR.DARK_2

    s_sig_b = get_shape_by_name(slide9, "Google Shape;208;p9")
    if s_sig_b:
        s_sig_b.top = 5070000
        s_sig_b.height = 680000
        set_shape_text(s_sig_b, [
            [
                ("• Safety Imperative: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Deploying models solely based on AUROC introduces severe patient risk from automation bias and uncalibrated clinical trust.", 11, False, MSO_THEME_COLOR.DARK_1),
                2
            ],
            [
                ("• Regulatory Readiness: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("C-XAI establishes an objective pre-deployment auditing standard directly addressing FDA SaMD, EU AI Act, and healthcare compliance mandates.", 11, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    slide10 = prs.slides[9]
    s_cfs_title = get_shape_by_name(slide10, "Google Shape;215;p10")
    if s_cfs_title:
        s_cfs_title.text_frame.text = "Conclusion & Future Scope"
        s_cfs_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    s_conc_b = get_shape_by_name(slide10, "Google Shape;220;p10")
    if s_conc_b:
        s_conc_b.top = 2580000
        s_conc_b.height = 2900000
        set_shape_text(s_conc_b, [
            [
                ("• C-XAI Auditing Framework Established: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Formulated the first comprehensive quantitative auditing protocol assessing explanation stability (SbLip), discordance (DXAI), clinical prior alignment (W_Clin^norm), and simulated decision utility (U_Clin_hat).", 11, False, MSO_THEME_COLOR.DARK_1),
                4
            ],
            [
                ("• The Accuracy-Explainability Paradox: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("High predictive accuracy does not imply explanation reliability. Tree ensembles decisively outperform deep tabular models in stability (0.051 vs. 0.491) and clinical utility (0.85 vs. 0.71).", 11, False, MSO_THEME_COLOR.DARK_1),
                4
            ],
            [
                ("• Clinical Deployment Imperative: ", 11.5, True, MSO_THEME_COLOR.DARK_2),
                ("Pre-deployment explanation auditing is essential to safeguard patients against misleading attributions and prevent clinician decision paralysis.", 11, False, MSO_THEME_COLOR.DARK_1),
                0
            ]
        ])

    s_fut_t = get_shape_by_name(slide10, "Google Shape;224;p10")
    if s_fut_t:
        s_fut_t.text_frame.text = "Future Scope"
        p = s_fut_t.text_frame.paragraphs[0]
        p.font.name = "Times New Roman"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    s_fut_b = get_shape_by_name(slide10, "Google Shape;225;p10")
    if s_fut_b:
        s_fut_b.top = 2580000
        s_fut_b.height = 2900000
        set_shape_text(s_fut_b, [
            [
                ("• Multimodal Clinical Expansion: ", 11.5, True, COLOR_LIGHT_BLUE),
                ("Extending C-XAI beyond tabular EHR to multimodal ICU telemetry, unstructured clinical progress notes, and medical radiograms.", 11, False, COLOR_WHITE),
                4
            ],
            [
                ("• Dynamic Trajectory Auditing: ", 11.5, True, COLOR_LIGHT_BLUE),
                ("Developing temporal stability metrics tailored for continuous vital sign streams across recurrent networks and clinical transformers.", 11, False, COLOR_WHITE),
                4
            ],
            [
                ("• Prospective Clinician Reader Trials: ", 11.5, True, COLOR_LIGHT_BLUE),
                ("Validating calibrated decision utility formulas against real-world physician triage decisions and cognitive workload in clinical simulation suites.", 11, False, COLOR_WHITE),
                0
            ]
        ])

    # =========================================================================
    # SLIDE 11: REFERENCES (All 28 Paper References across 2 columns!)
    # =========================================================================
    slide11 = prs.slides[10]
    s_ref_title = get_shape_by_name(slide11, "Google Shape;232;p11")
    if s_ref_title:
        s_ref_title.text_frame.text = "References"
        s_ref_title.text_frame.paragraphs[0].font.name = "Times New Roman"

    # Remove old reference box if present
    s_refs_old = get_shape_by_name(slide11, "Google Shape;233;p11")
    if s_refs_old:
        remove_shape_by_name(slide11, "Google Shape;233;p11")

    # Column 1 (Left: References 1-14)
    tb_c1 = slide11.shapes.add_textbox(457200, 1250000, 3950000, 4900000)
    col1_refs = [
        ("[1] S. M. Lundberg & S.-I. Lee, “A unified approach to interpreting model predictions,” in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 4765–4774, 2017.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[2] M. T. Ribeiro, S. Singh, & C. Guestrin, “Why should I trust you?: Explaining predictions of any classifier,” in Proc. ACM SIGKDD, pp. 1135–1144, 2016.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[3] M. Sundararajan, A. Taly, & Q. Yan, “Axiomatic attribution for deep networks,” in Proc. ICML, pp. 3319–3328, 2017.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[4] D. Muhammad & M. Bendechache, “Unveiling the black box: Systematic review of XAI in medical imaging,” CSBJ, vol. 23, pp. 248–261, 2024.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[5] K. Lamba & S. Rani, “BCI and Grad-CAM based explainable artificial intelligence for smart healthcare,” J. Neurosci. Methods, vol. 401, 2024.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[6] R. Caruana, Y. Lou, P. Koch, et al., “Intelligible and interpretable machine learning in healthcare,” ACM Comput. Surv., vol. 55, no. 8, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[7] C. Agarwal, S. Krishna, et al., “OpenXAI: Towards a unified benchmark of model explanations,” in Proc. NeurIPS, vol. 35, 2022.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[8] A. Hedström, L. Weber, et al., “Quantus: An explainable AI evaluation toolkit,” J. Mach. Learn. Res. (JMLR), vol. 24, pp. 1–11, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[9] S. Krishna, T. Han, A. Gu, et al., “The disagreement problem in explainable AI: Empirical studies,” in Proc. ACM CHI, pp. 1–16, 2022.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[10] A. E. W. Johnson, L. Bulgarelli, et al., “MIMIC-IV, a freely accessible electronic health record dataset,” Sci. Data, vol. 10, no. 1, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[11] T. J. Pollard, A. E. W. Johnson, et al., “The eICU collaborative research database benchmark pipeline,” Sci. Data, vol. 10, no. 1, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[12] C.-K. Yeh, C.-K. Hsieh, et al., “Quantifying sensitivity and robustness of post-hoc explanations,” Nat. Mach. Intell., vol. 5, pp. 782–792, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[13] G. Bansal, T. Wu, J. Zhou, et al., “Calibrating human-AI reliance in clinical decision support systems,” in Proc. ACM CHI, pp. 1–14, 2024.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[14] Z. Buçinca, P. Malaya, et al., “Evaluating explanation stability and clinician trust in healthcare AI,” Artif. Intell. Med., vol. 138, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 0)
    ]
    set_shape_text(tb_c1, col1_refs)

    # Column 2 (Right: References 15-28)
    tb_c2 = slide11.shapes.add_textbox(4550000, 1250000, 4100000, 4900000)
    col2_refs = [
        ("[15] S. M. Lauritsen, M. Kalør, et al., “Early clinical prediction of sepsis using scalable ML protocols,” Lancet Digit. Health, vol. 6, 2024.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[16] F. Bohlen, M. Mittermaier, et al., “Quantitative evaluation of explainable AI in intensive care risk,” IEEE JBHI, vol. 27, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[17] J. Duell, G. Stiglic, & P. Kocbek, “Cross-explainer disagreement and instability in EHR analytics,” J. Biomed. Inform., vol. 142, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[18] X. Niu, L. Wang, & J. Zhang, “Multi-level attention deep neural networks for patient risk prediction,” IEEE TNNLS, vol. 34, 2022.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[19] T. Mahmood, Y. Chen, & X. Zhao, “Quantifying transparency in gradient boosted trees for EHR risk,” Nat. Mach. Intell., vol. 4, 2022.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[20] J. Alderden, D. Drake, et al., “Clinical utility and usability auditing for interactive healthcare ML,” CIN, vol. 41, pp. 210–218, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[21] K. Ihalapathirana & T. Silva, “ReliefF and SHAP feature selection for disease risk prediction,” IEEE Access, vol. 11, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[22] P. Keyl, M. Becker, et al., “Multimodal deep neural networks for pan-cancer survival prognosis,” Lancet Digit. Health, vol. 6, 2024.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[23] A. Mohamed, S. Ibrahim, et al., “Clinician exclusion and evaluation gaps in cancer XAI: Review,” Lancet Oncol., vol. 25, 2024.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[24] Z. Shen, Y. Liu, & J. Wang, “Interpretable machine learning models for disease prognosis: A review,” Artif. Intell. Rev., vol. 57, 2024.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[25] S. Vijay, G. R. Ramya, et al., “An Integrated Two Layered Voting (TLV) Framework for CAD Prediction,” IEEE Access, vol. 11, pp. 45120–45133, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[26] G. R. Ramya, M. Senthil, et al., “Explainable Machine Learning Framework for Diabetes & CVD Risk,” LNCS, vol. 13840, Springer, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[27] G. R. Ramya, S. V. Manoj, et al., “Understanding CNNs with Explainable AI & White Box AI,” in Proc. IJCACI, Springer Nature, pp. 139–153, 2025.", 7.8, False, MSO_THEME_COLOR.DARK_1, 2.5),
        ("[28] G. R. Ramya, R. Prabha, et al., “Predictive Machine Learning and Feature Selection for Clinical EHR,” CCIS, vol. 1780, Springer, 2023.", 7.8, False, MSO_THEME_COLOR.DARK_1, 0)
    ]
    set_shape_text(tb_c2, col2_refs)

    # =========================================================================
    # SLIDE 12: THANK YOU
    # =========================================================================
    slide12 = prs.slides[11]
    s_ty_box = get_shape_by_name(slide12, "Google Shape;241;p12")
    if s_ty_box:
        s_ty_box.height = 1900000
        tf = s_ty_box.text_frame
        tf.clear()
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        p0.space_after = Pt(12)
        clear_paragraph_bullets_and_indents(p0)
        r0 = p0.add_run()
        r0.text = "Questions & Discussion"
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(28)
        r0.font.bold = True
        r0.font.color.theme_color = MSO_THEME_COLOR.DARK_1

        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(4)
        clear_paragraph_bullets_and_indents(p1)
        r1 = p1.add_run()
        r1.text = "Sheela Akshar Sakhi · Presenting Author (aksharsakhi@gmail.com)"
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(17)
        r1.font.color.theme_color = MSO_THEME_COLOR.DARK_1

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(4)
        clear_paragraph_bullets_and_indents(p2)
        r2 = p2.add_run()
        r2.text = "Dr. Ramya G R · Corresponding Author (gr_ramya@cb.amrita.edu)"
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(16)
        r2.font.color.theme_color = MSO_THEME_COLOR.DARK_1

        p3 = tf.add_paragraph()
        p3.alignment = PP_ALIGN.CENTER
        p3.space_after = Pt(8)
        clear_paragraph_bullets_and_indents(p3)
        r3 = p3.add_run()
        r3.text = "Department of Computer Science and Engineering, Amrita Vishwa Vidyapeetham, Coimbatore, India"
        r3.font.name = "Times New Roman"
        r3.font.size = Pt(15)
        r3.font.color.theme_color = MSO_THEME_COLOR.DARK_1

        p4 = tf.add_paragraph()
        p4.alignment = PP_ALIGN.CENTER
        clear_paragraph_bullets_and_indents(p4)
        r4 = p4.add_run()
        r4.text = "Paper ID: 857   ·   Code: github.com/aksharsakhi/C-XAI"
        r4.font.name = "Times New Roman"
        r4.font.size = Pt(16)
        r4.font.bold = True
        r4.font.color.theme_color = MSO_THEME_COLOR.ACCENT_2

    out_path_submission = "CONF_PRESENTATION/SUBMISSION_READY/ICMLDE-2026-857.pptx"
    out_path_template = "CONF_PRESENTATION/templates/ICMLDE_2026_Paper_Presentation_Template.pptx"

    prs.save(out_path_submission)
    prs.save(out_path_template)
    print(f"Successfully generated main presentation:\n  1. {out_path_submission}\n  2. {out_path_template}")

if __name__ == "__main__":
    create_presentation()
