"""
Safety Incident Advisor — Streamlit App
An agentic chatbot that analyzes historical safety incidents and recommends
actions/trainings based on what worked in the past.
"""

import streamlit as st
from data_loader import prepare_dataset
from incident_analyzer import IncidentAnalyzer
from chatbot_agent import ChatbotAgent
from data_writer import save_new_incident

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

tab1, tab2 = st.tabs(["💬 Chat Advisor", "📝 Report Incident"])

with tab1:
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

with tab2:
    st.markdown("### 📝 Report a New Incident")
    st.info("Fill out the form below to add a new incident to the historical database. This will help METHAN-AI provide better recommendations in the future.")
    
    with st.form("incident_report_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        
        with col_a:
            title = st.text_input("Incident Title*", placeholder="e.g., Gas leak during flange tightening")
            category = st.selectbox("Category*", analyzer.get_category_list())
            risk_level = st.selectbox("Risk Level*", analyzer.get_risk_levels())
            location = st.selectbox("Location*", analyzer.get_locations())
            date = st.date_input("Date*")
            
        with col_b:
            setting = st.text_input("Setting", placeholder="e.g., Maintenance, Operation")
            injury_category = st.text_input("Injury Category", placeholder="e.g., First Aid, Near Miss")
            severity = st.text_input("Severity", placeholder="e.g., Low, Medium, High")
            primary_classification = st.text_input("Primary Classification")

        st.markdown("---")
        st.markdown("#### Incident Details")
        what_happened = st.text_area("What Happened?*", placeholder="Describe the sequence of events...")
        what_could_have_happened = st.text_area("What Could Have Happened?", placeholder="describe potential consequences...")
        why_did_it_happen = st.text_area("Why Did It Happen? (Root Cause)", placeholder="Identify the underlying causes...")
        causal_factors = st.text_area("Causal Factors", placeholder="List specific contributing factors...")
        
        st.markdown("---")
        st.markdown("#### Lessons & Actions")
        what_went_well = st.text_area("What Went Well?", placeholder="Any positive actions taken during the incident...")
        lessons_to_prevent = st.text_area("Lessons to Prevent Reoccurrence*", placeholder="Key takeaways and preventive measures...")
        
        st.markdown("#### Corrective Actions")
        st.caption("Add at least one corrective action.")
        
        action_1 = st.text_input("Action 1", placeholder="Action description")
        owner_1 = st.text_input("Owner 1", placeholder="Role or department")
        
        action_2 = st.text_input("Action 2", placeholder="Action description")
        owner_2 = st.text_input("Owner 2", placeholder="Role or department")
        
        submitted = st.form_submit_button("Submit Incident Report", type="primary")
        
        if submitted:
            if not (title and what_happened and lessons_to_prevent and action_1):
                st.error("Please fill in all required fields (*) and at least one corrective action.")
            else:
                report_data = {
                    "title": title,
                    "category": category,
                    "risk_level": risk_level,
                    "location": location,
                    "date": str(date),
                    "setting": setting,
                    "injury_category": injury_category,
                    "severity": severity,
                    "primary_classification": primary_classification,
                    "what_happened": what_happened,
                    "what_could_have_happened": what_could_have_happened,
                    "why_did_it_happen": why_did_it_happen,
                    "causal_factors": causal_factors,
                    "what_went_well": what_went_well,
                    "lessons_to_prevent": lessons_to_prevent
                }
                
                actions = []
                if action_1:
                    actions.append({"action": action_1, "owner": owner_1 or "TBD"})
                if action_2:
                    actions.append({"action": action_2, "owner": owner_2 or "TBD"})
                
                success, result = save_new_incident(report_data, actions)
                
                if success:
                    st.success(f"✅ Incident {result} successfully reported! The similarity engine will be updated.")
                    st.balloons()
                    # Clear cache to reload new data
                    st.cache_resource.clear()
                    # st.rerun() # Optional: auto-rerun to refresh UI
                else:
                    st.error(f"❌ Failed to save incident: {result}")