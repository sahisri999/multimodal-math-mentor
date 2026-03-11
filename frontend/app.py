import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Multimodal Math Mentor")

st.title("📘 Multimodal Math Mentor")
st.write("Solve JEE-level math problems using text, image, or audio.")

# =========================
# TEXT INPUT
# =========================

st.header("Enter Math Problem")

text_input = st.text_area(
    "Type your math question",
    placeholder="Example: 2*x**2 - 7*x + 3 = 0",
    key="text_input_box"
)

if st.button("Solve Problem", key="text_solve_button"):

    if not text_input.strip():
        st.warning("Please enter a math problem.")
        st.stop()

    problem_text = text_input.strip().replace("\n", " ")

    print("Sending problem:", problem_text)

    response = requests.post(
        f"{API_URL}/agent/solve",
        json={"problem": problem_text}
    )

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    result = response.json()

    st.subheader("Solution")
    st.success(result.get("solution"))

    st.subheader("Verification")
    if result.get("verified"):
        st.success("Solution Verified")
    else:
        st.error("Verification Failed")

    st.subheader("Explanation")
    st.info(result.get("explanation"))

    with st.expander("📚 Retrieved Knowledge Context"):
        st.write(result.get("context"))
    
    st.subheader("Feedback")

    col1, col2 = st.columns(2)

    rating = None

    with col1:
              if st.button("👍 Helpful", key="feedback_up"):
                rating = "positive"

    with col2:
               if st.button("👎 Not Helpful", key="feedback_down"):
                  rating = "negative"


    comment = st.text_area("Optional comment", key="feedback_comment")

    if rating:

               feedback_payload = {
                 "problem": problem_text,
                 "solution": str(result.get("solution")),
                 "rating": rating,
                 "comment": comment
              }

               requests.post(
               f"{API_URL}/feedback",
               json=feedback_payload
                   )

               st.success("Thanks for your feedback!")


# =========================
# IMAGE INPUT
# =========================

st.header("Image Question")

image_mode = st.radio(
    "Choose input method",
    ["Upload Image", "Take Photo"],
    key="image_mode_radio"
)

image_file = None

if image_mode == "Upload Image":

    image_file = st.file_uploader(
        "Upload math question image",
        type=["png", "jpg", "jpeg"],
        key="image_upload"
    )

elif image_mode == "Take Photo":

    image_file = st.camera_input(
        "Take a photo of the math problem",
        key="image_camera"
    )


if image_file is not None:

    st.image(image_file, caption="Input Image", use_container_width=True)

    files = {
        "file": (
            image_file.name,
            image_file.getvalue(),
            image_file.type
        )
    }

    with st.spinner("Extracting text from image..."):

        response = requests.post(
            f"{API_URL}/multimodal/image",
            files=files
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        result = response.json()

    extracted_text = result.get("parsed_problem") or result.get("ocr_text", "")

    st.subheader("OCR Extracted Text")

    image_corrected_text = st.text_area(
        "Edit OCR text if incorrect",
        value=extracted_text,
        height=150,
        key="image_text_edit"
    )

    if st.button("Solve Image Problem", key="image_solve_button"):

        if not image_corrected_text.strip():
            st.warning("No problem detected from image.")
            st.stop()

        problem_text = image_corrected_text.strip().replace("\n", " ")

        response = requests.post(
            f"{API_URL}/agent/solve",
            json={"problem": problem_text}
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        result = response.json()

        st.subheader("Solution")
        st.success(result.get("solution"))

        st.subheader("Verification")
        if result.get("verified"):
            st.success("Solution Verified")
        else:
            st.error("Verification Failed")

        st.subheader("Explanation")
        st.info(result.get("explanation"))

        with st.expander("📚 Retrieved Knowledge Context"):
            st.write(result.get("context"))

        st.subheader("Feedback")

        col1, col2 = st.columns(2)

        rating = None

        with col1:
              if st.button("👍 Helpful", key="feedback_up"):
                rating = "positive"

        with col2:
               if st.button("👎 Not Helpful", key="feedback_down"):
                  rating = "negative"


        comment = st.text_area("Optional comment", key="feedback_comment")

        if rating:

               feedback_payload = {
                 "problem": problem_text,
                 "solution": str(result.get("solution")),
                 "rating": rating,
                 "comment": comment
              }

               requests.post(
               f"{API_URL}/feedback",
               json=feedback_payload
                   )

               st.success("Thanks for your feedback!")


# =========================
# AUDIO INPUT
# =========================

st.header("Record Audio Question")

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "audio_transcription" not in st.session_state:
    st.session_state.audio_transcription = ""

audio = mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=True,
    key="audio_recorder_widget"
)

if audio is not None and "bytes" in audio:
    st.session_state.audio_bytes = audio["bytes"]

if st.session_state.audio_bytes is not None:

    st.audio(st.session_state.audio_bytes, format="audio/wav")

    if st.button("Transcribe Audio", key="audio_transcribe_button"):

        files = {
            "file": (
                "recording.wav",
                st.session_state.audio_bytes,
                "audio/wav"
            )
        }

        response = requests.post(
            f"{API_URL}/multimodal/audio",
            files=files
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        result = response.json()

        st.session_state.audio_transcription = result.get("transcription", "")

    if st.session_state.audio_transcription != "":

        st.subheader("Edit Transcription")

        audio_corrected_text = st.text_area(
            "Correct transcription if needed",
            value=st.session_state.audio_transcription,
            height=120,
            key="audio_text_edit"
        )

        if st.button("Solve Audio Problem", key="audio_solve_button"):

            if not audio_corrected_text.strip():
                st.warning("Please provide a problem.")
                st.stop()

            problem_text = audio_corrected_text.strip().replace("\n", " ")

            response = requests.post(
                f"{API_URL}/agent/solve",
                json={"problem": problem_text}
            )

            if response.status_code != 200:
                st.error(response.text)
                st.stop()

            result = response.json()

            st.subheader("Solution")
            st.success(result.get("solution"))

            st.subheader("Verification")
            if result.get("verified"):
                st.success("Solution Verified")
            else:
                st.error("Verification Failed")

            st.subheader("Explanation")
            st.info(result.get("explanation"))

            with st.expander("📚 Retrieved Knowledge Context"):
                st.write(result.get("context"))

            st.subheader("Feedback")

            col1, col2 = st.columns(2)

            rating = None

            with col1:
              if st.button("👍 Helpful", key="feedback_up"):
                rating = "positive"

            with col2:
               if st.button("👎 Not Helpful", key="feedback_down"):
                  rating = "negative"


            comment = st.text_area("Optional comment", key="feedback_comment")

            if rating:

               feedback_payload = {
                 "problem": problem_text,
                 "solution": str(result.get("solution")),
                 "rating": rating,
                 "comment": comment
              }

               requests.post(
               f"{API_URL}/feedback",
               json=feedback_payload
                   )

               st.success("Thanks for your feedback!")