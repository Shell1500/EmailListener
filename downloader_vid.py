import youtube_dl
import sys
    
def download_link(final_link):
    save_location=r'D:\Path\to\your\save\location' ## path

    # setting properties for yt-dl module
    ydl_opts = {
        'format': 'best',
        # output location
        'outtmpl': save_location + '/%(title)s.%(ext)s',
        
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([final_link])