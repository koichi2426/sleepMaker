import os
from moviepy.editor import *

def create_video(image_path, audio_path, output_path, duration_minutes):
    # Convert duration from minutes to seconds
    duration = duration_minutes * 60

    # Load the image and audio files
    image_clip = ImageClip(image_path).set_duration(duration)
    audio_clip = AudioFileClip(audio_path)

    # Calculate the number of loops required for the audio
    audio_duration = audio_clip.duration
    loops = int(duration / audio_duration) + 1

    # Loop the audio to match the duration of the video
    audio_clip = concatenate_audioclips([audio_clip] * loops).subclip(0, duration)

    # Set the audio to the image clip
    video_clip = image_clip.set_audio(audio_clip)

    # Write the result to an mp4 file
    video_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

# Define the paths and duration
image_folder = 'image_folder'
audio_folder = 'audio_folder'
output_folder = 'output_folder'
duration_minutes = 1  # duration in minutes

# Get the image and audio files (assuming there's only one of each in the folder)
image_files = [f for f in os.listdir(image_folder) if f.endswith('.webp')]
audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3') or f.endswith('.wav')]

if image_files and audio_files:
    image_path = os.path.join(image_folder, image_files[0])
    audio_path = os.path.join(audio_folder, audio_files[0])
    output_path = os.path.join(output_folder, 'output_video.mp4')

    # Create the video
    create_video(image_path, audio_path, output_path, duration_minutes)
else:
    print("No image or audio files found in the specified folders.")
