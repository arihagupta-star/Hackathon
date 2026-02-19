# Configuration settings for the Agentic Safety Incident Chatbot
import os

# Data file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_CSV = os.path.join(BASE_DIR, "reports.csv")
ACTIONS_CSV = os.path.join(BASE_DIR, "actions.csv")

# Similarity settings
TOP_N_SIMILAR = 5          # Number of similar incidents to return
SIMILARITY_THRESHOLD = 0.1  # Minimum similarity score to consider relevant

# Text fields used for building the similarity index
TEXT_FIELDS = [
    "what_happened",
    "why_did_it_happen",
    "causal_factors",
    "title",
    "lessons_to_prevent",
]

# App settings
APP_TITLE = "🛡️ Safety Incident Advisor"
APP_ICON = "🛡️"

# Gemini AI Settings
# Note: Api key should be stored in streamlit secrets or environment variables
GEMINI_MODEL = "gemini-1.5-flash"
USE_GEMINI = True  # Toggle this to False to fall back to the offline engine only
