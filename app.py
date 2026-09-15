from __future__ import annotations

import streamlit as st

from utils.helpers import PRACTICE_BLUEPRINTS, SECTION_ORDER
from utils.streamlit_support import apply_brand_styles, get_services, render_status_strip, render_syllabus_strip


st.set_page_config(
    page_title="DP-600 Prep Hub",
    page_icon="📊",
    layout="wide",
)

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
        <div class="hero-title">DP-600 Prep Hub</div>
        <div class="hero-subtitle">
            An adaptive Streamlit + Gemini workspace built directly from the official DP-600
            skills-measured outline. All three skill areas — Maintain a Data Analytics
            Solution, Prepare Data, and Implement & Manage Semantic Models — get equal
            footing. Generate original questions, track performance per skill area, and
            sharpen exactly what the exam tests.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_status_strip(settings, gemini, repository)

st.subheader("Launch a Skill Area")
page_map = [
    ("Maintain a Data Analytics Solution", "pages/maintain_solution.py"),
    ("Prepare Data", "pages/prepare_data.py"),
    ("Implement & Manage Semantic Models", "pages/semantic_models.py"),
]
row1 = st.columns(4)
for column, (label, target) in zip(row1, page_map):
    column.page_link(target, label=label, use_container_width=True)
row1[3].page_link("pages/dashboard.py", label="Dashboard", use_container_width=True)

st.subheader("Platform Capabilities")
feature_cols = st.columns(3)
feature_cols[0].markdown(
    """
    <div class="metric-panel">
        <h4>Syllabus-Locked Generation</h4>
        <p>Every prompt is scoped to the exact skill area and topic from the official DP-600 skills-measured outline — nothing off-syllabus sneaks in.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
feature_cols[1].markdown(
    """
    <div class="metric-panel">
        <h4>Adaptive Difficulty</h4>
        <p>Difficulty shifts upward after strong performance and eases back when accuracy drops below target, per skill area.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
feature_cols[2].markdown(
    """
    <div class="metric-panel">
        <h4>Persistent Insights</h4>
        <p>Attempts can be stored in MongoDB and mirrored to local CSV logs, broken down by skill area and topic.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("All 3 Skill Areas")
st.caption("No skill area is optional — the layout below mirrors the DP-600 skills-measured outline's own weighting.")
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
