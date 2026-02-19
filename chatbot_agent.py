"""
Chatbot Agent Module
Routes user messages to the appropriate tools and formats responses.
"""

import os
from tools import (
    detect_intent,
    get_recommendations,
    get_training_suggestions,
    search_incidents,
    get_statistics,
)


import streamlit as st
import google.generativeai as genai
from config import USE_GEMINI, GEMINI_MODEL

class ChatbotAgent:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.name = "Safety Advisor"
        self.gemini_enabled = False
        
        # Initialize Gemini if configured
        if USE_GEMINI:
            api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel(GEMINI_MODEL)
                    self.gemini_enabled = True
                except Exception as e:
                    print(f"Error initializing Gemini: {e}")

    def _synthesize_with_gemini(self, query, context_text, intent_type="general"):
        """Uses Gemini to synthesize a natural language response based on the search context."""
        prompt = f"""
        You are METHAN-AI, an expert Safety Incident Advisor for Methanex. 
        Your goal is to help users understand safety risks and prevent incidents by learning from historical data.
        
        USER QUERY: {query}
        
        HISTORICAL CONTEXT:
        {context_text}
        
        INSTRUCTIONS:
        1. Act as a professional, helpful, and safety-conscious advisor.
        2. Use the provided historical context to answer the user's query.
        3. If specific corrective actions are in the context, emphasize them.
        4. Synthesize the information into a cohesive, conversational response.
        5. Use markdown for structure (bullet points, bold text).
        6. If the context doesn't contain a clear answer, use your general safety knowledge but clarify that it's based on general best practices, not specific historical cases from the database.
        7. Keep the response concise but thorough.
        
        INTENT: {intent_type}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini Synthesis Error: {e}")
            return "⚠️ Gemini synthesis failed. Falling back to structured data view."

    def respond(self, user_message):
        """
        Process a user message, detect intent, call the right tool,
        and return a formatted response string.
        """
        intent = detect_intent(user_message)

        if intent == "help":
            return self._help_response()
        elif intent == "stats":
            return self._stats_response()
        elif intent == "training":
            return self._training_response(user_message)
        elif intent == "search":
            return self._search_response(user_message)
        elif intent == "recommend":
            return self._recommend_response(user_message)
        else:
            return self._recommend_response(user_message)

    def _help_response(self):
        return (
            "👋 **Hi! I'm your Safety Incident Advisor.** Here's what I can do:\n\n"
            "🔍 **Describe an incident** — I'll find similar past cases and recommend actions\n\n"
            "📋 **Ask for recommendations** — e.g. *\"What should we do about a chemical spill?\"*\n\n"
            "🎓 **Ask for training suggestions** — e.g. *\"What training for confined space work?\"*\n\n"
            "📊 **Ask for statistics** — e.g. *\"How many high-risk incidents do we have?\"*\n\n"
            "🔎 **Search incidents** — e.g. *\"Show me incidents involving pressure release\"*\n\n"
            "Just type your question and I'll analyze our database of **196 historical incidents** and **1,688 corrective actions**!"
        )

    def _stats_response(self):
        stats = get_statistics(self.analyzer)
        lines = [
            f"📊 **Incident Database Overview**\n",
            f"📁 **Total Incidents:** {stats['total_incidents']}",
            f"✅ **Total Corrective Actions:** {stats['total_actions']}\n",
            "---",
            "**By Risk Level:**",
        ]
        for level, count in stats["by_risk_level"].items():
            emoji = "🔴" if "high" in str(level).lower() else "🟡" if "medium" in str(level).lower() else "🟢"
            lines.append(f"  {emoji} {level}: {count}")

        lines.append("\n**By Category:**")
        for cat, count in stats["by_category"].items():
            lines.append(f"  • {cat}: {count}")

        lines.append("\n**By Injury Category:**")
        for inj, count in list(stats["by_injury"].items())[:5]:
            lines.append(f"  • {inj}: {count}")

        return "\n".join(lines)

    def _recommend_response(self, query):
        result = get_recommendations(self.analyzer, query, top_n=5)
        similar = result["similar_incidents"]
        actions = result["recommended_actions"]

        if not similar:
            return (
                "🤔 I couldn't find closely matching incidents in our database. "
                "Try describing the situation in more detail, or ask me for general training recommendations."
            )

        if self.gemini_enabled:
            # Prepare context for Gemini
            context = f"Matched Incidents:\n"
            for inc in similar:
                context += f"- {inc['title']} (Risk: {inc.get('risk_level')})\n"
                context += f"  What Happened: {inc.get('what_happened')}\n"
                context += f"  Lessons: {inc.get('lessons_to_prevent')}\n"
            
            context += "\nRecommended Actions:\n"
            for act in actions[:10]:
                context += f"- {act['action']} (Owner: {act['owner']})\n"
                
            return self._synthesize_with_gemini(query, context, "recommendations")

        lines = [f"🔍 **Found {len(similar)} similar past incidents:**\n"]

        for i, inc in enumerate(similar, 1):
            score_pct = int(inc["similarity"] * 100)
            risk_emoji = "🔴" if "high" in str(inc.get("risk_level", "")).lower() else "🟡" if "medium" in str(inc.get("risk_level", "")).lower() else "🟢"
            lines.append(
                f"**{i}. {inc['title']}** ({score_pct}% match) {risk_emoji} {inc.get('risk_level', 'N/A')}"
            )
            lines.append(f"   📍 {inc.get('setting', 'N/A')} | 📅 {inc.get('date', 'N/A')} | 🌍 {inc.get('location', 'N/A')}")
            lines.append("")

        if actions:
            lines.append("---")
            lines.append(f"\n✅ **Recommended Actions** (from similar past incidents):\n")
            # Show up to 10 most relevant actions
            seen = set()
            count = 0
            for act in actions:
                action_text = act["action"]
                if action_text not in seen and count < 10:
                    seen.add(action_text)
                    lines.append(f"  {count + 1}. {action_text}")
                    lines.append(f"     ↳ *Owner:* {act['owner']} | *Timing:* {act['timing']} | *From:* {act['from_case']}")
                    lines.append("")
                    count += 1

        return "\n".join(lines)

    def _training_response(self, query):
        result = get_training_suggestions(self.analyzer, query, top_n=5)
        lessons = result["lessons_to_prevent"]
        practices = result["good_practices"]

        if not lessons and not practices:
            return (
                "🤔 I couldn't find specific training recommendations for that topic. "
                "Try being more specific about the type of work or hazard."
            )

        if self.gemini_enabled:
            context = "Training Lessons:\n"
            for l in lessons:
                context += f"- From {l['from_title']}: {l['lesson']}\n"
            context += "\nGood Practices:\n"
            for p in practices:
                context += f"- From {p['from_title']}: {p['practice']}\n"
                
            return self._synthesize_with_gemini(query, context, "training")

        lines = [f"🎓 **Training & Prevention Recommendations:**\n"]

        if lessons:
            lines.append("**📚 Lessons from Similar Incidents:**\n")
            for i, lesson in enumerate(lessons, 1):
                risk_emoji = "🔴" if "high" in str(lesson.get("risk_level", "")).lower() else "🟡" if "medium" in str(lesson.get("risk_level", "")).lower() else "🟢"
                lines.append(f"**{i}. From {lesson['from_case']}** — *{lesson['from_title']}* {risk_emoji}")
                lines.append(f"   {lesson['lesson'][:300]}{'...' if len(lesson['lesson']) > 300 else ''}")
                lines.append("")

        if practices:
            lines.append("---")
            lines.append("\n**✨ What Went Well (Good Practices to Reinforce):**\n")
            for i, p in enumerate(practices, 1):
                lines.append(f"**{i}. From {p['from_case']}** — *{p['from_title']}*")
                lines.append(f"   {p['practice'][:300]}{'...' if len(p['practice']) > 300 else ''}")
                lines.append("")

        return "\n".join(lines)

    def _search_response(self, query):
        # Extract potential filters from the query
        filters = {}
        query_lower = query.lower()
        if "high risk" in query_lower or "high-risk" in query_lower:
            filters["risk_level"] = "high"
        elif "medium risk" in query_lower or "medium-risk" in query_lower:
            filters["risk_level"] = "medium"
        elif "low risk" in query_lower or "low-risk" in query_lower:
            filters["risk_level"] = "low"

        results = search_incidents(self.analyzer, query, filters=filters, top_n=10)

        if not results:
            return "🤔 No incidents found matching your search. Try different keywords."

        if self.gemini_enabled and results:
            context = "Found Incidents:\n"
            for inc in results[:5]:
                context += f"- {inc['title']} ({inc.get('risk_level')})\n"
                context += f"  Context: {inc.get('what_happened')}\n"
            
            summary = self._synthesize_with_gemini(f"Summarize these search results for: {query}", context, "search")
            if not summary.startswith("⚠️"):
                lines = [f"🤖 **Gemini Summary:**\n{summary}\n", "---", f"🔎 **Full Search Results ({len(results)}):**\n"]
            else:
                lines = [f"🔎 **Found {len(results)} incidents:**\n"]
        else:
            lines = [f"🔎 **Found {len(results)} incidents:**\n"]

        for i, inc in enumerate(results, 1):
            score_pct = int(inc["similarity"] * 100)
            risk_emoji = "🔴" if "high" in str(inc.get("risk_level", "")).lower() else "🟡" if "medium" in str(inc.get("risk_level", "")).lower() else "🟢"
            lines.append(
                f"**{i}. {inc['title']}** ({score_pct}% match)"
            )
            lines.append(f"   {risk_emoji} {inc.get('risk_level', 'N/A')} | 📍 {inc.get('setting', 'N/A')} | 📅 {inc.get('date', 'N/A')}")
            # Short snippet of what happened
            what = str(inc.get("what_happened", ""))[:150]
            if what and what != "nan":
                lines.append(f"   > {what}...")
            lines.append("")

        return "\n".join(lines)