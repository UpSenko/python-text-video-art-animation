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


import os
import cv2
from PIL import Image
from pytube import YouTube

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

# Define Braille characters
braille_chars = "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿"

# Function to convert a frame to text art
def frame_to_text_art(frame, threshold=128):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply threshold to convert to black and white
    _, bw_frame = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    # Resize the frame for better text representation
    resized_frame = cv2.resize(bw_frame, (bw_frame.shape[1] // 4, bw_frame.shape[0] // 4))
    # Create a PIL image object from the numpy array
    pil_frame = Image.fromarray(resized_frame)
    # Convert the frame to text art using Braille characters
    text_art = ""
    for y in range(pil_frame.height):
        for x in range(pil_frame.width):
            pixel = pil_frame.getpixel((x, y))
            if pixel < 128:
                text_art += braille_chars[pixel // 32]  # Black pixels
            else:
                text_art += "𓇢"  # White pixels (use a solid block character for visibility)
        text_art += "\n"
    return text_art

# Example usage:
video_url = "https://www.youtube.com/watch?v=FtutLA63Cp8"
output_path = "video"
download_youtube_video(video_url, output_path)

video_path = os.path.join(output_path, "video.mp4")
cap = cv2.VideoCapture(video_path)

# Set the width and height of each text art frame
frame_width = 1080 
frame_height = 500   # Adjust height to maintain aspect ratio

print("Playing video:")
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    # Print the text art representation of the frame
    text_art = frame_to_text_art(frame)
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console screen
    print(text_art)

    # Increment frame count
    frame_count += 1
    print(f"Processed frame {frame_count}")

cap.release()
cv2.destroyAllWindows()

# Remove the video file after processing
os.remove(video_path)
