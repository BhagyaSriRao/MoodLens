import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from utils import load_detection_model, load_face_detector, process_frame

st.set_page_config(page_title="Live Webcam", page_icon="📸", layout="wide")

# --- Model Loading ---
# Load models once at the start using st.cache_resource to avoid reloading on every run
@st.cache_resource
def get_models():
    """Loads and caches the models."""
    model = None
    face_detector = None
    try:
        model = load_detection_model()
        face_detector = load_face_detector()
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None
    
    if model is None or face_detector is None:
        st.error("Model or face detector failed to load. Please check the files and logs.")
        return None, None
        
    return model, face_detector

model, face_detector = get_models()

# --- WebRTC Video Transformer ---
class EmotionTransformer(VideoTransformerBase):
    """
    A video transformer class that applies emotion detection to each frame.
    It inherits from VideoTransformerBase from streamlit-webrtc.
    """
    def __init__(self, model, face_detector):
        self.model = model
        self.face_detector = face_detector

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        """
        This method is called for each frame received from the webcam.
        """
        if self.model is None or self.face_detector is None:
            # If models didn't load, just return the original frame
            return frame

        try:
            # Convert the av.VideoFrame to a numpy array (BGR format)
            img = frame.to_ndarray(format="bgr24")

            # Process the frame using your existing utility function
            processed_img = process_frame(img, self.model, self.face_detector)

            # Convert the processed numpy array back to an av.VideoFrame
            return av.VideoFrame.from_ndarray(processed_img, format="bgr24")
        except Exception as e:
            # Using print for server-side logging, st.error() might clutter the UI
            print(f"Error processing frame: {e}")
            # In case of error, return the original, unprocessed frame
            return frame

# --- Streamlit App ---
if model and face_detector:
    # Check if models loaded successfully
    # st.write("Models loaded successfully. Ready to start webcam.")
    
    # Instantiate and run the WebRTC streamer
    webrtc_streamer(
        key="emotion-detection",
        # We pass a factory function that creates our transformer
        video_transformer_factory=lambda: EmotionTransformer(model=model, face_detector=face_detector),
        media_stream_constraints={"video": True, "audio": False}, # Request video, no audio
        async_processing=True, # Process frames asynchronously
    )
else:
    st.error("Cannot start webcam stream because models failed to load.")

# st.markdown("""
# <hr>
# <h3>How this works:</h3>
# <ol>
#     <li>We use <strong>streamlit-webrtc</strong> to get a live video stream from your camera.</li>
#     <li>A <code>VideoTransformer</code> class (<code>EmotionTransformer</code>) is defined to process video.</li>
#     <li>For every frame in the video, its <code>recv</code> method is called.</li>
#     <li>Inside <code>recv</code>, we convert the frame to a NumPy array, run your <code>process_frame</code> function, and send the processed frame back.</li>
#     <li>This processed video stream is sent back to you in real-time.</li>
# </ol>
# <p>Remember to install: <code>pip install streamlit-webrtc av</code></p>
# """, unsafe_allow_html=True)