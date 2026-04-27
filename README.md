👁️ V.E.R.A. (Visual Entity & Recognition Assistant)
Spatial Intelligence for the Modern Workspace

V.E.R.A. is an AI-powered agent designed to bridge the gap between physical environments and digital memory. Built for the 2026 Gemini Hackathon, it uses the Gemini 3 Flash engine to index workspaces, locate lost items, and monitor environmental safety through a simple camera feed.

🚀 Features
Open-World Indexing: Unlike standard vision models, V.E.R.A. doesn't need pre-training. It identifies any object on your desk in real-time.

Temporal Spatial Memory: Tracks the history of your environment. If you moved your keys 10 minutes ago, V.E.R.A. remembers.

Safety Sentinel: Automatically detects workplace hazards like liquid spills near electronics or cluttered walkways.

Voice-Guided Interaction: Fully interactive TTS (Text-to-Speech) allows for eyes-free assistance.

🛠️ Tech Stack
Language: Python 3.11+

Framework: Streamlit

Core AI: Google Gemini 3 Flash Preview

Vision Processing: PIL (Pillow)

Audio: gTTS (Google Text-to-Speech)

📦 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/manjima-21/vera-agent-pro.git
cd vera-agent-pro
Install dependencies:

Bash
pip install -r requirements.txt
Configure Secrets:
Create a .streamlit/secrets.toml file and add your API key:

Ini, TOML
GOOGLE_API_KEY = "your_gemini_api_key_here"
Run the App:

Bash
streamlit run app.py
🛡️ Security & Best Practices
This project implements Zero-Leak Security Protocols. API keys are managed via Streamlit Secrets and are strictly excluded from version control via .gitignore to ensure environment integrity.
