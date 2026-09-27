import streamlit as st
from llm.query_engine import QueryEngine
from utils.charts import ChartGenerator
from utils.kpi import KPIGenerator

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

if "question" not in st.session_state:
    st.session_state.question = ""

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

engine = QueryEngine()

# -----------------------------------------------------
# Header
# -----------------------------------------------------

st.title("📊 InsightSQL AI")

st.markdown(
    "<span style='color:#64748B;font-size:18px;'>"
    "AI-Powered Business Intelligence with PostgreSQL, RAG & Gemma 3"
    "</span>",
    unsafe_allow_html=True,
)

st.divider()

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

with st.sidebar:

    st.title("📊 InsightSQL AI")
    st.caption("Business Intelligence Assistant")

    st.divider()

    st.subheader("⚡ Suggested Questions")

    examples = [
        "Show the top 5 products by revenue.",
        "Which category generates the highest revenue?",
        "Show monthly revenue trend.",
        "Which cities have the most customers?",
        "Show payment method distribution.",
        "List the top 10 customers by revenue from Berlin."
    ]

    for i, q in enumerate(examples):
        if st.button(q, key=f"example_{i}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

    st.divider()

    st.subheader("🕘 Recent Questions")

    if not st.session_state.history:
        st.caption("No history yet.")

    else:
        for i, item in enumerate(st.session_state.history[:5]):
            if st.button(
                item["question"],
                key=f"history_{i}",
                use_container_width=True,
            ):
                st.session_state.pending_question = item["question"]
                st.rerun()

    st.divider()

    if st.button("🗑 Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.question = ""
        st.session_state.pending_question = None
        st.rerun()

# -----------------------------------------------------
# Input
# -----------------------------------------------------

# Apply pending question BEFORE widget creation
if st.session_state.pending_question:
    st.session_state.question = st.session_state.pending_question
    st.session_state.pending_question = None

question = st.text_input(
    "💬 Ask your database anything",
    key="question",
    placeholder="Example: Which category generates the highest revenue?"
)

col1, col2 = st.columns([1, 6])

with col1:
    run = st.button("🚀 Analyze", type="primary")

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

    st.subheader("📈 Key Metrics")

    kpis = KPIGenerator.generate(df)

    kpi_cols = st.columns(3)

    for col, metric in zip(kpi_cols, kpis):
        title, value = metric
        with col:
            st.metric(title, value)

    st.divider()

    # ---------------- AI Insight ----------------

    st.subheader("🧠 AI Business Insight")
    st.info(latest["insight"])

    # ---------------- Follow-up Questions ----------------

    followups = latest.get("followups", [])

    if followups:

        st.markdown("---")
        st.subheader("💡 Suggested Next Questions")

        cols = st.columns(min(3, len(followups)))

        for i, suggestion in enumerate(followups[:3]):
            with cols[i]:
                if st.button(
                    suggestion,
                    key=f"followup_{i}",
                    use_container_width=True,
                ):
                    st.session_state.pending_question = suggestion
                    st.rerun()

    st.divider()

    # ---------------- Chart ----------------

    chart = ChartGenerator.create_chart(df)

    if chart is not None:
        st.plotly_chart(chart, use_container_width=True)

    # ---------------- Result Table ----------------

    st.subheader("📋 Result Table")

    with st.container(border=True):

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=min(420, 45 * (len(df) + 1)),
        )

        st.caption(
            f"Showing {len(df)} rows × {len(df.columns)} columns"
        )

    # ---------------- Download ----------------

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        csv,
        file_name="insights.csv",
        mime="text/csv",
    )

    # ---------------- SQL ----------------

    with st.expander("🧾 View Generated SQL"):
        st.code(latest["sql"], language="sql")

# -----------------------------------------------------
# Previous History
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
                hide_index=True,
            )

            st.code(item["sql"], language="sql")