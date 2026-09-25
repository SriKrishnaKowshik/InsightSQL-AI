import streamlit as st
from llm.query_engine import QueryEngine
from utils.charts import ChartGenerator

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="InsightSQL AI",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------------------------
# Session State
# -----------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

engine = QueryEngine()

# -----------------------------------------------------
# Header
# -----------------------------------------------------

st.title("📊 InsightSQL AI")
st.caption("AI-Powered Business Intelligence using PostgreSQL + Gemma 3")

st.divider()

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

with st.sidebar:

    st.header("Example Questions")

    examples = [
        "Show the top 5 products by revenue.",
        "Which category generates the highest revenue?",
        "Show monthly revenue trend.",
        "Which cities have the most customers?",
        "Show payment method distribution."
    ]

    for q in examples:
        if st.button(q, use_container_width=True):
            st.session_state.selected_question = q

    st.divider()

    if st.button("🗑 Clear History", use_container_width=True):
        st.session_state.history = []

# -----------------------------------------------------
# Input
# -----------------------------------------------------

default = st.session_state.get("selected_question", "")

question = st.text_input(
    "Ask a business question",
    value=default,
    placeholder="e.g. Show the top 5 products by revenue"
)

col1, col2 = st.columns([1,5])

run = col1.button("Run", type="primary", use_container_width=True)

# -----------------------------------------------------
# Execute Query
# -----------------------------------------------------

if run and question:

    try:
        with st.spinner("Analyzing your database..."):
            result = engine.ask(question)

        st.session_state.history.insert(0, result)

    except Exception as e:
        st.error("Unable to generate a valid SQL query.")
        st.code(str(e))
        st.stop()

# -----------------------------------------------------
# Display Latest Result
# -----------------------------------------------------

if st.session_state.history:

    latest = st.session_state.history[0]

    df = latest["data"]

    # ---------------- KPI ----------------

    st.subheader("Key Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Rows Returned", len(df))

    with c2:
        if len(df.columns) >= 2:
            if df.iloc[:,1].dtype != object:
                st.metric(
                    "Total Value",
                    f"{df.iloc[:,1].sum():,.0f}"
                )

    with c3:
        if len(df.columns) >= 2:
            st.metric(
                "Top Result",
                str(df.iloc[0,0])
            )

    st.divider()

    # ---------------- Insight ----------------

    st.subheader("🧠 AI Insight")

    st.info(latest["insight"])

    # ---------------- Chart ----------------

    chart = ChartGenerator.create_chart(df)

    if chart:
        st.plotly_chart(chart, use_container_width=True)

    # ---------------- Table ----------------

    st.subheader("📋 Result Table")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------- Download ----------------

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        csv,
        file_name="insights.csv",
        mime="text/csv"
    )

    # ---------------- SQL ----------------

    with st.expander("🧾 Generated SQL"):

        st.code(latest["sql"], language="sql")

# -----------------------------------------------------
# History
# -----------------------------------------------------

if len(st.session_state.history) > 1:

    st.divider()

    st.subheader("🕘 Previous Questions")

    for item in st.session_state.history[1:]:

        with st.expander(item["question"]):

            st.write(item["insight"])

            st.dataframe(
                item["data"],
                use_container_width=True,
                hide_index=True
            )

            st.code(item["sql"], language="sql")