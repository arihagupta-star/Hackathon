"""
Data Loader Module
Loads and preprocesses the safety incident datasets.
"""

import pandas as pd
from config import REPORTS_CSV, ACTIONS_CSV, TEXT_FIELDS


def load_data():
    """
    Load both CSVs and return them as a dict of DataFrames.
    """
    try:
        # Explicit encoding to handle potential issues on different OS/environments
        reports = pd.read_csv(REPORTS_CSV, encoding='utf-8', errors='replace')
        actions = pd.read_csv(ACTIONS_CSV, encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"Error loading CSV files: {e}")
        # Create empty dummy data to allow app to start even if files are missing in cloud
        reports = pd.DataFrame(columns=["case_id", "title", "what_happened", "why_did_it_happen", "causal_factors", "lessons_to_prevent", "category", "risk_level", "location", "date", "setting", "injury_category", "severity"])
        actions = pd.DataFrame(columns=["case_id", "action_number", "action", "owner", "timing", "verification"])
        
    return {"reports": reports, "actions": actions}


def merge_data(reports, actions):
    """
    Merge reports with their corrective actions grouped by case_id.
    Returns reports DataFrame with an extra 'actions_list' column.
    """
    # Group actions by case_id into a list of dicts
    actions_grouped = (
        actions.groupby("case_id")
        .apply(lambda g: g[["action_number", "action", "owner", "timing", "verification"]].to_dict("records"), include_groups=False)
        .reset_index(name="actions_list")
    )
    merged = reports.merge(actions_grouped, on="case_id", how="left")
    # Fill NaN actions_list with empty list
    merged["actions_list"] = merged["actions_list"].apply(
        lambda x: x if isinstance(x, list) else []
    )
    return merged


def build_search_text(row):
    """
    Combine multiple text fields into a single searchable string for each incident.
    """
    parts = []
    for field in TEXT_FIELDS:
        val = row.get(field, "")
        if pd.notna(val) and str(val).strip():
            parts.append(str(val).strip())
    return " ".join(parts)


def prepare_dataset():
    """
    Full pipeline: load, merge, and add search text.
    Returns the fully prepared DataFrame.
    """
    data = load_data()
    merged = merge_data(data["reports"], data["actions"])
    merged["search_text"] = merged.apply(build_search_text, axis=1)
    return merged


if __name__ == "__main__":
    df = prepare_dataset()
    print(f"Loaded {len(df)} incidents with actions attached.")
    print(f"Sample columns: {list(df.columns)}")
    print(f"\nFirst incident: {df.iloc[0]['title']}")
    print(f"  Actions count: {len(df.iloc[0]['actions_list'])}")