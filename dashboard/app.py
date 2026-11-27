"""
dashboard/app.py
================
FastAPI backend serving the C-XAI Presentation Dashboard (ICMLDE 2026 · Paper ID 857).
All endpoints execute real scikit-learn, SciPy, SHAP, and PyTorch computations.
"""

import os
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from dashboard.engine import COHORT_SPECS, get_engine
from dashboard.paper_reference import (
    PAPER_ADVERSARIAL,
    PAPER_H_SCALING,
    PAPER_LATENCY,
    PAPER_META,
    PAPER_OVERALL_TABLE,
    PAPER_WEIGHT_SENSITIVITY,
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app = FastAPI(
    title="C-XAI Clinical Auditing Dashboard (ICMLDE 2026 · Paper 857)",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class PatientExplainRequest(BaseModel):
    cohort: str
    sample_idx: int = 0
    raw_features: Optional[Dict[str, float]] = None
    noise_h: float = Field(default=0.05, ge=0.0, le=0.30)
    mc_samples: int = Field(default=12, ge=3, le=30)
    seed: int = 42


class AttackRequest(BaseModel):
    cohort: str
    attack_mode: str = "fgsm"  # clean | gaussian | mcar_20 | fgsm | scal_pgd
    eps_adv: float = Field(default=0.05, ge=0.005, le=0.25)


class UtilitySimRequest(BaseModel):
    cohort: str
    alpha: float = Field(default=0.50, ge=0.0, le=1.0)
    beta: float = Field(default=0.30, ge=0.0, le=1.0)
    w_s: float = Field(default=0.333, ge=0.0, le=1.0)
    w_a: float = Field(default=0.333, ge=0.0, le=1.0)
    w_c: float = Field(default=0.334, ge=0.0, le=1.0)


@app.on_event("startup")
def startup_warm_engine():
    get_engine()


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/cohorts")
def list_cohorts():
    eng = get_engine()
    items = []
    for cname, spec in COHORT_SPECS.items():
        c = eng.cohorts[cname]
        items.append({
            "name": cname,
            "short": spec["short"],
            "clinical_domain": spec["clinical_domain"],
            "guideline": spec["guideline"],
            "n_total": c["n_total"],
            "n_test": c["n_test"],
            "n_features": len(c["features"]),
        })
    return {"cohorts": items}


@app.get("/api/overview")
def get_overview(cohort: str = Query(...), rebuild: bool = False):
    eng = get_engine()
    if cohort not in eng.cohorts:
        raise HTTPException(status_code=404, detail=f"Cohort '{cohort}' not found")
    return eng.get_cohort_overview(cohort, rebuild=rebuild)


@app.get("/api/patient/sample")
def get_patient_sample(cohort: str = Query(...), idx: int = 0):
    eng = get_engine()
    if cohort not in eng.cohorts:
        raise HTTPException(status_code=404, detail=f"Cohort '{cohort}' not found")
    return eng.get_patient_record(cohort, idx)


@app.post("/api/patient/explain")
def explain_patient(req: PatientExplainRequest):
    eng = get_engine()
    if req.cohort not in eng.cohorts:
        raise HTTPException(status_code=404, detail=f"Cohort '{req.cohort}' not found")
    return eng.explain_patient(
        cname=req.cohort,
        raw_features=req.raw_features,
        sample_idx=req.sample_idx,
        noise_h=req.noise_h,
        mc_samples=req.mc_samples,
        seed=req.seed,
    )


@app.post("/api/attack/run")
def run_attack(req: AttackRequest):
    eng = get_engine()
    if req.cohort not in eng.cohorts:
        raise HTTPException(status_code=404, detail=f"Cohort '{req.cohort}' not found")
    return eng.run_live_attack(cname=req.cohort, attack_mode=req.attack_mode, eps_adv=req.eps_adv)


@app.post("/api/utility/simulate")
def simulate_utility(req: UtilitySimRequest):
    eng = get_engine()
    if req.cohort not in eng.cohorts:
        raise HTTPException(status_code=404, detail=f"Cohort '{req.cohort}' not found")
    return eng.simulate_utility_sensitivity(
        cname=req.cohort,
        alpha=req.alpha,
        beta=req.beta,
        w_s=req.w_s,
        w_a=req.w_a,
        w_c=req.w_c,
    )


@app.get("/api/paper-reference")
def get_paper_reference():
    return {
        "meta": PAPER_META,
        "overall_table": PAPER_OVERALL_TABLE,
        "h_scaling": PAPER_H_SCALING,
        "weight_sensitivity": PAPER_WEIGHT_SENSITIVITY,
        "adversarial": PAPER_ADVERSARIAL,
        "latency": PAPER_LATENCY,
    }


if __name__ == "__main__":
    uvicorn.run("dashboard.app:app", host="127.0.0.1", port=8570, reload=False)
