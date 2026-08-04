import os
import subprocess

dot_content = """
digraph CXAI_Architecture {
    fontname="Helvetica,Arial,sans-serif";
    node [fontname="Helvetica,Arial,sans-serif", shape=rect, style="filled,rounded", linewidth=2.0];
    edge [fontname="Helvetica,Arial,sans-serif", fontsize=11, color="#1e3a8a", penwidth=2.5];
    rankdir=TB;
    nodesep=0.5;
    ranksep=0.4;
    bgcolor="#ffffff";

    // Header Title
    header [shape=none, margin=0, label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
        <TR><TD><FONT POINT-SIZE="18" COLOR="#1e3a8a"><B>C-XAI CLINICAL BENCHMARK PIPELINE</B></FONT></TD></TR>
        <TR><TD><FONT POINT-SIZE="12" COLOR="#475569">Author: Sheela Akshar Sakhi (cb.sc.u4cse23547) | Supervisor: Dr. G. R. Ramya</FONT></TD></TR>
    </TABLE>>];

    // TOP ROW: Stage 1 and Stage 2 side-by-side
    subgraph {
        rank=same;
        
        // STAGE 1: Clinical Data & Noise Engine
        subgraph cluster_0 {
            label=<<B><FONT POINT-SIZE="13" COLOR="#1e40af">STAGE 1: Clinical Data &amp; Noise Engine</FONT></B>>;
            style="filled,rounded";
            fillcolor="#eff6ff";
            color="#2563eb";
            penwidth=2.5;

            s1_box [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5">
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="11"><B>Clinical Data Cohorts</B></FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="#334155">• Multi-Hospital EHR Vitals &amp; Lab Feeds<br/>• Breast Cancer Diagnostic Dataset</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9" COLOR="#94a3b8">----------------------------------------------------</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="11" COLOR="#dc2626"><B>Noise Perturbation Engine</B></FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="#991b1b">• ε-Ball Noise Injection: δ ~ N(0, ε²I)<br/>• Perturbed Vector: x' = x + δ ∈ B_ε(x)</FONT></TD></TR>
            </TABLE>>, fillcolor="#ffffff", color="#93c5fd"];
        }

        // STAGE 2: Predictive Model Zoo
        subgraph cluster_1 {
            label=<<B><FONT POINT-SIZE="13" COLOR="#15803d">STAGE 2: Predictive Model Zoo</FONT></B>>;
            style="filled,rounded";
            fillcolor="#f0fdf4";
            color="#16a34a";
            penwidth=2.5;

            s2_box [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5">
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="11"><B>Model Architecture Zoo</B></FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="#166534">• Random Forest Classifier (100 Trees)<br/>• Extra Trees Ensemble (Randomized Splits)<br/>• Multi-Layer Perceptron (Dense 64x32 NN)</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9" COLOR="#94a3b8">----------------------------------------------------</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="#15803d"><B>Outputs:</B> Predictive Outcome y_hat ∈ {0,1}</FONT></TD></TR>
            </TABLE>>, fillcolor="#ffffff", color="#86efac"];
        }
    }

    // MIDDLE ROW: Stage 3 and Stage 4 side-by-side
    subgraph {
        rank=same;

        // STAGE 3: Post-Hoc Explainer Engine
        subgraph cluster_2 {
            label=<<B><FONT POINT-SIZE="13" COLOR="#7e22ce">STAGE 3: Post-Hoc Explainer Engine</FONT></B>>;
            style="filled,rounded";
            fillcolor="#faf5ff";
            color="#9333ea";
            penwidth=2.5;

            s3_box [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5">
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="11"><B>Explainer Algorithms</B></FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="#6b21a8">• TreeSHAP / KernelSHAP (Shapley φ_j)<br/>• LIME Tabular (Local Surrogates)<br/>• Permutation Feature Importance (PFI)</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9" COLOR="#94a3b8">----------------------------------------------------</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10" COLOR="#7e22ce"><B>Outputs:</B> Attribution Vector E_f(x) ∈ R^d</FONT></TD></TR>
            </TABLE>>, fillcolor="#ffffff", color="#d8b4fe"];
        }

        // STAGE 4: C-XAI Quantitative Metrics Core
        subgraph cluster_3 {
            label=<<B><FONT POINT-SIZE="13" COLOR="#a16207">STAGE 4: Quantitative Metrics Suite</FONT></B>>;
            style="filled,rounded";
            fillcolor="#fefce8";
            color="#ca8a04";
            penwidth=2.5;

            s4_box [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5">
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10.5"><B>1. Lipschitz Stability Index (S_Lip):</B><br/>   max ||E(x)-E(x')|| / ||x-x'||</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10.5"><B>2. Explainer Discordance (D_XAI):</B><br/>   1 - Spearman ρ(r^A, r^B)</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10.5"><B>3. Clinical Wasserstein Distance:</B><br/>   EMD(P_Model, P_Prior)</FONT></TD></TR>
                <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="10.5"><B>4. Calibrated Utility (U_Clin):</B><br/>   A_Model · T - (α OR + β UR)</FONT></TD></TR>
            </TABLE>>, fillcolor="#ffffff", color="#fef08a"];
        }
    }

    // BOTTOM ROW: Stage 5 Clinical Interface (Centered)
    subgraph cluster_4 {
        label=<<B><FONT POINT-SIZE="13" COLOR="#b91c1c">STAGE 5: Clinical Decision Support &amp; Governance Interface</FONT></B>>;
        style="filled,rounded";
        fillcolor="#fff5f5";
        color="#dc2626";
        penwidth=2.5;

        s5_box [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5">
            <TR><TD ALIGN="CENTER"><FONT POINT-SIZE="11"><B>Physician EHR Dashboard &amp; Calibration System</B></FONT></TD></TR>
            <TR><TD ALIGN="CENTER"><FONT POINT-SIZE="10" COLOR="#991b1b">• Interactive Clinical Risk Dashboard  |  • Real-Time Trust Calibration Score T_Clinician<br/>• Over-Reliance &amp; Under-Reliance Alerts  |  • FDA SaMD &amp; EU AI Act Regulatory Compliance</FONT></TD></TR>
        </TABLE>>, fillcolor="#ffffff", color="#fca5a5"];
    }

    // Connections
    header -> s1_box [style=invis];
    s1_box -> s2_box [label=" Perturbed Inputs x'"];
    s2_box -> s3_box [label=" Model Predictions"];
    s1_box -> s3_box [style=invis];
    s3_box -> s4_box [label=" Feature Attributions"];
    s4_box -> s5_box [label=" Quantitative Metrics"];
    s3_box -> s5_box [style=invis];

    // Feedback Loop
    s5_box -> s1_box [label="  Clinical Feedback & Model Re-Calibration Loop  ", style="dashed", color="#dc2626", penwidth=2.5];
}
"""

dot_path = "paper/figures/architecture.dot"
png_path_paper = "paper/figures/fig0_architecture.png"
png_path_ppt = "presentation/figures/fig0_architecture.png"

with open(dot_path, "w") as f:
    f.write(dot_content)

subprocess.run(["dot", "-Tpng", dot_path, "-o", png_path_paper, "-Gdpi=300"], check=True)
subprocess.run(["dot", "-Tpng", dot_path, "-o", png_path_ppt, "-Gdpi=300"], check=True)

print("Compact, highly legible block diagram generated!")
