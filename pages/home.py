from __future__ import annotations

import streamlit as st

from utils.streamlit_support import apply_brand_styles, get_services, render_status_strip, render_syllabus_strip


st.set_page_config(page_title="DP-600 Prep Hub | Home", page_icon="🏠", layout="wide")
apply_brand_styles()
services = get_services()
settings = services["settings"]
gemini = services["gemini"]
repository = services["repository"]

render_syllabus_strip()

st.markdown(
    """
    <div class="hero-panel">
        <div class="hero-eyebrow">Exam DP-600 · Implementing Analytics Solutions Using Microsoft Fabric</div>
        <div class="hero-title">Study Home</div>
        <div class="hero-subtitle">
            All three skill areas of the official DP-600 skills-measured outline, side by
            side, with no area treated as an afterthought. Generate original questions,
            track accuracy per skill area, and let difficulty adapt as you improve.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
render_status_strip(settings, gemini, repository)

overview_cols = st.columns(2)
overview_cols[0].markdown(
    """
    <div class="metric-panel">
        <h4>How To Use</h4>
        <p>1. Open any of the 3 skill areas from the sidebar.</p>
        <p>2. Pick a topic, a question style, and a difficulty mode.</p>
        <p>3. Generate one question at a time, answer it, and read the full solution.</p>
        <p>4. Visit the dashboard to see accuracy and topic trends across skill areas.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
overview_cols[1].markdown(
    """
    <div class="metric-panel">
        <h4>Adaptive Rules</h4>
        <p>Accuracy above 80% pushes the section toward harder questions.</p>
        <p>Accuracy below 50% lowers the difficulty to rebuild fundamentals.</p>
        <p>Recently generated questions are fed back into the prompt to avoid repeats.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Every Skill Area Counts")
st.caption("The DP-600 exam draws from all three skill areas below, weighted as shown. Rotate through them rather than over-practicing one.")

from utils.helpers import PRACTICE_BLUEPRINTS, SECTION_ORDER

section_cols = st.columns(2)
for index, key in enumerate(SECTION_ORDER):
    blueprint = PRACTICE_BLUEPRINTS[key]
    column = section_cols[index % 2]
    column.markdown(
        f"""
        <div class="section-card">
            <div class="section-number">SKILL AREA {index + 1:02d} · {blueprint["exam_weight"]}</div>
            <h4>{blueprint["title"]}</h4>
            <p>{blueprint["summary"]}</p>
        </div>
        <div style="height: 0.6rem;"></div>
        """,
        unsafe_allow_html=True,
    )

st.info("Use the sidebar to jump into any of the 3 skill areas, or open the Dashboard for full analytics.")
