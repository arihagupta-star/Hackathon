"""
Incident Analyzer Module
Uses TF-IDF + cosine similarity to find historical patterns in safety incidents.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import TOP_N_SIMILAR, SIMILARITY_THRESHOLD


class IncidentAnalyzer:
    def __init__(self, data):
        """
        Initialize the analyzer with prepared incident data.
        :param data: DataFrame with 'search_text' column (from data_loader.prepare_dataset)
        """
        self.data = data
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2),
        )
        # Build the TF-IDF matrix on all incident texts
        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.data["search_text"].fillna("")
        )

    def find_similar(self, query, top_n=None, filters=None):
        """
        Find the most similar historical incidents to a query.

        :param query: User's incident description or question
        :param top_n: Number of results to return (default from config)
        :param filters: Optional dict of column->value filters (e.g. {'risk_level': 'High'})
        :return: List of dicts with incident details + similarity score
        """
        if top_n is None:
            top_n = TOP_N_SIMILAR

        # Vectorize the query
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Create results DataFrame
        results = self.data.copy()
        results["similarity"] = similarities

        # Apply optional filters
        if filters:
            for col, val in filters.items():
                if col in results.columns and val:
                    results = results[
                        results[col].str.lower().str.contains(val.lower(), na=False)
                    ]

        # Filter by threshold and sort
        results = results[results["similarity"] >= SIMILARITY_THRESHOLD]
        results = results.sort_values("similarity", ascending=False).head(top_n)

        return results.to_dict("records")

    def get_statistics(self):
        """
        Return aggregate statistics about the incident database.
        """
        df = self.data
        stats = {
            "total_incidents": len(df),
            "total_actions": sum(len(a) for a in df["actions_list"]),
            "by_category": df["category"].value_counts().to_dict(),
            "by_risk_level": df["risk_level"].value_counts().to_dict(),
            "by_severity": df["severity"].value_counts().to_dict(),
            "by_year": df["date"].value_counts().sort_index().to_dict(),
            "by_location": df["location"].value_counts().to_dict(),
            "by_injury": df["injury_category"].value_counts().to_dict(),
        }
        return stats

    def get_category_list(self):
        """Return unique categories."""
        return sorted(self.data["category"].dropna().unique().tolist())

    def get_risk_levels(self):
        """Return unique risk levels."""
        return sorted(self.data["risk_level"].dropna().unique().tolist())

    def get_locations(self):
        """Return unique locations."""
        return sorted(self.data["location"].dropna().unique().tolist())


if __name__ == "__main__":
    from data_loader import prepare_dataset

    df = prepare_dataset()
    analyzer = IncidentAnalyzer(df)

    results = analyzer.find_similar("pressure release during maintenance")
    print(f"Found {len(results)} similar incidents:")
    for r in results:
        print(f"  [{r['similarity']:.2f}] {r['title']}")

    stats = analyzer.get_statistics()
    print(f"\nTotal incidents: {stats['total_incidents']}")
    print(f"Total actions: {stats['total_actions']}")