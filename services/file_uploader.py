import os

from pytube import YouTube


def download_and_save_file(args):
    url = args.get("url")
    name = args.get("name")

    yt = YouTube(url)

    video = yt.streams.filter(only_audio=True, bitrate="128kbps").first()

    out_file = video.download(output_path="results/original_audio/")

    os.rename(out_file, "results/original_audio/" + name + ".mp3")
