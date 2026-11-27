/* app.js — C-XAI Presentation Dashboard Client (Offline Plotly + Real FastAPI Calls) */

const STATE = {
  cohort: "MIMIC-IV ICU Mortality",
  overview: null,
  patientResult: null,
  attackResult: null,
  paperRef: null,
  customFeatures: {},
  maxSampleIdx: 100,
};

const MODEL_COLORS = {
  "Extra Trees": "#0F766E",
  "Random Forest": "#2563EB",
  "MLP": "#D97706",
  "Tabular Deep ResNet": "#DC2626",
};

const PLOT_CFG = { responsive: true, displayModeBar: false };

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

// =========================================================================
// TAB SWITCHING & RESIZE
// =========================================================================
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    const target = document.getElementById(btn.dataset.tab);
    target.classList.add("active");
    target.querySelectorAll(".plot-box").forEach((el) => {
      if (el.data) Plotly.Plots.resize(el);
    });
  });
});

// =========================================================================
// INITIALIZATION
// =========================================================================
async function init() {
  setStatus("Connecting to Engine...");
  const [cohortData, paperData] = await Promise.all([
    apiGet("/api/cohorts"),
    apiGet("/api/paper-reference"),
  ]);
  STATE.paperRef = paperData;
  renderPaperArchive(paperData);

  const sel = document.getElementById("cohort-select");
  sel.innerHTML = "";
  cohortData.cohorts.forEach((c) => {
    const opt = document.createElement("option");
    opt.value = c.name;
    opt.textContent = `${c.short} (${c.n_total.toLocaleString()} records · ${c.n_features} features)`;
    sel.appendChild(opt);
  });
  sel.value = STATE.cohort;
  sel.addEventListener("change", () => loadCohort(sel.value, false));

  document.getElementById("btn-rebuild").addEventListener("click", () => loadCohort(STATE.cohort, true));
  document.getElementById("btn-load-sample").addEventListener("click", loadSamplePatient);
  document.getElementById("btn-run-explain").addEventListener("click", runLivePatientExplain);
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

  ["sim-alpha", "sim-beta", "sim-ws", "sim-wa", "sim-wc"].forEach((id) => {
    document.getElementById(id).addEventListener("input", runUtilitySimulation);
  });

  await loadCohort(STATE.cohort, false);
}

async function loadCohort(cohortName, rebuild = false) {
  STATE.cohort = cohortName;
  setStatus(rebuild ? "Re-training Models & Auditing..." : "Loading Cohort Audit...");
  const ov = await apiGet(`/api/overview?cohort=${encodeURIComponent(cohortName)}&rebuild=${rebuild}`);
  STATE.overview = ov;
  STATE.maxSampleIdx = ov.counts.n_test - 1;
  document.getElementById("sample-idx").max = STATE.maxSampleIdx;

  document.getElementById("cohort-subtitle").textContent =
    `${ov.spec.clinical_domain} · ${ov.counts.n_total.toLocaleString()} records (${ov.counts.n_train.toLocaleString()} train / ${ov.counts.n_test.toLocaleString()} test) · Priors: ${ov.spec.guideline}`;
  document.getElementById("guideline-label").textContent = ov.spec.guideline;

  renderOverview(ov);
  renderNoiseScaling(ov);
  renderCalibration(ov);
  renderFairness(ov);
  renderRegulatoryGate();
  buildFeatureSliders(ov.feature_meta);

  await Promise.all([
    loadSamplePatient(),
    runLiveAttack(),
    runUtilitySimulation(),
  ]);
  setStatus(`Live Engine Ready (${ov.spec.short})`);
}

// =========================================================================
// TAB 1: BENCHMARK OVERVIEW & DECOUPLING
// =========================================================================
function renderOverview(ov) {
  const lb = ov.leaderboard;
  const et = lb.find((r) => r.model === "Extra Trees") || lb[0];
  const resnet = lb.find((r) => r.model === "Tabular Deep ResNet") || lb[lb.length - 1];

  const utilDiff = ((et.u_clin - resnet.u_clin) / Math.max(1e-6, resnet.u_clin)) * 100;
  const slipRatio = resnet.s_lip / Math.max(1e-6, et.s_lip);

  document.getElementById("kpi-cards").innerHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Cohort Audited</div>
      <div class="kpi-value">${ov.counts.n_total.toLocaleString()}</div>
      <div class="kpi-detail">${ov.spec.short} · ${ov.counts.n_features} clinical features · Pos rate ${(ov.counts.pos_rate * 100).toFixed(1)}%</div>
    </div>
    <div class="kpi-card teal">
      <div class="kpi-label">Extra Trees Net Utility (U<sub>Clin</sub>)</div>
      <div class="kpi-value">${et.u_clin.toFixed(4)}</div>
      <div class="kpi-detail">${utilDiff >= 0 ? "+" : ""}${utilDiff.toFixed(1)}% vs. Deep ResNet (${resnet.u_clin.toFixed(4)})</div>
    </div>
    <div class="kpi-card crimson">
      <div class="kpi-label">Explanation Instability (S<sub>Lip</sub>)</div>
      <div class="kpi-value">${resnet.s_lip.toFixed(4)}</div>
      <div class="kpi-detail">Deep ResNet vs. Extra Trees (${et.s_lip.toFixed(4)}) · ${slipRatio.toFixed(1)}× shift</div>
    </div>
    <div class="kpi-card blue">
      <div class="kpi-label">Accuracy–Utility Coupling (R²)</div>
      <div class="kpi-value">${ov.stats_et_vs_resnet.r2_auroc_vs_utility.toFixed(3)}</div>
      <div class="kpi-detail">AUROC fails to predict explanation reliability</div>
    </div>
  `;

  const st = ov.stats_et_vs_resnet;
  document.getElementById("stats-banner").innerHTML =
    `<strong>Paired Hypothesis Audit (Extra Trees vs. Tabular Deep ResNet across N=${st.n_audited_patients} test encounters):</strong> ` +
    `Paired <i>t</i> = <strong>${st.paired_t}</strong> (<i>p</i> = ${st.p_value_t.toExponential(2)}) · ` +
    `Wilcoxon <i>W</i> = <strong>${st.wilcoxon_w}</strong> (<i>p</i> = ${st.p_value_w.toExponential(2)}) · ` +
    `Cohen's <i>d</i> = <strong>${st.cohens_d}</strong> · Audited ${ov.timestamp}`;

  // Accuracy vs Utility bar chart
  const models = lb.map((r) => r.model);
  Plotly.newPlot(
    "chart-acc-util",
    [
      {
        x: models,
        y: lb.map((r) => r.accuracy * 100),
        name: "Predictive Accuracy (%)",
        type: "bar",
        marker: { color: "#1B365D" },
        text: lb.map((r) => (r.accuracy * 100).toFixed(1) + "%"),
        textposition: "outside",
      },
      {
        x: models,
        y: lb.map((r) => r.u_clin * 100),
        name: "Calibrated Clinical Utility (%)",
        type: "bar",
        marker: { color: "#0F766E" },
        text: lb.map((r) => (r.u_clin * 100).toFixed(1) + "%"),
        textposition: "outside",
      },
    ],
    {
      barmode: "group",
      margin: { t: 25, r: 20, b: 50, l: 52 },
      yaxis: { title: "Score (%)", range: [0, 112] },
      legend: { orientation: "h", y: 1.12 },
    },
    PLOT_CFG
  );

  // Decoupling scatter
  document.getElementById("decoupling-r2").textContent = `OLS R² = ${st.r2_auroc_vs_utility.toFixed(4)}`;
  Plotly.newPlot(
    "chart-decoupling",
    [
      {
        x: lb.map((r) => r.auroc),
        y: lb.map((r) => r.u_clin),
        text: lb.map((r) => `${r.model}<br>AUROC=${r.auroc}<br>U_Clin=${r.u_clin}<br>S_Lip=${r.s_lip}`),
        mode: "markers+text",
        textposition: "top center",
        marker: {
          size: lb.map((r) => Math.max(14, 34 - r.s_lip * 25)),
          color: lb.map((r) => MODEL_COLORS[r.model]),
          line: { width: 2, color: "#FFFFFF" },
        },
        hoverinfo: "text",
      },
    ],
    {
      margin: { t: 28, r: 24, b: 50, l: 58 },
      xaxis: { title: "Predictive AUROC", range: [Math.min(...lb.map((r) => r.auroc)) - 0.03, 1.01] },
      yaxis: { title: "Net Clinical Decision Utility (U_Clin)", range: [Math.min(...lb.map((r) => r.u_clin)) - 0.08, 1.0] },
    },
    PLOT_CFG
  );

  // Leaderboard table
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

// =========================================================================
// TAB 2: LIVE PATIENT EXPLAINER & NOISE LAB
// =========================================================================
function buildFeatureSliders(featureMeta) {
  const container = document.getElementById("feature-sliders");
  // Limit slider list cleanly if 30 features (BCWD shows top 10 editable + keeps rest)
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

function cssId(name) {
  return name.replace(/[^a-zA-Z0-9]/g, "_");
}

async function loadSamplePatient() {
  const idx = Number(document.getElementById("sample-idx").value) || 0;
  const rec = await apiGet(`/api/patient/sample?cohort=${encodeURIComponent(STATE.cohort)}&idx=${idx}`);
  STATE.customFeatures = { ...rec.raw_features };
  document.getElementById("patient-label-badge").textContent =
    `Sample #${rec.sample_idx} · True Outcome: ${rec.true_label === 1 ? "High Risk (1)" : "Low Risk / Benign (0)"}`;

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
  setStatus("Computing Live Multi-Explainer Audit...");
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
      <div class="kpi-label">Extra Trees P(Risk=1)</div>
      <div class="kpi-value">${(et.prob_clean * 100).toFixed(1)}%</div>
      <div class="kpi-detail">Noisy (x+δ): ${(et.prob_noisy * 100).toFixed(1)}% · S<sub>Lip</sub> = ${et.s_lip.toFixed(4)}</div>
    </div>
    <div class="kpi-card crimson">
      <div class="kpi-label">Deep ResNet P(Risk=1)</div>
      <div class="kpi-value">${(rn.prob_clean * 100).toFixed(1)}%</div>
      <div class="kpi-detail">Noisy (x+δ): ${(rn.prob_noisy * 100).toFixed(1)}% · S<sub>Lip</sub> = ${rn.s_lip.toFixed(4)}</div>
    </div>
    <div class="kpi-card teal">
      <div class="kpi-label">Extra Trees Discordance</div>
      <div class="kpi-value">${et.d_xai.toFixed(4)}</div>
      <div class="kpi-detail">W<sub>Clin</sub><sup>norm</sup> = ${et.w_clin_norm.toFixed(4)} (Prior Align ${(et.a_clin * 100).toFixed(1)}%)</div>
    </div>
    <div class="kpi-card crimson">
      <div class="kpi-label">Deep ResNet Discordance</div>
      <div class="kpi-value">${rn.d_xai.toFixed(4)}</div>
      <div class="kpi-detail">W<sub>Clin</sub><sup>norm</sup> = ${rn.w_clin_norm.toFixed(4)} (Prior Align ${(rn.a_clin * 100).toFixed(1)}%)</div>
    </div>
  `;

  // Pick explainer vectors
  const choice = document.getElementById("explainer-choice").value;
  function pickVec(mObj, noisy = false) {
    const dict = noisy ? mObj.explainers_noisy : mObj.explainers_clean;
    if (choice === "primary") return dict["TreeSHAP"] || dict["Integrated Gradients"];
    if (choice === "smoothgrad") return dict["SmoothGrad"] || dict["Zeroth-Order SmoothGrad"];
    return dict[choice] || Object.values(dict)[0];
  }

  // Show top 10 features by magnitude if high-dim
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

  Plotly.newPlot(
    "chart-patient-attr",
    [
      { x: feats, y: etC, name: "Extra Trees (Clean)", type: "bar", marker: { color: "#0F766E" } },
      { x: feats, y: etN, name: `Extra Trees (Noisy h=${res.noise_h})`, type: "bar", marker: { color: "#5EEAD4" } },
      { x: feats, y: rnC, name: "Deep ResNet (Clean)", type: "bar", marker: { color: "#B91C1C" } },
      { x: feats, y: rnN, name: `Deep ResNet (Noisy h=${res.noise_h})`, type: "bar", marker: { color: "#FCA5A5" } },
    ],
    {
      barmode: "group",
      margin: { t: 25, r: 20, b: 85, l: 55 },
      yaxis: { title: "Attribution (ΔRisk Contribution)" },
      legend: { orientation: "h", y: 1.16 },
    },
    PLOT_CFG
  );

  // Discordance Heatmaps
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
          text: dm.matrix.map((row) => row.map((v) => v.toFixed(3))),
          texttemplate: "%{text}",
          showscale: true,
        },
      ],
      {
        margin: { t: 20, r: 20, b: 85, l: 120 },
      },
      PLOT_CFG
    );
  }
  plotHeatmap("chart-dxai-et", et.discordance_matrix, "YlGnBu");
  plotHeatmap("chart-dxai-resnet", rn.discordance_matrix, "YlOrRd");

  // Clinical Prior Alignment Comparison
  const pc = et.prior_comparison;
  const pcRn = rn.prior_comparison;
  Plotly.newPlot(
    "chart-prior-align",
    [
      { x: pc.map((p) => p.feature), y: pc.map((p) => p.guideline_weight), name: "Medical Guideline Prior (P_clin)", type: "bar", marker: { color: "#1B365D" } },
      { x: pc.map((p) => p.feature), y: pc.map((p) => p.model_weight), name: "Extra Trees Attribution Share", type: "bar", marker: { color: "#0F766E" } },
      { x: pcRn.map((p) => p.feature), y: pcRn.map((p) => p.model_weight), name: "Deep ResNet Attribution Share", type: "bar", marker: { color: "#DC2626" } },
    ],
    {
      barmode: "group",
      margin: { t: 25, r: 20, b: 60, l: 55 },
      yaxis: { title: "Normalized Importance Mass", range: [0, 0.7] },
      legend: { orientation: "h", y: 1.15 },
    },
    PLOT_CFG
  );
}

// =========================================================================
// TAB 3: NOISE SCALING & LIVE ADVERSARIAL ATTACKS
// =========================================================================
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
      margin: { t: 25, r: 20, b: 50, l: 58 },
      xaxis: { title: "Gaussian Perturbation Radius (h)" },
      yaxis: { title: "Local Lipschitz Instability (S_Lip ↓)" },
      legend: { orientation: "h", y: 1.14 },
    },
    PLOT_CFG
  );
}

async function runLiveAttack() {
  setStatus("Executing Live Perturbation / Adversarial Attack...");
  const mode = document.getElementById("attack-mode").value;
  const eps = Number(document.getElementById("attack-eps").value) || 0.05;
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
      { x: rows.map((r) => r.model), y: rows.map((r) => r.acc_attacked), name: "Post-Attack Accuracy", type: "bar", marker: { color: "#1B365D" } },
      { x: rows.map((r) => r.model), y: rows.map((r) => r.rank_discordance_d_xai), name: "Post-Attack Rank Discordance (D_XAI ↓)", type: "bar", marker: { color: "#DC2626" } },
    ],
    {
      barmode: "group",
      margin: { t: 20, r: 20, b: 50, l: 55 },
      yaxis: { title: "Metric Value" },
      legend: { orientation: "h", y: 1.15 },
    },
    PLOT_CFG
  );

  const trHtml = rows
    .map((r) => {
      const shift = res.example_patient_top3[r.model];
      const badge = r.rank_discordance_d_xai <= 0.35
        ? `<span class="badge badge-pass">Robust</span>`
        : `<span class="badge badge-fail">Attribution Collapse</span>`;
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

// =========================================================================
// TAB 4: CALIBRATION & UTILITY SIMULATOR
// =========================================================================
function renderCalibration(ov) {
  const traces = [
    {
      x: [0, 1], y: [0, 1],
      mode: "lines",
      name: "Perfect Calibration (y = x)",
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
      margin: { t: 25, r: 20, b: 50, l: 55 },
      xaxis: { title: "Mean Predicted Probability", range: [0, 1] },
      yaxis: { title: "Observed Positive Fraction", range: [0, 1] },
      legend: { orientation: "h", y: 1.15 },
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
      { x: rows.map((r) => r.model), y: rows.map((r) => r.u_clin), name: "Net Clinical Utility (U_Clin ↑)", type: "bar", marker: { color: "#0F766E" } },
    ],
    {
      barmode: "group",
      margin: { t: 20, r: 20, b: 45, l: 50 },
      yaxis: { title: "Score", range: [0, 1.05] },
      legend: { orientation: "h", y: 1.15 },
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
        <th>Over-Reliance Rate</th><th>Under-Reliance Rate</th><th>Net Utility U<sub>Clin</sub></th>
        <th>ΔT (No Stability)</th><th>ΔT (No Prior)</th><th>ΔT (No Calibration)</th>
      </tr>
    </thead>
    <tbody>${trHtml}</tbody>
  `;
}

// =========================================================================
// TAB 5: FAIRNESS & REGULATORY AUDIT GATE
// =========================================================================
function renderFairness(ov) {
  const f = ov.fairness;
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
      margin: { t: 25, r: 20, b: 50, l: 55 },
      yaxis: { title: "Subgroup S_Lip Instability (↓)" },
      legend: { orientation: "h", y: 1.14 },
    },
    PLOT_CFG
  );
}

function renderRegulatoryGate() {
  if (!STATE.overview) return;
  const maxSlip = Number(document.getElementById("gate-slip").value) || 0.18;
  const maxDxai = Number(document.getElementById("gate-dxai").value) || 0.48;
  const maxEce = Number(document.getElementById("gate-ece").value) || 0.10;

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
          <td>${allPass ? '<span class="badge badge-pass">CERTIFIED (EU AI Act Art. 13/14)</span>' : '<span class="badge badge-fail">BLOCKED FOR CLINICAL DEPLOYMENT</span>'}</td>
        </tr>
      `;
    })
    .join("");
  document.getElementById("regulatory-table").innerHTML = `
    <thead>
      <tr>
        <th>Architecture</th><th>Stability Gate (≤ ${maxSlip})</th>
        <th>Consensus Gate (≤ ${maxDxai})</th><th>Calibration Gate (≤ ${maxEce})</th>
        <th>Pre-Deployment Verdict</th>
      </tr>
    </thead>
    <tbody>${trHtml}</tbody>
  `;
}

// =========================================================================
// TAB 6: ICMLDE PAPER ARCHIVE
// =========================================================================
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
