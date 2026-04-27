import streamlit as st
from google import genai

st.title("🧪 Gemini Model Scanner")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
    
    st.write("### All Available Model IDs:")
    
    # Simple list command
    for m in client.models.list():
        st.code(m.name)  # This will show the exact string like 'models/gemini-1.5-flash'

except Exception as e:
    st.error(f"Scanner failed: {e}")