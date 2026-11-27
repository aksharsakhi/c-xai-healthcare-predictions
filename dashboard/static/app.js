/* app.js — C-XAI Full-Project Visualization Website (Offline Plotly + Real FastAPI Backend) */

const STATE = {
  cohort: "MIMIC-IV ICU Mortality",
  cohortsMeta: [],
  overview: null,
  patientResult: null,
  attackResult: null,
  paperRef: null,
  customFeatures: {},
  activeLayer: "1",
};

const MODEL_COLORS = {
  "Extra Trees": "#0F766E",
  "Random Forest": "#2563EB",
  "MLP": "#D97706",
  "Tabular Deep ResNet": "#DC2626",
};

const PLOT_CFG = { responsive: true, displayModeBar: false };

const LAYER_DETAILS = {
  "1": {
    title: "Layer 1: Clinical Data & Telemetry Perturbation Engine",
    summary: "Standardizes 4 multi-center healthcare cohorts (51,369 encounters) via fold-isolated z-score scaling and injects realistic physiological telemetry noise (Gaussian h = 0.05), 20% MCAR clinical missingness, and adversarial attribution shifts.",
    bullets: [
      "MIMIC-IV ICU Mortality (40,000 records) — Sepsis-3 priors: SOFA (0.35), Lactate (0.30), Age (0.15), BP (0.10), HR (0.10)",
      "eICU Multi-Site Sepsis (10,000 records) — Hemodynamic priors: MAP (0.40), Temp (0.25), WBC (0.20), HR (0.15)",
      "BCWD Oncology (569 real records) — NPI nuclear morphometry priors across 30 features",
      "Cardio EHR (800 records) — ACC/AHA ASCVD 10-year cardiovascular risk priors",
    ],
    formula: "x_pert = x + δ_m,   δ_m ~ N(0, h² I),   h ∈ [0.01, 0.20]   |   20% MCAR masked to survivor median x'",
  },
  "2": {
    title: "Layer 2: Predictive Model Zoo & Zeroth-Order Gaussian Smoother",
    summary: "Trains two piecewise-constant tree ensembles (Platt-calibrated Extra Trees & Random Forest) alongside two continuous neural networks (MLP & PyTorch Tabular Deep ResNet). Bridges non-differentiable tree step boundaries using Stein's Lemma.",
    bullets: [
      "Extra Trees & Random Forest: Partition clinical space into axis-aligned leaf hyper-rectangles where interior predictions remain constant under small sensor drift",
      "Platt Sigmoid Calibration: Out-of-fold logistic calibration aligns predicted probabilities with empirical risk (ECE < 0.015)",
      "Tabular Deep ResNet & MLP: Continuous SiLU/ReLU skip-connection manifolds vulnerable to steep local Hessian curvature",
      "Zeroth-Order Smoother: Convolves tree predictions with isotropic Gaussian noise σ = 0.05 so gradient explainers run natively on trees",
    ],
    formula: "∇f_σ(x) = (1 / σ²) · E_{u ~ N(0, σ²I)} [ (f(x + u) − f(x)) · u ]   (Stein's Lemma Score Estimator)",
  },
  "3": {
    title: "Layer 3: Multi-Family Post-Hoc Explainer Suite",
    summary: "Computes local counterfactual feature attributions across competing mathematical foundations anchored at the healthy-survivor cohort median x' (homeostasis) rather than biologically invalid zeros.",
    bullets: [
      "Game Theory: TreeSHAP (exact polynomial path conditioning on tree ensembles) & KernelSHAP (coalition regression)",
      "Local Surrogates: LIME weighted Ridge regression over Gaussian neighborhood perturbations",
      "Gradient & Path Integrals: Integrated Gradients (from survivor median x' to x) & SmoothGrad",
      "Perturbation Ablation: Local Permutation Feature Importance (PFI) risk drop when replacing feature j with baseline x'_j",
    ],
    formula: "IG_j(x) = (x_j − x'_j) · ∫_{0}^{1} ∂f(x' + α(x − x')) / ∂x_j dα,   x' = median(X_train | y = 0)",
  },
  "4": {
    title: "Layer 4: Quantitative Reliability Auditing Metrics",
    summary: "Replaces anecdotal visual inspection with four formal metrics auditing local stability, cross-explainer rank consensus, medical guideline fidelity, and probability calibration.",
    bullets: [
      "Local Lipschitz Stability (S_Lip ↓): Measures relative attribution vector drift across M Monte Carlo noise draws",
      "Cross-Explainer Discordance (D_XAI ↓): Pairwise Spearman rank disagreement (1 − r_s) ∈ [0, 2] across explainers",
      "Clinical Prior Alignment (W_Clin^norm ↓): (d−1)-normalized 1D Earth Mover's (Wasserstein) distance to SOFA/NPI/ASCVD weights",
      "Expected Calibration Error (ECE ↓): Weighted gap between predicted risk confidence and true observed mortality",
    ],
    formula: "S_Lip = (1/M) ∑ ||E(x+δ_m)−E(x)||₂ / (||δ_m||₂+δ₀)   |   D_XAI = 1 − mean(r_s)   |   W_Clin^norm = W₁(E_norm, P_clin) / (d−1)",
  },
  "5": {
    title: "Layer 5: Pauker–Kassirer Calibrated Clinical Decision Utility",
    summary: "Translates technical explanation quality into clinician decision-theoretic net utility by modeling trust calibration T_Clin and asymmetric mortality penalties for over-reliance vs. under-reliance.",
    bullets: [
      "Trust Calibration Factor (T_Clin ↑): Weighted average of inverse instability, guideline alignment (1 − W_Clin^norm), and calibration (1 − ECE)",
      "Over-Reliance Penalty (α = 0.50): High cost of false reassurance when clinicians uncritically follow erroneous negative predictions",
      "Under-Reliance Penalty (β = 0.30): Diagnostic delay/burden when erratic explanations cause clinicians to dismiss valid alerts",
      "Pre-Deployment Certification: Operationalizes EU AI Act Articles 13 & 14 and FDA SaMD GMLP Principle 7",
    ],
    formula: "T_Clin = (1/3)[ 1/(1+S_Lip) + A_Clin + (1−ECE) ]   |   U_Clin = Acc·T_Clin − (0.50·OR + 0.30·UR)",
  },
};

function setStatus(msg) {
  document.getElementById("engine-status").textContent = msg;
}

async function apiGet(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function apiPost(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function cssId(name) {
  return name.replace(/[^a-zA-Z0-9]/g, "_");
}

// =========================================================================
// PIPELINE LAYER CLICK HANDLER
// =========================================================================
function renderLayerInspector(layerId) {
  STATE.activeLayer = layerId;
  document.querySelectorAll(".pipe-node").forEach((n) => {
    n.classList.toggle("active", n.dataset.layer === layerId);
  });
  const info = LAYER_DETAILS[layerId];
  const cohortNote = STATE.overview
    ? `<div style="margin-top:10px; font-size:12.5px; color:#0F766E; font-weight:600;">Active Cohort Snapshot (${STATE.overview.spec.short}): ${STATE.overview.counts.n_total.toLocaleString()} encounters · Guideline: ${STATE.overview.spec.guideline}</div>`
    : "";

  document.getElementById("layer-inspector").innerHTML = `
    <div>
      <h3 style="margin:0 0 6px; font-size:16px; color:#0F2744;">${info.title}</h3>
      <p style="margin:0 0 10px; font-size:13.5px; color:#334155;">${info.summary}</p>
      <div class="formula-pill">${info.formula}</div>
      ${cohortNote}
    </div>
    <div>
      <div style="font-size:12px; font-weight:700; text-transform:uppercase; color:#2563EB; margin-bottom:6px;">Implementation & Components</div>
      <ul style="margin:0; padding-left:18px; font-size:13px; color:#1E293B; display:flex; flex-direction:column; gap:6px;">
        ${info.bullets.map((b) => `<li>${b}</li>`).join("")}
      </ul>
    </div>
  `;
}

// =========================================================================
// ANALYTICS SUBTABS
// =========================================================================
document.querySelectorAll(".subtab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".subtab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".subpanel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    const target = document.getElementById(btn.dataset.sub);
    target.classList.add("active");
    setTimeout(() => {
      target.querySelectorAll(".plot-box, .plot-tall").forEach((el) => {
        if (el.data) Plotly.Plots.resize(el);
      });
    }, 30);
  });
});

// =========================================================================
// INITIALIZATION
// =========================================================================
async function init() {
  setStatus("Connecting...");
  document.querySelectorAll(".pipe-node").forEach((n) => {
    n.addEventListener("click", () => renderLayerInspector(n.dataset.layer));
  });
  renderLayerInspector("1");

  const [cohortData, paperData] = await Promise.all([
    apiGet("/api/cohorts"),
    apiGet("/api/paper-reference"),
  ]);
  STATE.cohortsMeta = cohortData.cohorts;
  STATE.paperRef = paperData;
  renderPaperArchive(paperData);

  const sel = document.getElementById("cohort-select");
  sel.innerHTML = "";
  cohortData.cohorts.forEach((c) => {
    const opt = document.createElement("option");
    opt.value = c.name;
    opt.textContent = `${c.short} (${c.n_total.toLocaleString()} · ${c.n_features} feat)`;
    sel.appendChild(opt);
  });
  sel.value = STATE.cohort;
  sel.addEventListener("change", () => loadCohort(sel.value, false));

  document.getElementById("btn-rebuild").addEventListener("click", () => loadCohort(STATE.cohort, true));
  document.getElementById("btn-load-sample").addEventListener("click", loadSamplePatient);
  document.getElementById("btn-run-explain").addEventListener("click", runLivePatientExplain);
  document.getElementById("btn-render-surface").addEventListener("click", render2DSurface);
  document.getElementById("explainer-choice").addEventListener("change", () => {
    if (STATE.patientResult) renderPatientCharts(STATE.patientResult);
  });
  document.getElementById("btn-run-attack").addEventListener("click", runLiveAttack);
  document.getElementById("btn-eval-gate").addEventListener("click", renderRegulatoryGate);

  ["noise-h-slider", "mc-samples-slider"].forEach((id) => {
    document.getElementById(id).addEventListener("input", () => {
      document.getElementById("noise-h-val").textContent = Number(document.getElementById("noise-h-slider").value).toFixed(2);
      document.getElementById("mc-samples-val").textContent = document.getElementById("mc-samples-slider").value;
    });
  });

  document.getElementById("surf-h").addEventListener("input", () => {
    document.getElementById("surf-h-val").textContent = Number(document.getElementById("surf-h").value).toFixed(2);
  });

  ["sim-alpha", "sim-beta", "sim-ws", "sim-wa", "sim-wc"].forEach((id) => {
    document.getElementById(id).addEventListener("input", runUtilitySimulation);
  });

  await loadCohort(STATE.cohort, false);
}

async function loadCohort(cohortName, rebuild = false) {
  STATE.cohort = cohortName;
  setStatus(rebuild ? "Re-training & Auditing..." : "Loading Cohort...");
  document.getElementById("sample-idx").value = 0;

  const ov = await apiGet(`/api/overview?cohort=${encodeURIComponent(cohortName)}&rebuild=${rebuild}`);
  STATE.overview = ov;
  document.getElementById("sample-idx").max = ov.counts.n_test - 1;
  document.getElementById("cohort-subtitle").textContent =
    `${ov.spec.clinical_domain} · ${ov.counts.n_total.toLocaleString()} records · Priors: ${ov.spec.guideline}`;
  document.getElementById("guideline-label").textContent = ov.spec.guideline;

  renderLayerInspector(STATE.activeLayer);
  populateSurfaceDropdowns(ov.feature_meta);
  buildFeatureSliders(ov.feature_meta);

  renderOverview(ov);
  renderNoiseScaling(ov);
  renderCalibration(ov);
  renderFairness(ov);
  renderRegulatoryGate();

  await Promise.all([
    loadSamplePatient(),
    render2DSurface(),
    runLiveAttack(),
    runUtilitySimulation(),
  ]);
  setStatus(`Live Engine Ready (${ov.spec.short})`);
}

// =========================================================================
// 2D DECISION GEOMETRY VISUALIZER (THE REPRESENTATION PARADOX)
// =========================================================================
function populateSurfaceDropdowns(featureMeta) {
  const fx = document.getElementById("surf-fx");
  const fy = document.getElementById("surf-fy");
  const names = featureMeta.map((f) => f.name);
  fx.innerHTML = names.map((n) => `<option value="${n}">${n}</option>`).join("");
  fy.innerHTML = names.map((n) => `<option value="${n}">${n}</option>`).join("");
  fx.value = names[0];
  fy.value = names[Math.min(1, names.length - 1)];
}

async function render2DSurface() {
  const fx = document.getElementById("surf-fx").value;
  const fy = document.getElementById("surf-fy").value;
  const noiseH = Number(document.getElementById("surf-h").value);

  const surf = await apiPost("/api/surface/2d", {
    cohort: STATE.cohort,
    feat_x: fx,
    feat_y: fy,
    raw_features: Object.keys(STATE.customFeatures).length ? STATE.customFeatures : null,
    noise_h: noiseH,
    seed: 42,
  });

  document.getElementById("surface-summary").innerHTML =
    `<strong>Live Geometric Audit (${surf.feat_x} vs. ${surf.feat_y}, noise radius h = ${noiseH.toFixed(2)}):</strong> ` +
    `Patient risk estimate: Extra Trees = <strong>${(surf.patient.p_et * 100).toFixed(1)}%</strong> (cloud σ = ${surf.noise_cloud.p_et_std.toFixed(4)}) · ` +
    `Deep ResNet = <strong>${(surf.patient.p_resnet * 100).toFixed(1)}%</strong> (cloud σ = ${surf.noise_cloud.p_resnet_std.toFixed(4)}). ` +
    `White star = patient encounter; yellow dots = 35 real Gaussian noise draws (x + δ).`;

  document.getElementById("surf-et-meta").textContent = `P(Risk)=${(surf.patient.p_et * 100).toFixed(1)}% · σ_cloud=${surf.noise_cloud.p_et_std.toFixed(4)}`;
  document.getElementById("surf-rn-meta").textContent = `P(Risk)=${(surf.patient.p_resnet * 100).toFixed(1)}% · σ_cloud=${surf.noise_cloud.p_resnet_std.toFixed(4)}`;

  function plotContour(divId, zGrid, colorscale) {
    Plotly.newPlot(
      divId,
      [
        {
          x: surf.x_grid,
          y: surf.y_grid,
          z: zGrid,
          type: "contour",
          colorscale: colorscale,
          zmin: 0,
          zmax: 1,
          contours: { coloring: "heatmap", showlabels: true, labelfont: { size: 10, color: "#FFFFFF" } },
          colorbar: { title: "P(Risk=1)", len: 0.88 },
        },
        {
          x: surf.noise_cloud.x,
          y: surf.noise_cloud.y,
          mode: "markers",
          name: `Noise Cloud (h=${noiseH.toFixed(2)})`,
          marker: { size: 6, color: "#FACC15", line: { width: 1, color: "#0F172A" } },
        },
        {
          x: [surf.patient.x],
          y: [surf.patient.y],
          mode: "markers",
          name: "Patient x",
          marker: { size: 14, symbol: "star", color: "#FFFFFF", line: { width: 2, color: "#0F172A" } },
        },
      ],
      {
        margin: { t: 48, r: 20, b: 56, l: 64 },
        xaxis: { title: `${surf.feat_x} (${surf.unit_x})`, automargin: true },
        yaxis: { title: `${surf.feat_y} (${surf.unit_y})`, automargin: true },
        legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
      },
      PLOT_CFG
    );
  }

  plotContour("chart-surf-et", surf.z_extra_trees, "Teal");
  plotContour("chart-surf-rn", surf.z_deep_resnet, "RdBu");
}

// =========================================================================
// LIVE PATIENT EXPLAINER & NOISE WORKBENCH
// =========================================================================
function buildFeatureSliders(featureMeta) {
  const container = document.getElementById("feature-sliders");
  const shown = featureMeta.slice(0, 12);
  container.innerHTML = shown
    .map((f) => `
      <div class="slider-item">
        <div class="slider-top">
          <span>${f.name} <small style="color:#64748B;">(${f.unit})</small>${f.prior_weight > 0 ? ` <span class="badge badge-pass">Prior ${f.prior_weight}</span>` : ""}</span>
          <span class="val" id="val-${cssId(f.name)}">${f.median}</span>
        </div>
        <input type="range" id="sl-${cssId(f.name)}" data-fname="${f.name}"
               min="${f.min}" max="${f.max}" step="${f.step}" value="${f.median}" />
      </div>
    `)
    .join("");

  container.querySelectorAll("input[type='range']").forEach((inp) => {
    inp.addEventListener("input", () => {
      const fn = inp.dataset.fname;
      STATE.customFeatures[fn] = Number(inp.value);
      document.getElementById(`val-${cssId(fn)}`).textContent = Number(inp.value).toFixed(2);
    });
  });
}

async function loadSamplePatient() {
  const idx = Number(document.getElementById("sample-idx").value) || 0;
  const rec = await apiGet(`/api/patient/sample?cohort=${encodeURIComponent(STATE.cohort)}&idx=${idx}`);
  STATE.customFeatures = { ...rec.raw_features };
  document.getElementById("patient-label-badge").textContent =
    `Sample #${rec.sample_idx} · Label: ${rec.true_label === 1 ? "High Risk (1)" : "Low Risk (0)"}`;

  Object.entries(rec.raw_features).forEach(([fn, val]) => {
    const sl = document.getElementById(`sl-${cssId(fn)}`);
    const lb = document.getElementById(`val-${cssId(fn)}`);
    if (sl && lb) {
      sl.value = val;
      lb.textContent = Number(val).toFixed(2);
    }
  });
  await runLivePatientExplain();
}

async function runLivePatientExplain() {
  setStatus("Running Patient Audit...");
  const noiseH = Number(document.getElementById("noise-h-slider").value);
  const mcSamples = Number(document.getElementById("mc-samples-slider").value);

  const res = await apiPost("/api/patient/explain", {
    cohort: STATE.cohort,
    raw_features: STATE.customFeatures,
    noise_h: noiseH,
    mc_samples: mcSamples,
    seed: 42,
  });
  STATE.patientResult = res;
  renderPatientCharts(res);
  setStatus(`Live Engine Ready (${STATE.overview.spec.short})`);
}

function renderPatientCharts(res) {
  const et = res.models["Extra Trees"];
  const rn = res.models["Tabular Deep ResNet"];

  document.getElementById("patient-kpis").innerHTML = `
    <div class="kpi-card teal">
      <div class="kpi-label">Extra Trees Risk & Stability</div>
      <div class="kpi-value">${(et.prob_clean * 100).toFixed(1)}%</div>
      <div class="kpi-detail">Noisy: ${(et.prob_noisy * 100).toFixed(1)}% · S<sub>Lip</sub> = ${et.s_lip.toFixed(4)}</div>
    </div>
    <div class="kpi-card crimson">
      <div class="kpi-label">Deep ResNet Risk & Stability</div>
      <div class="kpi-value">${(rn.prob_clean * 100).toFixed(1)}%</div>
      <div class="kpi-detail">Noisy: ${(rn.prob_noisy * 100).toFixed(1)}% · S<sub>Lip</sub> = ${rn.s_lip.toFixed(4)}</div>
    </div>
    <div class="kpi-card teal">
      <div class="kpi-label">Extra Trees Discordance</div>
      <div class="kpi-value">${et.d_xai.toFixed(4)}</div>
      <div class="kpi-detail">Prior Align ${(et.a_clin * 100).toFixed(1)}% (W=${et.w_clin_norm.toFixed(4)})</div>
    </div>
    <div class="kpi-card crimson">
      <div class="kpi-label">Deep ResNet Discordance</div>
      <div class="kpi-value">${rn.d_xai.toFixed(4)}</div>
      <div class="kpi-detail">Prior Align ${(rn.a_clin * 100).toFixed(1)}% (W=${rn.w_clin_norm.toFixed(4)})</div>
    </div>
  `;

  const choice = document.getElementById("explainer-choice").value;
  function pickVec(mObj, noisy = false) {
    const dict = noisy ? mObj.explainers_noisy : mObj.explainers_clean;
    if (choice === "primary") return dict["TreeSHAP"] || dict["Int. Grads"];
    if (choice === "smoothgrad") return dict["SmoothGrad"] || dict["ZO-SmoothGrad"];
    return dict[choice] || Object.values(dict)[0];
  }

  let feats = res.features;
  let etC = pickVec(et, false), etN = pickVec(et, true);
  let rnC = pickVec(rn, false), rnN = pickVec(rn, true);
  if (feats.length > 10) {
    const idxs = feats
      .map((_, i) => ({ i, mag: Math.abs(etC[i]) + Math.abs(rnC[i]) }))
      .sort((a, b) => b.mag - a.mag)
      .slice(0, 10)
      .map((o) => o.i);
    feats = idxs.map((i) => feats[i]);
    etC = idxs.map((i) => etC[i]);
    etN = idxs.map((i) => etN[i]);
    rnC = idxs.map((i) => rnC[i]);
    rnN = idxs.map((i) => rnN[i]);
  }

  // Horizontal paired bar charts (clean & readable)
  Plotly.newPlot(
    "chart-attr-et",
    [
      { y: feats, x: etC, name: "Clean (x)", type: "bar", orientation: "h", marker: { color: "#0F766E" } },
      { y: feats, x: etN, name: `Noisy (h=${res.noise_h})`, type: "bar", orientation: "h", marker: { color: "#5EEAD4" } },
    ],
    {
      title: { text: "Extra Trees Attribution", font: { size: 13, color: "#0F2744" } },
      barmode: "group",
      margin: { t: 62, r: 16, b: 44, l: 120 },
      xaxis: { title: "Risk Attribution (ΔP)", automargin: true },
      yaxis: { automargin: true, autorange: "reversed" },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );

  Plotly.newPlot(
    "chart-attr-rn",
    [
      { y: feats, x: rnC, name: "Clean (x)", type: "bar", orientation: "h", marker: { color: "#B91C1C" } },
      { y: feats, x: rnN, name: `Noisy (h=${res.noise_h})`, type: "bar", orientation: "h", marker: { color: "#FCA5A5" } },
    ],
    {
      title: { text: "Tabular Deep ResNet Attribution", font: { size: 13, color: "#0F2744" } },
      barmode: "group",
      margin: { t: 62, r: 16, b: 44, l: 120 },
      xaxis: { title: "Risk Attribution (ΔP)", automargin: true },
      yaxis: { automargin: true, autorange: "reversed" },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );

  document.getElementById("et-dxai-sub").textContent = `Mean D_XAI = ${et.discordance_matrix.mean_discordance.toFixed(4)}`;
  document.getElementById("resnet-dxai-sub").textContent = `Mean D_XAI = ${rn.discordance_matrix.mean_discordance.toFixed(4)}`;

  function plotHeatmap(divId, dm, colorscale) {
    Plotly.newPlot(
      divId,
      [
        {
          z: dm.matrix,
          x: dm.explainers,
          y: dm.explainers,
          type: "heatmap",
          colorscale: colorscale,
          zmin: 0,
          zmax: 1.5,
          text: dm.matrix.map((row) => row.map((v) => v.toFixed(2))),
          texttemplate: "%{text}",
          showscale: true,
        },
      ],
      {
        margin: { t: 24, r: 20, b: 68, l: 105 },
        xaxis: { automargin: true, tickangle: -20 },
        yaxis: { automargin: true },
      },
      PLOT_CFG
    );
  }
  plotHeatmap("chart-dxai-et", et.discordance_matrix, "YlGnBu");
  plotHeatmap("chart-dxai-resnet", rn.discordance_matrix, "YlOrRd");

  const pc = et.prior_comparison;
  const pcRn = rn.prior_comparison;
  Plotly.newPlot(
    "chart-prior-align",
    [
      { x: pc.map((p) => p.feature), y: pc.map((p) => p.guideline_weight), name: "Medical Guideline Prior (P_clin)", type: "bar", marker: { color: "#0F2744" } },
      { x: pc.map((p) => p.feature), y: pc.map((p) => p.model_weight), name: "Extra Trees Share", type: "bar", marker: { color: "#0F766E" } },
      { x: pcRn.map((p) => p.feature), y: pcRn.map((p) => p.model_weight), name: "Deep ResNet Share", type: "bar", marker: { color: "#DC2626" } },
    ],
    {
      barmode: "group",
      margin: { t: 56, r: 20, b: 56, l: 55 },
      yaxis: { title: "Normalized Importance Mass", range: [0, 0.72], automargin: true },
      xaxis: { automargin: true },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );
}

// =========================================================================
// COHORT BENCHMARK, ATTACKS, CALIBRATION, FAIRNESS & ARCHIVE
// =========================================================================
function renderOverview(ov) {
  const lb = ov.leaderboard;
  const et = lb.find((r) => r.model === "Extra Trees") || lb[0];
  const resnet = lb.find((r) => r.model === "Tabular Deep ResNet") || lb[lb.length - 1];

  const utilDiff = ((et.u_clin - resnet.u_clin) / Math.max(1e-6, resnet.u_clin)) * 100;
  const slipRatio = resnet.s_lip / Math.max(1e-6, et.s_lip);

  document.getElementById("kpi-cards").innerHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Active Cohort</div>
      <div class="kpi-value">${ov.counts.n_total.toLocaleString()}</div>
      <div class="kpi-detail">${ov.spec.short} · ${ov.counts.n_features} clinical features</div>
    </div>
    <div class="kpi-card teal">
      <div class="kpi-label">Extra Trees Net Utility (U<sub>Clin</sub>)</div>
      <div class="kpi-value">${et.u_clin.toFixed(4)}</div>
      <div class="kpi-detail">${utilDiff >= 0 ? "+" : ""}${utilDiff.toFixed(1)}% vs. Deep ResNet (${resnet.u_clin.toFixed(4)})</div>
    </div>
    <div class="kpi-card crimson">
      <div class="kpi-label">Neural Instability Ratio</div>
      <div class="kpi-value">${slipRatio.toFixed(2)}×</div>
      <div class="kpi-detail">Deep ResNet S<sub>Lip</sub>=${resnet.s_lip.toFixed(4)} vs. ET=${et.s_lip.toFixed(4)}</div>
    </div>
    <div class="kpi-card blue">
      <div class="kpi-label">AUROC–Utility Coupling (R²)</div>
      <div class="kpi-value">${ov.stats_et_vs_resnet.r2_auroc_vs_utility.toFixed(3)}</div>
      <div class="kpi-detail">Accuracy fails to predict explanation reliability</div>
    </div>
  `;

  const st = ov.stats_et_vs_resnet;
  document.getElementById("stats-banner").innerHTML =
    `<strong>Paired Hypothesis Audit (Extra Trees vs. Tabular Deep ResNet across N=${st.n_audited_patients} encounters):</strong> ` +
    `Paired <i>t</i> = <strong>${st.paired_t}</strong> (<i>p</i> = ${st.p_value_t.toExponential(2)}) · ` +
    `Wilcoxon <i>W</i> = <strong>${st.wilcoxon_w}</strong> (<i>p</i> = ${st.p_value_w.toExponential(2)}) · ` +
    `Cohen's <i>d</i> = <strong>${st.cohens_d}</strong> · Audited ${ov.timestamp}`;

  const models = lb.map((r) => r.model);
  Plotly.newPlot(
    "chart-acc-util",
    [
      {
        x: models, y: lb.map((r) => r.accuracy * 100),
        name: "Predictive Accuracy (%)", type: "bar", marker: { color: "#0F2744" },
        text: lb.map((r) => (r.accuracy * 100).toFixed(1) + "%"), textposition: "outside",
      },
      {
        x: models, y: lb.map((r) => r.u_clin * 100),
        name: "Calibrated Clinical Utility (%)", type: "bar", marker: { color: "#0F766E" },
        text: lb.map((r) => (r.u_clin * 100).toFixed(1) + "%"), textposition: "outside",
      },
    ],
    {
      barmode: "group",
      margin: { t: 60, r: 20, b: 50, l: 55 },
      yaxis: { title: "Score (%)", range: [0, 118], automargin: true },
      xaxis: { automargin: true },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );

  document.getElementById("decoupling-r2").textContent = `OLS R² = ${st.r2_auroc_vs_utility.toFixed(4)}`;
  Plotly.newPlot(
    "chart-decoupling",
    [
      {
        x: lb.map((r) => r.auroc),
        y: lb.map((r) => r.u_clin),
        text: lb.map((r) => r.model),
        customdata: lb.map((r) => [r.auroc, r.u_clin, r.s_lip]),
        hovertemplate: "<b>%{text}</b><br>AUROC: %{customdata[0]:.4f}<br>U_Clin: %{customdata[1]:.4f}<br>S_Lip: %{customdata[2]:.4f}<extra></extra>",
        mode: "markers+text",
        textposition: "top center",
        marker: {
          size: lb.map((r) => Math.max(15, 34 - r.s_lip * 25)),
          color: lb.map((r) => MODEL_COLORS[r.model]),
          line: { width: 2, color: "#FFFFFF" },
        },
      },
    ],
    {
      margin: { t: 44, r: 30, b: 54, l: 62 },
      xaxis: { title: "Predictive AUROC", range: [Math.min(...lb.map((r) => r.auroc)) - 0.03, 1.02], automargin: true },
      yaxis: { title: "Net Clinical Utility (U_Clin)", range: [Math.min(...lb.map((r) => r.u_clin)) - 0.08, 1.02], automargin: true },
    },
    PLOT_CFG
  );

  const rowsHtml = lb
    .map((r) => `
      <tr class="${r.model === "Extra Trees" ? "highlight-et" : ""}">
        <td><strong>${r.model}</strong></td>
        <td>${(r.accuracy * 100).toFixed(2)}%</td>
        <td>${r.auroc.toFixed(4)}</td>
        <td>${r.s_lip.toFixed(4)}</td>
        <td>${r.d_xai.toFixed(4)}</td>
        <td>${r.w_clin_norm.toFixed(4)}</td>
        <td>${r.ece.toFixed(4)}</td>
        <td>${r.t_clin.toFixed(4)}</td>
        <td><strong>${r.u_clin.toFixed(4)}</strong></td>
        <td>${r.latency_ms.toFixed(2)} ms</td>
      </tr>
    `)
    .join("");
  document.getElementById("leaderboard-table").innerHTML = `
    <thead>
      <tr>
        <th>Architecture</th><th>Accuracy</th><th>AUROC</th>
        <th>S<sub>Lip</sub> (↓)</th><th>D<sub>XAI</sub> (↓)</th>
        <th>W<sub>Clin</sub><sup>norm</sup> (↓)</th><th>ECE (↓)</th>
        <th>T<sub>Clin</sub> (↑)</th><th>U<sub>Clin</sub> (↑)</th><th>Latency / 10 pts</th>
      </tr>
    </thead>
    <tbody>${rowsHtml}</tbody>
  `;
}

function renderNoiseScaling(ov) {
  const ns = ov.noise_scaling;
  const hVals = ns.map((r) => r.h);
  const traces = ["Extra Trees", "Random Forest", "MLP", "Tabular Deep ResNet"].map((m) => ({
    x: hVals,
    y: ns.map((r) => r[m]),
    name: m,
    mode: "lines+markers",
    line: { width: 3, color: MODEL_COLORS[m] },
    marker: { size: 8 },
  }));

  Plotly.newPlot(
    "chart-h-scaling",
    traces,
    {
      margin: { t: 58, r: 20, b: 54, l: 60 },
      xaxis: { title: "Gaussian Perturbation Radius (h)", automargin: true },
      yaxis: { title: "Local Lipschitz Instability (S_Lip ↓)", automargin: true },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );
}

async function runLiveAttack() {
  setStatus("Executing Live Attack...");
  const mode = document.getElementById("attack-mode").value;
  const eps = Number(document.getElementById("attack-eps").value) || 0.12;
  const res = await apiPost("/api/attack/run", {
    cohort: STATE.cohort,
    attack_mode: mode,
    eps_adv: eps,
  });
  STATE.attackResult = res;

  const rows = res.results;
  Plotly.newPlot(
    "chart-attack-results",
    [
      { x: rows.map((r) => r.model), y: rows.map((r) => r.acc_attacked), name: "Post-Attack Accuracy", type: "bar", marker: { color: "#0F2744" } },
      { x: rows.map((r) => r.model), y: rows.map((r) => r.rank_discordance_d_xai), name: "Rank Discordance (D_XAI ↓)", type: "bar", marker: { color: "#DC2626" } },
    ],
    {
      barmode: "group",
      margin: { t: 54, r: 20, b: 50, l: 55 },
      yaxis: { title: "Value", automargin: true },
      xaxis: { automargin: true },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );

  const trHtml = rows
    .map((r) => {
      const shift = res.example_patient_top3[r.model];
      const badge = r.rank_discordance_d_xai <= 0.25
        ? `<span class="badge badge-pass">Robust</span>`
        : `<span class="badge badge-fail">Attribution Shift</span>`;
      return `
        <tr>
          <td><strong>${r.model}</strong></td>
          <td>${(r.acc_clean * 100).toFixed(1)}% → ${(r.acc_attacked * 100).toFixed(1)}%</td>
          <td>${(r.pred_preservation_rate * 100).toFixed(1)}%</td>
          <td>${r.s_lip_shift.toFixed(4)}</td>
          <td><strong>${r.rank_discordance_d_xai.toFixed(4)}</strong> ${badge}</td>
          <td>${shift.before.join(", ")}</td>
          <td>${shift.after.join(", ")}</td>
        </tr>
      `;
    })
    .join("");
  document.getElementById("attack-table").innerHTML = `
    <thead>
      <tr>
        <th>Architecture</th><th>Accuracy (Clean → Attacked)</th><th>Pred. Preserved</th>
        <th>S<sub>Lip</sub> Shift (↓)</th><th>Rank Discordance D<sub>XAI</sub> (↓)</th>
        <th>Patient #0 Top-3 (Clean)</th><th>Patient #0 Top-3 (Post-Attack)</th>
      </tr>
    </thead>
    <tbody>${trHtml}</tbody>
  `;
  setStatus(`Live Engine Ready (${STATE.overview.spec.short})`);
}

function renderCalibration(ov) {
  const traces = [
    {
      x: [0, 1], y: [0, 1],
      mode: "lines",
      name: "Ideal (y = x)",
      line: { dash: "dash", color: "#64748B", width: 2 },
    },
  ];
  ov.leaderboard.forEach((r) => {
    const rc = ov.reliability_curves[r.model];
    traces.push({
      x: rc.conf,
      y: rc.acc,
      mode: "lines+markers",
      name: `${r.model} (ECE=${r.ece.toFixed(3)})`,
      line: { width: 2.5, color: MODEL_COLORS[r.model] },
      marker: { size: 7 },
    });
  });

  Plotly.newPlot(
    "chart-calibration",
    traces,
    {
      margin: { t: 62, r: 20, b: 52, l: 58 },
      xaxis: { title: "Mean Predicted Probability", range: [0, 1], automargin: true },
      yaxis: { title: "Observed Positive Fraction", range: [0, 1], automargin: true },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );
}

async function runUtilitySimulation() {
  if (!STATE.overview) return;
  const alpha = Number(document.getElementById("sim-alpha").value);
  const beta = Number(document.getElementById("sim-beta").value);
  const w_s = Number(document.getElementById("sim-ws").value);
  const w_a = Number(document.getElementById("sim-wa").value);
  const w_c = Number(document.getElementById("sim-wc").value);

  document.getElementById("sim-alpha-v").textContent = alpha.toFixed(2);
  document.getElementById("sim-beta-v").textContent = beta.toFixed(2);
  document.getElementById("sim-ws-v").textContent = w_s.toFixed(2);
  document.getElementById("sim-wa-v").textContent = w_a.toFixed(2);
  document.getElementById("sim-wc-v").textContent = w_c.toFixed(2);

  const sim = await apiPost("/api/utility/simulate", {
    cohort: STATE.cohort, alpha, beta, w_s, w_a, w_c,
  });

  const rows = sim.models;
  Plotly.newPlot(
    "chart-utility-sim",
    [
      { x: rows.map((r) => r.model), y: rows.map((r) => r.t_clin), name: "Trust Calibration (T_Clin ↑)", type: "bar", marker: { color: "#2563EB" } },
      { x: rows.map((r) => r.model), y: rows.map((r) => r.u_clin), name: "Net Utility (U_Clin ↑)", type: "bar", marker: { color: "#0F766E" } },
    ],
    {
      barmode: "group",
      margin: { t: 54, r: 20, b: 44, l: 52 },
      yaxis: { title: "Score", range: [0, 1.08], automargin: true },
      xaxis: { automargin: true },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );

  const trHtml = rows
    .map((r) => `
      <tr>
        <td><strong>${r.model}</strong></td>
        <td>${(r.accuracy * 100).toFixed(2)}%</td>
        <td>${r.t_clin.toFixed(4)}</td>
        <td>${r.over_reliance.toFixed(4)}</td>
        <td>${r.under_reliance.toFixed(4)}</td>
        <td><strong>${r.u_clin.toFixed(4)}</strong></td>
        <td>±${r.ablation_stability_delta.toFixed(4)}</td>
        <td>±${r.ablation_alignment_delta.toFixed(4)}</td>
        <td>±${r.ablation_calibration_delta.toFixed(4)}</td>
      </tr>
    `)
    .join("");
  document.getElementById("utility-sim-table").innerHTML = `
    <thead>
      <tr>
        <th>Architecture</th><th>Accuracy</th><th>T<sub>Clin</sub></th>
        <th>Over-Reliance</th><th>Under-Reliance</th><th>Net Utility U<sub>Clin</sub></th>
        <th>ΔT (No Stability)</th><th>ΔT (No Prior)</th><th>ΔT (No Calibration)</th>
      </tr>
    </thead>
    <tbody>${trHtml}</tbody>
  `;
}

function renderFairness(ov) {
  const f = ov.fairness;
  if (!f || !f.length) return;
  Plotly.newPlot(
    "chart-fairness",
    [
      {
        x: f.map((r) => r.model),
        y: f.map((r) => r.below_median_s_lip),
        name: `${f[0].split_feature} < Median`,
        type: "bar",
        marker: { color: "#2563EB" },
      },
      {
        x: f.map((r) => r.model),
        y: f.map((r) => r.above_median_s_lip),
        name: `${f[0].split_feature} ≥ Median`,
        type: "bar",
        marker: { color: "#D97706" },
      },
    ],
    {
      barmode: "group",
      margin: { t: 56, r: 20, b: 50, l: 58 },
      yaxis: { title: "Subgroup S_Lip Instability (↓)", automargin: true },
      xaxis: { automargin: true },
      legend: { orientation: "h", y: 1.03, yanchor: "bottom", x: 0 },
    },
    PLOT_CFG
  );
}

function renderRegulatoryGate() {
  if (!STATE.overview) return;
  const maxSlip = Number(document.getElementById("gate-slip").value) || 0.18;
  const maxDxai = Number(document.getElementById("gate-dxai").value) || 0.45;
  const maxEce = Number(document.getElementById("gate-ece").value) || 0.05;

  const trHtml = STATE.overview.leaderboard
    .map((r) => {
      const passS = r.s_lip <= maxSlip;
      const passD = r.d_xai <= maxDxai;
      const passE = r.ece <= maxEce;
      const allPass = passS && passD && passE;
      return `
        <tr>
          <td><strong>${r.model}</strong></td>
          <td>${r.s_lip.toFixed(4)} ${passS ? '<span class="badge badge-pass">PASS</span>' : '<span class="badge badge-fail">FAIL</span>'}</td>
          <td>${r.d_xai.toFixed(4)} ${passD ? '<span class="badge badge-pass">PASS</span>' : '<span class="badge badge-fail">FAIL</span>'}</td>
          <td>${r.ece.toFixed(4)} ${passE ? '<span class="badge badge-pass">PASS</span>' : '<span class="badge badge-fail">FAIL</span>'}</td>
          <td>${allPass ? '<span class="badge badge-pass">CERTIFIED</span>' : '<span class="badge badge-fail">BLOCKED</span>'}</td>
        </tr>
      `;
    })
    .join("");
  document.getElementById("regulatory-table").innerHTML = `
    <thead>
      <tr>
        <th>Architecture</th><th>Stability (≤ ${maxSlip})</th>
        <th>Discordance (≤ ${maxDxai})</th><th>ECE (≤ ${maxEce})</th>
        <th>EU AI Act Art. 13/14</th>
      </tr>
    </thead>
    <tbody>${trHtml}</tbody>
  `;
}

function renderPaperArchive(pr) {
  document.getElementById("paper-overall-table").innerHTML = `
    <thead>
      <tr><th>Cohort</th><th>Records</th><th>Model</th><th>Accuracy</th><th>S<sub>bLip</sub> (↓)</th><th>D<sub>XAI</sub> (↓)</th><th>W<sub>Clin</sub><sup>norm</sup> (↓)</th><th>Û<sub>Clin</sub> (↑)</th></tr>
    </thead>
    <tbody>
      ${pr.overall_table.map((r) => `
        <tr class="${r.model === "Extra Trees" ? "highlight-et" : ""}">
          <td>${r.cohort}</td><td>${r.n_records.toLocaleString()}</td><td><strong>${r.model}</strong></td>
          <td>${r.acc.toFixed(4)}</td><td>${r.s_lip.toFixed(4)}</td><td>${r.d_xai.toFixed(4)}</td>
          <td>${r.w_clin_norm.toFixed(4)}</td><td><strong>${r.u_clin.toFixed(4)}</strong></td>
        </tr>`).join("")}
    </tbody>
  `;

  document.getElementById("paper-h-table").innerHTML = `
    <thead><tr><th>Noise Scale (h)</th><th>Extra Trees</th><th>Random Forest</th><th>MLP</th><th>Deep ResNet</th></tr></thead>
    <tbody>
      ${pr.h_scaling.map((r) => `
        <tr><td>${r.label}</td><td><strong>${r["Extra Trees"].toFixed(4)}</strong></td><td>${r["Random Forest"].toFixed(4)}</td><td>${r["MLP"].toFixed(4)}</td><td>${r["Tabular Deep ResNet"].toFixed(4)}</td></tr>
      `).join("")}
    </tbody>
  `;

  document.getElementById("paper-weight-table").innerHTML = `
    <thead><tr><th>Profile</th><th>(w<sub>s</sub>, w<sub>a</sub>, w<sub>c</sub>)</th><th>ET</th><th>RF</th><th>MLP</th><th>Deep ResNet</th></tr></thead>
    <tbody>
      ${pr.weight_sensitivity.map((r) => `
        <tr><td>${r.config}</td><td>${r.weights}</td><td><strong>${r.ET.toFixed(4)}</strong></td><td>${r.RF.toFixed(4)}</td><td>${r.MLP.toFixed(4)}</td><td>${r["Deep ResNet"].toFixed(4)}</td></tr>
      `).join("")}
    </tbody>
  `;

  document.getElementById("paper-adv-table").innerHTML = `
    <thead><tr><th>Mode</th><th>Model</th><th>Acc</th><th>S<sub>bLip</sub> (↓)</th><th>D<sub>XAI</sub> (↓)</th></tr></thead>
    <tbody>
      ${pr.adversarial.map((r) => `
        <tr class="${r.model === "Random Forest" ? "highlight-et" : ""}"><td>${r.mode}</td><td>${r.model}</td><td>${r.acc.toFixed(4)}</td><td>${r.s_lip.toFixed(4)}</td><td><strong>${r.d_xai.toFixed(4)}</strong></td></tr>
      `).join("")}
    </tbody>
  `;

  document.getElementById("paper-latency-table").innerHTML = `
    <thead><tr><th>Explainer</th><th>Asymptotic Complexity</th><th>Latency (ms)</th><th>Peak RAM (MB)</th></tr></thead>
    <tbody>
      ${pr.latency.map((r) => `
        <tr><td><strong>${r.explainer}</strong></td><td>${r.complexity}</td><td>${r.latency_ms.toFixed(1)}</td><td>${r.ram_mb}</td></tr>
      `).join("")}
    </tbody>
  `;
}

init().catch((err) => {
  console.error(err);
  setStatus("Initialization Error — Check console");
});
