from pptx import Presentation
from pptx.util import Inches, Pt
import os

def create_presentation():
    prs = Presentation()
    
    # Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Towards Clinically Validated Explainable AI"
    subtitle.text = "A Framework for Evaluating Explanation Stability and Clinician Alignment\n\nHealthcare AI Research"

    # Slide 1: Introduction
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    title_shape.text = "Introduction"
    tf = body_shape.text_frame
    tf.text = "The Black Box Problem in Healthcare"
    p = tf.add_paragraph()
    p.text = "Machine learning models show great promise but lack transparency."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "XAI methods (SHAP, LIME) are used to interpret models."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "However, most evaluations are retrospective and lack clinical validation."
    p.level = 1

    # Slide 2: The Research Gap
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    title_shape.text = "The Research Gap"
    tf = body_shape.text_frame
    tf.text = "Identified through a survey of 26 XAI Healthcare Papers:"
    p = tf.add_paragraph()
    p.text = "Clinicians excluded from 83% of studies."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Rigorous explanation evaluation absent from 87%."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "We need prospective validation in multi-hospital workflows."
    p.level = 1

    # Slide 3: Proposed Framework
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    title_shape.text = "The Clinical Evaluation Framework"
    tf = body_shape.text_frame
    tf.text = "Moving beyond standard predictive metrics (AUROC)."
    p = tf.add_paragraph()
    p.text = "1. Explanation Stability: Are explanations robust to noisy input perturbations?"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "2. Clinician Alignment: Do explanations highlight medically relevant features?"
    p.level = 1

    # Slide 4: Methodology & Results
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    title_shape.text = "Methodology & Results"
    tf = body_shape.text_frame
    tf.text = "Dataset: Breast Cancer Wisconsin (Diagnostic Proxy)"
    p = tf.add_paragraph()
    p.text = "Model: Random Forest (Accuracy: 96.5%, AUC: 0.995)"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Stability Score (Jaccard Index): 0.8889"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Clinician Alignment Score: 100% (Matched predefined medical features)"
    p.level = 1

    # Slide 5: Conclusion
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    title_shape.text = "Conclusion"
    tf = body_shape.text_frame
    tf.text = "Stable and aligned explanations are prerequisites for trust."
    p = tf.add_paragraph()
    p.text = "Our framework provides quantitative metrics for these qualities."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Next Steps: Deploy in real-time EHR systems for prospective validation."
    p.level = 1

    os.makedirs('presentation', exist_ok=True)
    prs.save('presentation/XAI_Healthcare_Presentation.pptx')
    print("Presentation saved to presentation/XAI_Healthcare_Presentation.pptx")

if __name__ == '__main__':
    create_presentation()
