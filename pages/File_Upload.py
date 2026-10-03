'''import streamlit as st
import cv2
import tempfile
import time
from utils import load_detection_model, load_face_detector, process_frame, read_image_from_buffer

st.set_page_config(page_title="File Upload", page_icon="📁", layout="wide")
st.title("Emotion Detection from File (Image/Video)")
st.write("Upload an image or video file to detect emotions.")

# Load models from utils.py
model = load_detection_model()
face_detector = load_face_detector()

uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'jpeg', 'png', 'mp4', 'avi'])

if uploaded_file is not None:
    # Check if models loaded successfully
    if model is None or face_detector is None:
        st.error("Model or face detector failed to load. Please check the files and logs.")
    else:
        file_type = uploaded_file.type
        
        # --- IMAGE PROCESSING ---
        if 'image' in file_type:
            st.write("Processing image...")
            
            # Read image from buffer
            image = read_image_from_buffer(uploaded_file)
            
            # Process the frame
            processed_image = process_frame(image, model, face_detector)
            
            # Display the processed image (convert BGR to RGB for Streamlit)
            st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), caption="Processed Image", use_column_width=True)
            
        # --- VIDEO PROCESSING ---
        elif 'video' in file_type:
            st.write("Processing video... This may take a moment.")
            
            # Save video to a temporary file
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            
            # Open the video file with OpenCV
            vf = cv2.VideoCapture(tfile.name)
            
            # Create a placeholder to display the video frames
            st_frame = st.empty()
            
            while vf.isOpened():
                ret, frame = vf.read()
                if not ret:
                    break
                
                # Process the frame
                processed_frame = process_frame(frame, model, face_detector)
                
                # Display the processed frame (convert BGR to RGB)
                st_frame.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), caption="Processed Video", use_column_width=True)
            
            vf.release()
            st.success("Video processing complete.")
            '''

import collections
import streamlit as st
import cv2
import tempfile
from utils import load_detection_model, load_face_detector, process_frame, read_image_from_buffer
from auth_db import log_emotion

st.set_page_config(page_title="File Upload", page_icon="📁", layout="wide")
st.markdown("[< Back to Home](/)") # Add a link back to the Home page
st.title("Emotion Detection from File (Image/Video)")
st.write("Upload an image or video file to detect emotions.")

# Require login
if "user" not in st.session_state or st.session_state.user is None:
    st.error("Please log in from the Home page before using File Upload.")
    st.stop()

user_info = st.session_state.user

# Load models only when needed
@st.cache_resource
def get_models():
    return load_detection_model(), load_face_detector()

uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'jpeg', 'png', 'mp4', 'avi'])

if uploaded_file is not None:
    model, face_detector = get_models()
    if model is None or face_detector is None:
        st.error("Model or face detector failed to load. Please check the files and logs.")
    else:
        file_type = uploaded_file.type
        dominant_emotion = None
        
        if 'image' in file_type:
            st.write("Processing image...")
            image = read_image_from_buffer(uploaded_file)
            processed_image, emotions = process_frame(image, model, face_detector, return_emotions=True)
            st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), caption="Processed Image", use_column_width=True)
            if emotions:
                dominant_emotion = collections.Counter(emotions).most_common(1)[0][0]
            
        elif 'video' in file_type:
            st.write("Processing video... This may take a moment.")
            
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            
            vf = cv2.VideoCapture(tfile.name)
            st_frame = st.empty()
            all_emotions = []
            
            while vf.isOpened():
                ret, frame = vf.read()
                if not ret:
                    break
                
                processed_frame, emotions = process_frame(frame, model, face_detector, return_emotions=True)
                if emotions:
                    all_emotions.extend(emotions)
                st_frame.image(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB), caption="Processed Video", use_column_width=True)
            
            vf.release()
            st.success("Video processing complete.")

            if all_emotions:
                dominant_emotion = collections.Counter(all_emotions).most_common(1)[0][0]

        # Log to SQLite if we have at least attempted processing
        if dominant_emotion is not None:
            try:
                log_emotion(
                    user_id=user_info["id"],
                    session_id=user_info.get("session_id"),
                    source_type="file",
                    source_text=None,
                    file_name=uploaded_file.name,
                    predicted_emotion=dominant_emotion,
                    extra=None,
                )
            except Exception:
                pass
