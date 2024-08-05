import streamlit as st
import yt_dlp

# Define a global variable for the progress bar
progress_bar = None


def update_progress_bar(percent):
    global progress_bar
    if progress_bar:
        progress_bar.progress(percent)


# Define the download function with progress update
def download_video(url):
    output_path = "C:/Users/New pc/Desktop"  # Define the output directory

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            update_progress_bar(int(percent))
        elif d['status'] == 'finished':
            update_progress_bar(100)

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
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
            download_video(url)
            st.success("Video downloaded successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            progress_bar = None
    else:
        st.error("Please enter a YouTube URL.")