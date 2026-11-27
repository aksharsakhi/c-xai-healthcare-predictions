# technical_reference_data.py
# Comprehensive Slide-by-Slide Technical Reference Data for ICMLDE 2026 (Paper ID: 857)
# Includes complete definitions of all specialized mathematical, ML, clinical, statistical,
# and regulatory terminology aligned with each presentation slide.
#
# Markup tags supported by build_technical_reference.py:
#   <b>...</b>, <i>...</i>, <sub>...</sub>, <sup>...</sup>

SLIDES_DATA = [
    {
        "slide_num": 1,
        "title": "Title, Authorship & Framework Scope",
        "overview": "Establishes the scope of Paper ID 857: C-XAI (Clinical Explainable AI), a quantitative auditing benchmark for explanation stability, cross-explainer discordance, clinical prior alignment, and calibrated decision utility in tabular healthcare AI.",
        "terminology": [
            ("C-XAI (Clinical Explainable AI)", "Open-source quantitative auditing framework and modular Python package (cxai-1.0.0) designed to stress-test and certify post-hoc explanations in clinical predictive pipelines."),
            ("EHR (Electronic Health Record) & Tabular Data", "Structured digital patient records organized in patient-by-feature matrices (e.g., laboratory assays, vital signs, demographics, clinical scores) rather than raw unstructured images or free text."),
            ("Explanation Stability (Ŝ<sub>Lip</sub>)", "Empirical Local Lipschitz Stability Index quantifying how violently a feature attribution vector fluctuates under small, realistic physiological sensor noise (noise radius h = 0.05)."),
            ("Cross-Explainer Discordance (D<sub>XAI</sub>)", "Pairwise rank-order disagreement between competing post-hoc explainers (e.g., SHAP vs. LIME vs. Integrated Gradients) evaluated on the identical patient record."),
            ("Clinical Prior Alignment (W<sub>Clin</sub><sup>norm</sup>)", "Dimension-normalized 1D Wasserstein (Earth Mover's) distance measuring how closely model feature importances match established medical guideline weights (SOFA, ASCVD, NPI)."),
            ("Calibrated Clinical Utility (Û<sub>Clin</sub>)", "Decision-theoretic metric estimating net clinician decision value by weighting accuracy against trust calibration (T<sub>Clin</sub>) and asymmetric over-/under-reliance error penalties."),
            ("Elsevier Procedia Computer Science", "Scopus-indexed open-access conference proceedings series publishing peer-reviewed papers from the 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026).")
        ],
        "mechanics": [
            ("Publication & Track Metadata", "Paper ID: 857. Title: 'C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI'. Track: Technical Session (ICMLDE 5.0, 27–28 November 2026, UPES Dehradun, India)."),
            ("Authorship & Affiliation", "Sheela Akshar Sakhi (Presenting Author, aksharsakhi@gmail.com), Ibbraheem Shaik, Settibattini Suhitha, and Dr. Ramya G R (Corresponding Author, gr_ramya@cb.amrita.edu). Department of Computer Science & Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Coimbatore, India."),
            ("Implementation & Package API", "Packaged as a Python toolkit exposing .evaluate(), .benchmark(), and .compare() interfaces supporting scikit-learn tree ensembles and PyTorch neural networks at https://github.com/aksharsakhi/c-xai-healthcare-predictions.")
        ],
        "clinical_context": [
            ("Domain Specificity vs. General XAI Suites", "General-purpose benchmarks (OpenXAI, Quantus) evaluate synthetic infidelity or weight recovery on vision and NLP datasets. C-XAI targets structured tabular EHR models under realistic physiological noise and medical guideline constraints."),
            ("Regulatory Context", "Designed to provide verifiable quantitative audit metrics aligned with the FDA Software as a Medical Device (SaMD) Action Plan and EU AI Act Articles 13 and 14.")
        ],
        "rationales": [
            ("Scope Distinction", "Unlike generic saliency benchmarks evaluating image pixels or text tokens, C-XAI addresses high-stakes tabular EHR pipelines where continuous telemetry noise and domain clinical guidelines govern deployment safety.")
        ]
    },
    {
        "slide_num": 2,
        "title": "Introduction & Research Context",
        "overview": "Establishes the healthcare AI black-box dilemma, quantifies the auditing void across clinical XAI literature, and introduces the 5-layer C-XAI auditing pipeline.",
        "terminology": [
            ("Black-Box Dilemma", "High-capacity models (deep tabular neural networks and complex ensembles) achieve AUROC ≥ 0.96 on clinical datasets while hiding internal decision boundaries from clinicians (Muhammad & Bendechache, 2024)."),
            ("AUROC / ROC-AUC (Area Under the Receiver Operating Characteristic Curve)", "Threshold-independent discrimination metric ranging from 0.5 (random chance) to 1.0 (perfect ranking), measuring the probability that a model scores a randomly chosen positive patient higher than a negative one."),
            ("Post-Hoc Explainability", "Attribution methods applied after model training (TreeSHAP, KernelSHAP, LIME, Integrated Gradients, SmoothGrad, PFI) to approximate feature importance without altering model weights."),
            ("Clinical Decision Support (CDS)", "Automated software systems providing diagnostic, prognostic, or triage risk scores to medical personnel in acute care settings."),
            ("ICU Triage", "Intensive Care Unit prioritization and risk stratification of critically ill patients to allocate time-sensitive clinical interventions."),
            ("Confounding Artifacts", "Spurious non-causal correlations (e.g., ICU bed numbers, laboratory batch timing, billing codes) exploited by models to inflate global accuracy without capturing true biology."),
            ("Pathophysiology", "Disordered physiological processes underlying disease (e.g., organ hypoperfusion and elevated lactate in sepsis), distinct from hospital workflow metadata."),
            ("Cross-Entropy Loss", "Standard classification training objective penalizing log-probability errors; minimizing it globally can encourage deep models to memorize fragile, high-frequency local shortcuts."),
            ("Anecdotal Visual Heatmaps", "Qualitative practice of displaying cherry-picked explanation charts for individual patients without cohort-wide statistical robustness auditing."),
            ("Alert Fatigue", "Clinician desensitization resulting from frequent noisy, unreliable, or contradictory decision-support warnings, causing eventual abandonment of clinical AI tools.")
        ],
        "mechanics": [
            ("Literature Auditing Gap", "Systematic reviews (Roychowdhury et al., npj Digit. Med. 2025; Kyrimi et al., 2025) report that >85% of clinical XAI studies omit quantitative explanation reliability metrics and 83% of cancer XAI evaluations omit clinician validation."),
            ("Accuracy-Reliability Decoupling", "Jin et al. (2023) established that models achieving high AUROC via empirical cross-entropy minimization can simultaneously produce chaotic, unstable local attribution vectors under minor input perturbations."),
            ("5-Layer Auditing Pipeline (Fig. 1)", "Ingests multi-hospital EHR feeds → Injects physiological Gaussian noise and adversarial attacks → Benchmarks tree and neural models → Computes 6 post-hoc explainers → Quantifies 4 auditing metrics and calibrated clinician reliance.")
        ],
        "clinical_context": [
            ("Clinical Safety Implications", "When an acute sepsis model achieves high accuracy via spurious hospital metadata while generating volatile explanations, clinicians lack verifiable insight into true physiological drivers such as lactate or organ dysfunction."),
            ("Clinician Trust & Adoption", "Consistent, guideline-aligned attributions sustain clinical trust across shifts, reducing cognitive burden during acute triage.")
        ],
        "rationales": [
            ("Auditing Complex Models vs. Shallow Interpretable Models", "Single shallow decision trees and basic generalized additive models (GAMs) offer native transparency but incur an 8–12% AUROC penalty on high-dimensional multi-center sepsis cohorts (MIMIC-IV, eICU). Auditing high-capacity ensembles preserves diagnostic sensitivity while verifying explanation stability."),
            ("Basis for Accuracy-Reliability Decoupling", "Global classification accuracy evaluates label agreement across a test distribution, whereas explanation reliability evaluates the local smoothness, cross-method consensus, and clinical grounding of the reasoning path around each patient.")
        ]
    },
    {
        "slide_num": 3,
        "title": "Problem Statement: The Clinical Explainability Gap",
        "overview": "Characterizes the three core failure modes of current clinical explanations—noise fragility (9.6×), cross-explainer conflict (>40%), and guideline detachment—and identifies affected stakeholders.",
        "terminology": [
            ("Automation Bias (Over-Reliance)", "Cognitive tendency of clinicians to uncritically follow erroneous AI predictions when shown confident-looking post-hoc explanations, increasing diagnostic error rates by up to 45% (Bussone et al., 2015; Jacobs et al., 2021)."),
            ("Confirmation Bias", "Psychological tendency to accept explanations that appear superficially plausible or match expectations without verifying causal robustness."),
            ("Algorithm Aversion (Under-Reliance)", "Complete dismissal of accurate AI recommendations after clinicians encounter erratic, unstable, or conflicting explanations across comparable patients."),
            ("Feature Attribution Vector", "Numerical vector assigning an importance score to each input feature indicating its local contribution to a specific patient's prediction."),
            ("Z-Score Standardization", "Feature scaling transformation z = (x − μ) / σ giving every clinical variable zero mean and unit variance so perturbation radii apply uniformly across heterogeneous units (mmHg, mmol/L, years)."),
            ("Isotropic Gaussian Telemetry Noise (h = 0.05)", "Independent zero-mean normal perturbations N(0, h²I) with equal standard deviation h = 0.05 (5% of 1 standard deviation) across features, modeling routine ICU transducer drift (±3–5 mmHg BP or ±2–4 bpm HR)."),
            ("Saliency / Attribution Ranking", "Visual or ordinal ranking highlighting which clinical variables most strongly influenced an algorithmic risk score."),
            ("Clinical Consensus Guidelines (SOFA, ASCVD, NPI)", "Validated medical scoring systems: Sequential Organ Failure Assessment (SOFA) for sepsis, ACC/AHA Pooled Cohort Equations (ASCVD) for cardiovascular risk, and Nottingham Prognostic Index (NPI) for breast pathology."),
            ("EU AI Act & FDA SaMD", "Regulatory frameworks mandating interpretable outputs for High-Risk medical AI (EU AI Act Art. 13), human oversight against automation bias (Art. 14), and Software as a Medical Device lifecycle monitoring (FDA SaMD).")
        ],
        "mechanics": [
            ("9.6× Instability Ratio", "Under h = 0.05 Gaussian noise on MIMIC-IV, Tabular Deep ResNet exhibits Ŝ<sub>Lip</sub> = 0.4912 compared to Extra Trees at Ŝ<sub>Lip</sub> = 0.0512 (0.4912 / 0.0512 = 9.59×)."),
            ("Cross-Explainer Disagreement (>40%)", "On Deep ResNet, mean pairwise Spearman rank correlation among explainers drops to r<sub>s</sub> = 0.565, yielding discordance D<sub>XAI</sub> = 1 − 0.565 = 0.435 (exceeding 43.5% rank divergence).")
        ],
        "clinical_context": [
            ("Stakeholder Impact", "1. ICU Clinicians face contradictory rationales during time-critical triage. 2. Healthcare Regulators lack objective pre-deployment certification thresholds. 3. Patients face elevated risk of delayed treatment or inappropriate intervention.")
        ],
        "rationales": [
            ("Empirical Basis for the 45% Error Figure", "Controlled clinical human-AI studies (Bussone et al., 2015; Jacobs et al., 2021) demonstrated that presenting uncalibrated visual explanations alongside wrong AI outputs increases clinician diagnostic errors by up to 45% due to automation and confirmation bias."),
            ("Realism of Noise Radius h = 0.05", "In standardized feature space, h = 0.05 equals 5% of one population standard deviation—smaller than routine intra-hour arterial line fluctuations and lab assay variance—establishing it as benign bedside noise rather than an extreme attack.")
        ]
    },
    {
        "slide_num": 4,
        "title": "Research Novelty: Why C-XAI is Necessary",
        "overview": "Details C-XAI's three pillars of novelty—Theoretical, Methodological, and Clinical Governance—relative to Captum, OpenXAI, Quantus, and SENN.",
        "terminology": [
            ("Captum, OpenXAI & Quantus", "General XAI software libraries: Captum provides PyTorch gradient/perturbation attributions; OpenXAI evaluates synthetic infidelity and ground-truth weight recovery; Quantus collects vision/NLP metrics. None integrate medical guidelines or clinical utility penalties."),
            ("SENN (Self-Explaining Neural Networks)", "Interpretable architecture framework (Alvarez-Melis & Jaakkola, 2018) using theoretical supremum Lipschitz bounds in continuous toy/synthetic neural settings; incompatible with discontinuous tree ensembles."),
            ("Supremum Lipschitz Bound", "Theoretical worst-case (maximum) local attribution sensitivity ratio across all possible infinitesimal input perturbations, generally intractable to compute on complex clinical models."),
            ("Infidelity", "Explanation evaluation metric measuring the discrepancy between predicted output changes under perturbation and changes implied by the attribution weights."),
            ("Pauker-Kassirer Decision Threshold", "Foundational medical decision-theory formulation (NEJM, 1975) stating a clinician should treat when disease probability p > T = Harm / (Harm + Benefit), grounding asymmetric loss weights α = 0.50 and β = 0.30."),
            ("Optimal Transport & 1D Wasserstein-1 (Earth Mover's Distance)", "Mathematical distance measuring minimum work required to redistribute probability mass from a normalized attribution vector into a clinical prior vector along ordered feature indices."),
            ("Piecewise-Constant Step Function", "Function (such as a decision tree) whose output remains constant within axis-aligned split regions and jumps abruptly at boundaries, leaving zero gradient almost everywhere."),
            ("Zeroth-Order Gaussian Smoother", "Expectation-based Gaussian kernel convolution applied to discontinuous tree ensembles so differentiable expectation gradients can be computed without native tree derivatives."),
            ("Stein's Lemma (Score-Function Identity)", "Mathematical identity proving that the gradient of a Gaussian-smoothed expectation equals E[(1/σ²) f(x + u)·u], enabling Monte Carlo gradient estimation without backpropagation."),
            ("Monte Carlo Expectation", "Numerical estimation of an expected value by averaging over M independent random samples (M = 100 Gaussian draws in C-XAI)."),
            ("FGSM & ScaL-PGD Attribution Attacks", "Adversarial attribution attacks (Fast Gradient Sign Method; Scaled Projected Gradient Descent) crafted to maximize feature explanation shift while keeping the predicted class label unchanged.")
        ],
        "mechanics": [
            ("Proof of (d − 1) Wasserstein Upper Bound", "For two discrete probability distributions P and Q supported on d ordered bins {1, 2, ..., d}, the maximum 1D Wasserstein-1 distance occurs when all mass of P concentrates at bin 1 and all mass of Q concentrates at bin d, yielding W<sub>1</sub>(P, Q) = ∑<sub>j=1</sub><sup>d−1</sup> |1 − 0| = d − 1. Dividing by (d − 1) strictly bounds W<sub>Clin</sub><sup>norm</sup> ∈ [0, 1]."),
            ("Zeroth-Order Score Function Estimator", "For non-differentiable tree f(x), define smoothed surface f<sub>σ</sub>(x) = E<sub>u ∼ N(0, σ²I)</sub>[f(x + u)]. By Stein's lemma, ∇f<sub>σ</sub>(x) = (1 / σ²) E<sub>u ∼ N(0, σ²I)</sub>[f(x + u) · u], approximated via M = 100 draws with σ = 0.05.")
        ],
        "clinical_context": [
            ("Governance Readiness", "Establishes quantitative pre-deployment acceptance gates linking explanation stability, clinical guideline alignment, and probability calibration directly to FDA SaMD GMLP Principle 7 and EU AI Act compliance.")
        ],
        "rationales": [
            ("Asymmetric Penalty Calibration (α = 0.50, β = 0.30)", "In acute care (e.g., ICU sepsis), false reassurance from over-reliance on a false negative delays urgent antibiotics and risks septic shock mortality, whereas under-reliance on a true positive prompts extra manual review. Setting α = 0.50 > β = 0.30 mirrors this risk asymmetry."),
            ("Gradient Attribution on Non-Differentiable Trees", "Because classical derivatives of tree step functions are zero almost everywhere and undefined at splits, Gaussian convolution creates an infinitely differentiable expectation surface compatible with SmoothGrad and Integrated Gradients.")
        ]
    },
    {
        "slide_num": 5,
        "title": "Proposed Methodology: The C-XAI Auditing Framework",
        "overview": "Specifies the 4-layer C-XAI architecture: Data & Noise Ingestion, Predictive Model Zoo, Post-Hoc Explainer Suite, and Quantitative Auditing Layer.",
        "terminology": [
            ("Layer 1: Data & Perturbation Layer", "Standardizes multi-center EHR cohorts and applies Gaussian noise δ<sub>m</sub> ∼ N(0, h²I), 20% Missing Completely At Random (MCAR) corruption, and FGSM / ScaL-PGD adversarial attacks."),
            ("MCAR (Missing Completely At Random)", "Missing-data mechanism in which missing lab or vital measurements occur independently of both observed and unobserved patient states (e.g., random sample processing delays)."),
            ("Random Forest vs. Extra Trees", "Random Forest grows bootstrapped decision trees optimizing deterministic Gini/entropy split thresholds; Extra Trees (Extremely Randomized Trees) selects split cut-points at random per candidate feature, producing smoother variance."),
            ("MLP (Multi-Layer Perceptron) & Tabular Deep ResNet", "MLP is a standard stacked feedforward neural network; Tabular Deep ResNet embeds features into dense representations ('feature tokenization') and propagates activations across residual skip-connection blocks."),
            ("Shapley Values & TreeSHAP / KernelSHAP", "Game-theoretic attribution assigning fair marginal feature contributions averaged over feature coalitions. TreeSHAP computes exact values along tree paths; KernelSHAP uses model-agnostic weighted linear regression."),
            ("LIME (Local Interpretable Model-agnostic Explanations)", "Post-hoc explainer fitting a sparse interpretable linear surrogate around locally perturbed copies of an individual patient record."),
            ("Integrated Gradients (IG) & SmoothGrad", "Gradient-based explainers for differentiable (or smoothed) models: IG integrates gradients along a straight line from a baseline x' to input x; SmoothGrad averages gradients across noisy Gaussian neighborhoods."),
            ("PFI (Permutation Feature Importance)", "Global perturbation explainer measuring predictive performance loss when values of a single feature are randomly shuffled across samples."),
            ("Expected Calibration Error (ECE) & Brier Score", "Calibration metrics measuring agreement between predicted probabilities and true empirical outcomes: ECE averages weighted |accuracy − confidence| across probability bins; Brier Score computes mean squared probability error."),
            ("Homeostasis (Healthy-Survivor Baseline)", "Stable physiological equilibrium used to define the Integrated Gradients baseline vector x' as the median feature profile of surviving non-critical patients.")
        ],
        "mechanics": [
            ("Metric 1 — Local Lipschitz Stability (Ŝ<sub>Lip</sub>)", "Ŝ<sub>Lip</sub>(x; f, E, h) = (1/M) ∑<sub>m=1</sub><sup>M</sup> [ ‖E<sub>f</sub>(x + δ<sub>m</sub>) − E<sub>f</sub>(x)‖<sub>2</sub> / (‖δ<sub>m</sub>‖<sub>2</sub> + δ<sub>0</sub>) ], where δ<sub>m</sub> ∼ N(0, h²I), M = 100, h = 0.05, and smoothing constant δ<sub>0</sub> = 10⁻⁸."),
            ("Metric 2 — Cross-Explainer Discordance (D<sub>XAI</sub>)", "D<sub>XAI</sub>(x; f) = 1 − [2 / K(K − 1)] ∑<sub>j < k</sub> r<sub>s</sub>(E<sub>j</sub>(x), E<sub>k</sub>(x)) ∈ [0, 2], where r<sub>s</sub> is Spearman rank correlation across K = 6 explainers."),
            ("Metric 3 — Clinical Prior Alignment (W<sub>Clin</sub><sup>norm</sup>)", "W<sub>Clin</sub><sup>norm</sup>(x) = W<sub>1</sub>(E<sub>norm</sub>(x), P<sub>clin</sub>) / (d − 1) ∈ [0, 1], with Alignment Score A<sub>Clin</sub> = 1 − W<sub>Clin</sub><sup>norm</sup>."),
            ("Metric 4 — Trust Factor & Clinical Utility (T<sub>Clin</sub>, Û<sub>Clin</sub>)", "T<sub>Clin</sub> = (1/3) [ 1/(1 + Ŝ<sub>Lip</sub>) + A<sub>Clin</sub> + (1 − ECE) ];  Û<sub>Clin</sub> = Acc · T<sub>Clin</sub> − (α · OR + β · UR), where OR = (1 − Acc)(1 − 0.4 T<sub>Clin</sub>), UR = Acc(1 − T<sub>Clin</sub>)(0.3), α = 0.50, β = 0.30.")
        ],
        "clinical_context": [
            ("Physiological Baseline Selection for Integrated Gradients", "Unlike computer vision where an all-zero tensor represents a neutral black image, zeroed clinical vitals (blood pressure = 0 mmHg, temp = 0 °C) are biologically invalid. Using the training-cohort healthy-survivor median ensures path integrals measure clinically meaningful deviation from homeostasis.")
        ],
        "rationales": [
            ("Multi-Explainer Coverage Across 4 Mathematical Families", "Hospital software systems deploy heterogeneous explainers (Shapley values, linear surrogates, path integrals, or permutations). Evaluating all 6 verifies whether explanations agree across methodological assumptions."),
            ("Healthy-Survivor Baseline Validity", "Anchoring Integrated Gradients at survivor medians isolates pathological deterioration (e.g., hyperlactatemia or hypotension) rather than measuring artificial distance from zero.")
        ]
    },
    {
        "slide_num": 6,
        "title": "Experimental Setup & Auditing Protocol",
        "overview": "Documents the 4 clinical cohorts (51,369 total encounters), codified medical prior vectors, software stack, hardware profile, and 50-seed stratified validation protocol.",
        "terminology": [
            ("MIMIC-IV (N = 40,000 encounters)", "Single-center Beth Israel Deaconess Medical Center ICU EHR database (Johnson et al., Sci. Data 2023). Task: Sepsis-3 mortality. Priors: SOFA (0.35), Serum Lactate (0.30), MAP (0.20), Age (0.15)."),
            ("eICU (N = 10,000 encounters)", "Multi-center Philips Healthcare ICU Collaborative Research Database (Pollard et al., Sci. Data 2023). Task: Acute hospital mortality. Priors: MAP (0.40), WBC (0.20), Creatinine (0.20), Temperature (0.20)."),
            ("Sepsis-3 & SOFA Score", "International consensus sepsis definition (Singer et al., JAMA 2016) based on acute Sequential Organ Failure Assessment (SOFA, 0–24 points) grading dysfunction across respiratory, coagulation, liver, cardiovascular, CNS, and renal systems."),
            ("Serum Lactate", "Blood biomarker quantifying cellular hypoperfusion and anaerobic metabolism; concentrations > 2 mmol/L indicate severe tissue hypoxia and septic shock risk."),
            ("MAP (Mean Arterial Pressure)", "Average blood pressure during a single cardiac cycle (≈ 1/3 SBP + 2/3 DBP); maintaining MAP ≥ 65 mmHg is a core ICU resuscitation target for organ perfusion."),
            ("WBC (White Blood Cell Count) & Serum Creatinine", "WBC tracks systemic immune/inflammatory response (infection); serum creatinine is a renal filtration biomarker where elevation indicates Acute Kidney Injury (AKI)."),
            ("BCWD (N = 569) & NPI (Nottingham Prognostic Index)", "Wisconsin Breast Cancer Diagnostic dataset classifying malignancy from fine-needle aspirate nuclear morphometry; aligned with NPI priors: Mean Area & Concavity (0.25), Perimeter (0.25), Texture (0.25), Radius (0.25)."),
            ("Cardio EHR (N = 800) & ACC/AHA ASCVD Equations", "10-year Atherosclerotic Cardiovascular Disease (ASCVD) risk cohort aligned with American College of Cardiology / AHA Pooled Cohort Equations: Systolic BP (0.30), Age (0.25), Total Cholesterol (0.25), Smoking (0.20)."),
            ("Stratified 5-Fold CV × 50 Seeds", "Repeated stratified 5-fold cross-validation across 50 independent random seeds (seeds 42–91), generating 250 trained models per architecture while preserving class balance."),
            ("Data Leakage", "Invalid contamination of training normalization or imputation parameters with validation/test data statistics, prevented here via fold-isolated scaling and median imputation.")
        ],
        "mechanics": [
            ("Computational & Software Environment", "Software: Python 3.10+, PyTorch 2.14, Scikit-learn, Captum, SHAP, SciPy. Hardware: Apple Silicon M-series and Linux x86_64 with 16 GB RAM, confirming reproducible execution without multi-GPU cluster dependencies."),
            ("Leakage-Free Preprocessing & Imputation", "Continuous clinical variables undergo fold-isolated z-score standardization: x<sub>scaled</sub> = (x − μ<sub>train</sub>) / σ<sub>train</sub>. Missing validation entries are imputed exclusively with training-fold medians.")
        ],
        "clinical_context": [
            ("Cross-Institutional & Cross-Specialty Generalization", "Evaluating single-center ICU (MIMIC-IV), multi-hospital ICU (eICU), oncology pathology (BCWD), and outpatient cardiology (Cardio EHR) tests generalizability across diverse patient populations and feature dimensionalities.")
        ],
        "rationales": [
            ("Objectivity & Robustness of Clinical Prior Weights", "Prior vectors P<sub>clin</sub> derive directly from published consensus instruments (Sepsis-3, NPI, ACC/AHA ASCVD). Sensitivity sweeps perturbing prior weights by ±20% showed 100% invariance in model rankings."),
            ("Statistical Power of 50-Seed Protocol", "Executing 50 independent trials across seeds 42–91 yields sufficient paired observations for non-parametric Wilcoxon and parametric t-tests, eliminating random split variance.")
        ]
    },
    {
        "slide_num": 7,
        "title": "Results: Accuracy vs. Clinical Explanation Reliability",
        "overview": "Presents primary MIMIC-IV findings demonstrating that Extra Trees achieves +19.6% higher calibrated clinical utility over Tabular Deep ResNet (0.8485 vs. 0.7095/0.7107, p < 0.001) despite slightly lower raw accuracy.",
        "terminology": [
            ("Absolute Gain (Percentage Points) vs. Relative Utility Gain", "Extra Trees (Û<sub>Clin</sub> = 0.8485) outperforms Tabular Deep ResNet (0.7095–0.7107) by +0.1390 absolute (+13.9 percentage points) and +19.6% proportionally relative to baseline (0.1390 / 0.7095)."),
            ("Non-Parametric Wilcoxon Signed-Rank Test (W = 0.0, p < 0.001)", "Distribution-free paired hypothesis test requiring no Gaussian normality assumption. W = 0.0 is the theoretical minimum statistic, proving Extra Trees outperformed Deep ResNet across all 50 paired seeds."),
            ("Parametric Paired t-test (t = 14.82, p < 0.001)", "Mean paired-difference significance test confirming decisive separation across the 50 trial seeds."),
            ("Cohen's d = 2.96 & Pooled Standard Deviation (s<sub>pooled</sub>)", "Standardized effect size defined as (μ<sub>1</sub> − μ<sub>2</sub>) / s<sub>pooled</sub>, where s<sub>pooled</sub> combines group variances. Values > 0.8 are conventionally large; d = 2.96 reflects extreme separation."),
            ("Boundary Memorization / Overfitting", "Tendency of over-parameterized neural networks to fit sharp, sample-specific decision boundaries around training noise, yielding marginal raw accuracy gains at the expense of explanation stability."),
            ("Inference Latency", "Per-patient scoring runtime: Extra Trees = 4.2 ms, Random Forest = 6.8 ms, Tabular Deep ResNet = 48.5 ms (11.5× slower than Extra Trees).")
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
            ("Why Lower Raw Accuracy Yields Higher Clinical Utility", "The 1.23% accuracy margin of Deep ResNet arises from high-frequency local boundary fitting, which drives 49.1% attribution instability under sensor noise and elevated calibration error (ECE = 0.055), degrading calibrated trust and net decision utility."),
            ("Extra Trees vs. Random Forest Stability Advantage (0.0512 vs. 0.0821)", "Random Forest optimizes deterministic split thresholds via Gini/entropy, yielding sharper sample-sensitive partitions. Extra Trees selects random split cut-points per candidate feature, acting as a regularizer that produces smoother local variance and tighter Lipschitz stability.")
        ]
    },
    {
        "slide_num": 8,
        "title": "Results: Explainer Discordance & Accuracy Decoupling",
        "overview": "Quantifies pairwise cross-explainer discordance matrices (Fig. 2) and demonstrates the statistical decoupling between predictive AUROC and calibrated clinical decision utility (Fig. 3, R² = 0.04).",
        "terminology": [
            ("Spearman Rank Correlation (r<sub>s</sub>) & D<sub>XAI</sub> Scale [0, 2]", "Non-parametric correlation measuring monotonic agreement between ordinal feature ranks (r<sub>s</sub> ∈ [−1, +1]). Discordance D<sub>XAI</sub> = 1 − r<sub>s</sub> spans 0 (perfect agreement), 1 (uncorrelated), to 2 (total rank inversion)."),
            ("Cosine Similarity", "Magnitude-sensitive vector angle metric; unlike Spearman r<sub>s</sub>, it can vary simply from scaling differences across explainer axioms rather than ordinal priority flips."),
            ("Ordinal Top-k Ranking", "Ordered priority list of the top k clinical drivers (e.g., top-3 features) used by physicians during rapid triage evaluation."),
            ("Tree Ensemble Consensus (D<sub>XAI</sub> = 0.059)", "Extra Trees achieves mean pairwise rank correlation r<sub>s</sub> = 0.941 across TreeSHAP, KernelSHAP, and LIME (94.1% ordinal consensus)."),
            ("Neural Architecture Conflict (D<sub>XAI</sub> = 0.435)", "Tabular Deep ResNet exhibits mean r<sub>s</sub> = 0.565 across Integrated Gradients, SmoothGrad, and LIME (7.4× higher disagreement than Extra Trees)."),
            ("Ordinary Least-Squares (OLS) & R² (Coefficient of Determination)", "Linear regression metric quantifying explained variance. Regressing Û<sub>Clin</sub> on AUROC across cohorts yields R² = 0.038 (≈ 0.04, p = 0.42), proving AUROC explains <4% of clinical utility variance."),
            ("Non-Convex Decision Manifold", "Complex, multi-curved geometric classification surface learned by deep neural nets where local linear surrogates (LIME) and path integrals (IG) project divergent approximations."),
            ("The Disagreement Problem", "Empirical conflict across competing post-hoc explainers documented by Krishna et al. (ACM CHI 2022), formalized in C-XAI via D<sub>XAI</sub> and shown to be architecture-dependent.")
        ],
        "mechanics": [
            ("Pairwise Discordance Breakdown (MIMIC-IV, Fig. 2)",
             "Tree Ensemble (Extra Trees): TreeSHAP vs. KernelSHAP = 0.042; TreeSHAP vs. LIME = 0.059; KernelSHAP vs. LIME = 0.075 (Mean D<sub>XAI</sub> = 0.059).\n"
             "Tabular Deep ResNet: Integrated Gradients vs. SmoothGrad = 0.312–0.392; Integrated Gradients vs. LIME = 0.435; SmoothGrad vs. LIME = 0.458–0.478 (Mean D<sub>XAI</sub> = 0.435).")
        ],
        "clinical_context": [
            ("Cognitive Dissonance in Multi-Tool Hospitals", "When Integrated Gradients ranks Serum Lactate as the primary sepsis driver while LIME ranks Patient Age first for the exact same patient encounter, clinicians receive irreconcilable rationales, causing decision paralysis.")
        ],
        "rationales": [
            ("Choice of Spearman Rank Correlation Over Cosine Similarity", "Bedside clinicians rely on ordinal top-k feature rankings rather than continuous floating-point magnitudes. Spearman correlation directly measures rank invariance across explainers without magnitude-scale distortion."),
            ("Interpretation of Explainer Divergence on Deep Networks", "Cross-explainer disagreement is a diagnostic signature of a convoluted, non-convex neural decision surface where distinct local approximation methods yield incompatible feature rankings.")
        ]
    },
    {
        "slide_num": 9,
        "title": "Discussion: Insights, Robustness & Regulatory Impact",
        "overview": "Resolves the Representation Paradox geometrically, reports noise-radius scaling and adversarial robustness under FGSM/ScaL-PGD, and details regulatory certification alignment.",
        "terminology": [
            ("The Representation Paradox", "Empirical refutation of the intuition that smooth, continuous neural networks generate more stable explanations than piecewise-constant tree ensembles."),
            ("Axis-Aligned Leaf Hyper-Rectangles", "Disjoint orthogonal feature cells R<sub>k</sub> partitioned by tree splits, inside which model predictions and local TreeSHAP attributions remain invariant."),
            ("ReLU / Swish Activations & Gradient Shattering", "Non-linear activation functions whose deep composition causes neural input gradients to oscillate rapidly across small neighborhoods ('gradient shattering')."),
            ("Hessian Matrix (∇²f(x)) & Eigenvalues", "Matrix of second-order partial derivatives quantifying local curvature of a neural decision surface; large Hessian eigenvalues cause minor vital-sign noise δ to trigger large attribution swings."),
            ("Sub-Linear vs. Supra-Linear Noise Scaling (h ∈ [0.01, 0.20])", "Sub-linear scaling grows slower than proportionally (Extra Trees Ŝ<sub>Lip</sub>: 0.018 → 0.103), whereas supra-linear scaling accelerates explosively (>12× degradation in deep models)."),
            ("Rank Inversion & Adversarial Attribution Collapse", "Severe distortion state (D<sub>XAI</sub> → 2.0) under FGSM (ε = 0.02) and 5-step ScaL-PGD attacks, where Deep ResNet collapses to D<sub>XAI</sub> = 1.862–1.928 and Ŝ<sub>Lip</sub> = 0.865–0.938 while Random Forest maintains D<sub>XAI</sub> ≤ 0.312 and Ŝ<sub>Lip</sub> ≤ 0.132."),
            ("FDA GMLP Principle 7 & Pre-Deployment Audit Gate", "FDA Good Machine Learning Practice Principle 7 mandating real-world risk monitoring; operationalized via quantitative release thresholds (e.g., Ŝ<sub>Lip</sub> ≤ 0.10–0.15, D<sub>XAI</sub> ≤ 0.10–0.15).")
        ],
        "mechanics": [
            ("Geometric Explanation of the Paradox",
             "Tree Partition Invariance: For input x inside leaf cell R<sub>k</sub>, any perturbation δ keeping (x + δ) ∈ R<sub>k</sub> satisfies f(x + δ) = f(x) and yields zero attribution change (‖E<sub>f</sub>(x + δ) − E<sub>f</sub>(x)‖<sub>2</sub> = 0) across the interior cell volume.\n"
             "Neural Manifold Curvature: For multi-layer networks f(x) = W<sub>L</sub>σ(...σ(W<sub>1</sub>x)), gradients ∇<sub>x</sub>f(x) vary continuously across curved manifolds with large Hessian eigenvalues, amplifying attribution shift for small δ."),
            ("Weight Sensitivity Verification (T<sub>Clin</sub> / Û<sub>Clin</sub>)", "Across 5 weight configurations (w<sub>s</sub>, w<sub>a</sub>, w<sub>c</sub>)—Balanced (0.33, 0.33, 0.33), Stability-Focused (0.60, 0.20, 0.20), Clinical-Prior Focused (0.20, 0.60, 0.20), Calibration-Focused (0.20, 0.20, 0.60), and Robust Clinical (0.40, 0.40, 0.20)—tree ensembles consistently outperform deep networks.")
        ],
        "clinical_context": [
            ("Regulatory Operationalization (FDA SaMD & EU AI Act)", "Translates high-level regulatory mandates (EU AI Act Articles 13 & 14; FDA GMLP Principle 7) into enforceable quantitative pre-deployment certification checks.")
        ],
        "rationales": [
            ("Why Discontinuous Trees Exhibit Higher Practical Stability", "Although decision trees exhibit step discontinuities at split boundaries, the interior volume of leaf hyper-rectangles dominates physiological noise neighborhoods (h = 0.05). Conversely, neural continuity does not imply flatness: steep local curvature produces large attribution volatility."),
            ("EU AI Act Articles 13 & 14 Alignment", "Article 13 mandates interpretable outputs for high-risk medical AI systems, and Article 14 mandates human oversight preventing automation bias. C-XAI supplies automated audit trails verifying both mandates prior to hospital deployment.")
        ]
    },
    {
        "slide_num": 10,
        "title": "Conclusion & Future Scope",
        "overview": "Synthesizes C-XAI's theoretical, empirical, and clinical contributions alongside defined study boundaries and future research directions.",
        "terminology": [
            ("Core Scientific Contributions", "1. Formulation of 4 auditing metrics (Ŝ<sub>Lip</sub>, D<sub>XAI</sub>, W<sub>Clin</sub><sup>norm</sup>, Û<sub>Clin</sub>). 2. Zeroth-Order Gaussian Smoother for step-function trees. 3. Proof of Accuracy-Reliability Decoupling (R² = 0.04) across 51,369 encounters. 4. Regulatory deployment gates."),
            ("Multimodal Clinical Data", "Heterogeneous medical data combining structured EHR tables, continuous physiological waveforms, free-text clinical notes, and medical imaging (radiograms)."),
            ("BioClinicalBERT", "Domain-adapted Bidirectional Encoder Representations from Transformers pre-trained on biomedical literature and clinical ICU notes for unstructured clinical text modeling."),
            ("LSTM (Long Short-Term Memory) & Clinical Transformers", "Sequential neural architectures capturing temporal dynamics across irregular longitudinal ICU vital-sign trajectories."),
            ("Dynamic Trajectory Auditing", "Planned formulation of temporal Lipschitz stability metrics evaluating explanation consistency across continuous time-series streams."),
            ("Human-in-the-Loop Prospective Reader Trials", "Controlled clinical simulation evaluations measuring real physicians' diagnostic accuracy, triage speed, and cognitive workload with audited explanations.")
        ],
        "mechanics": [
            ("Tri-Partite Synthesis", "Empirical: Extra Trees delivers +19.6% higher net clinical utility (0.8485 vs. 0.7095/0.7107, p < 0.001). Methodological: Post-hoc explanations require multi-explainer and noise-perturbation auditing prior to deployment. Theoretical: Continuous neural representations suffer severe attribution fragility on tabular healthcare data.")
        ],
        "clinical_context": [
            ("Clinical Deployment Principle", "Model selection in high-stakes healthcare cannot rely on predictive AUROC alone; pre-deployment auditing of stability, consensus, calibration, and guideline alignment is essential to prevent silent triage hazards.")
        ],
        "rationales": [
            ("Defined Study Scope & Limitations", "Three explicit boundaries define current scope: (1) evaluation targets structured tabular EHR cohorts rather than continuous high-frequency waveforms or imaging; (2) clinical utility is quantified via calibrated decision-theoretic modeling rather than prospective live ICU reader trials; and (3) clinical prior vectors cover four benchmark diseases and will expand across additional subspecialties.")
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
            ("Grad-CAM & BCI [5]", "Gradient-weighted Class Activation Mapping (CNN visual saliency method) and Brain-Computer Interface applications cited in Lamba & Rani (2024)."),
            ("Agarwal et al. (NeurIPS 2022) & Hedström et al. (JMLR 2023) [7, 8]", "OpenXAI and Quantus evaluation toolkits benchmarking synthetic fidelity and vision/NLP metrics."),
            ("Krishna et al. (ACM CHI 2022) [9]", "Empirical characterization of the XAI disagreement problem across competing post-hoc explainers."),
            ("ReliefF [21]", "Distance-based supervised filter feature-selection algorithm sensitive to conditional feature interactions."),
            ("Two-Layered Voting (TLV) & White-Box AI [25–28]", "Prior institutional publications by Dr. Ramya G R et al. on Two-Layered Voting ensembles for Coronary Artery Disease (CAD), explainable diabetes/CVD risk models, and intrinsically inspectable White-Box AI architectures.")
        ],
        "mechanics": [
            ("Advancement Beyond Prior Evaluation Literature", "While Krishna et al. (2022) documented explainer disagreement empirically and OpenXAI/Quantus formalized synthetic checks, C-XAI introduces a bounded cross-explainer discordance metric (D<sub>XAI</sub> ∈ [0, 2]), uncovers architectural root causes on tabular data, and integrates stability, prior alignment, and ECE into net decision utility.")
        ],
        "clinical_context": [
            ("Human-AI Clinical Literature Grounding", "Integrates empirical clinician reliance findings from Bussone et al. (2015), Jacobs et al. (2021), Buçinca et al. (Artif. Intell. Med. 2023), and Bansal et al. (ACM CHI 2024) into formal quantitative utility parameters.")
        ],
        "rationales": [
            ("Relation to Krishna et al. (CHI 2022)", "Krishna et al. identified cross-explainer disagreement empirically without proposing a resolution metric. C-XAI formalizes D<sub>XAI</sub> and demonstrates empirically that disagreement is strongly architecture-dependent (0.059 in Extra Trees vs. 0.435 in Deep ResNet).")
        ]
    },
    {
        "slide_num": 12,
        "title": "Author Contact & Reproducibility Artifacts",
        "overview": "Provides presenting/corresponding author contact information, Paper ID attribution, and open-source artifact details for code and benchmark reproduction.",
        "terminology": [
            ("Presenting Author", "Sheela Akshar Sakhi (aksharsakhi@gmail.com), Department of Computer Science & Engineering, Amrita School of Computing, Coimbatore."),
            ("Corresponding Author & Supervisor", "Dr. Ramya G R (gr_ramya@cb.amrita.edu), Department of Computer Science & Engineering, Amrita School of Computing, Coimbatore."),
            ("Deterministic Seeding", "Fixing pseudo-random generators (seeds 42–91 across NumPy, PyTorch, and scikit-learn) so cross-validation folds, noise draws, and neural initializations reproduce deterministically."),
            ("Public Code Repository", "https://github.com/aksharsakhi/c-xai-healthcare-predictions (cxai-1.0.0 library, metric modules, and experiment scripts).")
        ],
        "mechanics": [
            ("Repository Artifact Structure", "Core metrics implemented in src/cxai/metrics.py (compute_empirical_lipschitz_stability, compute_cross_explainer_discordance, compute_clinical_wasserstein_distance, compute_expected_calibration_error, compute_brier_score, compute_calibrated_clinical_utility); robustness and weight sensitivity tables in src/compute_revision_tables.py and src/run_revision_experiments.py.")
        ],
        "clinical_context": [
            ("Open-Science Verification", "All random seeds (42–91), codified clinical prior dictionaries, and statistical verification pipelines are openly archived to support independent hospital IT verification and regulatory auditing.")
        ],
        "rationales": [
            ("Concise Technical Summary", "C-XAI demonstrates across 51,369 clinical encounters that predictive AUROC does not guarantee explanation reliability (R² = 0.04), and establishes quantitatively that randomized tree ensembles deliver 19.6% higher calibrated clinical decision utility (p < 0.001, d = 2.96) than deep tabular networks.")
        ]
    }
]
