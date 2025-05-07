from moviepy.editor import VideoFileClip
import os

def extract_audio_from_video(video_path, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load the video file
    video_clip = VideoFileClip(video_path)

    # Extract audio
    audio_path = os.path.join(output_folder, f"{os.path.basename(video_path).split('.')[0]}.mp3")
    video_clip.audio.write_audiofile(audio_path, codec='mp3')

    # Close the video clip
    video_clip.close()

    return audio_path
