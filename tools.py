# Agent Tools for Incident Search and Analysis

def search_incidents(incident_data, query):
    """
    Search for incidents based on the given query.
    
    :param incident_data: List of incidents to search.
    :param query: Search term.
    :return: Filtered list of incidents.
    """
    return [incident for incident in incident_data if query.lower() in incident['description'].lower()]


def analyze_incident(incident):
    """
    Analyze a single incident and provide insights.
    
    :param incident: The incident to analyze.
    :return: Analysis report.
    """
    report = {...}  # Analysis logic here
    return report


# Example Usage:
# incidents = [{'id': 1, 'description': 'Power outage'}, {'id': 2, 'description': 'Network issue'}]
# found_incidents = search_incidents(incidents, 'Network')
# report = analyze_incident(found_incidents[0])
