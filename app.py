"""
Safety Incident Advisor — Streamlit App
An agentic chatbot that analyzes historical safety incidents and recommends
actions/trainings based on what worked in the past.
"""

import streamlit as st
from data_loader import prepare_dataset
from incident_analyzer import IncidentAnalyzer
from chatbot_agent import ChatbotAgent

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Safety Incident Advisor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Chat messages */
    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 8px !important;
    }

    /* Sidebar stats */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 16px;
        color: white;
        text-align: center;
        margin-bottom: 12px;
    }
    .stat-card h3 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }
    .stat-card p {
        margin: 4px 0 0 0;
        font-size: 13px;
        opacity: 0.85;
    }

    /* Example question buttons */
    section[data-testid="stSidebar"] .stButton button {
        width: 100% !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        height: auto !important;
        min-height: 44px !important;
        text-align: left !important;
    }
    section[data-testid="stSidebar"] .stButton button p {
        color: #111827 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        line-height: 1.25 !important;
        white-space: normal !important;
        text-align: left !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #e5e7eb !important;
        border-color: #9ca3af !important;
    }

    /* Main Header Styling */
    .header-container {
        text-align: center;
        padding: 40px 20px;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 40px;
    }
    .main-title {
        font-size: 64px;
        font-weight: 900;
        letter-spacing: -2px;
        background: linear-gradient(135deg, #00A6CE 0%, #004A99 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
        text-transform: uppercase;
    }
    .main-subtitle {
        color: #4a5568;
        font-size: 20px;
        margin: 15px 0 0 0;
        font-weight: 600;
        letter-spacing: 1px;
        opacity: 0.8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Cache data loading (runs once)
# ──────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading incident database...")
def init_system():
    dataset = prepare_dataset()
    analyzer = IncidentAnalyzer(dataset)
    agent = ChatbotAgent(analyzer)
    return analyzer, agent


analyzer, agent = init_system()
stats = analyzer.get_statistics()

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ METHAN-AI")
    st.caption("Advanced Incident Intelligence for Methanex")

    st.markdown("---")

    # Stats cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="stat-card"><h3>{stats["total_incidents"]}</h3><p>Incidents</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stat-card"><h3>{stats["total_actions"]}</h3><p>Actions</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Risk level breakdown
    st.markdown("#### Risk Levels")
    for level, count in stats["by_risk_level"].items():
        emoji = "🔴" if "high" in str(level).lower() else "🟡" if "medium" in str(level).lower() else "🟢"
        st.markdown(f"{emoji} **{level}:** {count}")

    st.markdown("---")

    # Quick example questions
    st.markdown("#### 💡 Try asking:")

    example_questions = [
        "We had a chemical spill during tank cleaning, what should we do?",
        "What training for confined space work?",
        "Show me high risk incidents involving pressure release",
        "Give me an overview of incident statistics",
        "What lessons from electrical incidents?",
    ]

    for q in example_questions:
        if st.button(q, key=f"ex_{hash(q)}"):
            st.session_state["prefill_question"] = q

    st.markdown("---")
    st.caption("Data: 196 incidents • 1,688 corrective actions")


# ──────────────────────────────────────────────
# Main Header (METHAN-AI)
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="header-container">
        <h1 class="main-title">METHAN-AI</h1>
        <p class="main-subtitle">Intelligent Safety & Incident Command Bot</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": agent.respond("help"),
        }
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check for prefilled question from sidebar
prefill = st.session_state.pop("prefill_question", None)

# Chat input
user_input = st.chat_input("Describe an incident or ask a question...")

# Use prefill if set, otherwise use typed input
prompt = prefill or user_input

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing historical patterns..."):
            response = agent.respond(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})