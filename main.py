import os
import whisper
import streamlit as st
from pydub import AudioSegment
import openai
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

st.set_page_config(
    page_title="Whisplit",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="auto",
)

upload_path = "./data/uploads/"
download_path = "./data/downloads/"
transcript_path = "./data/transcripts/"


def create_directory(directory_path):
    path = Path(directory_path)
    if not path.is_dir():
        path.mkdir(parents=True)


for d in [upload_path, download_path, transcript_path]:
    create_directory(d)


@st.cache_data()
# @st.cache(persist=True, allow_output_mutation=False, show_spinner=True, suppress_st_warning=True)
def to_mp3(audio_file, output_audio_file, upload_path, download_path):
    # get file extension using pathlib
    ext = Path(audio_file.name).suffix.lower()

    # create an audio segment from the given file
    audio_data = AudioSegment.from_file(
        os.path.join(upload_path, audio_file.name), format=ext[1:]
    )

    # export the audio segment to MP3 format
    audio_data.export(
        os.path.join(download_path, output_audio_file), format="mp3"
    )

    return output_audio_file


@st.cache_data()
# @st.cache(persist=True, allow_output_mutation=False, show_spinner=True, suppress_st_warning=True)
def process_audio(filename, model_type):
    model = whisper.load_model(model_type)
    result = model.transcribe(filename)
    return result["text"]


@st.cache_data()
# @st.cache(persist=True, allow_output_mutation=False, show_spinner=True, suppress_st_warning=True)
def save_transcript(transcript_data, txt_file):
    with open(os.path.join(transcript_path, txt_file), "w") as f:
        f.write(transcript_data)


st.title("🔊 OpenAI Whisper 🔊")
st.info('✨ Supports all popular audio formats - WAV, MP3, MP4, OGG, WMA, AAC, FLAC, FLV 😉')
st.markdown("First upload your audio file and then select the model type. \nThen click on the button to transcribe.")
uploaded_file = st.file_uploader("Upload audio file", type=[
                                 "wav", "mp3", "ogg", "wma", "aac", "flac", "mp4", "flv"])

audio_file = None

if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
        f.write((uploaded_file).getbuffer())
    with st.spinner(f"Processing Audio ... 💫"):
        output_audio_file = uploaded_file.name.split('.')[0] + '.mp3'
        output_audio_file = to_mp3(
            uploaded_file, output_audio_file, upload_path, download_path)
        audio_file = open(os.path.join(download_path, output_audio_file), 'rb')
        audio_bytes = audio_file.read()
    print("Opening ", audio_file)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Feel free to play your uploaded audio file 🎼")
        st.audio(audio_bytes)
    with col2:
        whisper_model_type = st.radio(
            "Please choose your model type", ('Tiny', 'Base', 'Small', 'Medium', 'Large'))

    if st.button("Generate Transcript"):
        with st.spinner(f"Generating Transcript... 💫"):
            transcript = process_audio(str(os.path.abspath(os.path.join(
                download_path, output_audio_file))), whisper_model_type.lower())
            # print(transcript)
            if transcript is not None:
                st.header("Transcript:")
                st.markdown(transcript)

            st.success('✅ Successful !!')

    # if st.button("Generate Transcript and Classification"):
    #     with st.spinner(f"Generating Transcript... 💫"):
    #         transcript = process_audio(str(os.path.abspath(os.path.join(
    #             download_path, output_audio_file))), whisper_model_type.lower())
    #         print(transcript)
    #         if transcript is not None:
    #             st.header("Transcript:")
    #             st.text(transcript)

    #             openai.api_key = os.getenv("OPENAI_API_KEY")

    #             response = openai.Completion.create(
    #                 model="text-davinci-002",
    #                 prompt=f"\n\n\n\n {transcript} \n\n",
    #                 temperature=0.7,
    #                 max_tokens=256,
    #                 top_p=1,
    #                 frequency_penalty=0,
    #                 presence_penalty=0
    #             )

    #             st.header("Sentiment analysis:")
    #             st.caption(
    #                 "very negativ, negativ, neutral, positive, very positive")
    #             st.text("Classified as:" + response.choices[0].text)

    #         st.balloons()
    #         st.success('✅ Successful !!')

else:
    st.warning('⚠ Please upload your audio file 😯')
