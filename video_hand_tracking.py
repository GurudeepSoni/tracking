import streamlit as st
import cv2
import mediapipe as mp
import tempfile

# Page config
st.set_page_config(page_title="Hand Tracking App")

st.title("✋ Hand Tracking App")

# Sidebar menu
option = st.sidebar.selectbox("Choose Mode", ["Live Camera", "Upload Video"])


# Hand tracking function
def process_frame(frame, hands, mp_draw, mp_hands):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    return frame


# ------------------ LIVE CAMERA ------------------
if option == "Live Camera":
    st.subheader("📷 Live Camera")

    st.warning("⚠️ Live camera works only on local machine, not on Streamlit Cloud")

    run = st.checkbox("Start Camera")
    FRAME_WINDOW = st.image([])

    if run:
        cap = cv2.VideoCapture(0)

        # ✅ Load mediapipe ONLY when needed
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils

        with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:

            while run:
                ret, frame = cap.read()
                if not ret:
                    st.warning("Camera not working")
                    break

                frame = process_frame(frame, hands, mp_draw, mp_hands)
                FRAME_WINDOW.image(frame, channels="BGR")

        cap.release()


# ------------------ VIDEO UPLOAD ------------------
elif option == "Upload Video":
    st.subheader("📁 Upload Video")

    uploaded_file = st.file_uploader(
        "Upload a video",
        type=["mp4", "mov", "avi"]
    )

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        cap = cv2.VideoCapture(tfile.name)
        FRAME_WINDOW = st.image([])

        # ✅ Load mediapipe ONLY when needed
        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils

        with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = process_frame(frame, hands, mp_draw, mp_hands)
                FRAME_WINDOW.image(frame, channels="BGR")

        cap.release()
