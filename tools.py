"""
Tools Module
High-level tool functions that the chatbot agent uses to answer user queries.
"""

from collections import Counter


def get_recommendations(analyzer, query, top_n=5):
    """
    Find similar past incidents and extract their corrective actions.

    Returns a dict with:
      - similar_incidents: list of matching incidents with details
      - recommended_actions: deduplicated list of corrective actions from those incidents
    """
    similar = analyzer.find_similar(query, top_n=top_n)

    # Collect all actions from similar incidents
    all_actions = []
    for incident in similar:
        for action in incident.get("actions_list", []):
            all_actions.append(
                {
                    "action": action["action"],
                    "owner": action.get("owner", "N/A"),
                    "timing": action.get("timing", "N/A"),
                    "from_case": incident["case_id"],
                    "from_title": incident["title"],
                    "similarity": incident["similarity"],
                }
            )

    return {
        "similar_incidents": similar,
        "recommended_actions": all_actions,
    }


def get_training_suggestions(analyzer, query, top_n=5):
    """
    Extract training-related recommendations from similar past incidents.

    Looks at 'lessons_to_prevent' and 'what_went_well' fields.
    """
    similar = analyzer.find_similar(query, top_n=top_n)

    lessons = []
    good_practices = []

    for incident in similar:
        # Extract lessons
        lesson_text = incident.get("lessons_to_prevent", "")
        if lesson_text and str(lesson_text) != "nan":
            lessons.append(
                {
                    "lesson": str(lesson_text).strip(),
                    "from_case": incident["case_id"],
                    "from_title": incident["title"],
                    "risk_level": incident.get("risk_level", "N/A"),
                    "similarity": incident["similarity"],
                }
            )

        # Extract what went well
        well_text = incident.get("what_went_well", "")
        if well_text and str(well_text) != "nan":
            good_practices.append(
                {
                    "practice": str(well_text).strip(),
                    "from_case": incident["case_id"],
                    "from_title": incident["title"],
                    "similarity": incident["similarity"],
                }
            )

    return {
        "lessons_to_prevent": lessons,
        "good_practices": good_practices,
    }


def search_incidents(analyzer, query, filters=None, top_n=10):
    """
    Search incidents by text similarity with optional filters.

    :param filters: dict like {'risk_level': 'High', 'category': 'Safety'}
    """
    return analyzer.find_similar(query, top_n=top_n, filters=filters)


def get_statistics(analyzer):
    """
    Return summary statistics about the entire incident database.
    """
    return analyzer.get_statistics()


def detect_intent(user_message):
    """
    Simple keyword-based intent detection.
    Returns one of: 'recommend', 'training', 'search', 'stats', 'help', 'general'
    """
    msg = user_message.lower().strip()

    # Stats / overview
    if any(
        kw in msg
        for kw in [
            "statistics",
            "stats",
            "overview",
            "summary",
            "how many",
            "total",
            "count",
            "breakdown",
            "distribution",
        ]
    ):
        return "stats"

    # Training suggestions
    if any(
        kw in msg
        for kw in [
            "training",
            "train",
            "lesson",
            "learn",
            "best practice",
            "what went well",
            "good practice",
            "prevent",
        ]
    ):
        return "training"

    # Recommendations / what to do
    if any(
        kw in msg
        for kw in [
            "recommend",
            "suggestion",
            "what should",
            "action",
            "corrective",
            "what to do",
            "how to handle",
            "advice",
            "fix",
            "mitigation",
        ]
    ):
        return "recommend"

    # Help
    if any(kw in msg for kw in ["help", "what can you do", "how do i use"]):
        return "help"

    # Search for specific incidents
    if any(
        kw in msg
        for kw in [
            "search",
            "find",
            "show",
            "list",
            "incidents",
            "filter",
            "look up",
            "high risk",
            "low risk",
            "medium",
        ]
    ):
        return "search"

    # Default: treat as an incident description for recommendations
    return "recommend"


if __name__ == "__main__":
    # Test intent detection
    test_messages = [
        "What training should we do for chemical handling?",
        "Show me high risk incidents",
        "How many incidents happened in 2023?",
        "We had a pressure release during valve replacement, what should we do?",
        "help",
    ]
    for msg in test_messages:
        print(f"  '{msg}' -> {detect_intent(msg)}")
