import streamlit as st
import yt_dlp
import os

# Define a global variable for the progress bar
progress_bar = None

def get_download_folder():
    if os.name == 'nt':  # Windows
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:  # macOS and Linux
        return os.path.join(os.environ['HOME'], 'Downloads')

def update_progress_bar(percent):
    global progress_bar
    if progress_bar:
        progress_bar.progress(percent)

# Define the download function with progress update
def download_video(url, download_folder):
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            update_progress_bar(int(percent))
        elif d['status'] == 'finished':
            update_progress_bar(100)

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
        "progress_hooks": [progress_hook]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Streamlit app layout
st.title("YouTube Video Downloader")

# User input
url = st.text_input("Enter YouTube video URL:")

if st.button("Download"):
    if url:
        progress_bar = st.progress(0)  # Initialize progress bar
        try:
            download_folder = get_download_folder()
            download_video(url, download_folder)
            st.success("Video downloaded successfully!")
            st.write(f"Video saved to: {download_folder}")

            # Provide a download link
            downloaded_files = [f for f in os.listdir(download_folder) if os.path.isfile(os.path.join(download_folder, f))]
            latest_file = max([os.path.join(download_folder, f) for f in downloaded_files], key=os.path.getctime)
            st.markdown(f"[Download {os.path.basename(latest_file)}](file://{latest_file})")

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            progress_bar = None
    else:
        st.error("Please enter a YouTube URL.")
