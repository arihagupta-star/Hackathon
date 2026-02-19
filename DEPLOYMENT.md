# 🌐 METHAN-AI Deployment Guide

Now that your code is secured in GitHub, follow these steps to move your bot from `localhost` to a permanent, public URL.

## Option 1: Streamlit Community Cloud (Recommended & Free)

This is the fastest way to get a professional URL for your hackathon presentation.

### 1. Sign Up / Log In
Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

### 2. Deploy a New App
1. Click the **"New app"** button.
2. Select your repository: `arihagupta-star/Hackathon`.
3. Select the branch: `main`.
4. Main file path: `app.py`.
5. Click **"Deploy!"**

### 3. Your New URL
After a few minutes, your app will be live at a URL like:
`https://methan-ai.streamlit.app` (you can customize this in the settings).

---

## Option 2: Persistence & Versioning

### ✅ Your Code is Safe
Your code is currently pushed to [github.com/arihagupta-star/Hackathon](https://github.com/arihagupta-star/Hackathon). Even if your local machine fails, your work is saved there.

### 🔒 Security
If you decide to add an OpenAI API key in the future:
1. **Local**: Add it to a `.env` file (never commit this).
2. **Streamlit Cloud**: Go to `Settings` -> `Secrets` and add your key there:
   ```toml
   OPENAI_API_KEY = "your-key-here"
   ```

## Summary of Files
- `app.py`: The main UI and entrance to the bot.
- `chatbot_agent.py`: The brain that routes user questions.
- `incident_analyzer.py`: The pattern-matching engine.
- `tools.py`: Helper functions for stats and recommendations.
- `base_reports - base_reports.csv.csv`: The primary incident dataset.
- `actions - actions.csv.csv`: The historical corrective actions dataset.
