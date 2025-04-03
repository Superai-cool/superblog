import streamlit as st
import openai
import os

# Load OpenAI key securely
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# Streamlit page settings
st.set_page_config(page_title="Superblog GPT", layout="centered")

# Custom CSS for modern, clean UI
st.markdown("""
    <style>
        body {
            background-color: #f9fafb;
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
            max-width: 700px;
            margin: auto;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
        }
        .stTextInput input, .stTextArea textarea {
            font-size: 1rem;
            padding: 0.75rem;
            border-radius: 8px;
        }
        .stButton>button {
            font-size: 1rem;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            background-color: #1a73e8;
            color: white;
            border: none;
        }
        .linkedin-post {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            font-size: 1.05rem;
            line-height: 1.6;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
            white-space: pre-wrap;
            margin-top: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("Superblog GPT for LinkedIn")

# Instructions
st.markdown("Craft short, sharp, and professional LinkedIn posts in seconds.")

# Input fields
topic = st.text_input("💡 Topic", placeholder="e.g., Remote leadership, AI in HR, Personal branding")

tone = st.selectbox("🧠 Tone of Voice", ["Professional", "Empathetic", "Thought-Leader"])

generate = st.button("✨ Generate Post")

# Generate Post
if generate and topic:
    with st.spinner("Writing your short, sharp LinkedIn post..."):

        prompt = f"""
You are a GPT assistant that writes high-engagement LinkedIn posts for professionals.

Write a short LinkedIn post (80 to 100 words) on the topic: "{topic}"
- Use a professional, engaging, and {tone.lower()} tone.
- Start with a compelling headline (no emojis).
- Use → arrows or bullet points for structure if needed.
- Ensure it's human-like and relatable.
- End with a strong closing line.
- Include 5–7 relevant, trending hashtags at the end.

Avoid fluff. Focus on clarity, brevity, and value.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            post = response['choices'][0]['message']['content'].strip()
            st.markdown("### 📝 Your LinkedIn Post")
            st.markdown(f"<div class='linkedin-post'>{post}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

elif generate:
    st.warning("Please enter a topic to generate your post.")
