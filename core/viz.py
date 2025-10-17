
import streamlit as st
import pandas as pd
import altair as alt

def render_visuals(df_norm: pd.DataFrame, tur1_out, tur2_out, viz_spec=None):
    # 1) AY development curves (incurred)
    st.subheader("Incurred — AY Gelişim Eğrileri")
    curve = alt.Chart(df_norm).mark_line().encode(
        x=alt.X("development_quarter:O", title="Gelişim Çeyreği"),
        y=alt.Y("incurred_cum:Q", title="Kümülatif Incurred"),
        color=alt.Color("accident_year:N", title="AY")
    ).properties(height=300)
    st.altair_chart(curve, use_container_width=True)

    # 2) Paid vs Incurred ratio by dev quarter
    if {"paid_cum","incurred_cum","development_quarter"}.issubset(df_norm.columns):
        st.subheader("Paid / Incurred Oranı — Gelişim Çeyreği")
        tmp = df_norm.groupby("development_quarter", as_index=False).apply(
            lambda g: pd.Series({
                "paid": g["paid_cum"].sum(),
                "incurred": g["incurred_cum"].sum()
            })
        ).reset_index(drop=True)
        tmp["ratio"] = tmp["paid"] / tmp["incurred"]
        bar = alt.Chart(tmp).mark_bar().encode(
            x="development_quarter:O", y="ratio:Q"
        ).properties(height=250)
        st.altair_chart(bar, use_container_width=True)

    # 3) (Optional) Use viz_spec later for custom charts
    if viz_spec and isinstance(viz_spec, dict):
        with st.expander("LLM'den gelen viz spec", expanded=False):
            st.json(viz_spec)
