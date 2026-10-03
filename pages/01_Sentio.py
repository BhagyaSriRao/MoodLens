import os
import streamlit as st
import google.generativeai as genai

# Optional: voice input via browser microphone (streamlit-mic-recorder)
# Install with: pip install streamlit-mic-recorder
try:
    from streamlit_mic_recorder import speech_to_text  # type: ignore[import]
    HAS_VOICE_INPUT = True
except Exception:
    speech_to_text = None  # type: ignore[assignment]
    HAS_VOICE_INPUT = False

# --- 1. Configure API key securely ---
def get_gemini_api_key():
    # Prefer Streamlit secrets, then environment variables; support both names
    key = None
    try:
        key = (
            st.secrets.get("GEMINI_API_KEY")  # type: ignore[attr-defined]
            or st.secrets.get("GOOGLE_API_KEY")  # type: ignore[attr-defined]
        )
    except Exception:
        # st.secrets may not be configured
        pass
    if not key:
        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    return key

MY_API_KEY = get_gemini_api_key()
# ---------------------------------


# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(page_title="🎭 Sentio", page_icon="🎭", layout="wide")




# -----------------------------
# CSS Styling
# -----------------------------
def get_css(dark_mode=True):
    # --- (Your CSS is unchanged) ---
    return f"""
    <style>
        body {{
            background-color: {'#000000' if dark_mode else '#FFFFFF'};
            color: {'#E0E0E0' if dark_mode else '#111111'};
            font-family: "Poppins", "Helvetica Neue", Arial, sans-serif;
        }}
        .block-container {{
            padding: 20px 60px 40px 60px !important;
            max-width: 100% !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {'#141414' if dark_mode else '#F7F7F7'} !important;
            border-right: 1px solid {'#2A2A2A' if dark_mode else '#DDDDDD'};
        }}
        
        section[data-testid="stSidebar"] h3 {{
             color: {'#E0E0E0' if dark_mode else '#111111'};
        }}
        
        section[data-testid="stSidebar"] .stSelectbox label {{
             color: {'#E0E0E0' if dark_mode else '#111111'} !important;
        }}

        /* This targets the ACTUAL inner box of the select widget */
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
            background: {'linear-gradient(90deg, #e81cff, #40c9ff)' if dark_mode else 'linear-gradient(90deg, #4b6cb7, #182848)'} !important;
            border: none !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(232, 28, 255, 0.2);
        }}
        
        /* This styles the SELECTED TEXT ("j-hartmann...") inside the box */
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {{
             color: {'white' if dark_mode else 'white'} !important;
             font-weight: 600; 
             /* Ensure no other background is clashing */
             background-color: transparent !important;
        }}

        /* This styles the arrow on the selectbox */
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {{
             fill: {'white' if dark_mode else 'white'} !important;
        }}
        
        .header-bar {{
            text-align: center;
            font-size: 40px;
            font-weight: 700;
            letter-spacing: 2px;
            padding: 20px;
            border-radius: 16px;
            background: {'linear-gradient(90deg, #e81cff, #40c9ff)' if dark_mode else 'linear-gradient(90deg, #4b6cb7, #182848)'};
            color: white;
            box-shadow: 0 6px 25px rgba(0,0,0,0.4);
            text-transform: uppercase;
        }}
        .chat-container {{
            border-radius: 16px;
            padding: 20px 40px;
            min-height: 60vh;
            max-height: 65vh;
            overflow-y: auto;
            background-color: {'#121212' if dark_mode else '#FAFAFA'};
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.5);
            border: 1px solid {'#333333' if dark_mode else '#DDDDDD'};
            margin-top: 20px;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .user-msg {{
            background: {'linear-gradient(135deg, #0078FF, #00A8FF)' if dark_mode else 'linear-gradient(135deg, #0078FF, #69B9FF)'};
            color: white;
            padding: 10px 15px;
            border-radius: 18px 18px 4px 18px;
            margin: 8px 0;
            text-align: right;
            width: fit-content;
            max-width: 70%;
            margin-left: auto;
            box-shadow: 0 2px 10px rgba(0,120,255,0.3);
            animation: fadeIn 0.5s ease-in-out;
        }}
        .bot-msg {{
            background: {'#1E1E1E' if dark_mode else '#EDEDED'};
            color: {'#E0E0E0' if dark_mode else '#111111'};
            padding: 10px 15px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px 0;
            width: fit-content;
            max-width: 70%;
            text-align: left;
            border: 1px solid {'#333333' if dark_mode else '#CCCCCC'};
            animation: fadeIn 0.5s ease-in-out;
        }}
        .emotion-badge {{
            display: inline-block;
            background: linear-gradient(90deg, #e81cff, #40c9ff);
            color: #FFFFFF;
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 12px;
            margin-top: 6px;
            margin-left: 6px;
            box-shadow: 0 0 10px rgba(74, 144, 226, 0.3);
        }}
        .controls-row {{ display:flex; gap:8px; align-items:center; }}
        
        /* Style for inline voice button */
        div[data-testid="column"]:last-child button {{
            background: linear-gradient(90deg, #e81cff, #40c9ff) !important;
            border: none !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 20px !important;
            margin-top: 8px !important;
        }}

        section[data-testid="stSidebar"] div[data-testid="stButton"],
        section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] {{
            margin-bottom: 8px;
        }}
        
        section[data-testid="stSidebar"] div[data-testid="stButton"] > button,
        section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button {{
            background: {'linear-gradient(90deg, #e81cff, #40c9ff)' if dark_mode else 'linear-gradient(90deg, #4b6cb7, #182848)'} !important;
            color: white !important;
            border: none !important;
            border-radius: 12px;
            padding: 0.9rem 1.4rem;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
            width: 100%; 
        }}
        
        section[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover,
        section[data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(232, 28, 255, 0.5);
        }}
        
        @keyframes dots {{
            0% {{ content: '.'; }}
            33% {{ content: '..'; }}
            66% {{ content: '...'; }}
        }}
        .typing::after {{
            content: '...';
            animation: dots 1.2s infinite;
        }}

        div[data-baseweb="popover"] ul {{
            background-color: {'#333333' if dark_mode else '#EEEEEE'} !important;
            border: 1px solid {'#555555' if dark_mode else '#DDDDDD'} !important;
        }}
        div[data-baseweb="popover"] li {{
            color: {'#E0E0E0' if dark_mode else '#111111'} !important;
        }}
        div[data-baseweb="popover"] li:hover {{
            background-color: {'#555555' if dark_mode else '#DDDDDD'} !important;
        }}

    </style>
    """


# -----------------------------
# Initialize Session State
# -----------------------------
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = {}
if "active_chat" not in st.session_state:
    st.session_state.active_chat = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


# -----------------------------
# Apply CSS
# -----------------------------
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    # --- 2. CONFIGURE API KEY ON START ---
    try:
        if MY_API_KEY:
            genai.configure(api_key=MY_API_KEY)
            
            # Use default model without API call for faster loading
            if "resolved_model_name" not in st.session_state:
                st.session_state.resolved_model_name = "gemini-1.5-flash"
    except Exception as e:
        pass
    # -----------------------------------

    st.markdown("### ⚙️ Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ New Chat"):
            name = f"Chat {len(st.session_state.saved_chats)+1}"
            st.session_state.saved_chats[name] = [
                {"role": "model", "parts": ["👋 Hey there! I’m Sentio — how are you feeling today?"]}
            ]
            st.session_state.active_chat = name
            st.rerun()
    with col2:
        if st.button("🌗 Toggle Theme"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("### 📜 History")
    history_container = st.container()
    with history_container:
        for chat_name in reversed(list(st.session_state.saved_chats.keys())):
            if st.button(chat_name, key=f"history_{chat_name}", use_container_width=True):
                st.session_state.active_chat = chat_name
                st.rerun()

    st.markdown("### 💾 Manage Chats")
    if st.button("🗑️ Clear All"):
        st.session_state.saved_chats = {}
        st.session_state.active_chat = None
        st.rerun()

    if st.session_state.active_chat:
        chat_text = "\n".join(
            [f"{msg['role']}: {msg['parts'][0]}"
             for msg in st.session_state.saved_chats[st.session_state.active_chat]]
        )
        st.download_button("⬇️ Download Chat", chat_text, file_name=f"{st.session_state.active_chat}.txt")


# -----------------------------
# Header
# -----------------------------
st.markdown("<div class='header-bar'>🎭 Sentio (Chat-Powered)</div>", unsafe_allow_html=True)


# -----------------------------
# Chat Interface
# -----------------------------
if st.session_state.active_chat is None:
    st.info("Start a new chat using the sidebar ➕")
else:
    chat = st.session_state.saved_chats[st.session_state.active_chat]
    chat_html = "<div class='chat-container'>"

    for msg in chat:
        sender = "user" if msg["role"] == "user" else "bot"
        chat_html += f"<div class='{'user-msg' if sender=='user' else 'bot-msg'}'>{msg['parts'][0]}</div>"

    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # -----------------------------
    # Voice Input with Text Box Integration
    # -----------------------------
    
    # Initialize voice text in session state
    if "voice_input_text" not in st.session_state:
        st.session_state.voice_input_text = ""
    
    # Voice recording section
    col1, col2 = st.columns([6, 1])
    
    with col2:
        if HAS_VOICE_INPUT and speech_to_text is not None:
            try:
                raw_voice = speech_to_text(
                    language="en-US",
                    start_prompt="🎤",
                    stop_prompt="🛑",
                    just_once=True,
                    use_container_width=True,
                    key="inline_voice",
                )
                
                if raw_voice:
                    if isinstance(raw_voice, dict):
                        voice_text = (raw_voice.get("text") or "").strip()
                    else:
                        voice_text = str(raw_voice).strip()
                    
                    if voice_text:
                        st.session_state.voice_input_text = voice_text
                        st.rerun()
            except Exception:
                st.button("🎤", disabled=True, help="Voice input error")
        else:
            st.button("🎤", disabled=True, help="Install streamlit-mic-recorder")
    
    # Text input with voice text pre-filled
    with col1:
        if st.session_state.voice_input_text:
            # Show voice text in a text input for editing
            user_input = st.text_input(
                "Message", 
                value=st.session_state.voice_input_text,
                placeholder="💬 Type a message...",
                label_visibility="collapsed"
            )
            # Auto-submit voice input
            if st.session_state.voice_input_text and not user_input:
                user_input = st.session_state.voice_input_text
        else:
            user_input = st.chat_input("💬 Type a message...")
    
    # Clear voice text after user sends message  
    if user_input and user_input.strip():
        st.session_state.voice_input_text = ""
        # Process the input
        final_input = user_input.strip()
    else:
        final_input = None
        
    if final_input:
        user_input = final_input
        
    if user_input and user_input.strip():
        
        # Check if API key is valid before proceeding
        if not MY_API_KEY:
            st.error("Set GEMINI_API_KEY or GOOGLE_API_KEY in Streamlit secrets or environment, then restart the app.")
            st.stop()
            
        # Append user message (no local Transformers-based emotion analysis)
        chat.append({"role": "user", "parts": [user_input]})
        
        if len(chat) == 2: # First user message
            new_name = user_input[:30] + "..." if len(user_input) > 30 else user_input
            old_name = st.session_state.active_chat
            st.session_state.saved_chats[new_name] = st.session_state.saved_chats.pop(old_name)
            st.session_state.active_chat = new_name

        placeholder = st.empty()
        placeholder.markdown("<div class='bot-msg typing'>🤖 Thinking</div>", unsafe_allow_html=True)

        try:
            # 2. Build persona and chat history for the request
            persona = """
            You are 🎭 Sentio, an empathetic and supportive AI chatbot. 
            Your goal is to engage in a natural, flowing conversation. You are a great listener. 
            You are NOT a medical professional and should not give medical advice.
            If the user seems very distressed, gently suggest they talk to a trusted friend, family member, or professional.
            """

            chat_history_for_prompt = []
            for msg in chat:
                chat_history_for_prompt.append({
                    "role": "model" if msg["role"] == "model" else "user",
                    "parts": [msg["parts"][0]]
                })

            final_prompt = f"""
            [SYSTEM PERSONA]
            {persona}

            [LATEST USER MESSAGE]
            "{user_input}"
            """

            # 3. Choose a model: prefer resolved from list_models; otherwise try a fallback set
            preferred = st.session_state.get("resolved_model_name")
            candidate_models = []
            if preferred:
                candidate_models.append(preferred)
            candidate_models += [
                # Prefer latest stable families first
                "gemini-2.5-flash",
                "gemini-2.5-pro",
                "gemini-flash-latest",
                "gemini-pro-latest",
                "gemini-2.0-flash",
                "gemini-2.0-flash-001",
                # Older families as fallback
                "gemini-1.5-flash",
                "gemini-1.5-flash-latest",
                "gemini-1.5-pro",
                "gemini-1.0-pro",
                "chat-bison-001",
                "text-bison-001",
            ]

            # de-duplicate while preserving order
            seen = set()
            candidate_models = [x for x in candidate_models if not (x in seen or seen.add(x))]

            bot_reply = None
            last_error = None
            for mname in candidate_models:
                try:
                    model = genai.GenerativeModel(model_name=mname)
                    chat_session = model.start_chat(history=chat_history_for_prompt[:-1])  # except latest user msg
                    response = chat_session.send_message(final_prompt)
                    bot_reply = response.text
                    # Save the working model for future turns
                    st.session_state.resolved_model_name = mname
                    break
                except Exception as inner_e:
                    last_error = inner_e
                    continue

            if bot_reply is None:
                raise last_error if last_error else RuntimeError("No compatible Gemini model available.")

        except Exception as e:
            st.error(
                "Gemini API error. Try upgrading the client with: pip install -U google-generativeai. "
                f"Details: {e}"
            )
            bot_reply = f"😥 Sorry, I ran into an error. (Details: {e})"

        # 5. Add bot reply and rerun
        placeholder.empty()
        chat.append({"role": "model", "parts": [bot_reply]})
        st.session_state.saved_chats[st.session_state.active_chat] = chat
        st.rerun()