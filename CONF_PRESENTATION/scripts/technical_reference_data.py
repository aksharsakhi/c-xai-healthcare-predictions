# technical_reference_data.py
# Formal Slide-by-Slide Technical Reference Data for ICMLDE 2026 (Paper ID: 857)
# Markup tags supported by build_technical_reference.py:
#   <b>...</b>, <i>...</i>, <sub>...</sub>, <sup>...</sup>

SLIDES_DATA = [
    {
        "slide_num": 1,
        "title": "Title, Authorship & Framework Scope",
        "overview": "Establishes the scope of Paper ID 857: C-XAI (Clinical Explainable AI), a quantitative auditing benchmark for explanation stability, cross-explainer discordance, clinical prior alignment, and calibrated decision utility in tabular healthcare AI.",
        "terminology": [
            ("C-XAI (Clinical Explainable AI)", "An open-source quantitative auditing framework and modular Python package (cxai-1.0.0) designed to audit post-hoc feature attributions for clinical tabular predictive models."),
            ("Explanation Stability (Ŝ<sub>Lip</sub>)", "Empirical Local Lipschitz Stability Index measuring the sensitivity of feature attribution vectors under bounded physiological sensor perturbations (noise radius h = 0.05)."),
            ("Cross-Explainer Discordance (D<sub>XAI</sub>)", "Pairwise rank-order disagreement across competing post-hoc explainers (SHAP, LIME, Integrated Gradients, SmoothGrad, PFI) evaluated on the same patient encounter."),
            ("Clinical Prior Alignment (W<sub>Clin</sub><sup>norm</sup>)", "Dimension-normalized 1D Wasserstein (Earth Mover's) distance between normalized model feature attributions and codified clinical guideline weightings (e.g., SOFA, ASCVD, NPI)."),
            ("Calibrated Clinical Utility (Û<sub>Clin</sub>)", "Decision-theoretic utility metric combining model accuracy, clinician trust calibration (T<sub>Clin</sub>), and asymmetric over-/under-reliance error penalties."),
            ("Elsevier Procedia Computer Science", "Scopus-indexed open-access conference proceedings series publishing the 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026).")
        ],
        "mechanics": [
            ("Publication & Track Metadata", "Paper ID: 857. Title: 'C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI'. Track: Technical Session (ICMLDE 5.0, 27–28 November 2026, UPES Dehradun, India)."),
            ("Authorship & Affiliation", "Sheela Akshar Sakhi (Presenting Author, aksharsakhi@gmail.com), Ibbraheem Shaik, Settibattini Suhitha, and Dr. Ramya G R (Corresponding Author, gr_ramya@cb.amrita.edu). Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore, India."),
            ("Implementation & Package API", "Implemented as a modular Python toolkit exposing standard .evaluate(), .benchmark(), and .compare() interfaces supporting scikit-learn tree ensembles and PyTorch neural networks at https://github.com/aksharsakhi/c-xai-healthcare-predictions.")
        ],
        "clinical_context": [
            ("Domain Specificity vs. General XAI Suites", "General-purpose benchmarks such as OpenXAI and Quantus evaluate synthetic infidelity or weight fidelity on vision and NLP datasets. C-XAI targets structured electronic health record (EHR) tabular models under realistic physiological noise and medical prior constraints."),
            ("Regulatory Context", "Designed to provide verifiable quantitative metrics aligned with the FDA Software as a Medical Device (SaMD) Action Plan and EU AI Act Articles 13 and 14.")
        ],
        "rationales": [
            ("Scope Distinction", "Unlike generic saliency benchmarks that evaluate pixels or text tokens, C-XAI focuses specifically on high-stakes tabular EHR decision pipelines where continuous physiological noise and multi-feature clinical guidelines govern deployment safety.")
        ]
    },
    {
        "slide_num": 2,
        "title": "Introduction & Research Context",
        "overview": "Establishes the healthcare AI black-box dilemma, quantifies the auditing void across clinical XAI literature, and introduces the 5-layer C-XAI auditing pipeline.",
        "terminology": [
            ("Black-Box Dilemma", "High-capacity models (deep tabular neural networks and gradient-boosted/randomized ensembles) achieve AUROC ≥ 0.96 on clinical datasets while obscuring internal decision logic from clinicians (Muhammad & Bendechache, 2024)."),
            ("Post-Hoc Explainability", "Attribution algorithms applied after model training (TreeSHAP, KernelSHAP, LIME, Integrated Gradients, SmoothGrad, PFI) without modifying the underlying predictive architecture."),
            ("Clinical Decision Support (CDS)", "Algorithmic systems providing diagnostic, prognostic, or acute triage risk estimates in hospital workflows such as Intensive Care Units (ICUs)."),
            ("Confounding Artifacts", "Spurious, non-causal correlations (e.g., ICU unit codes, laboratory timing metadata, billing indicators) exploited to elevate global accuracy without reflecting genuine pathophysiology."),
            ("Anecdotal Visual Inspection", "Qualitative evaluation relying on selected heatmaps or bar plots for individual patients without cohort-wide statistical robustness verification.")
        ],
        "mechanics": [
            ("Literature Auditing Gap", "Systematic reviews (Roychowdhury et al., npj Digit. Med. 2025; Kyrimi et al., 2025) report that >85% of clinical XAI studies omit quantitative explanation reliability metrics and 83% of oncology XAI evaluations omit clinician validation."),
            ("Accuracy-Reliability Decoupling", "Jin et al. (2023) established that minimizing cross-entropy loss can produce high AUROC via brittle local decision boundary shortcuts, yielding volatile attribution vectors under minor input perturbations."),
            ("5-Layer Auditing Pipeline (Fig. 1)", "Ingests multi-hospital EHR cohorts → Injects physiological Gaussian noise and adversarial shifts → Trains tree and deep neural baselines → Generates 6 post-hoc explainers → Evaluates 4 auditing metrics and calibrated reliance.")
        ],
        "clinical_context": [
            ("Clinical Safety Implications", "When an acute sepsis model achieves high accuracy via spurious hospital metadata while generating unstable explanations, clinicians lack verifiable insight into physiological drivers such as lactate or organ dysfunction."),
            ("Clinician Trust & Algorithm Aversion", "Inconsistent explanations across consecutive measurements erode clinical confidence, contributing to alert fatigue and abandonment of decision support tools.")
        ],
        "rationales": [
            ("Auditing Complex Models vs. Shallow Interpretable Models", "Single shallow decision trees and basic generalized additive models (GAMs) offer intrinsic transparency but incur an 8–12% AUROC degradation on high-dimensional multi-center sepsis cohorts (MIMIC-IV, eICU). Auditing high-performing ensembles preserves diagnostic sensitivity while verifying explanation stability."),
            ("Basis for Accuracy-Reliability Decoupling", "Global classification accuracy evaluates label agreement across a test set, whereas explanation reliability evaluates the local smoothness, rank invariance, and clinical plausibility of the feature attribution gradient/path around each patient point.")
        ]
    },
    {
        "slide_num": 3,
        "title": "Problem Statement: The Clinical Explainability Gap",
        "overview": "Characterizes the three core failure modes of current clinical explanations—noise fragility (9.6×), cross-explainer conflict (>40%), and guideline detachment—and identifies affected stakeholders.",
        "terminology": [
            ("Automation Bias (Over-Reliance)", "Tendency of clinicians to accept erroneous AI predictions when accompanied by plausible-looking post-hoc explanations, increasing diagnostic errors by up to 45% (Bussone et al., 2015; Jacobs et al., 2021)."),
            ("Algorithm Aversion (Under-Reliance)", "Rejection of valid AI recommendations after clinicians observe erratic, unstable, or contradictory explanations across similar patient profiles."),
            ("Physiological Telemetry Noise (h = 0.05)", "Isotropic Gaussian perturbation with standard deviation h = 0.05 in z-score normalized space (5% of 1 standard deviation), reflecting routine bedside monitor jitter (e.g., ±3–5 mmHg blood pressure or ±2–4 bpm heart rate)."),
            ("Clinical Guidelines (SOFA, ASCVD, NPI)", "Codified medical risk instruments: Sequential Organ Failure Assessment (SOFA) for ICU sepsis, ACC/AHA Pooled Cohort Equations (ASCVD) for 10-year cardiovascular risk, and Nottingham Prognostic Index (NPI) for breast pathology."),
            ("EU AI Act & FDA SaMD", "Regulatory standards requiring High-Risk clinical AI systems to provide interpretable outputs (EU AI Act Art. 13), enable effective human oversight (Art. 14), and support lifecycle performance monitoring (FDA SaMD Action Plan).")
        ],
        "mechanics": [
            ("9.6× Instability Ratio", "Under h = 0.05 Gaussian noise on MIMIC-IV, Tabular Deep ResNet exhibits Ŝ<sub>Lip</sub> = 0.4912 compared to Extra Trees at Ŝ<sub>Lip</sub> = 0.0512 (0.4912 / 0.0512 = 9.59×)."),
            ("Cross-Explainer Disagreement (>40%)", "On Deep ResNet, mean pairwise Spearman rank correlation among explainers drops to r<sub>s</sub> = 0.565, yielding discordance D<sub>XAI</sub> = 1 − 0.565 = 0.435 (exceeding 43.5% rank divergence).")
        ],
        "clinical_context": [
            ("Stakeholder Impact", "1. ICU Clinicians face contradictory risk rationales during time-critical triage. 2. Healthcare Regulators lack objective pre-deployment certification thresholds. 3. Patients face elevated risk of delayed intervention or inappropriate treatment.")
        ],
        "rationales": [
            ("Empirical Basis for the 45% Error Figure", "Controlled human-AI clinical interaction studies (Bussone et al., 2015; Jacobs et al., 2021) found that presenting uncalibrated visual explanations alongside incorrect AI predictions amplifies clinician error rates by up to 45% due to confirmation and automation bias."),
            ("Realism of Noise Radius h = 0.05", "In standardized clinical features (zero mean, unit variance), h = 0.05 equals 5% of one population standard deviation—smaller than routine intra-hour arterial line drift, motion artifacts, and assay variability—establishing it as benign physiological noise rather than an extreme adversarial perturbation.")
        ]
    },
    {
        "slide_num": 4,
        "title": "Research Novelty: Why C-XAI is Necessary",
        "overview": "Details C-XAI's three pillars of novelty—Theoretical, Methodological, and Clinical Governance—relative to Captum, OpenXAI, Quantus, and SENN.",
        "terminology": [
            ("Captum, OpenXAI & Quantus", "Existing XAI software libraries: Captum implements PyTorch attribution algorithms; OpenXAI evaluates synthetic infidelity and weight recovery; Quantus aggregates vision/NLP metrics. None integrate clinical guideline priors or medical decision-utility penalties."),
            ("Pauker-Kassirer Threshold Model", "Classic medical decision theory (NEJM, 1975) defining treatment threshold p > T = Harm / (Harm + Benefit), used here to parameterize asymmetric over-reliance (α = 0.50) and under-reliance (β = 0.30) loss weights."),
            ("1D Earth Mover's Distance (Wasserstein-1)", "Optimal transport metric measuring minimum work to transform normalized attribution mass into the clinical prior distribution across ordered feature indices."),
            ("Zeroth-Order Gaussian Smoother", "Expectation-based Gaussian convolution applied to discontinuous tree ensembles, enabling gradient computation via Stein's score-function identity."),
            ("FGSM & ScaL-PGD Attribution Attacks", "Gradient-based adversarial attribution attacks (Fast Gradient Sign Method and Scaled Projected Gradient Descent) designed to maximize explanation distortion while preserving class predictions.")
        ],
        "mechanics": [
            ("Proof of (d − 1) Wasserstein Upper Bound", "For two discrete probability distributions P and Q supported on d ordered discrete bins {1, 2, ..., d}, the maximum 1D Wasserstein-1 distance occurs when all probability mass of P concentrates at bin 1 and all mass of Q concentrates at bin d, yielding W<sub>1</sub>(P, Q) = ∑<sub>j=1</sub><sup>d−1</sup> |1 − 0| = d − 1. Dividing by (d − 1) strictly bounds W<sub>Clin</sub><sup>norm</sup> ∈ [0, 1]."),
            ("Zeroth-Order Score Function Estimator", "Given a non-differentiable step function f(x), define its Gaussian-smoothed expectation f<sub>σ</sub>(x) = E<sub>u ∼ N(0, σ²I)</sub>[f(x + u)]. By Stein's lemma, the exact gradient is ∇f<sub>σ</sub>(x) = (1 / σ²) E<sub>u ∼ N(0, σ²I)</sub>[f(x + u) · u], evaluated via M = 100 Monte Carlo draws with σ = 0.05.")
        ],
        "clinical_context": [
            ("Governance Readiness", "Establishes quantitative pre-deployment acceptance thresholds linking explanation stability, clinical guideline alignment, and calibration error directly to FDA SaMD GMLP Principle 7 and EU AI Act oversight requirements.")
        ],
        "rationales": [
            ("Asymmetric Penalty Calibration (α = 0.50, β = 0.30)", "In acute care (e.g., ICU sepsis), over-reliance on a false-negative prediction delays life-saving antibiotics and risks septic shock, whereas under-reliance on a true positive triggers redundant manual diagnostic confirmation. Setting α = 0.50 > β = 0.30 reflects this clinical mortality asymmetry."),
            ("Gradient Attribution on Non-Differentiable Trees", "Decision trees are piecewise-constant step functions whose classical gradients are zero almost everywhere and undefined at split thresholds. Convolving the ensemble with an isotropic Gaussian kernel produces a smooth expectation surface compatible with SmoothGrad and Integrated Gradients.")
        ]
    },
    {
        "slide_num": 5,
        "title": "Proposed Methodology: The C-XAI Auditing Framework",
        "overview": "Specifies the 4-layer C-XAI architecture: Data & Noise Ingestion, Predictive Model Zoo, Post-Hoc Explainer Suite, and Quantitative Auditing Layer.",
        "terminology": [
            ("Layer 1: Data & Perturbation Layer", "Standardizes multi-center EHR cohorts and applies physiological Gaussian noise δ<sub>m</sub> ∼ N(0, h²I), 20% Missing Completely At Random (MCAR) corruption, and FGSM / ScaL-PGD attribution attacks."),
            ("MCAR (Missing Completely At Random)", "Missingness mechanism in which the probability of an absent lab or vital observation is independent of both observed and unobserved patient variables."),
            ("Layer 2: Predictive Modeling Layer", "Benchmarks two tree ensembles (Random Forest, Extra Trees with Zeroth-Order Smoothing) against two neural architectures (Multi-Layer Perceptron, Tabular Deep ResNet with residual skip connections)."),
            ("Layer 3: Post-Hoc Explainer Layer", "Evaluates 6 explainers spanning cooperative game theory (TreeSHAP, KernelSHAP), local linear surrogates (LIME), gradient-based paths (SmoothGrad, Integrated Gradients), and perturbation importance (PFI)."),
            ("Layer 4: Quantitative Auditing Layer", "Computes Ŝ<sub>Lip</sub>, D<sub>XAI</sub>, W<sub>Clin</sub><sup>norm</sup>, Expected Calibration Error (ECE), Trust Calibration Factor (T<sub>Clin</sub>), and Net Clinical Decision Utility (Û<sub>Clin</sub>).")
        ],
        "mechanics": [
            ("Metric 1 — Local Lipschitz Stability (Ŝ<sub>Lip</sub>)", "Ŝ<sub>Lip</sub>(x; f, E, h) = (1/M) ∑<sub>m=1</sub><sup>M</sup> [ ‖E<sub>f</sub>(x + δ<sub>m</sub>) − E<sub>f</sub>(x)‖<sub>2</sub> / (‖δ<sub>m</sub>‖<sub>2</sub> + δ<sub>0</sub>) ], where δ<sub>m</sub> ∼ N(0, h²I), M = 100, h = 0.05, and smoothing constant δ<sub>0</sub> = 10⁻⁸."),
            ("Metric 2 — Cross-Explainer Discordance (D<sub>XAI</sub>)", "D<sub>XAI</sub>(x; f) = 1 − [2 / K(K − 1)] ∑<sub>j < k</sub> r<sub>s</sub>(E<sub>j</sub>(x), E<sub>k</sub>(x)) ∈ [0, 2], where r<sub>s</sub> is Spearman rank correlation across K explainers."),
            ("Metric 3 — Clinical Prior Alignment (W<sub>Clin</sub><sup>norm</sup>)", "W<sub>Clin</sub><sup>norm</sup>(x) = W<sub>1</sub>(E<sub>norm</sub>(x), P<sub>clin</sub>) / (d − 1) ∈ [0, 1], with Alignment Score A<sub>Clin</sub> = 1 − W<sub>Clin</sub><sup>norm</sup>."),
            ("Metric 4 — Trust Factor & Clinical Utility (T<sub>Clin</sub>, Û<sub>Clin</sub>)", "T<sub>Clin</sub> = (1/3) [ 1/(1 + Ŝ<sub>Lip</sub>) + A<sub>Clin</sub> + (1 − ECE) ];  Û<sub>Clin</sub> = Acc · T<sub>Clin</sub> − (α · OR + β · UR), where OR = (1 − Acc)(1 − 0.4 T<sub>Clin</sub>), UR = Acc(1 − T<sub>Clin</sub>)(0.3), α = 0.50, β = 0.30.")
        ],
        "clinical_context": [
            ("Physiological Baseline Selection for Integrated Gradients", "Unlike computer vision where an all-zero tensor represents a neutral black image, zeroed physiological features (e.g., blood pressure = 0 mmHg) are biologically invalid. C-XAI sets the baseline vector x' to the training-cohort median across healthy survivors, measuring clinical deviation from stable physiological homeostasis.")
        ],
        "rationales": [
            ("Multi-Explainer Coverage Across 4 Mathematical Families", "Hospital decision support vendors deploy heterogeneous explainers (Shapley values, local linear surrogates, or path integrals). Auditing 6 explainers spanning all major families tests whether attribution rankings remain consistent regardless of software implementation."),
            ("Healthy-Survivor Baseline Validity", "Using cohort survivor medians as the Integrated Gradients reference anchor ensures path integrals isolate pathological deviations (e.g., elevated lactate or depressed MAP) rather than artificial distance from zero.")
        ]
    },
    {
        "slide_num": 6,
        "title": "Experimental Setup & Auditing Protocol",
        "overview": "Documents the 4 clinical cohorts (51,369 total encounters), codified medical prior vectors, software stack, hardware profile, and 50-seed stratified validation protocol.",
        "terminology": [
            ("MIMIC-IV (N = 40,000 encounters)", "Beth Israel Deaconess Medical Center ICU database (Johnson et al., Sci. Data 2023). Task: ICU Sepsis-3 mortality prediction. Priors: SOFA (0.35), Serum Lactate (0.30), MAP (0.20), Age (0.15)."),
            ("eICU (N = 10,000 encounters)", "Multi-center Philips ICU Collaborative Research Database (Pollard et al., Sci. Data 2023). Task: Acute hospital mortality. Priors: MAP (0.40), WBC count (0.20), Creatinine (0.20), Temperature (0.20)."),
            ("BCWD (N = 569 encounters)", "Wisconsin Breast Cancer Diagnostic cohort. Task: Malignancy classification from nuclear morphometry. Priors (NPI-aligned): Area & Concavity (0.25), Perimeter (0.25), Texture (0.25), Radius (0.25)."),
            ("Cardio EHR (N = 800 encounters)", "Cardiovascular risk prediction cohort. Task: 10-year CVD event risk. Priors (ACC/AHA ASCVD-aligned): Systolic BP (0.30), Age (0.25), Total Cholesterol (0.25), Smoking (0.20)."),
            ("Stratified 5-Fold CV × 50 Seeds", "Repeated stratified 5-fold cross-validation across 50 independent random seeds (seeds 42–91), yielding 250 trained model evaluations per architecture while preserving class ratios.")
        ],
        "mechanics": [
            ("Computational & Software Environment", "Software: Python 3.10+, PyTorch 2.14, Scikit-learn, Captum, SHAP, SciPy. Hardware: Apple Silicon M-series and Linux x86_64 with 16 GB RAM, ensuring reproducible execution without specialized multi-GPU clusters."),
            ("Leakage-Free Preprocessing & Imputation", "Continuous features undergo fold-isolated z-score standardization: x<sub>scaled</sub> = (x − μ<sub>train</sub>) / σ<sub>train</sub>. Missing validation values are imputed exclusively using training-fold medians.")
        ],
        "clinical_context": [
            ("Cross-Institutional & Cross-Specialty Generalization", "Combining single-center ICU (MIMIC-IV), multi-hospital ICU (eICU), surgical oncology (BCWD), and outpatient cardiology (Cardio EHR) evaluates robustness across varying sample sizes, feature dimensions, and clinical care settings.")
        ],
        "rationales": [
            ("Objectivity & Robustness of Clinical Prior Weights", "Prior vectors P<sub>clin</sub> are derived from published consensus guidelines (Sepsis-3 / JAMA 2016, Nottingham Prognostic Index, ACC/AHA Pooled Cohort Equations). Sensitivity sweeps perturbing prior weights by ±20% demonstrated 100% invariance in relative model rankings."),
            ("Statistical Power of 50-Seed Protocol", "Executing 50 independent random trials across seeds 42–91 supports non-parametric Wilcoxon signed-rank and paired t-tests with sufficient power to rule out random data-split artifacts.")
        ]
    },
    {
        "slide_num": 7,
        "title": "Results: Accuracy vs. Clinical Explanation Reliability",
        "overview": "Presents primary MIMIC-IV findings demonstrating that Extra Trees achieves +19.6% higher calibrated clinical utility over Tabular Deep ResNet (0.8485 vs. 0.7095/0.7107, p < 0.001) despite slightly lower raw accuracy.",
        "terminology": [
            ("Relative Clinical Utility Gain (+19.6%)", "Comparison between Extra Trees (Û<sub>Clin</sub> = 0.8485) and Tabular Deep ResNet (0.7095–0.7107), representing +0.1390 absolute gain (+13.9 percentage points) and +19.6% relative improvement."),
            ("Wilcoxon Signed-Rank Test (W = 0.0, p < 0.001)", "Non-parametric paired rank test across N = 50 seeds. W = 0.0 denotes the theoretical minimum test statistic, indicating Extra Trees outperformed Deep ResNet in all 50 paired trials."),
            ("Paired t-test (t = 14.82, p < 0.001)", "Parametric hypothesis test confirming statistically significant separation across the 50 trial seeds."),
            ("Cohen's d = 2.96", "Standardized effect size ((μ<sub>1</sub> − μ<sub>2</sub>) / s<sub>pooled</sub>); values above 0.8 are classified as large, making d = 2.96 a decisive distributional separation."),
            ("Inference Latency", "Mean per-patient scoring latency: Extra Trees = 4.2 ms, Random Forest = 6.8 ms, Tabular Deep ResNet = 48.5 ms (11.5× slower than Extra Trees).")
        ],
        "mechanics": [
            ("MIMIC-IV Model Comparison Summary",
             "Tabular Deep ResNet: Acc = 89.35%, AUROC = 0.913, Ŝ<sub>Lip</sub> = 0.4912, D<sub>XAI</sub> = 0.435, W<sub>Clin</sub><sup>norm</sup> = 0.0380–0.044, ECE = 0.055, Û<sub>Clin</sub> = 0.7107 (0.7095 paired baseline).\n"
             "MLP Classifier: Acc = 89.20%, AUROC = 0.907, Ŝ<sub>Lip</sub> = 0.4850, D<sub>XAI</sub> = 0.412, W<sub>Clin</sub><sup>norm</sup> = 0.0389, ECE = 0.058, Û<sub>Clin</sub> = 0.7120.\n"
             "Random Forest: Acc = 88.45%, AUROC = 0.899, Ŝ<sub>Lip</sub> = 0.0821, D<sub>XAI</sub> = 0.081, W<sub>Clin</sub><sup>norm</sup> = 0.0285, ECE = 0.021, Û<sub>Clin</sub> = 0.8412.\n"
             "Extra Trees (C-XAI): Acc = 88.12%, AUROC = 0.903, Ŝ<sub>Lip</sub> = 0.0512, D<sub>XAI</sub> = 0.059, W<sub>Clin</sub><sup>norm</sup> = 0.0312, ECE = 0.015, Û<sub>Clin</sub> = 0.8485.")
        ],
        "clinical_context": [
            ("Accuracy vs. Reliability Tradeoff in ICU Triage", "Deep ResNet gains +1.23 percentage points in raw accuracy (89.35% vs. 88.12%) at the cost of 9.6× higher explanation instability, 7.4× higher explainer conflict, 3.7× higher calibration error (ECE 0.055 vs. 0.015), and 11.5× higher latency.")
        ],
        "rationales": [
            ("Why Lower Raw Accuracy Yields Higher Clinical Utility", "The 1.23% accuracy advantage of Deep ResNet stems from high-frequency non-linear boundary memorization, which simultaneously causes 49.1% attribution instability under routine sensor noise and elevated Expected Calibration Error (ECE = 0.055), lowering net calibrated trust and decision utility."),
            ("Extra Trees vs. Random Forest Stability Advantage (0.0512 vs. 0.0821)", "Random Forest selects optimal deterministic split cut-points via Gini/entropy minimization, creating sharper, sample-sensitive boundaries. Extra Trees draws random split thresholds per candidate feature, acting as a structural regularizer that yields smoother local variance and tighter Lipschitz stability.")
        ]
    },
    {
        "slide_num": 8,
        "title": "Results: Explainer Discordance & Accuracy Decoupling",
        "overview": "Quantifies pairwise cross-explainer discordance matrices (Fig. 2) and demonstrates the statistical decoupling between predictive AUROC and calibrated clinical decision utility (Fig. 3, R² = 0.04).",
        "terminology": [
            ("D<sub>XAI</sub> Scale [0, 2]", "Derived from Spearman rank correlation r<sub>s</sub> ∈ [−1, +1] via D<sub>XAI</sub> = 1 − r<sub>s</sub>: 0.0 indicates complete ordinal agreement, 1.0 indicates zero correlation, and 2.0 indicates complete rank inversion."),
            ("Tree Ensemble Consensus (D<sub>XAI</sub> = 0.059)", "Extra Trees achieves mean pairwise rank correlation r<sub>s</sub> = 0.941 across TreeSHAP, KernelSHAP, and LIME (94.1% ordinal consensus)."),
            ("Neural Architecture Conflict (D<sub>XAI</sub> = 0.435)", "Tabular Deep ResNet exhibits mean r<sub>s</sub> = 0.565 across Integrated Gradients, SmoothGrad, and LIME (7.4× higher disagreement than Extra Trees)."),
            ("Accuracy Decoupling (R² = 0.04)", "Ordinary least-squares regression of Û<sub>Clin</sub> against AUROC across all evaluated architectures and cohorts yields R² = 0.038 (≈ 0.04, p = 0.42), demonstrating negligible predictive linkage."),
            ("The Disagreement Problem", "Empirical conflict across post-hoc explainers documented by Krishna et al. (ACM CHI 2022), formalized here as a bounded metric and shown to be primarily driven by model architecture.")
        ],
        "mechanics": [
            ("Pairwise Discordance Breakdown (MIMIC-IV, Fig. 2)",
             "Tree Ensemble (Extra Trees): TreeSHAP vs. KernelSHAP = 0.042; TreeSHAP vs. LIME = 0.059; KernelSHAP vs. LIME = 0.075 (Mean D<sub>XAI</sub> = 0.059).\n"
             "Tabular Deep ResNet: Integrated Gradients vs. SmoothGrad = 0.312–0.392; Integrated Gradients vs. LIME = 0.435; SmoothGrad vs. LIME = 0.458–0.478 (Mean D<sub>XAI</sub> = 0.435).")
        ],
        "clinical_context": [
            ("Cognitive Dissonance in Multi-Tool Hospitals", "When Integrated Gradients ranks Serum Lactate as the primary sepsis driver while LIME ranks Patient Age first for the exact same patient record, clinicians receive irreconcilable rationales, inducing decision paralysis.")
        ],
        "rationales": [
            ("Choice of Spearman Rank Correlation Over Cosine Similarity", "Bedside clinicians evaluate ordinal top-k feature rankings (e.g., top-3 physiological drivers) rather than raw continuous attribution magnitudes. Spearman correlation captures strict ordinal rank invariance, whereas Cosine similarity is confounded by scale differences across explainer axioms."),
            ("Interpretation of Explainer Divergence on Deep Networks", "Cross-explainer disagreement is not a defect of a single explainer but a diagnostic indicator of a highly non-convex neural decision manifold, where linear surrogates (LIME) and path integrals (IG) extract conflicting local approximations.")
        ]
    },
    {
        "slide_num": 9,
        "title": "Discussion: Insights, Robustness & Regulatory Impact",
        "overview": "Resolves the Representation Paradox geometrically, reports noise-radius scaling and adversarial robustness under FGSM/ScaL-PGD, and details regulatory certification alignment.",
        "terminology": [
            ("The Representation Paradox", "Empirical refutation of the hypothesis that smooth, continuous neural networks generate more stable explanations than piecewise-constant tree ensembles."),
            ("Axis-Aligned Leaf Hyper-Rectangles", "Disjoint orthogonal feature partitions R<sub>k</sub> created by decision tree splits, inside which model predictions and local TreeSHAP paths remain invariant."),
            ("Gradient Shattering & Hessian Curvature", "Rapid directional oscillation of neural gradients across small neighborhoods caused by stacked non-linear activations and large Hessian eigenvalues (∇²f(x))."),
            ("Noise-Radius Scaling (h ∈ [0.01, 0.20])", "Sensitivity profile across perturbation magnitudes: Extra Trees scales sub-linearly (Ŝ<sub>Lip</sub>: 0.018 → 0.103), whereas deep networks degrade supra-linearly (>12× instability escalation)."),
            ("Adversarial Attribution Collapse", "Under FGSM (ε = 0.02) and 5-step ScaL-PGD attacks, Deep ResNet collapses to D<sub>XAI</sub> = 1.862–1.928 (near-complete rank inversion) and Ŝ<sub>Lip</sub> = 0.865–0.938, whereas Random Forest retains D<sub>XAI</sub> ≤ 0.312 and Ŝ<sub>Lip</sub> ≤ 0.132.")
        ],
        "mechanics": [
            ("Geometric Explanation of the Paradox",
             "Tree Partition Invariance: For an input x inside leaf cell R<sub>k</sub>, any perturbation δ keeping (x + δ) ∈ R<sub>k</sub> satisfies f(x + δ) = f(x) and yields zero attribution delta (‖E<sub>f</sub>(x + δ) − E<sub>f</sub>(x)‖<sub>2</sub> = 0) across the majority interior volume.\n"
             "Neural Manifold Curvature: For multi-layer networks f(x) = W<sub>L</sub>σ(...σ(W<sub>1</sub>x)), gradients ∇<sub>x</sub>f(x) depend continuously on all intermediate activations; high local Hessian curvature induces sharp attribution variance for small δ."),
            ("Weight Sensitivity Verification (T<sub>Clin</sub> / Û<sub>Clin</sub>)", "Across 5 weight configurations (w<sub>s</sub>, w<sub>a</sub>, w<sub>c</sub>) including Balanced (0.33, 0.33, 0.33), Stability-Focused (0.60, 0.20, 0.20), Clinical-Prior Focused (0.20, 0.60, 0.20), Calibration-Focused (0.20, 0.20, 0.60), and Robust Clinical (0.40, 0.40, 0.20), tree ensembles consistently outperform deep networks.")
        ],
        "clinical_context": [
            ("Regulatory Operationalization (FDA SaMD & EU AI Act)", "Translates high-level transparency mandates (EU AI Act Articles 13 & 14; FDA GMLP Principle 7) into enforceable pre-deployment audit gates (e.g., requiring Ŝ<sub>Lip</sub> ≤ 0.10–0.15 and D<sub>XAI</sub> ≤ 0.10–0.15 prior to clinical release).")
        ],
        "rationales": [
            ("Why Discontinuous Trees Exhibit Higher Practical Stability", "Although decision trees have step discontinuities along hyperplane boundaries, the interior volume of leaf hyper-rectangles dominates typical physiological noise neighborhoods (h = 0.05). Conversely, continuity in deep networks does not imply flatness: steep local curvature produces large attribution oscillations."),
            ("EU AI Act Articles 13 & 14 Alignment", "Article 13 mandates interpretable outputs for high-risk medical systems, and Article 14 mandates human oversight mechanisms mitigating automation bias. C-XAI provides automated audit logs verifying both requirements prior to deployment.")
        ]
    },
    {
        "slide_num": 10,
        "title": "Conclusion & Future Scope",
        "overview": "Synthesizes C-XAI's theoretical, empirical, and clinical contributions alongside defined study boundaries and future research directions.",
        "terminology": [
            ("Core Scientific Contributions", "1. Formalization of 4 auditing metrics (Ŝ<sub>Lip</sub>, D<sub>XAI</sub>, W<sub>Clin</sub><sup>norm</sup>, Û<sub>Clin</sub>). 2. Zeroth-Order Gaussian Smoother for step-function trees. 3. Proof of Accuracy-Reliability Decoupling (R² = 0.04) across 51,369 encounters. 4. Regulatory deployment thresholds."),
            ("Multimodal Clinical Expansion", "Planned extension from structured tabular EHR to unstructured clinical progress notes (BioClinicalBERT), physiological waveforms, and thoracic imaging."),
            ("Dynamic Trajectory Auditing", "Formulation of temporal Lipschitz stability metrics for sequential ICU time-series evaluated across recurrent architectures (LSTM) and clinical transformers."),
            ("Prospective Clinician Reader Trials", "Human-in-the-loop ICU simulation studies measuring empirical clinician diagnostic accuracy, triage speed, and cognitive workload.")
        ],
        "mechanics": [
            ("Tri-Partite Synthesis", "Empirical: Extra Trees delivers +19.6% higher net clinical utility (0.8485 vs. 0.7095/0.7107, p < 0.001). Methodological: Post-hoc explanations require multi-explainer and noise-perturbation auditing prior to deployment. Theoretical: Continuous neural representations suffer severe attribution fragility on tabular healthcare data.")
        ],
        "clinical_context": [
            ("Clinical Deployment Principle", "Model selection in high-stakes healthcare cannot rely on predictive AUROC alone; pre-deployment auditing of stability, consensus, calibration, and guideline alignment is essential to prevent silent triage hazards.")
        ],
        "rationales": [
            ("Defined Study Scope & Limitations", "Three explicit boundaries define the current scope: (1) evaluation focuses on structured tabular EHR cohorts rather than continuous high-frequency waveforms or imaging; (2) clinical utility is computed via calibrated decision-theoretic modeling rather than prospective live ICU reader trials; and (3) clinical prior vectors are codified for four benchmark cohorts and will expand across further specialties.")
        ]
    },
    {
        "slide_num": 11,
        "title": "References & Literature Context",
        "overview": "Maps the peer-reviewed literature foundation spanning foundational XAI methods, evaluation toolkits, clinical EHR cohorts, human-AI trust studies, and institutional research lineage.",
        "terminology": [
            ("Lundberg & Lee (NeurIPS 2017) [1]", "SHAP: Game-theoretic unified feature attribution framework based on Shapley values."),
            ("Ribeiro et al. (SIGKDD 2016) [2]", "LIME: Model-agnostic local surrogate explanations via perturbed linear approximations."),
            ("Sundararajan et al. (ICML 2017) [3]", "Integrated Gradients: Axiomatic path-integral attribution for differentiable neural networks."),
            ("Agarwal et al. (NeurIPS 2022) & Hedström et al. (JMLR 2023) [7, 8]", "OpenXAI and Quantus evaluation toolkits benchmarking synthetic fidelity and image/NLP metrics."),
            ("Krishna et al. (ACM CHI 2022) [9]", "Empirical characterization of the XAI disagreement problem across competing post-hoc explainers."),
            ("Johnson et al. & Pollard et al. (Sci. Data 2023) [10, 11]", "MIMIC-IV and eICU Collaborative Research Database open clinical EHR benchmarks."),
            ("Ramya et al. (IEEE Access 2023; LNCS 2023; CCIS 2023; IJCACI 2025) [25–28]", "Prior institutional publications on Two-Layered Voting (TLV) for CAD prediction, explainable ML for diabetes/CVD risk, White-Box AI, and clinical EHR feature selection.")
        ],
        "mechanics": [
            ("Advancement Beyond Prior Evaluation Literature", "While Krishna et al. (2022) identified explainer disagreement empirically and OpenXAI/Quantus formalized synthetic checks, C-XAI introduces a bounded cross-explainer discordance metric (D<sub>XAI</sub> ∈ [0, 2]), resolves architectural root causes on clinical tabular data, and unifies stability, prior alignment, and ECE into decision utility.")
        ],
        "clinical_context": [
            ("Human-AI Clinical Literature Grounding", "Integrates empirical clinician reliance findings from Bussone et al. (2015), Jacobs et al. (2021), Buçinca et al. (Artif. Intell. Med. 2023), and Bansal et al. (ACM CHI 2024) into formal quantitative utility parameters.")
        ],
        "rationales": [
            ("Relation to Krishna et al. (CHI 2022)", "Krishna et al. demonstrated empirically that explainers frequently disagree but offered no unified resolution metric. C-XAI formalizes D<sub>XAI</sub> and establishes empirically that cross-explainer disagreement is strongly architecture-dependent (0.059 in Extra Trees vs. 0.435 in Deep ResNet).")
        ]
    },
    {
        "slide_num": 12,
        "title": "Author Contact & Reproducibility Artifacts",
        "overview": "Provides presenting/corresponding author contact information, Paper ID attribution, and open-source artifact details for code and benchmark reproduction.",
        "terminology": [
            ("Presenting Author", "Sheela Akshar Sakhi (aksharsakhi@gmail.com), Department of Computer Science & Engineering, Amrita School of Computing, Coimbatore."),
            ("Corresponding Author & Supervisor", "Dr. Ramya G R (gr_ramya@cb.amrita.edu), Department of Computer Science & Engineering, Amrita School of Computing, Coimbatore."),
            ("Paper & Session Identifier", "Paper ID: 857 · Technical Session · ICMLDE 2026, UPES Dehradun, India."),
            ("Public Code Repository", "https://github.com/aksharsakhi/c-xai-healthcare-predictions (cxai-1.0.0 library, metric modules, and experiment scripts).")
        ],
        "mechanics": [
            ("Repository Artifact Structure", "Core metrics implemented in src/cxai/metrics.py (compute_empirical_lipschitz_stability, compute_cross_explainer_discordance, compute_clinical_wasserstein_distance, compute_expected_calibration_error, compute_calibrated_clinical_utility); robustness & sensitivity audits in src/compute_revision_tables.py and src/run_revision_experiments.py.")
        ],
        "clinical_context": [
            ("Open-Science Verification", "All experimental seeds (42–91), clinical prior dictionaries, and statistical evaluation pipelines are openly archived to support independent hospital IT verification and regulatory auditing.")
        ],
        "rationales": [
            ("Concise Technical Summary", "C-XAI demonstrates across 51,369 clinical encounters that predictive AUROC does not guarantee explanation reliability (R² = 0.04), and establishes quantitatively that randomized tree ensembles deliver 19.6% higher calibrated clinical decision utility (p < 0.001, d = 2.96) than deep tabular networks.")
        ]
    }
]
