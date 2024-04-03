import json
import os
import cv2
import subprocess
from pytube import YouTube
import time

# Define ASCII characters ordered by intensity
ASCII_CHARS = '@%#*+=-:. '

# Custom ASCII characters with varying intensities
CUSTOM_ASCII_CHARS = ' .,:;irsXA253hMHGS#9B&@'

# Function to download requirements file
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

# Function to download a YouTube video
def download_youtube_video(url, output_path):
    print("Downloading video...")
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Download the video to the output directory
    stream.download(output_path, filename="video.mp4")
    print("Video downloaded successfully.")

# Function to convert a frame to smoothed ASCII art
def frame_to_ascii(frame, width, height):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the frame to match desired width and height
    resized_frame = cv2.resize(gray_frame, (width, height))

    # Define ASCII art
    ascii_art = ''
    for row in resized_frame:
        for pixel in row:
            # Map pixel intensity to custom ASCII character
            ascii_art += CUSTOM_ASCII_CHARS[pixel // 16]
        ascii_art += '\n'

    return ascii_art

def clear_console():
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)  # Clear the console screen

def process_video_frames(cap, display_width, display_height, target_fps=60):
    while cap.isOpened():
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        # Convert frame to ASCII art
        ascii_art = frame_to_ascii(frame, display_width, display_height)

        # Clear console and print ASCII art
        clear_console()
        print(ascii_art, end='', flush=True)

        # Calculate the time required to process the frame
        elapsed_time = time.time() - start_time

        # Calculate the delay to achieve the target frame rate
        target_delay = 1 / target_fps

        # If processing time is less than the target delay, adjust the delay
        if elapsed_time < target_delay:
            remaining_delay = target_delay - elapsed_time
            time.sleep(remaining_delay)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    requirements_file = 'requirements.txt'
    convert_requirements_to_package_json(requirements_file)

    os.system("sudo apt update")
    os.system("sudo apt install -y libgl1-mesa-glx")
    os.system("pip install opencv-python pytube")
    os.system("pip install --upgrade pytube")

    video_url = "https://www.youtube.com/watch?v=FtutLA63Cp8"
    output_path = "video"

    # Download YouTube video
    download_youtube_video(video_url, output_path)

    video_path = os.path.join(output_path, "video.mp4")
    cap = cv2.VideoCapture(video_path)

    # Set display width and height (adjust as needed)
    display_width = 200
    display_height = 60

    print("Playing video:")

    # Process frames
    process_video_frames(cap, display_width, display_height)

    # Remove the video file after processing
    os.remove(video_path)
