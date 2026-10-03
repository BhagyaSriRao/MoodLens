import json
import streamlit as st
from auth_db import log_emotion

# Lazy import for transformers
def _get_pipeline():
    try:
        from transformers import pipeline
        return pipeline
    except ImportError:
        return None

# Simple chat-style Text Emotion Detection (no custom sidebar sections)
st.set_page_config(page_title="Text Emotion Detection", page_icon="📝", layout="wide")

# Require login
if "user" not in st.session_state or st.session_state.user is None:
    st.error("Please log in from the Home page before using Text Emotion Detection.")
    st.stop()

user_info = st.session_state.user

# Purple/black theme CSS (lightweight)
st.markdown(
    """
    <style>
    body { background-color: #000; color: #E0E0E0; }
    .block-container { padding: 20px 60px 40px 60px !important; }
    .header-bar {
        text-align: center; font-size: 40px; font-weight: 700; letter-spacing: 2px;
        padding: 20px; border-radius: 16px;
        background: linear-gradient(90deg, #e81cff, #40c9ff);
        color: white; box-shadow: 0 6px 25px rgba(0,0,0,0.4);
    }
    .chat-container {
        border-radius: 16px; padding: 20px 40px; min-height: 60vh; max-height: 65vh;
        overflow-y: auto; background-color: #121212;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
        border: 1px solid #333; margin-top: 20px;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(15px);} to { opacity:1; transform: translateY(0);} }
    .user-msg {
        background: linear-gradient(135deg, #0078FF, #00A8FF); color: white;
        padding: 10px 15px; border-radius: 18px 18px 4px 18px; margin: 8px 0; text-align: right;
        width: fit-content; max-width: 70%; margin-left: auto; box-shadow: 0 2px 10px rgba(0,120,255,0.3);
        animation: fadeIn 0.5s ease-in-out;
    }
    .bot-msg {
        background: #1E1E1E; color: #E0E0E0; padding: 10px 15px; border-radius: 18px 18px 18px 4px;
        margin: 8px 0; width: fit-content; max-width: 70%; text-align: left; border: 1px solid #333;
        animation: fadeIn 0.5s ease-in-out;
    }
    .emotion-badge { display:inline-block; background: linear-gradient(90deg, #e81cff, #40c9ff);
        color:#fff; padding:4px 8px; border-radius:10px; font-size:12px; margin-top:6px; margin-left:6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Classifier (cached)
DEFAULT_MODEL = "michellejieli/emotion_text_classifier"
FALLBACK_MODEL = "j-hartmann/emotion-english-distilroberta-base"

@st.cache_resource
def load_classifier(model_name: str = DEFAULT_MODEL):
    pipeline = _get_pipeline()
    if pipeline is None:
        st.error("Transformers not available")
        return None
    try:
        return pipeline("text-classification", model=model_name, return_all_scores=True)
    except Exception:
        st.warning("Loading fallback model…")
        return pipeline("text-classification", model=FALLBACK_MODEL, return_all_scores=True)

clf = load_classifier()

# Session state for chat history
if "td_history" not in st.session_state:
    st.session_state.td_history = []  # list of (role, text)

# Header
st.markdown("<div class='header-bar'>Text Emotion Detection</div>", unsafe_allow_html=True)

# Render chat transcript
chat_html = "<div class='chat-container'>"
for role, content in st.session_state.td_history:
    chat_html += f"<div class='{ 'user-msg' if role=='user' else 'bot-msg' }'>{content}</div>"
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# Input bar at bottom
prompt = st.chat_input("Type a sentence to detect emotion…")
if prompt:
    # Append user message
    st.session_state.td_history.append(("user", prompt))

    # Analyze
    with st.spinner("Analyzing…"):
        scores = clf(prompt)[0]
        top = max(scores, key=lambda x: x["score"]) if scores else None

    if top:
        emojis = {
            "joy": "😄", "sadness": "💙", "anger": "😠", "fear": "😨",
            "disgust": "🤢", "surprise": "😯", "neutral": "😐"
        }
        label = top["label"].lower()
        emoji = emojis.get(label, "🙂")
        pct = f"{top['score']*100:.1f}%"
        # Optional distribution summary
        dist = ", ".join(f"{s['label']} {s['score']*100:.0f}%" for s in sorted(scores, key=lambda x: -x['score'])[:4])
        reply = f"Detected: {top['label']} {emoji} ({pct}) <div class='emotion-badge'>Scores: {dist}</div>"

        # Log to SQLite
        try:
            log_emotion(
                user_id=user_info["id"],
                session_id=user_info.get("session_id"),
                source_type="text",
                source_text=prompt,
                file_name=None,
                predicted_emotion=top["label"],
                extra=json.dumps(scores),
            )
        except Exception:
            # Don't break UI if logging fails
            pass
    else:
        reply = "I couldn't detect an emotion from that. Try a longer sentence."

    st.session_state.td_history.append(("bot", reply))
    st.rerun()
