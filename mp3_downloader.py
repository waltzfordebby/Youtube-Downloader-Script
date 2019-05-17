import youtube_dl
import os
import traceback
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("mp3-youtube-dl.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Create Directory
savedir = "mixtape"
if not os.path.exists(savedir):
    os.makedirs(savedir)


def make_savepath(title, savedir=savedir):
    return os.path.join(savedir, f"{title}.mp3")


# Create Youtube Downloader
options = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "outtmpl": "%(id)s",
    "noplaylist": True,
}

ydl = youtube_dl.YoutubeDL(options)

url_list = [
    "https://www.youtube.com/watch?v=YlxfoMuRlA8",
    "https://www.youtube.com/watch?v=qyk1qp3ALAg",
    "https://www.youtube.com/watch?v=j7N  AeQJuHh0",
    "https://www.youtube.com/watch?v=FgzY01UQEzk",
    "https://www.youtube.com/watch?v=ydCVH9HttY8",
    "https://www.youtube.com/watch?v=NwFVSclD_uc",
    "https://www.youtube.com/watch?v=TjPhzgxe3L0",
]

with ydl:
    for url in url_list:
        result_metadata = ydl.extract_info(url, download=False)
        savepath = make_savepath(result_metadata["title"])
        try:
            os.stat(savepath)
            # logger.info(f"{savepath} already downloaded, continuing...")

        except OSError:
            try:
                result = ydl.extract_info(url, download=True)
                os.rename(result["id"], savepath)
                logger.info(f"Downloaded and converted {savepath} successfully!")

            except Exception as e:
                logger.debug(f"Can't download audio! {traceback.format_exc()}")

