import json

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

if __name__ == "__main__":
    requirements_file = 'requirements.txt'
    convert_requirements_to_package_json(requirements_file)


import cv2
import subprocess
import os
from pytube import YouTube
import time

# Define ASCII characters ordered by intensity
ASCII_CHARS = '@%#*+=-:. '

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

# Function to convert a frame to ASCII art
def frame_to_ascii(frame, width, height):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get binary image
    _, binary_frame = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours are found, zoom out to the entire frame
    if not contours:
        resized_frame = cv2.resize(gray_frame, (width, height))
    else:
        # Find bounding box of the largest contour (e.g., person)
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))

        # Expand the bounding box to include some blank space around the object
        padding = 10
        x -= padding
        y -= padding
        w += 2 * padding
        h += 2 * padding

        # Ensure the bounding box does not exceed frame boundaries
        x = max(0, x)
        y = max(0, y)
        w = min(gray_frame.shape[1] - 1, x + w) - x
        h = min(gray_frame.shape[0] - 1, y + h) - y

        # Crop the frame to the bounding box
        cropped_frame = gray_frame[y:y+h, x:x+w]

        # Resize the cropped frame to match desired width and height
        resized_frame = cv2.resize(cropped_frame, (width, height))

    # Convert resized frame to ASCII art
    ascii_art = ''
    for row in resized_frame:
        for pixel in row:
            ascii_art += ASCII_CHARS[pixel // 32]
        ascii_art += '\n'
    return ascii_art

def clear_console():
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)  # Clear the console screen

def process_video_frames(cap, display_width, display_height):
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        # Convert frame to ASCII art
        ascii_art = frame_to_ascii(frame, display_width, display_height)

        # Clear console and print ASCII art
        clear_console()
        print(ascii_art, end='', flush=True)

        # Introduce a small delay to control the frame rate
        time.sleep(0.1)

        # Increment frame count
        frame_count += 1

    # Print the processed frame count
    print(f"Processed frame {frame_count}")
    
    cap.release()
    cv2.destroyAllWindows()

# Example usage:
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=FtutLA63Cp8"
    output_path = "video"
    download_youtube_video(video_url, output_path)

    video_path = os.path.join(output_path, "video.mp4")
    cap = cv2.VideoCapture(video_path)

    # Set display width and height (adjust as needed)
    display_width = 100
    display_height = 30

    print("Playing video:")

    # Process frames
    process_video_frames(cap, display_width, display_height)

    # Remove the video file after processing
    os.remove(video_path)
