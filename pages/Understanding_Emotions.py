import streamlit as st

st.set_page_config(page_title="Understanding Your Emotions", page_icon="🧭", layout="wide")
st.markdown("[< Back to Home](/)")

st.title("Understanding Your Emotions")
st.markdown("Detecting an emotion is the first step. Here are quick, practical ways to respond to each state.")

st.warning(
    """
This information is educational and not medical advice. If you’re struggling, please seek professional help.
""",
    icon="⚠️",
)

emotions_list = [
    "Anger",
    "Sadness / Depression",
    "Fear / Anxiety",
    "Happiness",
    "Surprise",
    "Disgust",
    "Neutral",
]

(
    tab_anger,
    tab_sad,
    tab_fear,
    tab_happy,
    tab_surprise,
    tab_disgust,
    tab_neutral,
) = st.tabs(emotions_list)

with tab_anger:
    st.subheader("Managing Anger")
    with st.expander("Take a pause and breathe"):
        st.markdown(
            "Count to 10, take slow deep breaths (inhale 4s, exhale 6s), or walk away briefly before reacting."
        )
    with st.expander("Identify triggers"):
        st.markdown(
            "Note people/situations that spark anger so you can plan calmer responses next time."
        )
    with st.expander("Use ‘I’ statements"):
        st.markdown(
            "Say ‘I feel… when…’ to reduce blame and keep conversations constructive."
        )
    with st.expander("Move your body"):
        st.markdown(
            "Channel energy into a brisk walk or workout to reduce physiological arousal."
        )

with tab_sad:
    st.subheader("Coping with Sadness / Depression")
    with st.expander("Acknowledge your feelings"):
        st.markdown(
            "It’s okay to feel low. Allow space without judgment; gentle routines help."
        )
    with st.expander("Connect with others"):
        st.markdown(
            "Reach out to a friend/family member; social support reduces isolation."
        )
    with st.expander("Small wins"):
        st.markdown(
            "Break tasks into tiny steps and celebrate completion to rebuild momentum."
        )
    with st.expander("Professional help"):
        st.markdown(
            "If low mood persists or worsens, talk to a mental health professional."
        )

with tab_fear:
    st.subheader("Handling Fear / Anxiety")
    with st.expander("Grounding (5–4–3–2–1)"):
        st.markdown(
            "Name 5 things you see, 4 touch, 3 hear, 2 smell, 1 taste to return to the present."
        )
    with st.expander("Challenge thoughts"):
        st.markdown(
            "Ask: What’s the evidence? What’s the realistic worst case? What can I do now?"
        )
    with st.expander("Breathing"):
        st.markdown(
            "Inhale 4s, hold 4s, exhale 6–8s to activate the relaxation response."
        )
    with st.expander("Limit stimulants & doomscrolling"):
        st.markdown("Reduce caffeine and news intake when anxiety spikes.")

with tab_happy:
    st.subheader("Cultivating Happiness")
    with st.expander("Gratitude"):
        st.markdown(
            "List 3 things you’re grateful for daily; focus shifts increase positive affect."
        )
    with st.expander("Savoring"):
        st.markdown(
            "Slow down and fully enjoy pleasant moments; describe details to yourself."
        )
    with st.expander("Acts of kindness"):
        st.markdown("Help someone—small prosocial acts reliably boost wellbeing.")
    with st.expander("Flow activities"):
        st.markdown("Spend time on absorbing hobbies that match your skill level.")

with tab_surprise:
    st.subheader("Working with Surprise")
    with st.expander("Pause to process"):
        st.markdown("Give yourself a beat before judging or reacting; then gather info.")
    with st.expander("Stay curious"):
        st.markdown("Ask open questions: What changed? What can I learn here?")
    with st.expander("Reframe"):
        st.markdown("Look for opportunity or a next-best step in unexpected situations.")

with tab_disgust:
    st.subheader("Understanding Disgust")
    with st.expander("Identify the source"):
        st.markdown(
            "Is it physical (smell/taste) or moral (behavior)? Adjust response accordingly."
        )
    with st.expander("Boundaries"):
        st.markdown(
            "Set clear limits around situations or behaviors that violate your values."
        )
    with st.expander("Don’t dwell"):
        st.markdown("Remove the trigger if possible and redirect attention.")

with tab_neutral:
    st.subheader("Using Neutral as a Resource")
    with st.expander("Rest and reset"):
        st.markdown(
            "Neutral is a stable baseline; use it for recovery between highs and lows."
        )
    with st.expander("Deep work"):
        st.markdown("Capitalize on calm focus for study or problem‑solving.")
    with st.expander("Cultivate with mindfulness"):
        st.markdown(
            "Simple breath awareness can sustain a balanced, neutral state."
        )
