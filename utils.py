import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Lazy imports for heavy dependencies
def _get_tensorflow():
    try:
        from tensorflow.keras.models import load_model
        from tensorflow.keras.applications.resnet50 import preprocess_input
        return load_model, preprocess_input
    except ImportError:
        return None, None

# --- IMPORTANT ---
# You MUST update these to match your model
# 1. The emotion labels in the EXACT order your model was trained on
EMOTION_LABELS = {
    0: "Angry",
    1: "Disgust",
    2: "Fear",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprise"
}
# 2. The input size your model expects (ResNet50: 224x224 RGB)
MODEL_INPUT_SIZE = (224, 224)
# ---

# Cache the model loading
@st.cache_resource
def load_detection_model(model_path="resnet50_fer2013_model.keras"):
    """Loads the pre-trained Keras emotion detection model."""
    try:
        load_model, preprocess_input = _get_tensorflow()
        if load_model is None:
            st.error("TensorFlow not available")
            return None
        return load_model(
            model_path,
            custom_objects={"preprocess_input": preprocess_input},
            compile=False,
        )
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Cache the face detector
@st.cache_resource
def load_face_detector(cascade_path="haarcascade_frontalface_default.xml"):
    """Loads the OpenCV Haar Cascade for face detection."""
    try:
        return cv2.CascadeClassifier(cascade_path)
    except Exception as e:
        st.error(f"Error loading Haar Cascade: {e}. Make sure 'haarcascade_frontalface_default.xml' is in the root folder.")
        return None

def process_frame(frame, model, face_detector, return_emotions: bool = False):
    """Processes a single frame (image) to detect faces and predict emotions.

    If return_emotions is False (default), returns just the processed frame.
    If True, returns (processed_frame, [list of predicted emotion labels]).
    """
    if model is None or face_detector is None:
        return (frame, []) if return_emotions else frame

    emotions = []

    # Convert to grayscale for face detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest) from the original color frame
        roi_color = frame[y:y + h, x:x + w]

        # Resize ROI to the model's expected input size (224x224)
        roi_color = cv2.resize(roi_color, MODEL_INPUT_SIZE, interpolation=cv2.INTER_AREA)

        if np.sum(roi_color) != 0:
            # Convert BGR (OpenCV) to RGB (Keras/ResNet expected)
            roi_rgb = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)

            # Convert to float32 and apply ResNet50 preprocess_input
            roi_rgb = roi_rgb.astype("float32")
            roi_rgb = np.expand_dims(roi_rgb, axis=0)  # Add batch dimension -> (1, 224, 224, 3)
            _, preprocess_input = _get_tensorflow()
            if preprocess_input:
                roi_rgb = preprocess_input(roi_rgb)

            # Make prediction
            prediction = model.predict(roi_rgb, verbose=0)[0]
            label = EMOTION_LABELS[prediction.argmax()]
            emotions.append(label)
            label_position = (x, y - 10)
            
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Draw the emotion label
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'No Face Found', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
    return (frame, emotions) if return_emotions else frame

def read_image_from_buffer(buffer):
    """Converts a file buffer (from st.file_uploader) into a cv2 image."""
    bytes_data = buffer.getvalue()
    cv_image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    return cv_image