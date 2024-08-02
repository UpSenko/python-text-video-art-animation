import os
import subprocess
import json
import time

# Update pip to the latest version
subprocess.check_call(["pip", "install", "--upgrade", "pip"])

# Install Dependencies
os.system("sudo apt update")
os.system("sudo apt install -y libgl1-mesa-glx")
os.system("pip install opencv-python yt-dlp")

import cv2
import yt_dlp as youtube_dl  # Use yt-dlp for downloading YouTube videos

# Define ASCII characters ordered by intensity
ASCII_CHARS = '@%#*+=-:. '

# Custom ASCII characters with varying intensities
CUSTOM_ASCII_CHARS = ' .,:;irsXA253hMHGS#9B&@'



# Function to convert requirements.txt to package.json
def convert_requirements_to_package_json(requirements_file, output_file='package.json'):
    dependencies = {}
    with open(requirements_file, 'r') as f:
        for line in f:
            package, version = line.strip().split('==')
            dependencies[package] = version

    package_json = {
        "name": "python_project",
        "version": "1.0.0",
        "description": "Python project dependencies converted to package.json",
        "main": "index.js",
        "dependencies": dependencies,
        "author": "Your Name",
        "license": "MIT"
    }

    with open(output_file, 'w') as f:
        json.dump(package_json, f, indent=4)

# Function to download a YouTube video using yt-dlp
def download_youtube_video(url, output_path):
    print("Downloading video...")
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, 'video.mp4'),
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Video downloaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to convert a frame to ASCII art
def frame_to_ascii(frame, width, height):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the frame
    resized_frame = cv2.resize(gray_frame, (width, height))

    # Convert the resized frame to ASCII art
    ascii_art = ''
    for row in resized_frame:
        for pixel in row:
            # Map pixel intensity to ASCII character
            ascii_art += CUSTOM_ASCII_CHARS[pixel // 16]
        ascii_art += '\n'

    return ascii_art

# Function to clear the console
def clear_console():
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

# Function to process video frames and display ASCII art
def process_video_frames(cap, display_width, display_height):
    # Get the original video frame rate
    original_fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        # Convert frame to ASCII art
        ascii_art = frame_to_ascii(frame, display_width, display_height)

        # Clear console and display ASCII art
        clear_console()
        print(ascii_art, end='', flush=True)

        # Calculate the time elapsed since the start of processing
        elapsed_time = time.time() - start_time

        # Calculate delay to maintain the original frame rate
        delay = 1 / original_fps - elapsed_time
        if delay > 0:
            time.sleep(delay)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    requirements_file = 'requirements.txt'
    convert_requirements_to_package_json(requirements_file)

    video_url = "https://youtu.be/AjFijrXaxkg"
    output_path = "video"

    # Download YouTube video
    download_youtube_video(video_url, output_path)

    video_path = os.path.join(output_path, "video.mp4")
    cap = cv2.VideoCapture(video_path)

    # Set display width and height (adjust as needed)
    display_width = 200
    display_height = 60

    print("Playing video:")

    # Process video frames and display ASCII art
    process_video_frames(cap, display_width, display_height)

    # Remove the video file after processing
    os.remove(video_path)
