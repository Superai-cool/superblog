import streamlit as st
import openai
import os

# Set your OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

st.set_page_config(page_title="Superblog GPT", layout="centered")

# Custom styling for mobile-friendly and elegant UI
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .block-container {
            max-width: 700px;
            margin: auto;
        }
        h1 {
            color: #2C3E50;
            text-align: center;
        }
        .stTextArea textarea {
            font-size: 1rem;
        }
        .linkedin-post {
            background-color: #F4F6F6;
            padding: 1.5rem;
            border-radius: 12px;
            font-size: 1.05rem;
            line-height: 1.6;
            white-space: pre-wrap;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Superblog GPT for LinkedIn")

st.markdown("Generate high-impact, professional LinkedIn posts with a single topic.")

topic = st.text_input("🔍 Enter a Topic", placeholder="e.g., Remote leadership, AI in HR, Personal branding")

tone_options = ["Professional & Insightful", "Empathetic & Bold", "Thought-leader Style"]
selected_tone = st.selectbox("🧠 Select Writing Style", tone_options)

submit = st.button("Generate LinkedIn Post")

if submit and topic:
    with st.spinner("Crafting your perfect LinkedIn post..."):

        prompt = f"""
You are a GPT expert at writing high-engagement LinkedIn posts for professionals. Based on the topic below, write a professional and emotionally engaging LinkedIn article that includes:

1. A **Compelling Headline** (no emojis).
2. A **Professional and Relatable Tone** matching this style: {selected_tone}.
3. A **Concise and Insightful Body** (max 300 words).
4. Use of **bullet points** or → arrows where relevant for readability.
5. A **Subtle Emotional Connection** through thoughtful phrasing.
6. A **Strong Conclusion** with a takeaway or statement.
7. Include **5–7 Relevant Hashtags** at the end (trending but relevant).

**Topic**: {topic}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600
            )
            generated_post = response['choices'][0]['message']['content'].strip()
            st.markdown("### ✨ Your LinkedIn Post")
            st.markdown(f"<div class='linkedin-post'>{generated_post}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Failed to generate post: {e}")

elif submit:
    st.warning("Please enter a topic to generate your post.")
