import os
import subprocess
from pydub import AudioSegment


def extract_voice(args):
    audio_file_name = args.get("name")
    start_time = int(args.get("start_time"))
    path = "results/original_audio/" + audio_file_name + ".mp3"
    output_base_path = "results/output/" + audio_file_name + "/"

    subprocess.run('spleeter separate -p spleeter:2stems -o results/output/ ' + path, shell=True)

    remove_accompaniment(output_base_path)

    split_audio(output_base_path, start_time)


def remove_accompaniment(output_base_path: str):
    path = output_base_path + "accompaniment.wav"
    os.remove(path)


def split_audio(output_base_path: str, start_time: int = 0):
    path = output_base_path + "vocals.wav"
    t1 = start_time * 1000  # Works in milliseconds
    t2 = t1 + 20000
    new_audio = AudioSegment.from_wav(path)
    new_audio = new_audio[t1:t2]
    new_audio.export(path, format="wav")
