import youtube_dl
import os
import traceback
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("mp4-youtube-dl.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Create Directory
savedir = "videos"
if not os.path.exists(savedir):
    os.makedirs(savedir)


def make_savepath(title, savedir=savedir):
    return os.path.join(savedir, f"{title}.mp4")


options = {"outtmpl": "%(id)s", "noplaylist": True}

ydl = youtube_dl.YoutubeDL(options)

url_list = []

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

