import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key = API_KEY)
model = 'whisper-large-v3'

def audio_to_text(filepath):
    with open(filepath, 'rb') as files:
        translation = client.audio.translations.create(
            file = (filepath, files.read()),
            model = 'whisper-large-v3'
        )
    return translation.text