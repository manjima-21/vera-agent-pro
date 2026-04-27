import streamlit as st
from google import genai
from PIL import Image
from gtts import gTTS
import io
import time
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="V.E.R.A. Omni-Vision", page_icon="👁️", layout="wide")

# --- 2. API SETUP ---
# We use gemini-3-flash-preview as the primary driver.
MODEL_ID = "gemini-3-flash-preview"

# In app.py
try:
    # Instead of a hardcoded string, we tell Streamlit to pull from secrets.toml
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found in secrets.toml!")
    st.stop()

# --- 3. PERSISTENT SPATIAL MEMORY ---
if "spatial_memory" not in st.session_state:
    st.session_state.spatial_memory = []

# --- 4. VOICE ENGINE ---
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format="audio/mp3", autoplay=True)
    except Exception:
        pass

# --- 5. SIDEBAR: AGENT CONTROLS ---
with st.sidebar:
    st.header("🤖 V.E.R.A. Search")
    user_query = st.text_input("🔍 Ask V.E.R.A.:", placeholder="e.g., Find my glasses...")
    
    st.divider()
    st.subheader("⚙️ System Settings")
    sentinel_mode = st.toggle("Active Awareness (Loop)", value=False)
    
    if st.button("🗑️ Reset Memory"):
        st.session_state.spatial_memory = []
        st.rerun()

# --- 6. MAIN DASHBOARD ---
st.title("👁️ V.E.R.A. | Gemini 3")
st.caption("Visual Entity & Recognition Assistant")

col1, col2 = st.columns([1.2, 0.8])

with col1:
    cam_image = st.camera_input("Live Vision Feed", label_visibility="collapsed")

with col2:
    if cam_image:
        if st.button("🛰️ Audit Environment", use_container_width=True) or sentinel_mode:
            with st.spinner(f"Analyzing via {MODEL_ID}..."):
                
                # Image compression for 2026 API speeds
                img = Image.open(cam_image).convert("RGB")
                img.thumbnail((1024, 1024)) 
                
                # Context building
                history = "\n".join([m['desc'] for m in st.session_state.spatial_memory[-3:]])
                prompt = f"""
                Act as V.E.R.A., a Spatial Intelligence Agent.
                
                QUERY: {user_query if user_query else "Describe all visible objects."}
                MEMORY: {history if history else "Start of session."}

                INSTRUCTIONS:
                1. INDEX: Identify and list all objects in the frame.
                2. RESPONSE: Directly answer the user query based on spatial positions.
                3. SAFETY: Identify any workplace hazards (spills, wires, etc).

                FORMAT:
                Index: [list of items]
                Result: [your detailed answer]
                Safety: [hazard or 'None']
                """

                try:
                    # Single-model call
                    response = client.models.generate_content(model=MODEL_ID, contents=[prompt, img])
                    response_text = response.text
                    
                    # Extraction
                    lines = response_text.split('\n')
                    all_items = next((l.split("Index:")[1] for l in lines if "Index:" in l), "Scanning...").strip()
                    main_ans = next((l.split("Result:")[1] for l in lines if "Result:" in l), "I see the environment.").strip()
                    hazard = next((l.split("Safety:")[1] for l in lines if "Safety:" in l), "None").strip()

                    # UI Response
                    st.success(f"🤖 **V.E.R.A.:** {main_ans}")
                    if hazard.lower() != "none":
                        st.error(f"🚨 **HAZARD:** {hazard}")
                    
                    with st.expander("📝 View Full Object Index"):
                        st.write(all_items)

                    # Output & Persistence
                    speak(main_ans)
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    st.session_state.spatial_memory.append({"time": timestamp, "desc": main_ans, "items": all_items})

                except Exception as e:
                    st.error(f"Model Error: {e}")
                    if "404" in str(e):
                        st.info("Tip: If gemini-3 is not found, try 'gemini-flash-latest' as a fallback.")

            if sentinel_mode:
                time.sleep(20) # Keeps you safe from 429 Rate Limits
                st.rerun()

# --- 7. SPATIAL TIMELINE ---
st.divider()
st.subheader("📜 Spatial Timeline")
if st.session_state.spatial_memory:
    for entry in reversed(st.session_state.spatial_memory[-5:]):
        with st.chat_message("assistant"):
            st.write(f"**{entry['time']}** | {entry['desc']}")
            st.caption(f"Items seen: {entry['items']}")