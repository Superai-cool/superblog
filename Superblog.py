import streamlit as st
import openai
import os

# Load API key securely
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# Page settings
st.set_page_config(page_title="Google Review Reply GPT", layout="centered")

# Custom CSS for modern mobile-friendly UI
st.markdown("""
    <style>
        body {
            background-color: #f4f6f8;
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            max-width: 720px;
            padding-top: 2rem;
            margin: auto;
        }
        h1 {
            text-align: center;
            font-size: 2.2rem;
            color: #2c3e50;
        }
        .stTextArea textarea, .stTextInput input {
            font-size: 1rem;
            padding: 0.8rem;
            border-radius: 10px;
        }
        .stButton>button {
            font-size: 1rem;
            padding: 0.6rem 1.5rem;
            border-radius: 8px;
            background-color: #1a73e8;
            color: white;
            border: none;
        }
        .reply-box {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            font-size: 1.05rem;
            line-height: 1.6;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-top: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🗨️ Google Review Reply GPT")

st.markdown("Reply to Google Reviews with professionalism and personality. Paste a review, choose a tone, and get a short, smart response (20–50 words).")

# User Inputs
review = st.text_area("📌 Paste Google Review Here", height=150, placeholder="e.g., Loved the service and the food was amazing!")
tone = st.selectbox("🎯 Select Tone", ["Professional", "Friendly", "Empathetic", "Apologetic", "Appreciative"])

generate = st.button("✍️ Generate Reply")

# Guard Clause
if generate and not review.strip():
    st.warning("Please paste a review to generate a reply.")
elif generate:
    with st.spinner("Crafting your perfect response..."):

        system_prompt = """
You are a specialized GPT assistant designed ONLY to generate short, human-sounding replies to Google Reviews.

Your ONLY task is to reply to pasted customer reviews (positive, neutral, or negative) based on the selected tone.

Instructions:
- Respond in 20–50 words.
- Use a professional, natural tone based on the user's selection.
- Avoid emojis.
- Do not use generic phrases unless appropriate.
- Address the sentiment/context of the review.
- Do NOT answer unrelated queries.
If the user enters anything other than a review, reply with:

"This GPT is designed only to generate short replies to Google Reviews. Please paste a review and select a tone to receive a reply."
"""

        user_prompt = f"""
Review: "{review}"
Tone: {tone}
Generate a 20–50 word reply that fits this review and tone.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )

            reply = response["choices"][0]["message"]["content"].strip()

            # Show reply
            st.markdown("### ✅ Suggested Reply")
            st.markdown(f"<div class='reply-box'>{reply}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
