import streamlit as st
from openai import OpenAI

# ------------------- Setup -------------------
client = OpenAI(api_key="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")  # Replace with your key

SYSTEM_PROMPT = """
You are Dr. Athena, a senior researcher and highly respected computer scientist with a PhD in Computer Science, 
over 35 years of experience, more than 70 internationally recognized research papers and journal publications, 
and over 10 bestselling books in the field of computer science.

Your primary role is to act as an elite research assistant and writing mentor. 
When a user provides text (academic, technical, or otherwise), your job is to:

1. Rephrase and refine the text into polished, journal-ready academic writing.
2. Maintain a natural, human-like tone—never robotic or AI-generated.
3. Ensure accuracy, clarity, and sophistication while avoiding redundancy.
4. Present writing that meets the highest standards of scholarly communication.

Always respond as a world-class academic mentor providing polished, publication-ready revisions.
"""

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Athena – Research Writing Mentor",
    page_icon="🎓",
    layout="centered",
)

# ------------------- Custom CSS for Elegant Look -------------------
st.markdown(
    """
    <style>
    body {
        background: #fefefe;
        font-family: 'Merriweather', serif;
        color: #2c2c2c;
    }
    .main {
        padding: 2rem;
        background: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    .assistant {
        background: #fafafa;
        color: #2c2c2c;
        padding: 1em;
        border-left: 4px solid #4B8BBE;
        border-radius: 8px;
        margin-bottom: 1em;
        font-size: 1.05em;
    }
    .user {
        background: #f0f7ff;
        color: #2c2c2c;
        padding: 1em;
        border-left: 4px solid #1E88E5;
        border-radius: 8px;
        margin-bottom: 1em;
        font-size: 1.05em;
    }
    .title {
        font-size: 2.2em;
        font-weight: bold;
        margin-bottom: 0.3em;
        color: #1E1E1E;
        text-align: center;
    }
    .subtitle {
        font-size: 1.15em;
        margin-bottom: 2em;
        color: #555555;
        text-align: center;
    }
    .stButton button {
        width: 100%;
        background: #1E88E5;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6em;
        font-size: 1em;
        transition: background 0.3s ease;
    }
    .stButton button:hover {
        background: #1669bb;
    }
    textarea {
        border-radius: 8px !important;
        border: 1px solid #ddd !important;
        padding: 10px !important;
        font-size: 1em !important;
        font-family: 'Georgia', serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------- App Title -------------------
st.markdown('<div class="title">Athena</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Personal Research Writing Mentor</div>', unsafe_allow_html=True)

# ------------------- Initialize Chat State -------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ------------------- Chat Function -------------------
def get_bot_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=messages,
            max_tokens=400,
            temperature=0.6,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ------------------- Display Conversation -------------------
with st.container():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user'><strong>You:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='assistant'><strong>Athena:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)

# ------------------- Input Box -------------------
st.session_state.user_input = st.text_area(
    "Enter your research text or question:", 
    st.session_state.user_input, 
    height=120
)

col1, col2 = st.columns([5, 1])
with col2:
    submit = st.button("Discuss", use_container_width=True)

# ------------------- Handle Submission -------------------
if submit and st.session_state.user_input.strip():
    user_text = st.session_state.user_input
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.user_input = ""  # CLEAR INPUT AFTER SUBMISSION
    with st.spinner("Athena is analyzing and refining your text..."):
        bot_reply = get_bot_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()
