# Home.py

''' import streamlit as st

st.set_page_config(page_title="MOODLENS Home", page_icon="🎭", layout="wide")

st.markdown(
     """
    <style>
        .block-container {
            padding: 20px 60px 40px 60px !important;
        }
        .header-bar {
            text-align: center;
            font-size: 40px;
            font-weight: 700;
            letter-spacing: 2px;
            padding: 20px;
            border-radius: 16px;
            background: linear-gradient(90deg, #e81cff, #40c9ff);
            color: white;
            box-shadow: 0 6px 25px rgba(0,0,0,0.4);
            text-transform: uppercase;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='header-bar'>🎭 WELCOME TO MOODLENS</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.title("Your All-in-One Emotion Detection Project")
st.subheader("Use the navigation menu in the sidebar to choose your input method.")
st.info("👈 Select an app from the sidebar to get started!", icon="🤖")

st.divider()

st.header("About This Project")
st.write("""
This project, **MOODLENS**, is designed to detect emotions from three different sources:
- **Chatbot:** Analyze emotions from the text you type.
- **File Upload:** Upload an image or video to detect faces and their emotions.
- **Live Webcam:** Use your webcam for real-time emotion analysis.
""")
'''

import streamlit as st
from utils import apply_global_styles

# --- Page Configuration ---
st.set_page_config(
    page_title="MOODLENS Home",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar by default
)
apply_global_styles()

# --- Video Background and Custom CSS ---
video_url = "https://firebasestorage.googleapis.com/v0/b/imentiv-assets/o/home-new-video%2Fimentiv.mp4?alt=media&token=82e9683e-bb9d-47dc-b271-02234a3a200a"

# HTML for the background video and overlay
video_html = f"""
    <video id="bg-video" autoplay loop muted playsinline>
        <source src="{video_url}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <div id="video-overlay"></div>
"""

# CSS for styling
custom_css = """
<style>
    /* --- 1. Video Background and Overlay --- */
    #bg-video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -2; /* Behind overlay and content */
    }

    #video-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* 60% Black Overlay */
        z-index: -1; /* Behind content, on top of video */
    }

    /* --- 2. Hide Streamlit Elements --- */
    [data-testid="stSidebar"] {
        display: none; /* Hide the sidebar */
    }
    
    /* Make main app area transparent */
    [data-testid="stAppViewContainer"] {
        background: transparent;
    }
    .block-container {
        padding: 20px 60px 40px 60px !important;
    }

    /* --- 3. Global Text Styling (Dark Background) --- */
    body, .st-write, .st-markdown, [data-testid="stMarkdownContainer"], p {
        color: #FFFFFF !important; /* White text */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important; /* White headers */
    }
    h2 {
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        padding-bottom: 5px;
    }
    a {
        color: #40c9ff !important; /* Bright blue for links */
    }
    
    /* --- 4. "Frosted Glass" Card Style --- */
    .glass-card {
        background: rgba(255, 255, 255, 0.1); /* 10% white */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); /* For Safari */
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    /* --- 5. Custom Navigation Cards --- */
    .nav-card-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-top: 20px;
    }
    a.nav-link-card {
        display: block;
        padding: 20px;
        border-radius: 15px;
        text-decoration: none;
        color: #FFFFFF !important;
        font-size: 1.5rem;
        font-weight: 600;
        transition: background 0.3s ease, transform 0.3s ease;
        
        /* Apply glass style */
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    a.nav-link-card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-5px);
    }
    .nav-link-card span {
        margin-right: 15px;
        font-size: 2rem;
    }

    /* --- 6. Styled Streamlit Widgets (Dark Theme) --- */
    
    /* Header Bar (Unchanged, already good) */
    .header-bar {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        letter-spacing: 2px;
        padding: 20px;
        border-radius: 16px;
        background: linear-gradient(90deg, #f7b733 0%, #fc4a1a 35%, #e81cff 70%, #40c9ff 100%);
        color: white;
        box-shadow: 0 6px 25px rgba(0,0,0,0.4);
        text-transform: uppercase;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        background-color: transparent;
        color: #E5E7EB;
        font-weight: 600;
        font-size: 16px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        color: #FFFFFF;
        border-radius: 8px 8px 0 0;
        border-bottom: 2px solid #40c9ff;
    }
    
    /* Expander (Accordion) */
    details summary {
        font-size: 18px;
        font-weight: 600;
        color: #E5E7EB;
        background-color: rgba(255, 255, 255, 0.15); /* Slightly brighter glass */
        padding: 10px 15px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.2s ease;
        margin-top: 10px;
    }
    details summary:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    details div[data-testid="stExpanderDetails"] {
        background-color: rgba(255, 255, 255, 0.05); /* Darker glass */
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-top: none;
        padding: 15px;
        border-radius: 0 0 8px 8px;
    }
    
    /* Warning Box */
    [data-testid="stAlert"] {
        background: rgba(255, 229, 100, 0.1); /* Glassy Yellow */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 229, 100, 0.2);
        border-left: 5px solid #f1c40f;
        border-radius: 8px;
    }
    [data-testid="stAlert"] .st-markdown {
        color: #FFFFFF !important; /* Make text inside alert white */
    }

    /* Emotion Accent Bars */
    .accent-bar {
        height: 5px;
        width: 100px;
        border-radius: 3px;
        margin-bottom: 15px;
    }
    .accent-bar-anger    { background-color: #e74c3c; } /* Red */
    .accent-bar-sad      { background-color: #3498db; } /* Blue */
    .accent-bar-fear     { background-color: #9b59b6; } /* Purple */
    .accent-bar-happy    { background-color: #f1c40f; } /* Yellow */
    .accent-bar-surprise { background-color: #e67e22; } /* Orange */
    .accent-bar-disgust  { background-color: #27ae60; } /* Green */
    .accent-bar-neutral  { background-color: #95a5a6; } /* Gray */
</style>
"""

# Inject the video HTML and CSS
st.markdown(video_html, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)


# --- Page Content ---

# --- Header ---
st.markdown("<div class='header-bar'>🎭 WELCOME TO MOODLENS</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Top Section: Navigation and Intro ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    # --- Native Streamlit navigation links ---
    st.header("Start Exploring")
    # Use st.page_link so navigation works reliably with the pages/ directory
    st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)
st.page_link("pages/01_Sentio.py", label="🤖 Sentio")
    st.page_link("pages/File_Upload.py", label="🖼️ File Upload")
    st.page_link("pages/Live_Webcam.py", label="📷 Live Webcam")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("*(Select an app to get started)*", unsafe_allow_html=True)


with col2:
    # --- Introduction in a Glass Card ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("Your All-in-One Emotion Analysis Toolkit")
    st.subheader("Detect, understand, and get insights into your emotional expressions.")
    st.write("""
    Welcome to **MOODLENS**, an interactive project designed to analyze emotions from three different sources. 
    It uses advanced deep learning models to understand expressions from text, images, and live video.
    <br><br>
    This homepage also serves as a resource center for understanding and managing 
    the very emotions this tool detects.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- Bottom Section: Emotion Details ---
st.header("Understanding Your Emotions")
st.write("""
Detecting an emotion is the first step. Understanding and managing it is the next. 
Below are some brief insights and tips for navigating common emotions.
""")

st.warning("""
**Disclaimer:** This information is for educational purposes only and IS NOT a substitute for 
professional medical advice, diagnosis, or treatment. If you are struggling with your mental health, 
please seek help from a qualified professional.
""", icon="⚠️")
st.markdown("<br>", unsafe_allow_html=True)

# --- Tabs for Each Emotion (Styled by CSS) ---
emotions_list = ["Anger 😠", "Sadness 😔", "Fear / Anxiety 😨", "Happiness 😊", "Surprise 😮", "Disgust 🤢", "Neutral 😐"]
tab_anger, tab_sad, tab_fear, tab_happy, tab_surprise, tab_disgust, tab_neutral = st.tabs(emotions_list)

with tab_anger:
    st.markdown('<div class="accent-bar accent-bar-anger"></div>', unsafe_allow_html=True)
    st.subheader("Managing Anger")
    st.image("https://images.pexels.com/photos/167699/pexels-photo-167699.jpeg", 
             caption="Photo by Johannes Plenio", width=400)
    
    with st.expander("**Take a Pause & Breathe**"):
        st.write("When you feel anger rising, take a 'timeout.' Count to ten, take several deep breaths, or walk away from the situation. This gives you time to cool down before you react.")
    with st.expander("**Identify Your Triggers**"):
        st.write("Understand what makes you angry. Is it a specific person, place, or time of day? Recognizing your triggers is the first step to learning how to control them.")
    with st.expander("**Use 'I' Statements**"):
        st.write("Express your feelings calmly without blaming others. (e.g., 'I feel frustrated when this happens...' instead of 'You always...'). This reduces defensiveness and promotes discussion.")
    with st.expander("**Use Physical Activity**"):
        st.write("Channel the energy into exercise. A brisk walk, run, or workout can be a great, healthy outlet for pent-up anger and frustration.")
    st.markdown("---")
    st.markdown("🔗 **Learn More:** [Mind.org.uk on Anger](https://www.mind.org.uk/information-support/types-of-mental-health-problems/anger/managing-anger/)")


with tab_sad:
    st.markdown('<div class="accent-bar accent-bar-sad"></div>', unsafe_allow_html=True)
    st.subheader("Coping with Sadness")
    st.image("https://images.pexels.com/photos/3775095/pexels-photo-3775095.jpeg", 
             caption="Photo by Liza Summer", width=400)
    with st.expander("**Acknowledge Your Feelings**"):
        st.write("Allow yourself to feel sad. Crying can be a healthy release. Don't bottle it up or judge yourself for feeling down. It's a normal reaction to difficult life events.")
    with st.expander("**Connect with Others**"):
        st.write("Talk to a trusted friend or family member. Don't isolate yourself, even if you feel like it. Sharing your feelings can make you feel less alone and more supported.")
    with st.expander("**Practice Self-Care**"):
        st.write("Engage in activities that comfort you. Listen to music, take a warm bath, read a good book, or eat a healthy, comforting meal. Be kind to yourself.")
    with st.expander("**Set Small, Achievable Goals**"):
        st.write("If you feel overwhelmed, break tasks into small, manageable steps (e.g., 'get out of bed,' 'take a shower,' 'make coffee'). Celebrate each small victory.")
    st.markdown("---")
    st.markdown("🔗 **Learn More:** [HelpGuide.org on Coping with Sadness](https://www.helpguide.org/articles/depression/coping-with-depression.htm)")

with tab_fear:
    st.markdown('<div class="accent-bar accent-bar-fear"></div>', unsafe_allow_html=True)
    st.subheader("Dealing with Fear & Anxiety")
    st.image("https://images.pexels.com/photos/3847620/pexels-photo-3847620.jpeg", 
             caption="Photo by Anete Lusina", width=400)
    with st.expander("**Use Grounding Techniques**"):
        st.write("Focus on the present. Name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 you can smell, and 1 you can taste. This pulls your mind away from future worries.")
    with st.expander("**Challenge Anxious Thoughts**"):
        st.write("Ask yourself: 'Is this worry realistic? What's the worst that can *actually* happen? Can I handle it?' Often, our fears are worse than reality.")
    with st.expander("**Practice Deep Breathing**"):
        st.write("Inhale slowly for 4 counts, hold for 4, and exhale slowly for 6. This simple technique can activate your body's relaxation response and calm you down quickly.")
    with st.expander("**Limit Caffeine & News**"):
        st.write("Both caffeine and a constant stream of negative news can be major triggers for anxiety and make you feel on-edge. Try to limit your intake of both.")
    st.markdown("---")
    st.markdown("🔗 **Learn More:** [Anxiety & Depression Association of America (ADAA)](https://adaa.org/managing-stress-anxiety)")

with tab_happy:
    st.markdown('<div class="accent-bar accent-bar-happy"></div>', unsafe_allow_html=True)
    st.subheader("Cultivating Happiness")
    st.image("https://images.pexels.com/photos/1563355/pexels-photo-1563355.jpeg", 
             caption="Photo by Binh Ly", width=400)
    with st.expander("**Practice Gratitude**"):
        st.write("Regularly list things you are thankful for, big or small. This simple act shifts your focus from what you lack to what you have, boosting your mood.")
    with st.expander("**Savor the Moment (Mindfulness)**"):
        st.write("Pay full attention to good experiences. Whether it's a good meal, a beautiful sunset, or a chat with a friend, try to be fully present and enjoy it.")
    with st.expander("**Perform Acts of Kindness**"):
        st.write("Helping others can significantly boost your own mood and sense of well-being. It's a win-win.")
    with st.expander("**Find Your 'Flow'**"):
        st.write("Engage in a hobby or activity that you find so absorbing that you lose track of time (e.g., painting, coding, playing music, gardening). This is a powerful source of joy.")
    st.markdown("---")
    st.markdown("🔗 **Learn More:** [Greater Good Science Center at Berkeley](https://greatergood.berkeley.edu/topic/happiness/definition)")

with tab_surprise:
    st.markdown('<div class="accent-bar accent-bar-surprise"></div>', unsafe_allow_html=True)
    st.subheader("Embracing Surprise")
    st.image("https://images.pexels.com/photos/355934/pexels-photo-355934.jpeg", 
             caption="Photo by picjumbo.com", width=400)
    with st.expander("**Take a Beat**"):
        st.write("Surprise is the briefest emotion. It's a transition. Give yourself a moment to process the new information before forming a judgment or reacting.")
    with st.expander("**Stay Curious**"):
        st.write("Ask questions. Use the surprise as an opportunity to learn something new. 'Wow, I didn't expect that. Tell me more.'")
    with st.expander("**Reframe the Situation**"):
        st.write("If the surprise is neutral or negative, try to find a potential opportunity or lesson within it. 'This isn't what I planned, but maybe it's a chance to try... '")
    with st.expander("**Practice Adaptability**"):
        st.write("Life is full of surprises. Building your general resilience and flexibility helps you handle life's unexpected turns more smoothly and with less stress.")
    st.markdown("---")
    st.markdown("🔗 **Learn More:** [Psychology Today on Surprise](https://www.psychologytoday.com/us/basics/surprise)")


with tab_disgust:
    st.markdown('<div class="accent-bar accent-bar-disgust"></div>', unsafe_allow_html=True)
    st.subheader("Understanding Disgust")
    st.image("https://images.pexels.com/photos/4046107/pexels-photo-4046107.jpeg", 
             caption="Photo by Karolina Grabowska", width=400)
    with st.expander("**Identify the Source**"):
        st.write("Is your disgust physical (a smell, a taste, a sight) or moral (an action, an idea)? Knowing the source helps you understand your reaction.")
    with st.expander("**Set Boundaries**"):
        st.write("If you feel moral disgust at someone's behavior, it's often a strong signal from your conscience. It's a sign to set clear boundaries or distance yourself from the situation.")
    with st.expander("**Don't Dwell on It**"):
        st.write("If it's a physical reaction (like spoiled food), your body is telling you to avoid it. Trust that. Remove yourself from the source. Dwelling on it isn't helpful.")
    with st.expander("**Challenge Your Perspective**"):
        st.write("Sometimes we feel disgust due to prejudice or a learned bias. If your disgust is aimed at a person or group, it's a critical time to ask if your reaction is truly justified.")
    st.markdown("---")
    st.markdown("🔗 **Learn More:** [Scientific American on Disgust](https://www.scientificamerican.com/article/the-science-of-disgust/)")


with tab_neutral:
    st.markdown('<div class="accent-bar accent-bar-neutral"></div>', unsafe_allow_html=True)
    st.subheader("The Value of Neutral")
    st.image("https://images.pexels.com/photos/1287145/pexels-photo-1287145.jpeg", 
             caption="Photo by eberhard grossgasteiger", width=400)
    with st.expander("**It's a State of Rest**"):
        st.write("Constant high emotion (even happiness) is exhausting. A neutral state is not 'bad' or 'empty'—it's a restorative state of calm and balance.")
    with st.expander("**It's a Sign of Stability**"):
        st.write("Often, a neutral state means things are stable, you are safe, and you are not under any immediate threat. It's a sign of contentment.")
    with st.expander("**It's Perfect for Focus**"):
        st.write("This is the ideal state for deep work, study, or complex problem-solving. It allows for clear, logical thinking without emotional bias.")
    with st.expander("**Cultivate It with Mindfulness**"):
        st.write("You can intentionally cultivate this state of calm presence through meditation and mindfulness, focusing on your breath and the present moment.")
    st.markdown("---")
    st.markdown("🔗 **Learn More:** [PositivePsychology.com on Emotional Baselines](https://positivepsychology.com/emotional-baseline/)")