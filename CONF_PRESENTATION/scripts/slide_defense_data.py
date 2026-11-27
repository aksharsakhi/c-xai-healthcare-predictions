# slide_defense_data.py
# Complete technical reference data for all 12 presentation slides

SLIDES_DATA = [
    {
        "slide_num": 1,
        "title": "Title & Author Attribution",
        "core_message": "Establishes C-XAI as the first rigorous quantitative evaluation benchmark auditing explanation stability, cross-explainer discordance, and calibrated clinical decision utility in healthcare AI, accepted at ICMLDE 2026 (Elsevier Procedia Computer Science).",
        "key_terms": [
            ("C-XAI", "Clinical Explainable Artificial Intelligence. An open-source quantitative auditing framework and Python package for healthcare predictive models."),
            ("Explanation Stability (SbLip)", "The mathematical invariance of feature attribution rankings when clinical inputs experience small, realistic physiological noise."),
            ("Cross-Explainer Discordance (DXAI)", "The degree of pairwise rank-order disagreement among competing explainers (SHAP, LIME, Integrated Gradients) on the exact same patient."),
            ("Clinical Decision Utility (U_Clin)", "A decision-theoretic metric quantifying net clinician decision quality when relying on AI predictions and explanations, penalizing both over-reliance and under-reliance."),
            ("Elsevier Procedia Computer Science", "The official Scopus-indexed open-access conference proceedings publisher for ICMLDE 2026.")
        ],
        "technical_mechanics": [
            ("Paper Metadata", "Paper ID: 857. Title: 'C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI'. Track: Technical Session."),
            ("Authorship & Institutional Attribution", "Primary Presenter: Sheela Akshar Sakhi. Co-authors: Ibbraheem Shaik, Settibattini Suhitha. Faculty Supervisor & Corresponding Author: Dr. G. R. Ramya. Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore, Tamil Nadu, India."),
            ("Code & Artifact Availability", "Complete benchmark code, trained model checkpoints, and reproduction scripts are publicly hosted at: https://github.com/aksharsakhi/c-xai-healthcare-predictions.")
        ],
        "clinical_relevance": [
            ("The Clinical Motivation", "Clinicians in intensive care units and acute triage do not trust raw black-box AI predictions without explanations. However, if explanations are unstable or contradictory, clinicians suffer decision paralysis or make fatal triage errors."),
            ("Regulatory Urgency", "Both the FDA Software as a Medical Device (SaMD) Action Plan and the EU AI Act (Articles 13 & 14) now mandate verifiable transparency and algorithmic auditing before clinical deployment.")
        ],
        "tough_questions": [
            (
                "Why is this work titled C-XAI, and what makes it different from general XAI benchmarks?",
                "General XAI benchmarks like OpenXAI or Quantus evaluate explanations against synthetic ground truth or internal model weights on vision and NLP tasks. C-XAI is specifically designed for Clinical tabular EHR. It introduces the first quantitative auditing framework that stress-tests explanations under real physiological telemetry noise, measures pairwise discordance across explainers on acute patients, and grounds attributions against validated clinical scoring guidelines like SOFA and ASCVD."
            ),
            (
                "What is the commercial or practical readiness of this framework?",
                "C-XAI is packaged as a modular, pip-installable Python library (cxai-1.0.0) with standard .evaluate(), .benchmark(), and .compare() APIs. It operates out-of-the-box on scikit-learn tree ensembles, PyTorch neural networks, and standard tabular clinical data feeds."
            )
        ]
    },
    {
        "slide_num": 2,
        "title": "Introduction & Research Context",
        "core_message": "High predictive accuracy fails to guarantee safe clinical explanations. Over 85% of clinical XAI papers rely on anecdotal visual inspection, masking dangerous attribution volatility and confounding artifacts.",
        "key_terms": [
            ("Black-Box Dilemma", "High-capacity models (deep tabular neural nets, gradient boosted trees) achieve AUROC >= 0.96 but hide internal decision boundaries, preventing clinical validation."),
            ("Post-Hoc Explainability", "Methods (SHAP, LIME, Grad-CAM, Integrated Gradients) that extract feature attributions after a model has been trained without altering its weights."),
            ("Clinical Decision Support (CDS)", "Automated digital health systems providing active diagnostic, triage, or prognostic recommendations to medical staff."),
            ("Confounding Artifacts", "Non-causal spurious correlations (e.g., ICU bed assignment, hospital protocol tokens, recording time) that deep nets exploit to inflate accuracy without learning true pathology."),
            ("Anecdotal Visual Heatmaps", "The widespread practice of cherry-picking a few plausible-looking explanation plots in a paper without formal statistical testing across patient cohorts.")
        ],
        "technical_mechanics": [
            ("The Empirical Evidence", "Surveys by Roychowdhury et al. (npj Digit. Med. 2025) and Kyrimi et al. (2025) reveal that 83% of cancer XAI studies completely excluded clinicians from evaluation, and >85% lacked any quantitative metric for explanation quality."),
            ("The Accuracy-Reliability Decoupling", "Jin et al. (2023) demonstrated that models trained to minimize empirical cross-entropy loss can maximize AUROC by memorizing high-frequency sensor noise, resulting in chaotic local attribution vectors."),
            ("Figure 1: 5-Layer Auditing Architecture", "Ingests EHR feeds -> Injects Gaussian telemetry noise & missingness -> Evaluates tree vs. deep models -> Generates 6 post-hoc explainers -> Quantifies 4 formal auditing metrics -> Models clinician reliance calibration.")
        ],
        "clinical_relevance": [
            ("Patient Safety Hazard", "If an ICU model predicts high mortality for a septic patient because of a spurious hospital billing code rather than lactate levels, and the explanation hides this, doctors may withdraw care inappropriately."),
            ("Clinician Burnout & Alarm Fatigue", "When post-hoc explainers fluctuate between shifts, clinicians experience cognitive dissonance, leading to complete abandonment of the AI tool (algorithm aversion).")
        ],
        "tough_questions": [
            (
                "Why don't doctors just use inherently interpretable models like single decision trees or logistic regression?",
                "While single shallow decision trees and generalized additive models (GAMs) offer direct transparency, they suffer from a substantial performance penalty in high-dimensional EHR tasks. In acute multi-center sepsis (MIMIC-IV, eICU), single trees drop 8 to 12% in AUROC compared to ensembles, missing subtle non-linear multi-organ interactions. Clinicians require both high predictive sensitivity AND trustworthy explanations—which is why auditing complex models via C-XAI is essential."
            ),
            (
                "What do you mean by 'accuracy and explanation reliability are decoupled'?",
                "In traditional ML, practitioners assume that higher test accuracy implies better feature understanding. We prove mathematically and empirically that a model can achieve 89.4% accuracy by relying on fragile local decision boundary shortcuts. While its output label is correct, its explanation vector shifts by up to 49% under imperceptible noise (h=0.05). Accuracy measures the global label agreement; explanation reliability measures the local stability and causal grounding of the reasoning path."
            )
        ]
    },
    {
        "slide_num": 3,
        "title": "Problem Statement: The Clinical Explainability Gap",
        "core_message": "Explanations in clinical AI are fragile under physiological noise, contradictory across explainers, and detached from medical priors, driving up clinician triage error rates by up to 45%.",
        "key_terms": [
            ("Automation Bias & Over-Reliance", "The psychological phenomenon where clinicians uncritically follow erroneous AI advice because the presence of a visual explanation creates a false illusion of algorithmic competence (Bussone et al., Jacobs et al.)."),
            ("Algorithm Aversion & Under-Reliance", "The complete dismissal of correct AI alerts by clinicians after encountering erratic, unscientific, or conflicting explanations."),
            ("Physiological Sensor Noise (h=0.05)", "Baseline electronic telemetry drift, breathing motion artifacts, and transducer calibration errors. A noise radius of h=0.05 corresponds to standard deviations of ~3-5 mmHg blood pressure or ~2-4 bpm heart rate."),
            ("Medical Guidelines (SOFA & ASCVD)", "SOFA (Sequential Organ Failure Assessment) is the international standard for defining ICU sepsis. ASCVD (Atherosclerotic Cardiovascular Disease) is the ACC/AHA clinical standard for 10-year cardiac risk."),
            ("EU AI Act & FDA SaMD Mandates", "Article 13 requires High-Risk AI to be sufficiently transparent for users to interpret outputs. Article 14 requires technical design enabling human oversight to prevent automation bias. FDA SaMD mandates predetermined change control and real-world performance monitoring.")
        ],
        "technical_mechanics": [
            ("9.6x Instability Factor", "Under standard noise radius h=0.05, Tabular Deep ResNet exhibits an explanation instability of SbLip = 0.4912, whereas Extra Trees exhibits SbLip = 0.0512. The ratio 0.4912 / 0.0512 = 9.59x (~9.6x higher instability)."),
            ("40% Explainer Disagreement", "On deep neural nets, the average Spearman rank correlation between SHAP, LIME, and Integrated Gradients is only r_s = 0.565, meaning the discordance DXAI = 1 - 0.565 = 0.435 (exceeding 43.5% contradiction).")
        ],
        "clinical_relevance": [
            ("Who is Affected", "1. ICU Physicians: Subject to conflicting rationales during critical 15-minute triage windows. 2. Hospital Regulators: Risk legal liability under emerging AI governance laws. 3. Patients: At risk of fatal undertreatment or overtreatment.")
        ],
        "tough_questions": [
            (
                "How can providing an explanation increase clinician errors by 45%?",
                "Seminal clinical human-AI interaction studies by Bussone et al. and Jacobs et al. demonstrated that when clinicians are shown confident-looking visual heatmaps or feature bars for an incorrect AI prediction, their diagnostic error rate jumps by up to 45%. Clinicians assume that because the AI 'has an explanation,' it must be right, succumbing to confirmation bias and automation bias."
            ),
            (
                "Is h = 0.05 noise realistic, or is it an extreme stress-test?",
                "In normalized feature space (where features have zero mean and unit variance), h = 0.05 represents a perturbation of just 5% of one standard deviation. In an ICU, a patient's mean arterial pressure fluctuating from 75 to 78 mmHg or heart rate moving from 82 to 85 bpm easily exceeds 5% of variance. It is not an adversarial attack; it is routine bedside telemetry noise."
            )
        ]
    },
    {
        "slide_num": 4,
        "title": "Research Novelty: Why C-XAI is Necessary",
        "core_message": "C-XAI establishes a tri-fold novelty across theoretical mathematics, machine learning methodology, and clinical governance, bridging the gap between toy benchmarks and hospital deployment.",
        "key_terms": [
            ("Captum, OpenXAI, Quantus", "Existing XAI benchmarking toolkits. Captum provides PyTorch attribution algorithms. OpenXAI benchmarks synthetic infidelity. Quantus collects image/NLP metrics. None evaluate clinical guidelines or decision utility."),
            ("Pauker-Kassirer Decision Threshold", "A seminal medical decision-theory formulation (NEJM 1975). A clinician should treat if disease probability p > T = Harm / (Harm + Benefit). C-XAI models clinician reliance around this threshold with asymmetric penalties alpha=0.50 and beta=0.30."),
            ("1D Earth Mover's Distance (Wasserstein-1)", "The minimal work required to transform one probability distribution into another along a metric space. In 1D, it equals the integral of absolute differences between cumulative distribution functions."),
            ("Zeroth-Order Gaussian Smoother", "Convolving a discontinuous, step-function tree model with a Gaussian score kernel to estimate continuous gradients via Monte Carlo sampling without needing differentiability."),
            ("ScaL-PGD Attribution Attack", "Scaled Projected Gradient Descent attack that perturbs inputs to maximize attribution shift while constraining the output label to remain unchanged.")
        ],
        "technical_mechanics": [
            ("Theoretical Proof: (d-1) Normalization Upper Bound", "For two discrete probability distributions supported on d ordered feature bins {1, 2, ..., d}, the maximum possible 1D Wasserstein distance occurs when all mass of P is at bin 1 and all mass of Q is at bin d. Then W_1(P, Q) = sum_{k=1}^{d-1} |1 - 0| = d - 1. Thus, dividing by (d - 1) strictly normalizes W_Clin^norm in [0, 1]."),
            ("Zeroth-Order Gradient Derivation", "For discontinuous tree f(x), define f_sigma(x) = E_{u ~ N(0, sigma^2 I)}[f(x + u)]. By Stein's lemma / log-derivative trick: nabla f_sigma(x) = (1 / sigma^2) * E[f(x + u) * u]. This enables computing gradient-based explainers (SmoothGrad, Integrated Gradients) on non-differentiable tree ensembles.")
        ],
        "clinical_relevance": [
            ("Clinical Governance Fulfillment", "Directly addresses FDA SaMD predetermined change control requirements and EU AI Act Articles 13 & 14 by providing objective, quantitative thresholds for explanation stability and guideline compliance.")
        ],
        "tough_questions": [
            (
                "Why did you choose alpha = 0.50 and beta = 0.30 for decision utility penalties?",
                "In medical decision theory and acute clinical triage (e.g. ICU sepsis), false reassurance (over-reliance on a false-negative AI prediction) causes delayed antibiotic administration, leading to septic shock and death. Conversely, under-reliance (ignoring a true positive) leads to redundant manual diagnostics. Over-reliance carries higher direct patient mortality risk than under-reliance. Hence, we set alpha = 0.50 (over-reliance penalty) > beta = 0.30 (under-reliance penalty), directly mirroring clinical risk asymmetry."
            ),
            (
                "How can you compute Integrated Gradients on random forests if trees are not differentiable?",
                "Standard Integrated Gradients requires evaluating the gradient of the model along a straight path from baseline to input. Because decision trees are piecewise-constant step functions, their classical gradients are zero almost everywhere and undefined at split boundaries. We solved this by implementing a Zeroth-Order Gaussian Smoother: we convolve the tree ensemble with an isotropic Gaussian kernel (sigma = 0.05, M = 100 draws). This produces an infinitely differentiable expectation surface whose gradients are computed via the score function estimator."
            )
        ]
    },
    {
        "slide_num": 5,
        "title": "Proposed Methodology: The C-XAI Auditing Framework",
        "core_message": "A structured 4-layer auditing architecture ingesting multi-center EHR, evaluating tree vs. deep models, computing 6 diverse explainers, and auditing via 4 mathematically grounded metrics.",
        "key_terms": [
            ("Layer 1: Data & Perturbation Layer", "Standardizes 4 clinical cohorts, injects Gaussian noise u_m ~ N(0, h^2 I), 20% MCAR missingness, and gradient-crafted adversarial shifts."),
            ("MCAR (Missing Completely At Random)", "Clinical data missingness where the probability of being missing is independent of both observed and unobserved data (e.g., random laboratory batch delays)."),
            ("Layer 2: Predictive Modeling Layer", "Trains Random Forest, Extra Trees (with Zeroth-Order Smoother), Multi-Layer Perceptron (MLP), and Tabular Deep ResNet with feature tokenization."),
            ("Layer 3: Post-Hoc Explainer Layer", "Evaluates 6 explainers spanning 4 mathematical families: TreeSHAP, KernelSHAP, LIME, SmoothGrad, Integrated Gradients, and Permutation Feature Importance (PFI)."),
            ("Layer 4: Quantitative Auditing Layer", "Computes SbLip (stability), DXAI (discordance), W_Clin^norm (prior distance), and U_Clin_hat (net decision utility).")
        ],
        "technical_mechanics": [
            ("Metric 1: Local Lipschitz Stability Formula", "SbLip(x; f, E, h) = (1/M) * sum_{m=1}^M [ ||E_f(x + delta_m) - E_f(x)||_2 / (||delta_m||_2 + epsilon_0) ], where delta_m ~ N(0, h^2 I), M = 100 Monte Carlo draws, h = 0.05, epsilon_0 = 1e-6."),
            ("Metric 2: Cross-Explainer Discordance Formula", "DXAI(x; f) = 1 - [2 / (K(K - 1))] * sum_{j < k} r_s(E_j(x), E_k(x)), where r_s is Spearman rank correlation across K=6 explainers. Range is [0, 2]."),
            ("Metric 3: Dimension-Normalized Prior Alignment Formula", "W_Clin^norm(x) = W_1(E_norm(x), P_clin) / (d - 1) = [1 / (d - 1)] * sum_{j=1}^{d-1} |F_E(j) - F_clin(j)|, where F are cumulative attribution distributions."),
            ("Metric 4: In-Silico Clinical Utility Formula", "U_Clin = w_s * (1 - SbLip) + w_d * (1 - DXAI) + w_p * (1 - W_Clin^norm) + w_c * (1 - Loss_rel), with weights w_s=0.30, w_d=0.25, w_p=0.25, w_c=0.20.")
        ],
        "clinical_relevance": [
            ("Baseline Selection for Integrated Gradients", "In computer vision, a black image (all zeros) is a valid baseline. In medicine, setting all features to zero is biologically impossible (e.g., blood pressure = 0 mmHg, body temp = 0 C is fatal). We establish the median physiological value across healthy survivors as the baseline x', guaranteeing physiologically grounded path integration.")
        ],
        "tough_questions": [
            (
                "Why evaluate 6 different explainers instead of just SHAP?",
                "Different explainers are based on completely different mathematical axioms: TreeSHAP uses cooperative game theory with tree path conditioning; KernelSHAP uses weighted linear regression; LIME uses localized perturbation surrogates; SmoothGrad and Integrated Gradients use gradient path integrals. In clinical practice, hospitals deploy whatever explainer their software vendor supports. If different explainers give contradictory advice on the same patient, clinicians cannot know which to trust. Evaluating all 6 proves whether explainer consensus exists."
            ),
            (
                "What baseline did you choose for Integrated Gradients on clinical data?",
                "We set the baseline vector x' to the median feature values computed across healthy survivors in the training cohort. This represents a normal, stable physiological state. Path integration from this baseline directly measures how a patient's abnormal vitals and lab values deviate from healthy equilibrium."
            )
        ]
    },
    {
        "slide_num": 6,
        "title": "Experimental Setup & Auditing Protocol",
        "core_message": "Rigorous multi-cohort evaluation across 51,369 records spanning MIMIC-IV, eICU, BCWD, and Cardio EHR, evaluated over 50 stratified cross-validation trials (seeds 42–91).",
        "key_terms": [
            ("MIMIC-IV ($N=40,000$ encounters)", "Beth Israel Deaconess Medical Center ICU database. Task: ICU Sepsis-3 mortality prediction. Clinical priors: SOFA score (0.35), Serum Lactate (0.30), MAP (0.20), Age (0.15)."),
            ("eICU ($N=10,000$ encounters)", "Multi-center Philips healthcare ICU database across multiple US hospitals. Task: Acute hospital mortality. Clinical priors: MAP (0.40), WBC count (0.20), Creatinine (0.20), Temperature (0.20)."),
            ("BCWD ($N=569$ encounters)", "Wisconsin Breast Cancer Diagnostic dataset. Task: Malignancy classification from fine-needle aspirates. Clinical priors: Nottingham Prognostic Index (NPI) morphometry: Mean Area & Concavity (0.25), Perimeter (0.25), Texture (0.25), Radius (0.25)."),
            ("Cardio EHR ($N=800$ encounters)", "Cardiovascular risk cohort. Task: 10-year CVD risk. Clinical priors: ACC/AHA pooled cohort ASCVD equations: Systolic BP (0.30), Age (0.25), Total Cholesterol (0.25), Smoking (0.20)."),
            ("Stratified 5-Fold Cross-Validation (50 Seeds)", "50 independent repetitions with seeds 42 to 91. Guarantees that class imbalance is preserved across folds and eliminates random split bias.")
        ],
        "technical_mechanics": [
            ("Hardware & Software Reproducibility", "Hardware: Apple Silicon M-series & Linux x86_64, 16 GB RAM. Software: Python 3.10+, PyTorch 2.14, Scikit-learn, Captum, SHAP, SciPy. Fully deterministic execution with seeded random generators."),
            ("Feature Normalization & Missingness", "Numerical features standardized via z-score scaling: x_scaled = (x - mu) / sigma. Missing values in validation folds imputed using training-fold medians to prevent data leakage.")
        ],
        "clinical_relevance": [
            ("Multi-Center Generalizability", "Evaluating on single-hospital data creates models that overfit local practice patterns. Combining single-center ICU (MIMIC-IV), multi-center ICU (eICU), oncology (BCWD), and cardiology (Cardio EHR) proves that C-XAI generalizes across diverse clinical specialties.")
        ],
        "tough_questions": [
            (
                "Are the clinical prior weights P_clin subjective?",
                "No. The prior weights are directly codified from international medical consensus guidelines: Sepsis-3 definitions (Singer et al., JAMA 2016) prioritize organ failure via SOFA and cellular hypoperfusion via lactate; the Nottingham Prognostic Index (NPI) governs breast pathology; and ACC/AHA pooled cohort equations govern cardiovascular risk. Furthermore, we conducted a sensitivity analysis perturbing prior weights by +/- 20%: the ranking of models remained 100% invariant."
            ),
            (
                "Why run 50 random trials instead of standard 5-fold cross-validation?",
                "In medical ML, small sample variations can produce false statistical significance. Running 50 random trials across seeds 42 to 91 produces 250 trained model instances per architecture. This allows us to perform rigorous non-parametric hypothesis testing (Wilcoxon signed-rank test and paired t-tests) with true statistical power, proving that our findings are not random artifacts."
            )
        ]
    },
    {
        "slide_num": 7,
        "title": "Results: Accuracy vs. Clinical Explanation Reliability",
        "core_message": "Extra Trees delivers +19.6% higher clinical decision utility (0.849 vs. 0.711, p < 0.001) over Tabular Deep ResNet on MIMIC-IV, despite deep nets achieving slightly higher raw accuracy.",
        "key_terms": [
            ("Relative Utility Gain (+19.6%)", "Calculated as (0.8485 - 0.7095) / 0.7095 = +0.1390 / 0.7095 = +19.59% (~19.6%). Absolute gain: +13.9 percentage points."),
            ("Wilcoxon Signed-Rank Test (W = 0.0)", "A non-parametric paired hypothesis test. W = 0.0 is the theoretical minimum test statistic, meaning Extra Trees achieved higher utility than Deep ResNet in 100% of the 50 trials (50 out of 50 wins, zero ties or losses, p < 0.001)."),
            ("Paired t-test (t = 14.82, p < 0.001)", "Parametric test confirming overwhelming statistical significance across the 50 paired cross-validation seeds."),
            ("Cohen's d = 2.96", "Standardized effect size metric. Conventionally, d = 0.2 is small, 0.5 is medium, 0.8 is large. A Cohen's d of 2.96 represents an enormous, definitive separation between distributions."),
            ("Inference Latency Advantage", "Extra Trees requires 4.2 ms per patient encounter; Random Forest requires 6.8 ms; Tabular Deep ResNet requires 48.5 ms (11.5x slower).")
        ],
        "technical_mechanics": [
            ("MIMIC-IV Benchmark Breakdown Table",
             "Tabular Deep ResNet: Acc = 89.35%, AUC = 0.913, SbLip = 0.4912, DXAI = 0.435, W_Clin^norm = 0.044, U_Clin = 0.7107.\n"
             "MLP Classifier: Acc = 89.20%, AUC = 0.907, SbLip = 0.4850, DXAI = 0.412, W_Clin^norm = 0.039, U_Clin = 0.7120.\n"
             "Random Forest: Acc = 88.45%, AUC = 0.899, SbLip = 0.0821, DXAI = 0.081, W_Clin^norm = 0.029, U_Clin = 0.8412.\n"
             "Extra Trees (C-XAI): Acc = 88.12%, AUC = 0.903, SbLip = 0.0512, DXAI = 0.059, W_Clin^norm = 0.031, U_Clin = 0.8485*.")
        ],
        "clinical_relevance": [
            ("The Clinical Triage Tradeoff", "Deep ResNet gains +1.2% in raw accuracy (89.4% vs 88.1%) but suffers a 9.6x explosion in explanation instability and a 7.4x increase in explainer conflict. In an ICU, trading 9.6x worse reliability for 1.2% accuracy is a dangerous, indefensible clinical tradeoff.")
        ],
        "tough_questions": [
            (
                "Why would a hospital choose an 88.1% accurate model over an 89.4% accurate model?",
                "Because raw accuracy in healthcare is an incomplete metric. The 1.2% accuracy margin in Deep ResNet is achieved by memorizing high-frequency non-causal correlations. In exchange, the model's explanations fluctuate by 49% under routine vital sign noise and disagree with competing explainers 43% of the time. When doctors see conflicting or jittery explanations, they lose trust and either reject the AI completely or make catastrophic triage errors. Extra Trees provides 88.1% accuracy with stable, guideline-aligned explanations, yielding +19.6% higher clinical utility."
            ),
            (
                "Why did Extra Trees outperform Random Forest in explanation stability (0.051 vs. 0.082)?",
                "Random Forest optimizes split cut-points deterministically using Gini impurity or entropy, which can produce sharp, brittle decision boundaries tailored to training sample quirks. Extra Trees (Extremely Randomized Trees) draws split thresholds completely at random for each candidate feature and selects the best of these random splits. This extreme randomization acts as an ensemble-level regularizer, producing smoother, less brittle decision boundaries with lower variance."
            )
        ]
    },
    {
        "slide_num": 8,
        "title": "Results: Explainer Discordance & Accuracy Decoupling",
        "core_message": "Tree ensembles achieve tight consensus across explainers (DXAI = 0.059), whereas Deep ResNet exhibits severe cross-explainer conflict (DXAI = 0.435, 7.4x higher). AUROC has near-zero correlation with explanation quality (R^2 = 0.04).",
        "key_terms": [
            ("DXAI Range [0, 2]", "Spearman rank correlation r_s ranges from -1 to +1. DXAI = 1 - r_s. If explainers perfectly agree, r_s = +1 -> DXAI = 0. If uncorrelated, r_s = 0 -> DXAI = 1. If explainers completely invert rankings, r_s = -1 -> DXAI = 2."),
            ("Tree Agreement (94.1%)", "On Extra Trees, mean r_s across TreeSHAP, KernelSHAP, and LIME is 0.941, corresponding to DXAI = 0.059 (94.1% consensus)."),
            ("Neural Disagreement (56.5% Agreement)", "On Tabular Deep ResNet, mean r_s across Integrated Gradients, SmoothGrad, and LIME is 0.565, corresponding to DXAI = 0.435 (7.4x higher disagreement)."),
            ("Accuracy Decoupling Theorem (R^2 = 0.04)", "Linear regression between predictive AUROC and clinical utility across all models and cohorts yields R^2 = 0.038 (~0.04, p = 0.42), proving that AUROC explains less than 4% of explanation utility variance."),
            ("The Disagreement Problem", "Originally identified by Krishna et al. (ACM CHI 2022) as an empirical dilemma. C-XAI formalizes it into a bounded metric and proves that model architecture (trees vs deep nets) is the primary driver.")
        ],
        "technical_mechanics": [
            ("Pairwise Explainer Matrix Breakdown (MIMIC-IV)",
             "Tree Ensemble Matrix: TreeSHAP vs KernelSHAP = 0.042; TreeSHAP vs LIME = 0.059; KernelSHAP vs LIME = 0.075. Mean DXAI = 0.059.\n"
             "Tabular Deep ResNet Matrix: IntGrad vs SmoothGrad = 0.312; IntGrad vs LIME = 0.435; SmoothGrad vs LIME = 0.458. Mean DXAI = 0.435.")
        ],
        "clinical_relevance": [
            ("The Clinician Dilemma", "If a clinician consults an AI system that runs Integrated Gradients, it highlights Serum Lactate as the primary risk factor. If the hospital IT runs LIME, it highlights Patient Age. The clinician faces contradictory rationales for the same patient, causing decision paralysis.")
        ],
        "tough_questions": [
            (
                "Why did you use Spearman rank correlation instead of Pearson or Cosine similarity?",
                "Clinicians in emergency triage do not read continuous attribution floating-point numbers (e.g. +0.0342 vs +0.0289). Clinicians process the top-k ranked clinical factors (e.g., 'What are the top 3 drivers of sepsis risk?'). Spearman rank correlation operates strictly on the ordinal permutation of feature importance, directly matching human cognitive decision-making. Cosine similarity is overly sensitive to vector magnitude scaling rather than rank order."
            ),
            (
                "If SHAP and LIME disagree on a patient in Deep ResNet, which one is right?",
                "Neither can be definitively trusted in isolation. The disagreement itself is mathematical proof that the underlying deep model has learned a highly convoluted, non-convex decision boundary where local linear surrogates (LIME) and path integrals (Integrated Gradients) project radically different tangent approximations. The solution is not to pick an explainer, but to switch to an architecture like Extra Trees where all explainers converge to consensus."
            )
        ]
    },
    {
        "slide_num": 9,
        "title": "Discussion: Insights, Robustness & Regulatory Impact",
        "core_message": "Resolves the Representation Paradox: deep nets form chaotic gradient manifolds that collapse under noise, while tree ensembles form stable piecewise-constant partitions. Fulfills FDA and EU AI Act mandates.",
        "key_terms": [
            ("The Representation Paradox", "The counter-intuitive empirical rejection of the hypothesis that continuous neural networks produce smoother explanations than step-function trees."),
            ("Axis-Aligned Hyper-Rectangles", "The geometric decision cells formed by orthogonal splits in decision trees. Within each leaf cell, the prediction is constant."),
            ("Gradient Shattering / Saturation", "In deep networks with non-linear activations (ReLU, Swish), gradients can oscillate rapidly across tiny input neighborhoods (gradient shattering), creating high attribution sensitivity."),
            ("Sub-Linear vs. Supra-Linear Scaling", "As sensor noise h increases from 0.01 to 0.20, Extra Trees explanation instability grows sub-linearly (0.018 to 0.103), while deep models scale supra-linearly (>12x degradation)."),
            ("Adversarial Attribution Collapse", "Under ScaL-PGD attacks, neural explainers completely collapse to DXAI > 1.84 (near-total rank inversion), while tree ensembles remain robust (DXAI <= 0.312).")
        ],
        "technical_mechanics": [
            ("Mathematical Explanation of the Paradox",
             "Let x be a patient vector inside tree leaf cell R_k. For any perturbation delta such that (x + delta) in R_k, f(x + delta) = f(x). The attribution E_f(x + delta) is strictly identical to E_f(x). Thus, ||E_f(x + delta) - E_f(x)||_2 = 0, giving zero instability within the cell!\n"
             "In deep networks, f(x) = W_L * sigma(W_{L-1} ... sigma(W_1 x)). The gradient nabla_x f(x) depends continuously on all intermediate activations. In tabular data with unnormalized feature correlations, the Hessian nabla^2 f(x) has large eigenvalues, meaning tiny delta produces massive gradient shifts.")
        ],
        "clinical_relevance": [
            ("Regulatory Alignment: FDA SaMD & EU AI Act",
             "FDA Good Machine Learning Practice (GMLP) Principle 7 requires risk-based monitoring of clinical model outputs. EU AI Act Article 13 mandates that high-risk systems be interpretable, and Article 14 requires human oversight measures. C-XAI provides the exact quantitative metrics (SbLip <= 0.10, DXAI <= 0.10) to certify compliance.")
        ],
        "tough_questions": [
            (
                "Aren't decision tree boundaries discontinuous? How can a discontinuous function be more stable than a smooth neural net?",
                "This is the core insight of our paper. While decision trees are discontinuous at cell boundaries, the volume of the interior of leaf cells is massive compared to the boundary surface area. For 95% of random physiological noise draws, the perturbed point (x + delta) remains within the same hyper-rectangle, where the attribution is 100% constant. In contrast, neural networks are continuous but have steep, highly curved manifolds with large second derivatives (Hessians). Continuous does not mean flat—and steep slopes create massive explanation instability."
            ),
            (
                "How does C-XAI operationalize EU AI Act compliance?",
                "The EU AI Act classifies clinical diagnostic AI as 'High-Risk AI Systems'. Article 13 mandates that models be accompanied by instructions enabling users to interpret outputs. Article 14 mandates human oversight to prevent automation bias. C-XAI operationalizes this by generating an automated audit report before clinical deployment. If a model has DXAI > 0.15 or SbLip > 0.15, it fails certification and cannot be deployed in clinical workflows."
            )
        ]
    },
    {
        "slide_num": 10,
        "title": "Conclusion & Future Scope",
        "core_message": "C-XAI establishes an objective pre-deployment auditing standard. High accuracy is not enough for medical AI; tree ensembles decisively dominate deep tabular nets in explanation stability and clinical decision utility.",
        "key_terms": [
            ("Summary of Contributions", "1. Formulated 4 mathematical metrics (SbLip, DXAI, W_Clin^norm, U_Clin). 2. Created Zeroth-Order Gaussian Smoother. 3. Proved Accuracy-Explainability Decoupling across 51.3K records. 4. Established pre-deployment regulatory standard."),
            ("Multimodal Clinical Expansion", "Future roadmap: Extending C-XAI from tabular EHR to multimodal ICU telemetry, BioClinicalBERT progress notes, and chest radiograms."),
            ("Dynamic Trajectory Auditing", "Developing temporal Lipschitz stability metrics for continuous ICU vital sign streams across recurrent networks (LSTM) and clinical transformers."),
            ("Prospective Clinician Reader Trials", "Conducting human-in-the-loop simulation trials measuring diagnostic speed, error rates, and cognitive load among real ICU physicians.")
        ],
        "technical_mechanics": [
            ("The Tri-Partite Conclusion", "1. Empirical: Tree ensembles achieve +19.6% higher clinical utility. 2. Methodological: Post-hoc explanations must be audited before clinical deployment. 3. Theoretical: Continuous representations induce explanation fragility on tabular data.")
        ],
        "clinical_relevance": [
            ("The Ultimate Clinical Takeaway", "Deploying healthcare AI models based purely on AUROC without explanation auditing introduces silent, fatal triage hazards into hospitals.")
        ],
        "tough_questions": [
            (
                "What is the single most important takeaway you want the conference audience to remember?",
                "Never trust a healthcare AI model based on high AUROC alone. In acute medical settings, high accuracy frequently masks severe explanation instability and explainer contradiction. By using C-XAI, hospitals can audit models before deployment, ensuring that explanations remain stable under sensor noise and align with validated clinical guidelines."
            ),
            (
                "What are the primary limitations of your current study?",
                "We identify three clear limitations: First, our evaluation is focused on structured tabular EHR data; extending C-XAI to high-frequency continuous waveforms and medical imaging is underway. Second, while our decision utility metric models clinician reliance based on established medical decision theory, formal prospective clinical reader trials in ICU simulation centers are the next validation step. Third, clinical prior vectors were defined for four major diseases and will be expanded across additional clinical subspecialties."
            )
        ]
    },
    {
        "slide_num": 11,
        "title": "References & Literature Context",
        "core_message": "Grounded in foundational works in explainable AI (Lundberg NeurIPS'17, Ribeiro SIGKDD'16, Sundararajan ICML'17, Krishna CHI'22), healthcare benchmarks (Johnson Sci. Data'23, Pollard Sci. Data'23), and prior institutional research (Ramya et al.).",
        "key_terms": [
            ("Lundberg & Lee (NeurIPS 2017) [1]", "SHAP: Unified framework for interpreting predictions using Shapley values."),
            ("Ribeiro et al. (SIGKDD 2016) [2]", "LIME: Local Interpretable Model-agnostic Explanations using sparse linear surrogates."),
            ("Sundararajan et al. (ICML 2017) [3]", "Integrated Gradients: Axiomatic attribution for neural networks satisfying Completeness and Implementation Invariance."),
            ("Krishna et al. (ACM CHI 2022) [9]", "The Disagreement Problem in Explainable AI: Empirical evidence that explainers disagree in practice."),
            ("Ramya et al. (2023, 2025) [25-28]", "Prior peer-reviewed research by faculty supervisor Dr. G. R. Ramya on Two-Layered Voting frameworks, Explainable ML for Diabetes/CVD Risk (Springer LNCS), and White-Box AI (Springer Nature 2025).")
        ],
        "technical_mechanics": [
            ("Literature Lineage", "C-XAI directly addresses the open challenge posed by Krishna et al. (CHI'22) by providing mathematical metrics to resolve the disagreement problem, and operationalizes the evaluation principles advocated by Caruana et al. (ACM Comput. Surv. 2023).")
        ],
        "clinical_relevance": [
            ("Scientific Rigor", "Demonstrates strong foundational alignment with international peer-reviewed literature across AI, computational biology, and medical informatics.")
        ],
        "tough_questions": [
            (
                "How does your work advance beyond Krishna et al.'s CHI 2022 paper on explainer disagreement?",
                "Krishna et al. conducted an empirical study highlighting that explainers disagree, but they concluded with a dilemma, offering no metric to evaluate or resolve it. C-XAI makes two decisive advances: First, we formulate the Cross-Explainer Discordance metric DXAI bounded in [0, 2] and integrate it into a decision-theoretic utility framework. Second, we discover that the disagreement problem is architecture-dependent: while neural nets exhibit severe disagreement (DXAI = 0.435), tree ensembles resolve the disagreement problem naturally (DXAI = 0.059)."
            )
        ]
    },
    {
        "slide_num": 12,
        "title": "Thank You, Open Defense & General Viva Strategy",
        "core_message": "Concluding slide inviting questions from the audience, session chairs, and reviewers, backed by the 3 Golden Rules of Technical Defense.",
        "key_terms": [
            ("Presenting Author", "Sheela Akshar Sakhi (aksharsakhi@gmail.com)"),
            ("Corresponding Author", "Dr. Ramya G R (gr_ramya@cb.amrita.edu)"),
            ("Paper ID", "857"),
            ("Track", "Technical Session, ICMLDE 2026, Dehradun, India")
        ],
        "technical_mechanics": [
            ("The 3 Golden Rules of Technical Defense",
             "Rule 1: Acknowledge & Bridge: 'That is an excellent point. In our clinical framework, we addressed this by...'\n"
             "Rule 2: Ground in Concrete Numbers: Always cite specific metrics: 'Extra Trees achieved +19.6% utility with W=0.0 and p<0.001 across 50 seeds, whereas Deep ResNet suffered 9.6x higher instability (0.491 vs 0.051).'\n"
             "Rule 3: Frame Boundaries as Controlled Scope: 'Our study specifically focused on acute tabular EHR; extending to temporal waveforms is our defined future work.'")
        ],
        "clinical_relevance": [
            ("Professional Composure", "Demonstrates deep subject matter mastery, statistical maturity, and clinical empathy under tough academic examination.")
        ],
        "tough_questions": [
            (
                "If you had to summarize your paper in one sentence, what would you say?",
                "C-XAI proves that high predictive accuracy in healthcare AI masks dangerous explanation instability and explainer conflict, and provides the first quantitative auditing benchmark showing that tree ensembles deliver 19.6% higher clinical decision utility than deep neural networks."
            )
        ]
    }
]
