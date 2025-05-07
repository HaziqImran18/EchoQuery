from pytube import YouTube
import os

def download_youtube_audio(url, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

        if not audio_stream:
            raise Exception("No audio stream found for this video.")

        filename = f"{yt.title}.mp4".replace(" ", "_").replace("|", "_")
        audio_path = os.path.join(output_folder, filename)
        audio_stream.download(output_path=output_folder, filename=filename)
        return audio_path

    except Exception as e:
        print(f"Failed to download audio: {e}")
        return None
