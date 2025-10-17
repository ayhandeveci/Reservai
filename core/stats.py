
import pandas as pd
import numpy as np

def run_basic_eda(df: pd.DataFrame) -> dict:
    out = {}
    out["shape"] = {"rows": int(df.shape[0]), "cols": int(df.shape[1])}
    out["columns"] = df.columns.tolist()
    out["null_counts"] = df.isna().sum().to_dict()
    # monotonic checks per AY for cumulative columns
    checks = {}
    for col in ["incurred_cum","paid_cum","reported_claims_cum"]:
        if col in df.columns:
            bad = []
            for ay, g in df.groupby("accident_year", dropna=True):
                vals = g[col].fillna(0).values
                if np.any(np.diff(vals) < 0):
                    bad.append(int(ay))
            checks[col+"_nondecreasing"] = {"ok": len(bad)==0, "violations_by_AY": bad}
    out["monotonicity"] = checks
    # dev coverage by AY
    if "development_quarter" in df.columns:
        coverage = df.groupby("accident_year")["development_quarter"].max().to_dict()
        out["dev_quarter_max_by_AY"] = {int(k): int(v) for k,v in coverage.items()}
    # rough age-to-age factors (incurred)
    try:
        piv = df.pivot_table(index="accident_year", columns="development_quarter", values="incurred_cum", aggfunc="last")
        piv = piv.sort_index()
        age_to_age = {}
        for j in range(1, piv.shape[1]):
            num = piv[j+1].sum(skipna=True)
            den = piv[j].sum(skipna=True)
            if den and den != 0:
                age_to_age[f"{j}->{j+1}"] = float(num/den)
        out["age_to_age_incurred"] = age_to_age
    except Exception:
        out["age_to_age_incurred"] = {}
    return out
