import os
import streamlit as st
from moviepy.editor import AudioFileClip
from dotenv import load_dotenv
from groq import Groq
from speech_to_text import audio_to_text
from embeddings import store_embeddings
from question_answers import query_vector_database, transcript_chat_completion
from langchain.docstore.document import Document
from video_utils import extract_audio_from_video
from youtube_utils import download_youtube_audio

# Load API key
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.error("API key not found. Please set GROQ_API_KEY in your .env file.")
    st.stop()

client = Groq(api_key=API_KEY)

# Folder setup
mp3_file_folder = "uploaded_files"
mp3_chunk_folder = "chunks"
os.makedirs(mp3_file_folder, exist_ok=True)
os.makedirs(mp3_chunk_folder, exist_ok=True)

# Streamlit Config
st.set_page_config(page_title="Podcast Q&A", layout="centered")
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 700px;
            margin: auto;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .stTextInput, .stFileUploader, .stTextArea, .stButton, .stRadio {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>input, .stFileUploader>div>input {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 0.5rem;
        }
        h1, h2, h3, h4 {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎙️ Podcast & Video Q&A App")

# Session state init
if "transcriptions" not in st.session_state:
    st.session_state.transcriptions = []
if "docsearch" not in st.session_state:
    st.session_state.docsearch = None

filepath = None

# --- Sidebar ---
with st.sidebar:
    st.header("Upload Options")
    uploaded_type = st.radio("Select Upload Type", ["Audio (MP3)", "Video (MP4)"])
    uploaded_file = st.file_uploader("Upload File", type=["mp3", "mp4"], key="uploader")
    yt_link = st.text_input("📺 Or paste a YouTube video link")

# --- Handle File Upload ---
if uploaded_file is not None:
    # Reset on new upload
    st.session_state.transcriptions = []
    st.session_state.docsearch = None

    filepath = os.path.join(mp3_file_folder, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Convert if it's a video
    if uploaded_type == "Video (MP4)":
        filepath = extract_audio_from_video(filepath, mp3_file_folder)

# --- Handle YouTube Link ---
if yt_link:
    try:
        # Reset on new link
        st.session_state.transcriptions = []
        st.session_state.docsearch = None

        st.info("Downloading YouTube audio...")
        filepath = download_youtube_audio(yt_link, mp3_file_folder)
        st.success("YouTube audio downloaded successfully!")
    except Exception as e:
        st.error(f"Failed to download audio: {e}")
        st.stop()

# --- Transcription and Embedding ---
if filepath:
    st.info("⏳ Processing audio and generating transcript...")
    audio = AudioFileClip(filepath)
    chunk_length = 60  # seconds

    st.write(f"Audio duration: {audio.duration} seconds")

    for start in range(0, int(audio.duration), chunk_length):
        end = min(start + chunk_length, int(audio.duration))
        st.write(f"Processing chunk from {start} to {end} seconds")
        audio_chunk = audio.subclip(start, end)
        chunk_filename = os.path.join(mp3_chunk_folder, f"chunk_{start}.mp3")
        audio_chunk.write_audiofile(chunk_filename, verbose=False, logger=None)

        transcription = audio_to_text(chunk_filename)
        st.session_state.transcriptions.append(transcription)

    combined_transcript = " ".join(st.session_state.transcriptions)
    st.success("✅ Transcription completed.")
    st.write(f"**Preview:** {combined_transcript[:400]}...")

    # Store embeddings
    documents = [Document(page_content=combined_transcript)]
    st.session_state.docsearch = store_embeddings(documents)
    st.success("✅ LLM is ready! You can now ask questions about this content.")

# --- Ask a Question ---
st.markdown("---")
user_question = st.text_input("❓ Ask a question about the content")

if user_question and st.session_state.docsearch:
    relevant_transcripts = query_vector_database(st.session_state.docsearch, user_question)
    response = transcript_chat_completion(client, relevant_transcripts, user_question)
    st.markdown("### 🧠 Answer")
    st.success(response)
