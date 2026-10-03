import streamlit as st
from auth_db import init_db, create_user, authenticate_user, start_session, end_session

st.set_page_config(
    page_title="MOODLENS Home",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_db()

# --- Background Video and Overlay (no iframe) ---
video_url = "https://firebasestorage.googleapis.com/v0/b/imentiv-assets/o/home-new-video%2Fimentiv.mp4?alt=media&token=82e9683e-bb9d-47dc-b271-02234a3a200a"

video_html = f"""
    <video id="bg-video" autoplay loop muted playsinline>
        <source src="{video_url}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <div id="video-overlay"></div>
"""

custom_css = """
<style>
    html, body { height: 100%; background: transparent !important; }
    [data-testid="stApp"], main, [data-testid="stAppViewContainer"] { background: transparent !important; }
    /* Make all text white */
    body, .st-markdown, [data-testid="stMarkdownContainer"], p, h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }

    #bg-video {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        object-fit: cover; z-index: -2; margin: 0; padding: 0;
    }
    #video-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.25); z-index: -1; /* lighter overlay for brighter video */
    }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding: 4vh 5vw 5vh 5vw !important; }
    .nav-card-container { display: flex; flex-direction: column; gap: 16px; margin-top: 16px; }
    /* Header without purple box */
    .header-bar { text-align:left; font-size: 48px; font-weight:800; padding: 0; margin-bottom: 8px;
                  background: transparent; color:#ffffff; box-shadow:none; border-radius:0; }
    /* Style Streamlit page links to look like big cards */
    a[data-testid="stPageLink"] { display:block; width: 600px; padding:32px 36px; border-radius:20px; text-decoration:none; font-weight:800; font-size:2rem;
        color:#fff !important; background: rgba(255,255,255,0.12); backdrop-filter: blur(12px); border:1px solid rgba(255,255,255,0.25); }
    a[data-testid="stPageLink"]:hover { background: rgba(255,255,255,0.22); transform: translateY(-3px); }
</style>
"""

# Apply CSS once
st.markdown(custom_css, unsafe_allow_html=True)

# Always show background video on the home page
st.markdown(video_html, unsafe_allow_html=True)

# --- Auth state ---
if "user" not in st.session_state:
    st.session_state.user = None

user = st.session_state.user

# --- Header with login / register or logout on the right ---
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.markdown("<div class='header-bar'>Welcome to Moodlens</div>", unsafe_allow_html=True)
    if user is None:
        st.markdown(
            "<div>Select your analysis tool to begin — please log in first.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div>Select your analysis tool to begin, <strong>{user['username']}</strong>.</div>",
            unsafe_allow_html=True,
        )

with header_col2:
    # Small spacer to align controls with the header vertically
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    if user is None:
        # Compact login / register popover on the top-right
        popover_fn = getattr(st, "popover", None)
        if popover_fn is not None:
            with popover_fn("Login / Register", use_container_width=True):
                login_tab, register_tab = st.tabs(["Login", "Register"])

                # Login form
                with login_tab:
                    login_username = st.text_input("Username", key="login_username")
                    login_password = st.text_input("Password", type="password", key="login_password")
                    if st.button("Login"):
                        user_row = authenticate_user(login_username, login_password)
                        if user_row:
                            session_id = start_session(user_row["id"])
                            st.session_state.user = {
                                "id": user_row["id"],
                                "username": user_row["username"],
                                "session_id": session_id,
                            }
                            st.success(f"Logged in as {user_row['username']}")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")

                # Registration form
                with register_tab:
                    reg_username = st.text_input("New username", key="reg_username")
                    reg_password = st.text_input("Password", type="password", key="reg_password")
                    reg_password2 = st.text_input("Confirm password", type="password", key="reg_password2")
                    if st.button("Register"):
                        if reg_password != reg_password2:
                            st.error("Passwords do not match.")
                        else:
                            ok, err = create_user(reg_username, reg_password)
                            if ok:
                                st.success("Account created. You can now log in.")
                            else:
                                st.error(err or "Failed to create user.")
        else:
            # Fallback for older Streamlit: use an expander instead of popover
            with st.expander("Login / Register", expanded=False):
                login_tab, register_tab = st.tabs(["Login", "Register"])

                with login_tab:
                    login_username = st.text_input("Username", key="login_username")
                    login_password = st.text_input("Password", type="password", key="login_password")
                    if st.button("Login"):
                        user_row = authenticate_user(login_username, login_password)
                        if user_row:
                            session_id = start_session(user_row["id"])
                            st.session_state.user = {
                                "id": user_row["id"],
                                "username": user_row["username"],
                                "session_id": session_id,
                            }
                            st.success(f"Logged in as {user_row['username']}")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")

                with register_tab:
                    reg_username = st.text_input("New username", key="reg_username")
                    reg_password = st.text_input("Password", type="password", key="reg_password")
                    reg_password2 = st.text_input("Confirm password", type="password", key="reg_password2")
                    if st.button("Register"):
                        if reg_password != reg_password2:
                            st.error("Passwords do not match.")
                        else:
                            ok, err = create_user(reg_username, reg_password)
                            if ok:
                                st.success("Account created. You can now log in.")
                            else:
                                st.error(err or "Failed to create user.")

    else:
        # Logged-in view: show a simple logout button on the top-right
        if st.button("Logout"):
            if user.get("session_id") is not None:
                end_session(user["session_id"])
            st.session_state.user = None
            st.rerun()

# --- Navigation cards (only when logged in) ---
if user is not None:
    st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)
    st.page_link("pages/01_Sentio.py", label="Sentio")
    st.page_link("pages/Text_detection.py", label="Text Detection")
    st.page_link("pages/File_Upload.py", label="File Upload")
    st.page_link("pages/Live_Webcam.py", label="Live Webcam")
    st.page_link("pages/Understanding_Emotions.py", label="Understanding Your Emotions")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # When not logged in, keep the home page visible but prevent navigation
    st.markdown("\n\n_Login to access Sentio, File Upload, Live Webcam, and Understanding Your Emotions._")
