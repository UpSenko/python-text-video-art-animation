import os
import subprocess
import json
import time
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import cv2
import yt_dlp as youtube_dl

# Define ASCII characters ordered by intensity
ASCII_CHARS = '@%#*+=-:. '
CUSTOM_ASCII_CHARS = ' .,:;irsXA253hMHGS#9B&@'

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for development

# Function to check if FFmpeg is installed
def check_ffmpeg():
    try:
        subprocess.check_call(["ffprobe", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("FFmpeg is already installed.")
    except FileNotFoundError:
        print("FFmpeg is not installed. Installing...")
        install_ffmpeg()

# Function to install FFmpeg
def install_ffmpeg():
    try:
        if os.name == 'posix':
            if os.path.isfile('/etc/debian_version'):
                subprocess.check_call(["sudo", "apt", "update"])
                subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            else:
                print("Unsupported Unix-based system for automatic installation.")
        elif os.name == 'nt':
            print("Please install FFmpeg manually from https://ffmpeg.org/download.html")
            exit(1)
        else:
            print("Unsupported operating system for automatic installation.")
            exit(1)
    except Exception as e:
        print(f"Failed to install FFmpeg: {e}")
        exit(1)

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

# Function to extract audio from video and save it
def extract_audio_from_video(video_path):
    print("Extracting audio...")
    audio_path = video_path.replace('.mp4', '.wav')
    try:
        subprocess.check_call(['ffmpeg', '-i', video_path, audio_path])
        print("Audio extraction complete.")
        return audio_path
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")
        return None

# Function to convert a frame to ASCII art
def frame_to_ascii(frame, width, height):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (width, height))
    ascii_art = ''
    for row in resized_frame:
        for pixel in row:
            ascii_art += CUSTOM_ASCII_CHARS[pixel // 16]
        ascii_art += '\n'
    return ascii_art

# Function to process video frames and send ASCII art to the client
def process_video_frames(cap, display_width, display_height):
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break
        ascii_art = frame_to_ascii(frame, display_width, display_height)
        socketio.emit('update_frame', {'ascii_art': ascii_art})
        elapsed_time = time.time() - start_time
        delay = 1 / original_fps - elapsed_time
        if delay > 0:
            time.sleep(delay)
    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory('audio', filename)

def play_audio(audio_path):
    from pydub import AudioSegment
    from pydub.playback import play
    audio = AudioSegment.from_wav(audio_path)
    play(audio)

if __name__ == "__main__":
    check_ffmpeg()
    requirements_file = 'requirements.txt'
    convert_requirements_to_package_json(requirements_file)

    video_url = "https://youtu.be/AjFijrXaxkg"
    output_path = "video"
    download_youtube_video(video_url, output_path)
    video_path = os.path.join(output_path, "video.mp4")
    audio_path = extract_audio_from_video(video_path)

    if audio_path:
        socketio.start_background_task(lambda: play_audio(audio_path))

    cap = cv2.VideoCapture(video_path)
    display_width = 200
    display_height = 60
    socketio.start_background_task(process_video_frames, cap, display_width, display_height)

    # Run the app with HTTPS on port 8443
    context = ('cert.pem', 'key.pem')  # Path to the SSL certificate and key files
    port = 8443  # Change to a port number above 1024
    socketio.run(app, debug=True, ssl_context=context, port=port)
