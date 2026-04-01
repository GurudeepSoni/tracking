import streamlit as st
import cv2
import tempfile

st.set_page_config(page_title="Simple Video Viewer")

st.title("🎥 Video Processing App")

option = st.sidebar.selectbox("Choose Mode", ["Upload Video"])

# ------------------ VIDEO UPLOAD ------------------
if option == "Upload Video":
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

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            FRAME_WINDOW.image(frame, channels="BGR")

        cap.release()
