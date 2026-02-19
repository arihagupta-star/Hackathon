import csv
import os
import pandas as pd
from datetime import datetime
from config import REPORTS_CSV, ACTIONS_CSV

def ensure_newline(filepath):
    """Ensures the file ends with a newline character."""
    if not os.path.exists(filepath):
        return
    with open(filepath, 'rb+') as f:
        f.seek(0, os.SEEK_END)
        if f.tell() > 0:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            if last_char != b'\n':
                f.write(b'\n')

def generate_case_id(existing_ids):
    """Generates a new unique case ID."""
    if not existing_ids:
        return "INC-001"
    
    # Try to extract numbers from existing IDs like 'INC-001'
    numeric_ids = []
    for cid in existing_ids:
        try:
            if isinstance(cid, str) and '-' in cid:
                numeric_ids.append(int(cid.split('-')[-1]))
            elif isinstance(cid, (int, float)):
                numeric_ids.append(int(cid))
        except (ValueError, IndexError):
            continue
    
    if not numeric_ids:
        return f"INC-{len(existing_ids) + 1:03d}"
    
    new_id = max(numeric_ids) + 1
    return f"INC-{new_id:03d}"

def save_new_incident(report_data, action_data_list):
    """
    Appends a new incident report and its actions to the CSV files.
    
    report_data: dict containing report fields
    action_data_list: list of dicts containing action fields
    """
    # 1. Load existing reports to get a new case_id
    reports_df = pd.read_csv(REPORTS_CSV)
    new_case_id = generate_case_id(reports_df['case_id'].tolist())
    
    # 2. Prepare report row
    report_data['case_id'] = new_case_id
    report_data['date'] = report_data.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Ensure all columns exist in the right order
    report_cols = reports_df.columns.tolist()
    report_row = {col: report_data.get(col, "") for col in report_cols}
    
    # 3. Prepare action rows
    action_rows = []
    for i, action_item in enumerate(action_data_list):
        action_row = {
            'case_id': new_case_id,
            'action_number': i + 1,
            'action': action_item.get('action', ""),
            'owner': action_item.get('owner', "TBD"),
            'timing': action_item.get('timing', ""),
            'verification': action_item.get('verification', "")
        }
        action_rows.append(action_row)
    
    # 4. Append to CSVs
    try:
        # Append Report
        ensure_newline(REPORTS_CSV)
        with open(REPORTS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=report_cols)
            writer.writerow(report_row)
            
        # Append Actions
        actions_df = pd.read_csv(ACTIONS_CSV)
        action_cols = actions_df.columns.tolist()
        ensure_newline(ACTIONS_CSV)
        with open(ACTIONS_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=action_cols)
            for row in action_rows:
                # Ensure all columns are present
                clean_row = {col: row.get(col, "") for col in action_cols}
                writer.writerow(clean_row)
                
        return True, new_case_id
    except Exception as e:
        print(f"Error saving incident: {e}")
        return False, str(e)
