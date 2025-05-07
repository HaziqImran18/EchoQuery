# EchoQuery 🎧💬  
**"Turn Your Podcasts, Videos, and YouTube Talks into Intelligent Conversations"**

EchoQuery is an AI-powered app that transforms any audio or video file into a conversational chatbot. Upload MP3s, MP4s, or paste a YouTube link — EchoQuery will transcribe, understand, and let you ask natural language questions about it, just like ChatGPT.

---

## 🌟 Features

- 🎙️ Upload Audio (MP3) or Video (MP4)
- 🔗 Paste YouTube Links (extracts audio automatically)
- ⚡ Chunking + Transcription with OpenAI Whisper
- 🧠 Smart Retrieval using LangChain + FAISS
- 🤖 Answer Generation with Mixtral LLM via Groq API
- 🧩 Clean interface built with Streamlit
- 💬 Chat in real-time about long audios/videos

---

## ⚙️ How It Works (Behind the Scenes)

Here's what happens behind the scenes when you upload a file or paste a YouTube link:

1. **Audio/Video Upload or Link Input**  
   - Upload `.mp3` or `.mp4` or paste a YouTube link.  
   - If YouTube: we use `pytube` to download and extract audio.

2. **Audio Extraction and Chunking**  
   - Long audio files are split into 30-second chunks using `PyDub` or `MoviePy`.

3. **Transcription**  
   - Each chunk is passed through `OpenAI Whisper` to generate accurate transcripts.

4. **Embedding and Vector Store**  
   - Each transcript chunk is converted into an embedding using `LangChain`.
   - These embeddings are stored in a `FAISS` vector store for fast retrieval.

5. **Conversational Q&A**  
   - Your question is embedded and used to fetch the most relevant chunks.
   - Context is passed to `Mixtral` (via Groq API) to generate a smart, concise answer.

---

## 🛠️ Tech Stack

| Component      | Tech/Library            |
|----------------|-------------------------|
| UI Framework   | Streamlit               |
| Transcription  | Whisper (OpenAI)        |
| LLM Backend    | Mixtral via Groq API    |
| Vector DB      | FAISS (LangChain)       |
| YouTube Support| pytube                  |
| Video Audio    | MoviePy                 |
| Audio Chunks   | PyDub                   |
| Env Handling   | python-dotenv           |

---

## 📈 Future Roadmap
 Add support for Urdu, Arabic, Hindi transcripts

 Integrate Text-to-Speech (TTS) for voice replies

 Export Q&A history to PDF or Notion

 Support speaker diarization (who spoke what)

 Add multilingual summaries

 Enable full session memory (for long chats)

## 🎯 Ideal For
📚 Students studying recorded lectures

📈 Business professionals analyzing interviews

🎧 Podcast fans who want key takeaways

🕌 Islamic scholars or learners who want to engage with lectures

🧠 Deep learners and productivity nerds

## 🧠 Developer Info
This project is part of a larger vision by Muhammad Haziq Imran, a deep learning student and MMA aspirant from Pakistan, determined to build global AI tools and practical tech solutions for the Ummah and beyond.

Mentored by Muhammad Irfan Malik
Built using real-world tools and deployment-ready workflows.

---

## 🧱 Folder Structure

```bash
EchoQuery/
│
├── main.py                   # Main Streamlit App
├── youtube_utils.py          # YouTube audio handling
├── video_utils.py            # MP4 video to audio
├── speech_to_text.py         # Transcription logic
├── embeddings.py             # Embedding + Vector store
├── question_answers.py       # LLM query handler
├── uploaded_files/           # Temporary uploads
├── chunks/                   # Audio chunks folder
├── .env                      # Groq & Pinecone API Key
├── requirements.txt          # Dependencies
└── README.md                 # You're reading it!
