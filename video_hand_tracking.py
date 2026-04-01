import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

st.set_page_config(page_title="Hand Tracking App", layout="wide")

# ==== SIDEBAR NAVIGATION ====
mode = st.sidebar.radio("Select Mode", ["Live Camera", "Video Upload"])

# ==== MEDIAPIPE SETUP ====
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)

# ==== FRAME PROCESSING FUNCTION ====
def process_frame(frame):
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
    return frame

# ==== LIVE CAMERA VIA BROWSER ====
if mode == "Live Camera":
    st.header("Live Hand Tracking (Browser Camera)")
    uploaded_img = st.camera_input("Use your camera to capture video frames")

    if uploaded_img is not None:
        # Convert uploaded camera image to OpenCV format
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_img.read())
        cap = cv2.VideoCapture(tfile.name)
        FRAME_WINDOW = st.image([])
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = process_frame(frame)
            FRAME_WINDOW.image(frame, channels="BGR")
        cap.release()

# ==== VIDEO UPLOAD ====
elif mode == "Video Upload":
    st.header("Upload Video for Hand Tracking")
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)

        FRAME_WINDOW = st.image([])
        progress_bar = st.progress(0)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = process_frame(frame)
            FRAME_WINDOW.image(frame, channels="BGR")
            current_frame += 1
            progress_bar.progress(min(current_frame / frame_count, 1.0))

        cap.release()
        st.success("Video processing complete!")
