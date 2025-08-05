import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import base64

st.set_page_config(page_title="LumaCare – Light for your mind", layout="centered")


def getBase64(background):
    with open(background, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = getBase64("bg.png")

st.markdown(f"""
    <style>
    .stApp {{
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        z-index: -2;
    }}

    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* dark overlay */
        z-index: -1;
    }}
    </style>

    <div class="background"></div>
    <div class="overlay"></div>
""", unsafe_allow_html=True)


st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .icon {
            margin-right: 10px;
        }
        .title {
            font-size: 50px;
            font-weight: bolder;
            text-align: center;
            margin-bottom: 10px;
           
        }
        .subtitle {
            text-align: center;
            color: #ccc;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


st.session_state.setdefault('conversationHistory', [])


def generate_response(user_input):
    st.session_state['conversationHistory'].append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state['conversationHistory']
    )
    ai_response = response.choices[0].message.content
    st.session_state['conversationHistory'].append({"role": "assistant", "content": ai_response})
    return ai_response


def genAffirmation():
    prompt = "Share a short and uplifting affirmation to encourage someone who is feeling stressed or overwhelmed."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content


def genMeditationGuidance():
    prompt = "Create a calming 5-minute guided meditation script to help someone relax, unwind, and release stress."
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content


st.markdown('<div class="title">🌟LumaCare</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Mental Wellness Companion</div>', unsafe_allow_html=True)


for msg in st.session_state['conversationHistory']:
    role = "🧑 You" if msg['role'] == 'user' else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}")


user_message = st.text_input("How can I help you today?")
if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")

col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Give me a Positive Affirmation"):
        affirmation = genAffirmation()
        st.markdown(f"""
        <p><i class="fas fa-heart icon" style="color:#e25555;"></i>
        <strong>Affirmation:</strong> <em>{affirmation}</em></p>
        """, unsafe_allow_html=True)

with col2:
    if st.button("🧘 Guide me through Meditation"):
        meditation_guide = genMeditationGuidance()
        st.markdown(f"""
        <p><i class="fas fa-brain icon" style="color:#4caf50;"></i>
        <strong>Guided Meditation:</strong> <em>{meditation_guide}</em></p>
        """, unsafe_allow_html=True)
