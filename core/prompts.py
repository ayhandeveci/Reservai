
import json

def prompt_tur1(eda_result: dict) -> str:
    return f"""
    You are an actuarial assistant focusing on Kasko (Auto Hull) cumulative claims triangles.
    Summarize the following EDA (JSON) briefly and highlight potential data-quality issues and
    next-step analyses. Keep it under 150 words.
    EDA_JSON:
    {json.dumps(eda_result, ensure_ascii=False)}
    """

def prompt_tur2(df_norm, tur1_out) -> str:
    sample = df_norm.head(25).to_dict(orient="records")
    return f"""
    You are an actuarial analyst. Based on the normalized cumulative claims data SAMPLE (first 25 rows)
    and the prior EDA summary, propose:
    - 3-6 segmentation ideas specific to Auto Hull (e.g., vehicle age bands, region, repair type),
    - 3-6 additional features to engineer (e.g., inflation indices, part type mix),
    - any data-quality/collection improvements.
    Output valid JSON with keys: notes (string), segments (list), features (list).
    SAMPLE_ROWS_JSON: {json.dumps(sample, ensure_ascii=False)}
    EDA_JSON: {json.dumps(tur1_out, ensure_ascii=False)}
    """

def prompt_tur3(df_norm, tur1_out, tur2_out) -> str:
    # We ask LLM for visualization spec, but we'll draw defaults regardless.
    sample = df_norm.head(50).to_dict(orient="records")
    return f"""
    Act as a visualization planner for actuarial reporting.
    Suggest a JSON visualization spec for 3-5 charts suitable for Auto Hull cumulative claims:
    examples: AY dev curves, heatmap of age-to-age, paid vs incurred ratios by development quarter,
    and open claims proxy (reported vs ultimate). Avoid long descriptions. 
    Use keys: charts=[{{type, title, x, y, group, agg}}].
    CONTEXT_TUR1={json.dumps(tur1_out, ensure_ascii=False)}
    CONTEXT_TUR2={json.dumps(tur2_out, ensure_ascii=False)}
    SAMPLE_ROWS={json.dumps(sample, ensure_ascii=False)}
    """
