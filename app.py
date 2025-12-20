from __future__ import annotations

import csv
import json
from io import StringIO
from pathlib import Path
import streamlit as st
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown


st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Week 01 • Day 04 — Streamlit GUI")
st.markdown(
    """
    <style>
      header { 
        background: #FFE3EE !important; 
      }

      .block-container {
        padding-top: 2.5rem !important;
        background: #FFE3EE !important;
      }
      .stApp {
        background: #FFE3EE !important;
      }
      section[data-testid="stSidebar"] {
        background: #FFE3EE !important;
      }

      section[data-testid="stSidebar"] > div {
        background: #FFE3EE !important;
      }
      .stButton>button, button[kind="primary"] {
        background: #F8A8C7 !important;
        border: none !important;
        border-radius: 14px !important;
        color: #2E2A2B !important;
        font-weight: 600 !important;
      }
      .stButton>button:hover {
        background: #F48FB7 !important;
      }
      h1, h2, h3, h4, p, label, span, div {
        color: #2E2A2B !important;
      }
      thead th {
        white-space: nowrap !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Inputs")

def parse_uploaded_csv(uploaded_file):
    raw = uploaded_file.getvalue() 
    text = raw.decode("utf-8-sig")  
    reader = csv.DictReader(StringIO(text))
    return list(reader)


def is_effectively_empty(rows: list[dict[str, str]]):
    if len(rows) == 0:
        return True

    for r in rows:
        if any((v or "").strip() != "" for v in r.values()):
            return False
    return True
uploaded = st.sidebar.file_uploader("Upload a CSV", type=["csv"])
show_preview = st.sidebar.checkbox("Show preview", value=True)
report_name = st.sidebar.text_input("Report name", value="report").strip() or "report"

rows: list[dict[str, str]] | None = None
report = st.session_state.get("report")

if uploaded is None:
    st.info("No file uploaded yet. Upload a CSV from the sidebar to begin")
else:
    try:
        rows = parse_uploaded_csv(uploaded)#if empty csv
        if is_effectively_empty(rows):
            st.error("CSV loaded, but it has no data rows.")
            st.stop()

        st.success(f"Loaded: {uploaded.name}")

        if show_preview:
            st.subheader("Preview (first 5 rows)")
            st.write(rows[:5])

    except Exception as e:
        st.error("Could not read this CSV: " + str(e))
        st.stop()
st.divider()

if rows is not None:
    if st.button("Generate report", type="primary"):
        try:
            report = profile_rows(rows)
            st.session_state["report"] = report
            st.success("Report generated.")
        except Exception as e:
            st.error("Profiling failed: " + str(e))
            st.stop()

if report is not None:
    st.subheader("Summary")
    n_rows = report.get("n_rows")
    n_cols = report.get("n_cols")

    c1, c2 = st.columns(2)
    c1.metric("Rows", n_rows if n_rows is not None else "-")
    c2.metric("Columns", n_cols if n_cols is not None else "-")

    st.subheader("Column table")
    columns_info = report.get("columns", [])
    if columns_info:
        st.dataframe(columns_info, use_container_width=True, hide_index=True)
    else:
        st.warning("No column profiles found in report['columns'].")

    with st.expander("Markdown preview", expanded=True):
        md_text = render_markdown(report)
        st.markdown(md_text)

    with st.expander("Raw JSON", expanded=False):
        st.json(report)

if report is not None:
    st.divider()
    st.subheader("Export outputs")

    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    md_text = render_markdown(report)

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "Download JSON",
            data=json_text,
            file_name=f"{report_name}.json",
            mime="application/json",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "Download Markdown",
            data=md_text,
            file_name=f"{report_name}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.caption("Download means to your computer and Save will write into outputs into your projects folder ")

    if st.button("Save to outputs/"):
        try:
            out_dir = Path("outputs")
            out_dir.mkdir(parents=True, exist_ok=True)

            (out_dir / f"{report_name}.json").write_text(json_text, encoding="utf-8")
            (out_dir / f"{report_name}.md").write_text(md_text, encoding="utf-8")

            st.success(f"Saved: outputs/{report_name}.json and outputs/{report_name}.md")
        except Exception as e:
            st.error("Could not save files: " + str(e))
else:
    st.caption("Upload a CSV and click **Generate report** to enable exports.")
